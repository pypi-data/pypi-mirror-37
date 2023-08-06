#!/usr/bin/env python

"""
This application presents a 'console' prompt to the user asking for Who-Is
and I-Am commands which create the related APDUs, then lines up the
corresponding I-Am for incoming traffic and prints out the contents.
"""

import sys

from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser
from bacpypes.consolecmd import ConsoleCmd

from bacpypes.core import run, enable_sleeping, deferred

from bacpypes.pdu import Address, GlobalBroadcast
from bacpypes.apdu import (
    WhoIsRequest, IAmRequest, ReadPropertyRequest, ReadPropertyACK
)
from bacpypes.apdu import SimpleAckPDU, WritePropertyRequest
from bacpypes.basetypes import ServicesSupported
from bacpypes.errors import DecodingError

from bacpypes.service.device import LocalDeviceObject
from bacpypes.object import get_object_class, get_datatype
from bacpypes.constructeddata import Array, Any
from bacpypes.primitivedata import Null, Atomic, Integer, Unsigned, Real

from bacpypes.iocb import IOCB

from mstplib import MSTPSimpleApplication

# some debugging
_debug = 1
_log = ModuleLogger(globals())

# globals
this_device = None
this_application = None

#
#   BacnetClientApplication
#


@bacpypes_debugging
class BacnetClientApplication(MSTPSimpleApplication):

    def __init__(self, *args):
        if _debug:
            BacnetClientApplication._debug("__init__ %r", args)
        MSTPSimpleApplication.__init__(self, *args)

        # keep track of requests to line up responses
        self._request = None

    def request(self, apdu):
        if _debug:
            BacnetClientApplication._debug("request %r", apdu)

        # save a copy of the request
        self._request = apdu

        # forward it along
        MSTPSimpleApplication.request(self, apdu)

    def confirmation(self, apdu):
        if _debug:
            BacnetClientApplication._debug("confirmation %r", apdu)

        # forward it along
        MSTPSimpleApplication.confirmation(self, apdu)

    def indication(self, apdu):
        if _debug:
            BacnetClientApplication._debug("indication %r", apdu)

        if (
            (isinstance(self._request, WhoIsRequest)) and
            (isinstance(apdu, IAmRequest))
        ):
            device_type, device_instance = apdu.iAmDeviceIdentifier
            if device_type != 'device':
                raise DecodingError("invalid object type")

            if (
                (self._request.deviceInstanceRangeLowLimit is not None) and
                (device_instance < self._request.deviceInstanceRangeLowLimit)
            ):
                pass
            elif (
                (self._request.deviceInstanceRangeHighLimit is not None) and
                (device_instance > self._request.deviceInstanceRangeHighLimit)
            ):
                pass
            else:
                # print out the contents
                sys.stdout.write('pduSource = ' + repr(apdu.pduSource) + '\n')
                sys.stdout.write(
                    'iAmDeviceIdentifier = ' +
                    str(apdu.iAmDeviceIdentifier) + '\n'
                )
                sys.stdout.write(
                    'maxAPDULengthAccepted = ' +
                    str(apdu.maxAPDULengthAccepted) + '\n'
                )
                sys.stdout.write(
                    'segmentationSupported = ' +
                    str(apdu.segmentationSupported) + '\n'
                )
                sys.stdout.write('vendorID = ' + str(apdu.vendorID) + '\n')
                sys.stdout.flush()

        # forward it along
        MSTPSimpleApplication.indication(self, apdu)

    def close(self):
        self.close_socket()

#
#   BacnetClientConsoleCmd
#


@bacpypes_debugging
class BacnetClientConsoleCmd(ConsoleCmd):

    def do_discover(self, args):
        """discover <addr> <device-id>"""
        args = args.split()
        try:

            if len(args) != 2:
                raise ValueError('Expected 2 arguments')

            addr, device_id = args[:2]

            addr = int(addr)
            device_id = int(device_id)

            # used across requests
            self._instance_list = [0]
            self._first_req = True
            self._addr = addr
            self._device_id = device_id

            self._discovery()

        except Exception as error:
            BacnetClientConsoleCmd._exception("exception: %r", error)

    def do_read(self, args):
        """read <addr> <type> <inst> <prop> [ <indx> ]"""
        args = args.split()
        if _debug:
            BacnetClientConsoleCmd._debug("do_read %r", args)

        try:
            addr, obj_type, obj_inst, prop_id = args[:4]

            if obj_type.isdigit():
                obj_type = int(obj_type)
            elif not get_object_class(obj_type):
                raise ValueError("unknown object type")

            obj_inst = int(obj_inst)

            datatype = get_datatype(obj_type, prop_id)
            if not datatype:
                raise ValueError("invalid property for object type")

            # build a request
            request = ReadPropertyRequest(
                objectIdentifier=(obj_type, obj_inst),
                propertyIdentifier=prop_id,
                )
            request.pduSource = Address(this_device._mac_address)
            request.pduDestination = Address(int(addr))

            if len(args) == 5:
                request.propertyArrayIndex = int(args[4])
            if _debug:
                BacnetClientConsoleCmd._debug("    - request: %r", request)

            # make an IOCB
            iocb = IOCB(request)
            if _debug:
                BacnetClientConsoleCmd._debug("    - iocb: %r", iocb)

            # give it to the application
            this_application.request_io(iocb)

            # wait for it to complete
            iocb.wait()

            # do something for error/reject/abort
            if iocb.ioError:
                sys.stdout.write(str(iocb.ioError) + '\n')

            # do something for success
            elif iocb.ioResponse:
                apdu = iocb.ioResponse

                # should be an ack
                if not isinstance(apdu, ReadPropertyACK):
                    if _debug:
                        BacnetClientConsoleCmd._debug("    - not an ack")
                    return

                # find the datatype
                datatype = get_datatype(
                    apdu.objectIdentifier[0], apdu.propertyIdentifier
                )
                if _debug:
                    BacnetClientConsoleCmd._debug(
                        "    - datatype: %r", datatype
                    )
                if not datatype:
                    raise TypeError("unknown datatype")

                # special case for array parts, others are managed by cast_out
                if (
                    (issubclass(datatype, Array)) and
                    (apdu.propertyArrayIndex is not None)
                ):
                    if apdu.propertyArrayIndex == 0:
                        value = apdu.propertyValue.cast_out(Unsigned)
                    else:
                        value = apdu.propertyValue.cast_out(datatype.subtype)
                else:
                    value = apdu.propertyValue.cast_out(datatype)
                if _debug:
                    BacnetClientConsoleCmd._debug("    - value: %r", value)

                sys.stdout.write(str(value) + '\n')
                if hasattr(value, 'debug_contents'):
                    value.debug_contents(file=sys.stdout)
                sys.stdout.flush()

            # do something with nothing?
            else:
                if _debug:
                    BacnetClientConsoleCmd._debug(
                        "    - ioError or ioResponse expected"
                    )

        except Exception as error:
            BacnetClientConsoleCmd._exception("exception: %r", error)

    def do_write(self, args):
        """ write <addr> <type> <inst> <prop> <value> [<indx>] [<prio>] """
        args = args.split()
        BacnetClientConsoleCmd._debug("do_write %r", args)

        try:
            addr, obj_type, obj_inst, prop_id = args[:4]
            if obj_type.isdigit():
                obj_type = int(obj_type)
            obj_inst = int(obj_inst)
            value = args[4]

            indx = None
            if len(args) >= 6:
                if args[5] != "-":
                    indx = int(args[5])
            if _debug:
                BacnetClientConsoleCmd._debug("    - indx: %r", indx)

            priority = None
            if len(args) >= 7:
                priority = int(args[6])
            if _debug:
                BacnetClientConsoleCmd._debug("    - priority: %r", priority)

            # get the datatype
            datatype = get_datatype(obj_type, prop_id)
            if _debug:
                BacnetClientConsoleCmd._debug("    - datatype: %r", datatype)

            # change atomic values into something encodeable,
            # null is a special case
            if (value == 'null'):
                value = Null()
            elif issubclass(datatype, Atomic):
                if datatype is Integer:
                    value = int(value)
                elif datatype is Real:
                    value = float(value)
                elif datatype is Unsigned:
                    value = int(value)
                value = datatype(value)
            elif issubclass(datatype, Array) and (indx is not None):
                if indx == 0:
                    value = Integer(value)
                elif issubclass(datatype.subtype, Atomic):
                    value = datatype.subtype(value)
                elif not isinstance(value, datatype.subtype):
                    raise TypeError(
                        "invalid result datatype, expecting %s"
                        % (datatype.subtype.__name__,)
                    )
            elif not isinstance(value, datatype):
                raise TypeError(
                    "invalid result datatype, expecting %s"
                    % (datatype.__name__,)
                )
            if _debug:
                BacnetClientConsoleCmd._debug(
                    "    - encodeable value: %r %s",
                    value, type(value)
                )

            # build a request
            request = WritePropertyRequest(
                objectIdentifier=(obj_type, obj_inst),
                propertyIdentifier=prop_id
                )
            request.pduDestination = Address(addr)

            # save the value
            request.propertyValue = Any()
            try:
                request.propertyValue.cast_in(value)
            except Exception as error:
                BacnetClientConsoleCmd._exception(
                    "WriteProperty cast error: %r", error
                )

            # optional array index
            if indx is not None:
                request.propertyArrayIndex = indx

            # optional priority
            if priority is not None:
                request.priority = priority

            if _debug:
                BacnetClientConsoleCmd._debug("    - request: %r", request)

            # make an IOCB
            iocb = IOCB(request)
            if _debug:
                BacnetClientConsoleCmd._debug("    - iocb: %r", iocb)

            # give it to the application
            this_application.request_io(iocb)

            # wait for it to complete
            iocb.wait()

            # do something for success
            if iocb.ioResponse:
                # should be an ack
                if not isinstance(iocb.ioResponse, SimpleAckPDU):
                    if _debug:
                        BacnetClientConsoleCmd._debug("    - not an ack")
                    return

                sys.stdout.write("ack\n")

            # do something for error/reject/abort
            if iocb.ioError:
                sys.stdout.write(str(iocb.ioError) + '\n')

        except Exception as error:
            BacnetClientConsoleCmd._exception("exception: %r", error)

    def do_whois(self, args):
        """whois [ <addr>] [ <lolimit> <hilimit> ]"""
        args = args.split()
        if _debug:
            BacnetClientConsoleCmd._debug("do_whois %r", args)

        try:
            # build a request
            request = WhoIsRequest()
            if (len(args) == 1) or (len(args) == 3):
                request.pduDestination = Address(args[0])
                del args[0]
            else:
                request.pduDestination = GlobalBroadcast()

            if len(args) == 2:
                request.deviceInstanceRangeLowLimit = int(args[0])
                request.deviceInstanceRangeHighLimit = int(args[1])
            if _debug:
                BacnetClientConsoleCmd._debug("    - request: %r", request)

            # make an IOCB
            iocb = IOCB(request)
            if _debug:
                BacnetClientConsoleCmd._debug("    - iocb: %r", iocb)

            # give it to the application
            this_application.request_io(iocb)

        except Exception as err:
            BacnetClientConsoleCmd._exception("exception: %r", err)

    def do_iam(self, args):
        """iam"""
        args = args.split()
        if _debug:
            BacnetClientConsoleCmd._debug("do_iam %r", args)

        # code lives in the device service
        this_application.i_am()

    def do_rtn(self, args):
        """rtn <addr> <net> ... """
        args = args.split()
        if _debug:
            BacnetClientConsoleCmd._debug("do_rtn %r", args)

        # safe to assume only one adapter
        adapter = this_application.nsap.adapters[0]
        if _debug:
            BacnetClientConsoleCmd._debug("    - adapter: %r", adapter)

        # provide the address and a list of network numbers
        router_address = Address(args[0])
        network_list = [int(arg) for arg in args[1:]]

        # pass along to the service access point
        this_application.nsap.add_router_references(
            adapter, router_address, network_list
        )

    def _discovery(self):
        global device_address

        # build a request
        obj_type, prop_id = ('device', 'objectList')

        # build a request
        request = ReadPropertyRequest(
            objectIdentifier=(obj_type, self._device_id),
            propertyIdentifier=prop_id,
        )
        request.pduSource = Address(this_device._mac_address)
        request.pduDestination = Address(int(self._addr))
        request.propertyArrayIndex = self._instance_list.pop(0)

        if _debug:
            BacnetClientConsoleCmd._debug("    - request: %r", request)

        # make an IOCB
        iocb = IOCB(request)

        # set a callback for the response
        iocb.add_callback(self._discovery_response)
        if _debug:
            BacnetClientConsoleCmd._debug("    - iocb: %r", iocb)

        # send the request
        this_application.request_io(iocb)

    def _discovery_response(self, iocb):
        if _debug:
            BacnetClientConsoleCmd._debug("complete_request %r", iocb)

        if iocb.ioResponse:
            apdu = iocb.ioResponse

            # should be an ack
            if not isinstance(apdu, ReadPropertyACK):
                if _debug:
                    BacnetClientConsoleCmd._debug("    - not an ack")
                return

            # find the datatype
            datatype = get_datatype(
                apdu.objectIdentifier[0], apdu.propertyIdentifier
            )
            if _debug:
                BacnetClientConsoleCmd._debug("    - datatype: %r", datatype)
            if not datatype:
                raise TypeError("unknown datatype")

            # special case for array parts, others are managed by cast_out
            if (
                (issubclass(datatype, Array)) and
                (apdu.propertyArrayIndex is not None)
            ):
                if apdu.propertyArrayIndex == 0:
                    value = apdu.propertyValue.cast_out(Unsigned)
                else:
                    value = apdu.propertyValue.cast_out(datatype.subtype)
            else:
                value = apdu.propertyValue.cast_out(datatype)
            if _debug:
                BacnetClientConsoleCmd._debug("    - value: %r", value)

            sys.stdout.write(str(value) + '\n')

            if hasattr(value, 'debug_contents'):
                value.debug_contents(file=sys.stdout)
            sys.stdout.flush()

            if self._first_req:
                self._instance_list = range(1, value+1)
                self._first_req = False

                # fire off another request
                deferred(self._discovery)
                return

            if self._instance_list:
                # fire off another request
                deferred(self._discovery)

#
#   __main__
#


def main():
    global this_device
    global this_application

    # parse the command line arguments
    parser = ConfigArgumentParser(description=__doc__)
    parser.add_argument(
        '--mstp_dir',
        dest='mstp_dir',
        default='/var/tmp',
        help='mstp directory where the agent looks for (default: /var/tmp )'
    )
    args = parser.parse_args()

    if _debug:
        _log.debug("initialization")
    if _debug:
        _log.debug("    - args: %r", args)

    # make a device object
    this_device = LocalDeviceObject(
        objectName=args.ini.objectname,
        objectIdentifier=int(args.ini.objectidentifier),
        maxApduLengthAccepted=int(args.ini.maxapdulengthaccepted),
        segmentationSupported=args.ini.segmentationsupported,
        vendorIdentifier=int(args.ini.vendoridentifier),
        _interface=args.ini.interface,
        _mac_address=int(args.ini.address),
        _max_masters=int(args.ini.max_masters),
        _baudrate=int(args.ini.baudrate),
        _maxinfo=int(args.ini.maxinfo),
        _mstp_dir=str(args.mstp_dir)
    )

    # build a bit string that knows about the bit names
    pss = ServicesSupported()
    pss['whoIs'] = 1
    pss['iAm'] = 1
    pss['readProperty'] = 1
    pss['writeProperty'] = 1

    # set the property value to be just the bits
    this_device.protocolServicesSupported = pss.value

    # make a simple application
    this_application = BacnetClientApplication(this_device, args.ini.address)

    # get the services supported
    services_supported = this_application.get_services_supported()
    if _debug:
        _log.debug("    - services_supported: %r", services_supported)

    # let the device object know
    this_device.protocolServicesSupported = services_supported.value

    # make a console
    this_console = BacnetClientConsoleCmd()
    if _debug:
        _log.debug("    - this_console: %r", this_console)

    # enable sleeping will help with threads
    enable_sleeping()

    _log.debug("running")

    run()

    this_application.close()

    _log.debug("fini")

if __name__ == "__main__":
    main()

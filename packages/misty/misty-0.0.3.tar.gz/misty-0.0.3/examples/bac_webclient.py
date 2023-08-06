#!/usr/bin/python

"""
HTTPServer
"""

import threading
import json
import sys

from urlparse import urlparse, parse_qs
import SocketServer
import SimpleHTTPServer

from bacpypes.debugging import class_debugging, ModuleLogger
from bacpypes.debugging import bacpypes_debugging
from bacpypes.consolelogging import ConfigArgumentParser

from bacpypes.core import run
from bacpypes.iocb import IOCB
from bacpypes.errors import DecodingError
from bacpypes.constructeddata import Array

from bacpypes.pdu import Address, GlobalBroadcast
from bacpypes.apdu import WhoIsRequest, IAmRequest, ReadPropertyRequest, ReadPropertyACK

from mstplib import MSTPSimpleApplication
from bacpypes.object import get_object_class, get_datatype
from bacpypes.service.device import LocalDeviceObject

# some debugging
_debug = 0
_log = ModuleLogger(globals())

# reference a simple application
this_application = None
server = None
device_info = {}

#
#   BacnetClientWebApplication
#

@bacpypes_debugging
class BacnetClientWebApplication(MSTPSimpleApplication):

    def __init__(self, *args):
        if _debug: BacnetClientWebApplication._debug("__init__ %r", args)
        MSTPSimpleApplication.__init__(self, *args)

        # keep track of requests to line up responses
        self._request = None

    def request(self, apdu):
        if _debug: BacnetClientWebApplication._debug("request %r", apdu)

        # save a copy of the request
        self._request = apdu

        # forward it along
        MSTPSimpleApplication.request(self, apdu)

    def confirmation(self, apdu):
        if _debug: BacnetClientWebApplication._debug("confirmation %r", apdu)

        # forward it along
        MSTPSimpleApplication.confirmation(self, apdu)

    def indication(self, apdu):
        if _debug: BacnetClientWebApplication._debug("indication %r", apdu)

        if (isinstance(self._request, WhoIsRequest)) and (isinstance(apdu, IAmRequest)):
            device_type, device_instance = apdu.iAmDeviceIdentifier
            if device_type != 'device':
                raise DecodingError("invalid object type")

            if (self._request.deviceInstanceRangeLowLimit is not None) and \
                (device_instance < self._request.deviceInstanceRangeLowLimit):
                pass
            elif (self._request.deviceInstanceRangeHighLimit is not None) and \
                (device_instance > self._request.deviceInstanceRangeHighLimit):
                pass
            else:
                # print out the contents
                sys.stdout.write('pduSource = ' + repr(apdu.pduSource) + '\n')
                sys.stdout.write('iAmDeviceIdentifier = ' + str(apdu.iAmDeviceIdentifier) + '\n')
                sys.stdout.write('maxAPDULengthAccepted = ' + str(apdu.maxAPDULengthAccepted) + '\n')
                sys.stdout.write('segmentationSupported = ' + str(apdu.segmentationSupported) + '\n')
                sys.stdout.write('vendorID = ' + str(apdu.vendorID) + '\n')
                sys.stdout.flush()

                mac = int(str(apdu.pduSource))
                device = apdu.iAmDeviceIdentifier[1]
                device_info[mac]={}
                device_info[mac][device]={}
                device_info[mac][device]['maxAPDULengthAccepted'] = str(apdu.maxAPDULengthAccepted)
                device_info[mac][device]['segmentationSupported'] = str(apdu.segmentationSupported)
                device_info[mac][device]['vendorID'] = str(apdu.vendorID)


        # forward it along
        MSTPSimpleApplication.indication(self, apdu)

    def close(self):
        self.close_socket()



#
#   ThreadedHTTPRequestHandler
#

@class_debugging
class ThreadedHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        if _debug: ThreadedHTTPRequestHandler._debug("do_GET")

        # get the thread
        cur_thread = threading.current_thread()
        if _debug: ThreadedHTTPRequestHandler._debug("    - cur_thread: %r", cur_thread)

        # parse query data and params to find out what was passed
        parsed_params = urlparse(self.path)
        if _debug: ThreadedHTTPRequestHandler._debug("    - parsed_params: %r", parsed_params)
        parsed_query = parse_qs(parsed_params.query)
        if _debug: ThreadedHTTPRequestHandler._debug("    - parsed_query: %r", parsed_query)

        # find the pieces
        args = parsed_params.path.split('/')
        if _debug: ThreadedHTTPRequestHandler._debug("    - args: %r", args)

        if (args[1] == 'read'):
            result = self.do_read(args[2:])
        elif (args[1] == 'whois'):
            result = self.do_whois(args[2:])
        elif (args[1] == 'device'):
            result = device_info

        #send code 200 response
        self.send_response(200)

        #send header first
        self.send_header('Content-type','application/json')
        self.end_headers()
        # write the result
        json.dump(result, self.wfile)

    def _update_device_info(self, addr, device_id, obj_type, obj_inst, prop_id, value):
        import pdb
        pdb.set_trace()

        if addr not in device_info:
            device_info[addr] = {}
        prop_dict = device_info[addr]

        if device_id not in prop_dict:
            prop_dict[device_id] = {}
        device_id_dict = prop_dict[device_id]

        if obj_type not in device_id_dict:
            device_id_dict[obj_type] = {}
        obj_type_dict = device_id_dict[obj_type]

        if obj_inst not in obj_type_dict:
            obj_type_dict[obj_inst] = {}
        obj_inst_dict = obj_type_dict[obj_inst]

        if prop_id not in obj_inst_dict:
            obj_inst_dict[prop_id] = {}
        prop_id_dict = obj_inst_dict[prop_id]

        prop_id_dict['value'] = value


    def do_read(self, args):
        if _debug: ThreadedHTTPRequestHandler._debug("do_read %r", args)

        result = {}

        try:
            addr, obj_type, obj_inst = args[:3]

            # get the object type
            if not get_object_class(obj_type):
                raise ValueError("unknown object type")

            # get the instance number
            obj_inst = int(obj_inst)

            # implement a default property, the bain of committee meetings
            if len(args) == 4:
                prop_id = args[3]
            else:
                prop_id = "presentValue"

            # look for its datatype, an easy way to see if the property is
            # appropriate for the object
            datatype = get_datatype(obj_type, prop_id)
            if not datatype:
                raise ValueError("invalid property for object type")

            # build a request
            request = ReadPropertyRequest(
                objectIdentifier=(obj_type, obj_inst),
                propertyIdentifier=prop_id,
                )
            request.pduDestination = Address(addr)

            # look for an optional array index
            if len(args) == 5:
                request.propertyArrayIndex = int(args[4])
            if _debug: ThreadedHTTPRequestHandler._debug("    - request: %r", request)

            # make an IOCB
            iocb = IOCB(request)
            if _debug: ThreadedHTTPRequestHandler._debug("    - iocb: %r", iocb)

            # give it to the application
            this_application.request_io(iocb)

            # wait for it to complete
            iocb.wait()

            # do something for error/reject/abort
            if iocb.ioError:
                result['error'] = 'iocb Error :{}'.format(str(iocb.ioError))
                return result

            # do something for success
            elif iocb.ioResponse:
                apdu = iocb.ioResponse

                # should be an ack
                if not isinstance(apdu, ReadPropertyACK):
                    if _debug: ThreadedHTTPRequestHandler._debug("    - not an ack")
                    return {'error': 'Incorrect response from the server'}

                # find the datatype
                datatype = get_datatype(apdu.objectIdentifier[0], apdu.propertyIdentifier)
                if _debug: ThreadedHTTPRequestHandler._debug("    - datatype: %r", datatype)
                if not datatype:
                    result['error'] = 'Incorrect datatype response from the server'
                    return result

                # special case for array parts, others are managed by cast_out
                if issubclass(datatype, Array) and (apdu.propertyArrayIndex is not None):
                    if apdu.propertyArrayIndex == 0:
                        value = apdu.propertyValue.cast_out(Unsigned)
                    else:
                        value = apdu.propertyValue.cast_out(datatype.subtype)
                else:
                    value = apdu.propertyValue.cast_out(datatype)

                if _debug: ThreadedHTTPRequestHandler._debug("    - value: %r", value)

                # proper result
                result['value'] = value

                self._update_device_info(addr, 600, obj_type, obj_inst, prop_id, value)

                if hasattr(value, 'debug_contents'):
                    result['debug_contents'] = value.debug_contents()


            # do something with nothing?
            else:
                if _debug: ThreadedHTTPRequestHandler._debug("    - ioError or ioResponse expected")
                result['error'] = 'No response from the server'
                return result


        except Exception as err:
            ThreadedHTTPRequestHandler._exception("exception: %r", err)
            result['error'] = "exception :{}".format(str(err))

        return result

    def do_whois(self, args):
        if _debug: ThreadedHTTPRequestHandler._debug("do_whois %r", args)

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
            if _debug: ThreadedHTTPRequestHandler._debug("    - request: %r", request)

            # make an IOCB
            iocb = IOCB(request)
            if _debug: ThreadedHTTPRequestHandler._debug("    - iocb: %r", iocb)

            # give it to the application
            this_application.request_io(iocb)

            # no result -- it would be nice if these were the matching I-Am's
            result = {}

        except Exception as err:
            ThreadedHTTPRequestHandler._exception("exception: %r", err)
            result = { "exception": str(err) }

        if _debug: ThreadedHTTPRequestHandler._debug("    - result: %r", result)

        return result

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

#
#   __main__
#

try:
    # parse the command line arguments
    parser = ConfigArgumentParser(description=__doc__)
    parser.add_argument(
        '--mstp_dir',
        dest='mstp_dir',
        default='/var/tmp',
        help='mstp directory where the agent looks for (default: /var/tmp )'
    )

    # add an option to override the port in the config file
    parser.add_argument('--port', type=int,
        help="override the port in the config file to PORT",
        default=9000,
        )
    args = parser.parse_args()

    if _debug: _log.debug("initialization")
    if _debug: _log.debug("    - args: %r", args)

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

    # make a simple application
    this_application = BacnetClientWebApplication(this_device, args.ini.address)

    # get the services supported
    services_supported = this_application.get_services_supported()
    if _debug: _log.debug("    - services_supported: %r", services_supported)

    # let the device object know
    this_device.protocolServicesSupported = services_supported.value

    # local host, special port
    HOST, PORT = "", int(args.port)
    server = ThreadedTCPServer((HOST, PORT), ThreadedHTTPRequestHandler)
    if _debug: _log.debug("    - server: %r", server)

    # Start a thread with the server -- that thread will then start a thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    if _debug: _log.debug("    - server_thread: %r", server_thread)

    # exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    if _debug: _log.debug("running")

    run()

except Exception as err:
    _log.exception("an error has occurred: %s", err)

finally:
    if server:
        server.shutdown()

    if _debug: _log.debug("finally")

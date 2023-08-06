
#  misty

The misty project helps build [bacpypes](https://github.com/JoelBender/bacpypes)   applications that work on MS/TP Networks. The existing bacpypes BIP (BACnet IP ) applications can be easily ported to to use misty and work on MS/TP Networks.

# Table of Contents


[TOC]

# How does this Work ?

For supporting bacpypes applications on MSTP Network, a new class for application called **MSTPSimpleApplication** has been created.  All the MSTP applications need to derive from the MSTPSimpleApplication. 

A bacpypes application derived from MSTPSimpleApplication sends and receives data to an MSTP Agent. The MSTP Agent receives the packets sent out by the bacpypes application and sends it out on the Serial port using the Serial port Driver. In the response path, the Serial port Driver receives the MSTP Frame sent by the peer and passes it to the MSTP Agent. The MSTP agent hands it over to the bacpypes application.
Each bacpypes application derived from MSTPSimpleApplication is tied to a Physical Interface (e.g. ttyS0). 

The MSTP Agent relies on the open source [bacnet-stack version 0.8.4](https://sourceforge.net/projects/bacnet/files/bacnet-stack/) by skarg for communicating with the Serial port. The MSTP Agent uses the dlmstp_xxx functions of the bacnet-stack to send/receive the MSTP Frames and also to set configuration parametersof the Serial port (like baud rate, max_info).


# Installation and Usage

Install the bacpypes package in your python environment

```
$ pip install bacpypes
```

Clone the MSTP Agent repository with the following command:
```
$ git clone https://github.com/raghavan97/mstp_agent.git
```
Make the MSTP Agent library and install the mstplib package by using the following commands
```
$ cd mstp_agent
$ make clean_build
$ cd ..
$ python setup.py install
```
Edit the bac_client.ini file in the **examples** directory to set the following values as appropriate to your setup.

*  MS/TP address
*  interface
*  baudrate
*  max masters
* max info

A sample bac_client.ini file is shown below
```ini
[BACpypes]
objectName: BACClient
; MSTP Local address
address: 25
; The serial port device
interface:/dev/ttyS0
; other mstp config parameters max_masters, baudrate, maxinfo
max_masters: 127
baudrate: 38400
maxinfo:1
objectIdentifier: 599
maxApduLengthAccepted: 1024
segmentationSupported: segmentedBoth
vendorIdentifier: 15
foreignPort: 0
foreignBBMD: 128.253.109.254
foreignTTL: 30
```

Start the bacnet client program in the **examples** directory
```
$ cd examples
$ python bac_client.py --ini bac_client.ini
```
The bacnet client program console offers commands to do basic BACnet commands like

*  whois
*  iam
*  read
*  write
* discover

A sample demo for using the bac_client.py with real devices is shown [here](https://youtu.be/w8TfY2-21Q8). 


# Testing MSTP  Applications

The **socat** utility is useful  to test the MSTP applications even without having a real mstp device. 

The following is the procedure for using *socat* to test the interaction of BACnet server and BACnet client.


Execute the socat utility to create two connected virtual serial ports ptyp0 and ttyp0 in a terminal window
```
$ socat PTY,link=/var/tmp/ptyp0,b38400 PTY,link=/var/tmp/ttyp0,b38400
```

On a new terminal window , start the BACnet server on ptyp0. The configuration file bac_server.ini has the interface ptyp0 configured at 38400 baud rate.
```
$ cd examples
$ python bac_server.py --ini bac_server.ini
```
On a new terminal window, start the BACnet client on ttyp0. The configuration file bac_client.ini has the interface ptyp0 configured at 38400 baud rate.
```
$ cd examples
$ python bac_client.py --ini bac_client.ini
```
Now we can use any of the commands supported on the BACnet client console to send messages to BACnet Server

*  whois
*  discover
*  read
*  write


This [video](https://youtu.be/Xej6H1doN90) shows a sample interaction between the BACnet Server, and BACnet client program running on the same machine using socat utility
 

# Porting IP Apps to MSTP
 
 To port an bacpypes BIPSimpleApplication to use the MSTP Networks, the following changes are required in the configuration file and application. 
 
(1) The ini file used for the configuration of the MSTPSimpleApplication would contain additional MSTP interface details.
 
*  address - MSTP Mac Address
*  interface - Physical Device (e.g. ttyS0) 
*  max_masters
*  baudrate
*  maxinfo


A Sample **INI File** for MSTPSimpleApplication is shown below

```ini
[BACpypes]
objectName: BACClient
address: 25
interface:/dev/ttyS0
max_masters: 127
baudrate: 38400
maxinfo:1
objectIdentifier: 599
maxApduLengthAccepted: 1024
segmentationSupported: segmentedBoth
vendorIdentifier: 15
foreignPort: 0
foreignBBMD: 128.253.109.254
foreignTTL: 30
```

(2) The Application class needs to be derived from MSTPSimpleApplication instead of BIPSimpleApplication.
```python
class BacnetClientApplication(BIPSimpleApplication):
```
would be changed to 

```python
from mstplib import MSTPSimpleApplication
class BacnetClientApplication(MSTPSimpleApplication):
```
(3) The Local device object in the MSTPSimpleApplication should be initialised with the additional MSTP interface details. The following shows a typical local object initialisation for a MSTP Simple Application.

```python
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
   _maxinfo=int(args.ini.maxinfo)
)
```

# Limitations
The following are the known limitations of MSTP Agent Project

*  Support for Linux only
* 



> Written with [StackEdit](https://stackedit.io/).

<!--stackedit_data:
eyJoaXN0b3J5IjpbODc4OTE3NTY0LC0xNDA5Njk1MjgxLC0yND
AzNTA2MjYsMTQwODI5MTA2OSw4NzgyNjU2MywtNjUxMTc4NTA5
LDEwODk0MTM4MTIsLTEwNzE1NTUxNjFdfQ==
-->
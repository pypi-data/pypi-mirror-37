import os, sys, re
import inspect, pkg_resources

## Version check
def versionCompare(version1, version2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    return cmp(normalize(version1), normalize(version2))

def getQuarchPyVersion ():
    return pkg_resources.get_distribution("quarchpy").version

def requiredQuarchpyVersion (requiredVersion):
    return versionCompare (requiredVersion, getQuarchPyVersion())


## Adds / to the path.
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "//")
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)

## Adds /disk_test to the path.
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "//disk_test")
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)

## Adds /connection_specific to the path.
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "//connection_specific")
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)

## Adds /device_specific to the path.
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "//device_specific")
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)

## Adds /serial to the path.
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "//connection_specific//serial")
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)

## Adds /QIS to the path.
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "//connection_specific//QIS")
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)

## Adds /usb_libs to the path.
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "//connection_specific//usb_libs")
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)

from device import *

current_path = os.path.dirname(os.path.abspath(__file__))
## Import all the modules in /device_specific.
for name in os.listdir(current_path +"//device_specific"):
    if name.endswith(".py"):
         # Strip the extension.
         module = name[:-3]
         # Import.
         exec("from " + module + " import *")

from connection import startLocalQis, closeQIS, startLocalQps, closeQPS

from connection_specific.connection_QIS import QisInterface as qisInterface
from connection_specific.connection_QIS import isQisRunning

from connection_specific.connection_QPS import *
from connection_specific.connection_QPS import QpsInterface as qpsInterface

from FIO_interface import *

try:    
    from DiskTargetSelection import *
except ImportError:
    pass
try:
    from IometerAutomation import *
except ImportError:
    pass
try:
    from ModuleSelection import *
except ImportError:
    pass
#--------------------------

from connection_specific.connection_USB import importUSB, USBConn
from connection_specific.connection_Serial import serialList, serial

from socket import *
import time


def scanDevices(target_conn = "all"):

    def list_serial():
        serial_ports = serialList.comports()
        serial_modules = []

        for i in serial_ports:
            try:
                ser = serial.Serial(i[0], 19200, timeout=1)
                ser.write(b'*serial?\r\n')
                time.sleep(2)
                s = ser.read(size = 64)
                serial_module = s.splitlines()[1]
            
                serial_module = str(serial_module)[1:].replace("'","")
            
                if "QTL" not in serial_module:
                    serial_module = "QTL" + serial_module
            
                module = str(i[0]), str(serial_module)

                if serial_module[7] == "-" and serial_module[10] == "-":
                    serial_modules.append(module)

                ser.close()
            except:
                pass
        return serial_modules

    def list_USB():
        QUARCH_VENDOR_ID = 0x16d0
        QUARCH_PRODUCT_ID1 = 0x0449

        usb1 = importUSB()

        context = usb1.USBContext()
        usb_list = context.getDeviceList()

        usb_modules = []
            
        for i in usb_list:
            if hex(i.device_descriptor.idVendor) == hex(QUARCH_VENDOR_ID) and hex(i.device_descriptor.idProduct) == hex(QUARCH_PRODUCT_ID1):
                i_handle = i.open()
                module_sn = i_handle.getASCIIStringDescriptor(3)

                if "QTL" not in module_sn:
                    module_sn = "QTL" + module_sn
                
                module = str(i_handle._USBDeviceHandle__device).split(":")[0], str(module_sn.strip())
                
                usb_modules.append(module)
            
                i_handle.close()

        return usb_modules
    
    def list_network(target_conn):
        # Create and configure the socket for broadcast.
        mySocket = socket(AF_INET, SOCK_DGRAM)
        mySocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        mySocket.settimeout(1)

        # Broadcast the message.
        mySocket.sendto(b'Discovery: Who is out there?\0\n',('255.255.255.255', 30303))
        
        telnet_modules = []
        rest_modules = []
    
        # Receive messages until timeout.
        while True:
            network_modules = {}

            # Receive raw message until timeout, then break.
            try:
                msg_received = mySocket.recvfrom(256)
            except:
                break
            cont = 0

            for lines in msg_received[0].splitlines():
                if cont <= 1:
                    index = cont
                    data = repr(lines).replace("'","").replace("b","")
                    cont += 1
                else:
                    index = repr(lines[0]).replace("'","")
                    data = repr(lines[1:]).replace("'","").replace("b","")

                network_modules[index] = data
                    
            # Filter the raw message to get the module and ip adress.
            module_name = network_modules.get(0).strip()
        
            ip_module = msg_received[1][0].strip()

            telnet_ip_list = []
            rest_ip_list = []
                
            try:
                # Add a QTL before modules without it.
                if "QTL" not in module_name.decode("utf-8"):
                    module_name = "QTL" + module_name.decode("utf-8")
            except:
                # Add a QTL before modules without it.
                if "QTL" not in module_name:
                    module_name = "QTL" + module_name
            
            # Checks if there's a value in the TELNET key.
            if network_modules.get("\\x8a") or network_modules.get("138"):
                ip_module_telnet = "TELNET:" + ip_module
                # Append the information to the list.
                module = ip_module_telnet, str(module_name)
                telnet_modules.append(module)
                del(module)
                del(ip_module_telnet)

            # Checks if there's a value in the REST key.
            if network_modules.get("\\x84") or network_modules.get("132"):
                ip_module_rest = "REST:" + ip_module
                # Append the information to the list.
                module = ip_module_rest, str(module_name)
                rest_modules.append(module)
                del(module)
                del(ip_module_rest)
                
        if target_conn.lower() == "rest":
            return rest_modules
        
        if target_conn.lower() == "telnet":
            return telnet_modules
    
    if target_conn.lower() == "all":
        return list_USB(), list_serial(), list_network("telnet"), list_network("rest")

    if target_conn.lower() == "serial":
        return list_serial()

    if target_conn.lower() == "usb":
        return list_USB()

    if target_conn.lower() == "rest" or target_conn.lower() == "telnet":
        return list_network(target_conn)
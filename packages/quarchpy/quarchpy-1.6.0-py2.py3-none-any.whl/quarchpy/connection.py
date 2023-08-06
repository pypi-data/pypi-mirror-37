import os, sys
import inspect
import time 
from connection_QIS import QisInterface, isQisRunning
from connection_QPS import QpsInterface, isQpsRunning
import subprocess

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def startLocalQis(QisPath=None):

    blockPrint()

    if QisPath == None:
        QisPath = os.path.join(os.path.abspath(__file__), "..", "connection_specific", "QIS", "qis.jar")

    else:
        QisPath = QisPath.replace("\r", "\\r")
        QisPath = os.path.normpath(QisPath)

    current_direc = os.getcwd()

    os.chdir(QisPath + "\\..")

    startQISchar = "start /high /b javaw -jar " + QisPath
    
    os.system(startQISchar)
    
    while not isQisRunning():
        time.sleep(0.1)

    os.chdir(current_direc)
   
    try:
        startLocalQis.func_code = (lambda:None).func_code
    except:
        startLocalQis.__code__ = (lambda:None).__code__ 
    
    enablePrint()

def closeQIS(host='127.0.0.1', port=9722):
    myQis = QisInterface(host, port)
    myQis.sendAndReceiveCmd(cmd = "$shutdown")
    del myQis

def startLocalQps(QpsPath=None, keepQisRunning=False):
    
    if keepQisRunning:
        if not isQisRunning():
            startLocalQis()
    
    blockPrint()

    if QpsPath == None:
        QpsPath = os.path.join(os.path.abspath(__file__), "..", "connection_specific", "QPS", "qps.jar")

    else:
        QpsPath = QpsPath.replace("\r", "\\r")
        QpsPath = os.path.normpath(QpsPath)

    current_direc = os.getcwd()
    
    os.chdir(QpsPath + "\\..")

    startQPSchar = "start /high /b javaw -Djava.awt.headless=true -jar " + QpsPath

    os.system(startQPSchar)
    #subprocess.Popen(startQPSchar, shell = True)


    while not isQpsRunning():
        time.sleep(0.1)
        pass

    os.chdir(current_direc)

    try:
        startLocalQps.func_code = (lambda:None).func_code
    except:
        startLocalQps.__code__ = (lambda:None).__code__ 
    enablePrint()

def closeQPS(host='127.0.0.1', port=9822):
    myQps = QpsInterface(host, port)
    myQps.sendCmdVerbose("$shutdown")
    del myQps



class QISConnection:
    
    def __init__(self, ConString, host, port):
        self.qis = QisInterface(host, port)     # Create an instance of QisInterface. Before this is ran QIS needs to have been started


class PYConnection:
    
    def __init__(self, ConString):
        # Finds the separator.
        Pos = ConString.find (':')
        if Pos is -1:
            raise ValueError ('Please check your module name!')
        # Get the connection type and target.
        self.ConnTypeStr = ConString[0:Pos]
        self.ConnTarget = ConString[(Pos+1):]
        
        if self.ConnTypeStr.lower() == 'rest':
            from connection_ReST import ReSTConn
            self.connection = ReSTConn(self.ConnTarget)
            
        elif self.ConnTypeStr.lower() == 'usb':
            from connection_USB import USBConn
            self.connection = USBConn(self.ConnTarget)
        
        elif self.ConnTypeStr.lower() == 'serial':
            from connection_Serial import SerialConn
            self.connection = SerialConn(self.ConnTarget)
        
        elif self.ConnTypeStr.lower() == 'telnet':
            from connection_Telnet import TelnetConn
            self.connection = TelnetConn(self.ConnTarget)
        
        else:
            return "Please check your connection string."


class QPSConnection:

    def __init__(self, host, port):
        self.qps = QpsInterface(host, port)
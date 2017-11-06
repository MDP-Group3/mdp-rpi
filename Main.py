#!/usr/bin/python
import sys
import time
import threading
from SerialConn import *
from BTConn import *
from PCConn import *

class Main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sr = SerialConn()
        self.bt = BTConn()
        self.pc = PCConn()
        self.sr.connect()
        self.bt.connect()
        self.pc.connect() 

    def readPCmsg(self):         
        while True:
            try:
                print "In Read PC Message"
                msg = self.pc.read()
              	if (msg[0] == ''):
                    print "empty string"
                    time.sleep(30)
                    break
                else:
                    print "Received from PC: ", str(msg)
                    # if destination is tablet
                    if(msg[0] == 'T'):
                        self.bt.write(msg[1:])
                        print "PC>Tablet: ", str(msg[1:])
                    # else if destination is arduino
                    elif(msg[0] == 'A'):
                        if(len(msg)==4):    # if faulty reception: two commands received together
                            self.sr.write(msg[1])
                            print "PC>Arduino: ", str(msg[1])
                            delay(3)
                            self.sr.write(msg[3])
                            print "PC>Arduino: ", str(msg[3])
                        else:               # if faultless reception 
                            self.sr.write(msg[1:])
                            print "PC>Arduino: ", str(msg[1:])
                    # no valid destination           
                    else:
                        print "Invalid Header: ", str(msg)
            except Exception, e:
                continue
        
    def readBTmsg(self):            
        while True:
            try:
                print "In Read BT Message"
                msg = self.bt.read()
                print "Receive from BT: ", str(msg)
                #if destination is PC
                if(msg[0] == 'P'):
                    self.pc.write(msg[1:])
                    print "BT>PC: ", str(msg[1:])
                #if destination is Arduino
                elif(msg[0] == 'A'):
                    self.sr.write(msg[1:])
                    print "BT>Arduino: ", str(msg[1:])
                # no valid destination
                else:
                    print "Invalid Header: ", str(msg)
            except Exception, e:
                continue
    
    def readSerialMsg(self):
        while True:
            print "In Read Serial Message"
            msg = self.sr.read()
            print "Received from Arduino: ", str(msg[1:])
            self.pc.write(str(msg[1:]))            
                    
    def threadInit(self):     
        pcReadT = threading.Thread(target = self.readPCmsg, name = "PC Read Thread")
        pcWriteT = threading.Thread(target = self.pc.write, args = ("",), name = "PC Write Thread")
        print "PC Read/Write init"
        
        btReadT = threading.Thread(target = self.readBTmsg, name = "BT Read Thread")
        btWriteT = threading.Thread(target = self.bt.write, args = ("",), name = "BT Write Thread")
        print "BT Read/Write init"
        
        serialReadT = threading.Thread(target = self.readSerialMsg, name = "Serial Read Thread")
        serialWriteT = threading.Thread(target = self.sr.write, args = ("",), name = "Serial Write Thread")
        print "Serial Read/Write init"
        
        pcReadT.daemon = True
        pcWriteT.daemon = True
        btReadT.daemon = True
        btWriteT.daemon = True
        serialReadT.daemon = True
        serialWriteT.daemon = True
        pcReadT.start()
        pcWriteT.start()
        btReadT.start()
        btWriteT.start()
        serialReadT.start()
        serialWriteT.start()

    def close(self):
        self.pc.close()
        self.bt.close()
        self.sr.close()
        print "Closing"
    
    def sleep(self):
        while True:
            time.sleep(0.5)

if __name__ == "__main__":
    m = Main()
    try:
        m.threadInit()
        m.sleep()
    except KeyboardInterrupt:
        m.close()

#!/usr/bin/python
import serial
import time

class SerialConn(object):
    def _init_(self):
        self.port='/dev/ttyACM0'
        self.baud_rate=115200
        self.ser=None
        print "init Serial"
        print "/dev/ttyACM0"
        print "115200"

    def connect(self):
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 115200,)
            print "Serial Connected"
        except Exception, e:
            print e.message
            
    def write(self, text):
        try:
            #text = text.upper()
            print "in serial write"
            text = str(text).replace('\n', '\r')
            text = text + '\r'
            self.ser.write(text)
            self.ser.flush()
            print "serial write finished"
            #print text
        except Exception, e:
            print e.message

    def read(self):
        try:
            #self.ser.flushInput()
            received = self.ser.readline()          
            #print "Received: " + str(received)
            return received
        except Exception, e:
            print e.message
    
    def close(self):
        if(self.ser):
            self.ser.close()
            #print "close"
    
if __name__ == "__main__":
    sr = SerialConn()
    sr._init_()
    #time.sleep(2)
    print "1. connect"
    sr.connect()
    time.sleep(2)
    #print "2. write"
    #sr.write('F')
    #print "3. read" 
    #st = sr.read()
    #print st

    while(1):
        sr.write('F')
        st=sr.read()
        print st
        sr.write('R')
        st=sr.read()
        print st
    #print "received: %s" %sr.read
    #sr.close
    

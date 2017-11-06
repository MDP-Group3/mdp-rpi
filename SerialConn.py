#!/usr/bin/python
import serial
import time

class SerialConn(object):
    def _init_(self):
        self.port='/dev/ttyACM0'
        self.baud_rate=115200
        self.ser=None
        print "init Serial"

    def connect(self):
        try:
            # Connect to device through Serial Port at specified baud rate
            self.ser = serial.Serial('/dev/ttyACM0', 115200)
            print "Serial Connected"
        except Exception, e:
            print e.message
            
    def write(self, text):
        try:
            text = str(text).replace('\n', '\r')
            text = text + '\r'
            self.ser.write(text)    # write data to serial port
            self.ser.flush()
            print "Sent: "+ text
        except Exception, e:
            print e.message

    def read(self):
        try:
            received = self.ser.readline()  # read data from serial port     
            print "Received: " + str(received)  
            return received
        except Exception, e:
            print e.message
    
    def close(self):
        if(self.ser):
            self.ser.close()
    
if __name__ == "__main__":
    sr = SerialConn()
    sr._init_()
    sr.connect()
    time.sleep(2)
    sr.write('X')
    st = sr.read()
    print st
    sr.close()

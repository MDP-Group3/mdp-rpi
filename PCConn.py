#!/usr/bin/python
import socket
import sys
import time

class PCConn(object):

    def __init__(self):
        self.serverIP = "192.168.3.1"
        self.port = 1818
        self.isConnected = False
        self.server = None
        self.client = None
    
    def connect(self):
        try:
            # Connect to client using TCP for defined IP address and port number
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.serverIP, self.port))
            self.server.listen(1)
            print "PC waiting for connection..."
            self.client, self.clientIP = self.server.accept()
            print "PC connection from ", self.clientIP
            self.isConnected = True
        except Exception, e:
            time.sleep(5)
            print "PC connection Error: ", str(e)

    def reconnect(self):
        while True:
            try:
                if (self.isConnected == False):
                    print "Reconnecting..."
                    self.connect()
            except Exception, e:
                print str(e)
                continue
            else:
                break

    def write(self, message):
        while True:
            try:
                self.client.sendto(message, self.clientIP)  # send data to client
                print "PC Sent: ", str(message)
            except Exception, e:
                print "PC write Error: ", str(e)
                self.isConnected = False
                self.reconnect()
                continue
            else:
                break

    def read(self):
        while True:
            try:
                text = self.client.recv(2048)   # receive upto buffersize bytes from client
                print str(text)
                return text
            except Exception, e:
                print "PC read Error: ", str(e)
                self.isConnected = False
                self.reconnect()
                continue
            else:
                break

    def close(self):
        if self.server:
            self.server.close()
        if self.client:
            self.client.close()
        self.pc_is_connect = False

if __name__ == "__main__":
    pcc = PCConn()
    pcc.connect()
    time.sleep(5)
    #pcc.write('Hello from rpi')
    text = pcc.read()
    print "Read: ",str(text)
    pcc.close()

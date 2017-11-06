#!/usr/bin/python
import bluetooth
import time 

class BTConn(object):

    def __init__(self):
        self.isConnected = False
        
    def connect(self):
        try:
            print("connect start")
            self.btSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            print("init socket")
            self.btSocket.bind(("", 4))
            print("bind socket")
            self.btSocket.listen(1) # Start listening on rfcomm socket 4
            print("listening")  
            port = self.btSocket.getsockname()[1]
            print("got socket name")
            # Wait for an incoming connection, then return new socket
            # representing the connection and its address/port
            print "BT waiting for connection..."
            self.clientSocket, clientAddr = self.btSocket.accept()
            print "BT connected to ", clientAddr            
            self.isConnected = True
        except Exception, e:
            time.sleep(5)
            print "BT connection failed:" + str(e)

    def reconnect(self):
        while True:
            try:
                if (self.isConnected == False):
                    print "Waiting..Reconnecting"
                    self.connect()
            except Exception, e:
                print str(e)
                continue
            else:
                break
    
    def write(self,text):
        while True:
            try:
                self.clientSocket.send(str(text))   # Send data string to socket
                print "BT sent: " + str(text)
            except Exception, e:
                print "BT write failed: " + str(e)
                self.isConnected = False
                self.reconnect()
                continue
            else:
                break
    
    def read(self):
        while True:
            try:
                text = self.clientSocket.recv(2048)  # Receive upto buffersize bytes from socket
                print "BT Received: " + str(text)
                return text
            except Exception, e:
                print "BT Receive failed:" + str(e)
                self.isConnected = False
                self.reconnect()
                continue
            else:
                break
    
    def close(self):
        if self.clientSocket:
            self.clientSocket.close()
        if self.btSocket:
            self.btSocket.close()
            self.bt_is_connected = False


if __name__ == "__main__":
    bt = BTConn()
    bt.connect()
    time.sleep()
    #bt.write("00000020008002000800000001f8000200040008438098010002000400880f00000000000080")
    while(1):
        str=bt.read()
        print(str)

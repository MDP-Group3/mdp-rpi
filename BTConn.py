#!/usr/bin/python
import bluetooth
import time 

class BTConn(object):

	def _init_(self):
		#self.nexus_addr = "08:60:6E:A5:8C:8A"
		self.isConnected = False
        def connect(self):
		try:
			self.btSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
			self.btSocket.bind(("", 4))
			self.btSocket.listen(1) # Start listening on rfcomm socket
			
			port = self.btSocket.getsockname()[1]
			#android app
			#uuid = "8ce255c0-200a-11e0-ac64-0800200c9a66"
			
			#s2 terminal
			uuid = "00001101-0000-1000-8000-00805F9B34FB"

			# Advertise bluetooth service with local SDP server
			bluetooth.advertise_service(self.btSocket, "raspberrypi", service_id = uuid, 
					  service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
					  profiles = [ bluetooth.SERIAL_PORT_PROFILE ]
					  )

			# Wait for an incoming connection, then return new socket
			# representing the connection and its address/port
			print "BT waiting for connection..."
			self.clientSocket, clientAddr = self.btSocket.accept()
			print "BT connected to ", clientAddr			
			self.isConnected = True
		except Exception, e:
			print "BT connection failed:" + str(e)
	def write(self,text):
		try:
			self.clientSocket.send(str(text))
			#print "BT sent: " + str(text)
		except Exception, e:
			print "BT write failed: " + str(e)
			print "Waiting..Reconnecting"
			self.connect()
	def read(self):
		try:
			text = self.clientSocket.recv(2048)
			#print "BT Received: " + str(text)
			return text
		except Exception, e:
			print "BT Receive failed:" + str(e)
			print "BT Waiting..Reconnecting"
			self.connect()
	def close(self):
		try:
			if self.clientSocket:
				self.clientSocket.close()
			if self.btSocket:
				self.btSocket.close()
			self.bt_is_connected = False
		except Exception, e:
			print str(e)
if __name__ == "__main__":
	bt = BTConn()
	bt._init_()
	bt.connect()
	time.sleep(5)
	#var = 1
	#while var==1:
	#	text = raw_input("send: ")
	#	if var == 10:
	#		break
	#	else:
	bt.write("wwww")
	
	time.sleep(5)	
	text = bt.read()
	print str(text)

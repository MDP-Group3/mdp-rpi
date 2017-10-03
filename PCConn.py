#!/usr/bin/python

import socket
import sys
import time

class PCConn(object):

	def __init__(self):
		self.serverIP = "192.168.8.1"
		self.port = 1818
		self.isConnected = False
		self.server = None
		self.client = None
	def connect(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.bind((self.serverIP, self.port))
			self.server.listen(1)
			print "PC waiting for connection..."

			self.client, self.clientIP = self.server.accept()
			print "PC connection from ", self.clientIP
			self.isConnected = True

		except Exception, e:
			print "PC connection Error: ", str(e)

	def write(self, message):
		try:
			self.client.sendto(message, self.clientIP)
			#print "PC Sent: ", str(message)
		except Exception, e:
			print "PC write Error: ", str(e)

	def read(self):
		try:
			text = self.client.recv(2048)
			#print str(text)
			return text
		except Exception, e:
			print "PC read Error: ", str(e)

	def close(self):
		if self.server:
			self.server.close()
		if self.client:
			self.client.close()
		self.pc_is_connect = False

if __name__ == "__main__":
	pcc = PCConn()
	pcc.connect()

	time.sleep(3)
	pcc.write('a')

	text = pcc.read()
	print "Read: ",text
	pcc.close()

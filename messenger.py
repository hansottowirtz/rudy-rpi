#!/usr/bin/env python

import sys
from serial import Serial

class Messenger:
	def __init__(self):
		self.port = Serial('/dev/ttyAMA0', baudrate=9600, timeout=3)

	def send(self, message):
		self.port.write(message + '\n')

	def send_string(self, message, arguments):
		self.send(message + arguments)

	def send_integer(self, message, arguments):
		self.send(message + str(arguments).zfill(3))

if __name__ == "__main__":
	if len(sys.argv) == 1:
		raise ValueError('Usage: ./messenger.py <message> [integer_argument]')
	messenger = Messenger()
	if len(sys.argv) == 2:
		messenger.send(sys.argv[1])
	elif len(sys.argv) == 3:
		messenger.send_integer(sys.argv[1], sys.argv[2])

#!/usr/bin/env python

import BaseHTTPServer

class Server:
	def __init__(self):
		address = ('', 80)
		self.httpd = BaseHTTPServer.HTTPServer(address, BaseHTTPServer.BaseHTTPRequestHandler)

	def update(self):
		self.httpd.handle_request()

if __name__ == "__main__":
	server = Server()
	while True:
		server.update()

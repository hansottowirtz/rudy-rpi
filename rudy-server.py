#!/usr/bin/env python

import zmq
from flask import Flask, request, send_from_directory
from distutils.dir_util import mkpath
app = Flask(__name__, static_url_path='')

context = zmq.Context()
socket = context.socket(zmq.PUB)
mkpath('/tmp/rudy')
socket.bind("ipc:///tmp/rudy/0")

@app.route('/', methods = ['GET'])
def root():
	return send_from_directory('web', 'index.html')

@app.route('/web/<path:path>', methods = ['GET'])
def static_file(path):
    return send_from_directory('web', path)

@app.route("/api/command", methods = ['PUT'])
def command():
	c = request.get_json()['command'].encode('utf-8')
	print 'sending'
	socket.send('command ' + c)
	print 'sent'
	print c
	return ('', 204)

@app.route("/api/park", methods = ['PUT'])
def park():
	socket.send('park left')
	return ('', 204)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)

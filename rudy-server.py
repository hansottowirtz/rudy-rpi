#!/usr/bin/env python

import zmq
import flask
app = flask.Flask(__name__, static_url_path='')

context = zmq.Context.instance()

sock = context.socket(zmq.REQ)
sock.bind('tcp://*:1337')

@app.route("/", methods = ['GET'])
def root():
	return flask.send_from_directory('web', 'index.html')

@app.route('/web/<path:path>', methods = ['GET'])
def static_file(path):
    return flask.send_from_directory('web', path)

@app.route("/api/command", methods = ['PUT'])
def command():
	sock.send(flask.request.get_json()['command'].encode('utf-8'))
	sock.recv()
	return ('', 204)

if __name__ == "__main__":
	app.run(port=80)

#!/usr/bin/env python

import RPi.GPIO as GPIO
from wifi_switcher import WifiSwitcher
from messenger import Messenger
from parking import Parking
import time
import sys
import select
import zmq
from distutils.dir_util import mkpath

class Rudy:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.wifi_switcher = WifiSwitcher()
        self.messenger = Messenger()
        self.parking = Parking(self.messenger)
        self.messenger.send('I')

        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        mkpath('/tmp/rudy')
        self.socket.connect("ipc:///tmp/rudy/0")
        self.socket.setsockopt(zmq.SUBSCRIBE, 'command')
        self.socket.setsockopt(zmq.SUBSCRIBE, 'park')

    def update(self):
        self.wifi_switcher.update()
        try:
            message = self.socket.recv(flags=zmq.NOBLOCK)
            topic, data = message.split()
            if topic == 'command':
                print('Command:', data)
                self.messenger.send(data)
            elif topic == 'park':
                print('Starting parking')
                self.parking.park()
            else:
                print(message)

        except zmq.Again as e:
            pass

        time.sleep(0.01)

    def parse(self, line):
        self.messenger.send(line)

if __name__ == "__main__":
    rudy = Rudy()
    while True:
        rudy.update()

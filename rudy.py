#!/usr/bin/env python

import RPi.GPIO as GPIO
from wifi_switcher import WifiSwitcher
from messenger import Messenger
import time
import sys
import select

class Rudy:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.wifi_switcher = WifiSwitcher()
        self.messenger = Messenger()
        self.messenger.send('I')
        context = zmq.Context.instance()
        self.sock = context.socket(zmq.REP)
        self.sock.connect('tcp://localhost:1337')

    def update(self):
        self.wifi_switcher.update()
        import zmq

        while True:
            message = sock.recv()
            print message
            sock.send("lol")

    def parse(self, line):
        self.messenger.send(line)

if __name__ == "__main__":
    rudy = Rudy()
    while True:
        rudy.update()

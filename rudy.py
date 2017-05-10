#!/usr/bin/env python

import RPi.GPIO as GPIO
from wifi_switcher import WifiSwitcher
from messenger import Messenger
import time

GPIO.setmode(GPIO.BCM)

class Rudy:
    def __init__(self):
        self.wifi_switcher = WifiSwitcher()
        self.messenger = Messenger()
        self.messenger.send('I')

    def update(self):
        self.wifi_switcher.update()

if __name__ == "__main__":
    rudy = Rudy()
    while True:
        rudy.update()

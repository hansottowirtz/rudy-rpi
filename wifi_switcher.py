#!/usr/bin/env python

import os
import time
import RPi.GPIO as GPIO
import shutil
import sys
import time

SWITCH_PIN = 23
root = os.path.dirname(os.path.abspath(__file__))

class WifiSwitcher:
	def __init__(self):
		os.system('ifdown wlan1')
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.prev_value = None
		if 'alive (running)' in os.popen('systemctl status wpa_supplicant').read():
			print('WiFi mode already is client')
			self.prev_value = 1
		elif 'alive (running)' in os.popen('systemctl status hostapd').read():
			print('WiFi mode already is AP')
			self.prev_value = 0
		self.update()

	def update(self):
		value = GPIO.input(SWITCH_PIN)
		if self.prev_value != value:
			if value == 0:
				self.change_to_ap()
			else:
				self.change_to_client()
			self.prev_value = value

	def change_to_ap(self):
		print('WiFi mode is AP')
		self.stop_interface()
		shutil.copyfile(root + '/interfaces-ap.conf', '/etc/network/interfaces')
		self.stop_service('wpa_supplicant')
		time.sleep(1)
		self.start_service('hostapd')
		time.sleep(1)
		self.assign_static_ip()
		time.sleep(1)
		self.start_interface()
		time.sleep(5)
		while '192.168.42.1' not in os.popen('hostname -I').read():
			print('Waiting for ip')
			time.sleep(1)
		self.start_service('isc-dhcp-server')

	def change_to_client(self):
		print('WiFi mode is client')
		self.stop_interface()
		shutil.copyfile(root + '/interfaces-client.conf', '/etc/network/interfaces')
		self.stop_service('isc-dhcp-server')
		time.sleep(1)
		self.stop_service('hostapd')
		time.sleep(1)
		self.start_service('wpa_supplicant')
		time.sleep(1)
		self.assign_dynamic_ip()
		time.sleep(1)
		self.start_interface()

	def stop_interface(self):
		os.system('ifdown wlan0')

	def start_interface(self):
		os.system('ip addr flush dev wlan0')
		os.system('ifup wlan0')

	def start_service(self, name):
		os.system('systemctl start ' + name)

	def stop_service(self, name):
		os.system('systemctl stop ' + name)

	def assign_static_ip(self):
		os.system('ifconfig wlan0 192.168.42.1')

	def assign_dynamic_ip(self):
		os.system('ifconfig wlan0 0.0.0.0 0.0.0.0')

if __name__ == "__main__":
	if len(sys.argv) == 1:
		raise ValueError('Usage: ./wifi_switcher.py ap|client')
	wifi_switcher = WifiSwitcher()
	if sys.argv[1] == 'ap':
		wifi_switcher.change_to_ap()
	elif sys.argv[1] == 'client':
		wifi_switcher.change_to_client()

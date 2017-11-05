#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import socket
import logging

import time

from client import *


HOST = ""   # All available interfaces
PORT = 8080  # The server port




if __name__ == "__main__":

    #create sock
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	name = raw_input('name: ')
	client = Client(s, name)
	try:
		logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
		logging.info("Starting Secure IM Server v1.0")

		client.menu()
		client.loop()

	except KeyboardInterrupt:
	    #client.socket.close()
		try:
			logging.info("Press CTRL-C again within 2 sec to quit")
			time.sleep(2)
		except KeyboardInterrupt:
			logging.info("CTRL-C pressed twice: Quitting!")

	except:
		logging.exception("Server ERROR")
		# if client is not (None):
		#     client.socket.close()
		time.sleep(10)

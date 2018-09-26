#!/usr/bin/python3 -tt

import socket
import threading
import sys

SERVER_IP="127.0.0.1"
SERVER_PORT=8080
print("[!] Connecting to rchat server")


def main():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((SERVER_IP,SERVER_PORT))
	print("[*] Connected to rchat server")
	username=input("Username : ")
	usr_str="username:"+username
	s.send(usr_str.encode('utf-8'))

	
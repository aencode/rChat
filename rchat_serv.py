#!/usr/bin/python3 -tt

import socket
import threading
import sys
import re

#client socket list
MAX_CLIENTS=100
clients=[None]*MAX_CLIENTS
client_name=[None]*MAX_CLIENTS
client_friend=[None]*MAX_CLIENTS	#this list will have keys of clients friends,
#recving thread name
client_thread=[]
#kill switch for client thread
kill_connection=[0]*MAX_CLIENTS

#usercount incremental
client_key_counter=0

#Known commands
known_cmds=['default','quit']


#every time we send string it needs to string to be in bytes not in str, so custom funct

def sendb(client,txt):
	txt=txt.encode('utf-8')
	client.send(txt)

def recvb(client,sz):
	return client.recv(sz).decode('utf-8').rstrip() #removing last char ie 0xa

def send_flag(client):
	sendb(client,"       ___ _           _   \r\n _ __ / __\ |__   __ _| |_ \r\n| '__/ /  | '_ \ / _` | __|\r\n| | / /___| | | | (_| | |_ \r\n|_| \____/|_| |_|\__,_|\__|\r\n                           \r\n")
	
def accept_conn(skt):
	global client_key_counter
	
	while True:
		#client socket
		cs=skt.accept()
		
		clients[client_key_counter]=cs
		#accept() function returns a tuple 0th is recvd connection identifier, second is tuplw with ip and port combo
		send_flag(cs[0])
		print("[*] ",cs[1], " connected")
		client_thread.append(threading.Thread(target=init_client,args=(client_key_counter,)))
		client_thread[-1].start()
		client_key_counter+=1

def username_available(username):
	if username not in known_cmds:
		if username not in client_name:
			return True
	return False

def init_client(client_key):
	#cs is client socket
	cs=clients[client_key][0]
	sendb(cs,"\r\n")
	#username for this connection
	this_username=""
	while True:
		sendb(cs,"Username : ")
		#temp username will store string and check with our criteria
		temp_username=recvb(cs,100)
		if len(temp_username) > 3:
			#check if username is alphanumeric
			if (re.match('^[\w-]+$',temp_username) is not None) == True:
				if username_available(temp_username):
					this_username=temp_username
				else:
					sendb(cs,"[!] Username not available.\r\n")
		if len(this_username) < 4:	#basically checking if this_username variable is set or not,dont get confused with again size checking
			sendb(cs,"[!] Invalid Username, Try Again\r\n")
		else:
			sendb(cs,"\r\n[*] Welcome "+this_username+" !!!\r\n")
			break
	client_name[client_key]=this_username

	#at the end of initalization process start_chat
	#first argument is clients key , second is client_friend key
	start_chat(client_key)



def client_name_to_key(username):
	try:
		key=client_name.index(username)
	except ValueError:
		key=-1
	return key


def execute_client_cmd(client_key,cmd,cmd_arg):
	cs=clients[client_key][0]
	if cmd == "default": 		#replacing friend command with default keyword because it may create confusion
		friend_key=client_name_to_key(cmd_arg)
		if friend_key != -1:
			client_friend[client_key]=friend_key
			sendb(cs,"[*] "+cmd_arg+" is set as friend.\r\n")
		else:
			sendb(cs,"[!] "+cmd_arg+" seems to be offline.\r\n")
	elif cmd == "quit":
		kill_connection[client_key]=1
		cs.close()
		clients[client_key]=None
		client_name[client_key]=None
		client_friend[client_key]=None
		



#after one disconnects remove him/her from clients list
#check while registeration for uniq username
#while chatting let everybody msgs to us, send to particular banda, with :username
#if chatting to one person only add them to :current username or :friend username
#then simple msg will got frnd

#from input msg this func will extract the command
def parse_cmd(client_key,rcv_txt):
	cs=clients[client_key][0]
	if rcv_txt[0] == ":":
		cmd=rcv_txt[1:].split(" ")[0]
		try:
			cmd_arg=rcv_txt[1:].split(" ")[1]
		except IndexError:
			cmd_arg=""

		if cmd in known_cmds: 	#there is some command to be executed (ie a username can not be a known commands)
			execute_client_cmd(client_key,cmd,cmd_arg)
		else:	#After colon there is username
			friend_key=client_name_to_key(cmd)
			if friend_key != -1:
				#message to be sent
				msg_s="\r\n"+client_name[client_key]+" > "+rcv_txt.split(' ',1)[1]+"\r\n"
				sendb(clients[friend_key][0],msg_s)
			elif friend_key == -1:
				sendb(cs,"[!] "+cmd+" seems to be offline.\r\n")
				
	else:
		#this is a message to added friend
		if client_friend[client_key] is not None: #if client has added som friend using cmd :friend username
			msg_s="\r\n"+client_name[client_key]+" > "+rcv_txt+"\r\n"
			sendb(clients[client_friend[client_key]][0],msg_s)
		else: #if client hasnt added any firend , then display help and error msg not sent
			sendb(cs,"[!] Message delivery failed\r\nTo send message\r\n\t1. :friend_username Your_message <cr>\r\n\t2. :firend friend_username <cr> [to set default friend]\r\n")

def start_chat(client_key):
	#cs is client socket 
	cs=clients[client_key][0]
	while True:
		#sendb(cs,"\r\n")
		if kill_connection[client_key]:
			break
		rcv_txt=recvb(cs,1024)
		
		if len(rcv_txt) > 1:
			parse_cmd(client_key,rcv_txt)
			#refresh_chat(friend_key,rcv_txt)
        

def main():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('',8080))
	s.listen(MAX_CLIENTS)
	thread_accept=threading.Thread(target=accept_conn,args=(s,))
	thread_accept.start()

if __name__ == '__main__':
	main()
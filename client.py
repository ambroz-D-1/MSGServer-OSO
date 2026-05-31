from dotenv import load_dotenv
import json
import os
import socket
from time import sleep
from server_messages import TEXT, ACTION, make_message
load_dotenv()

port = int(os.getenv('SRV_PORT'))
addr = os.getenv('SRV_ADDR')

server = socket.socket()

try:
    server.connect((addr, port))
except ConnectionRefusedError:
    exit(-1)

print (server.recv(1024).decode())

user="Admin01"
passwd="elo"

listUsers=make_message(content="",sender=user,recipient="Server",action=ACTION["listAllUsers"])
login="""{"action":"login", "properties":{"login":"Admin01", "password":"elo"}}""".encode()
listOnline=make_message(content="",sender="Client",recipient="Server", action=ACTION["listOnlineUsers"])
# json_packet="""{"action":"register","properties":{"login":"Rassena","password":"elozelo"}}"""
server.send(login)
print(server.recv(1024).decode())
sleep(1)
server.send(listUsers)
print(server.recv(1024).decode())
sleep(1)
server.send(listOnline)
print(server.recv(1024).decode())
sleep(1)

# while input()!='exit':
while True:
    msg=server.recv(1024).decode()
    print(msg+"\n")
    server.send(input().encode())

server.close()
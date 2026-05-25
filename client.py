from dotenv import load_dotenv
import json
import os
import socket


load_dotenv()

port = int(os.getenv('SRV_PORT'))
addr = os.getenv('SRV_ADDR')

server = socket.socket()

try:
    server.connect((addr, port))
except ConnectionRefusedError:
    exit(-1)

print (server.recv(1024).decode())

json_packet="""{"action":"login","properties":{"login":"Admin01","password":"elo"}}"""
server.send(json_packet.encode())
actualJson=json.loads(json_packet)

print("")

while input()!='exit':
    msg=server.recv(1024).decode()
    print(msg)
server.close()
from dotenv import load_dotenv
import json
import os
import psycopg2
import socket
import threading
from user import User

class Server():
    def __init__(self):
        load_dotenv()
        self.dbUrl = os.getenv('DATABASE_URL')
        self.port = int(os.getenv('SRV_PORT'))
        self.maxClientCount = int(os.getenv('SRV_MAX_CONN'))
        self.dbConnection = psycopg2.connect(self.dbUrl)
        self.userConnMap = {}

        print(f"Port: {self.port}\nMax klientów: {self.maxClientCount}")

    def openConnection(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")

        self.server.bind(('0.0.0.0', self.port))
        print("Socket bound to port %s" %(self.port))

    def listen(self):        
        self.server.listen(self.maxClientCount)
        print("socket is listening")

        while True: 
            client, addr = self.server.accept()     
            print('Got connection from', addr)

            threading.Thread(target=self.connectionHandler,args=(client,addr)).start()

    def connectionHandler(self, conn, addr):
        user = User(self,conn,addr, self.dbConnection)
        conn.send('Thank you for connecting!'.encode())
        conn.send(str(user.getSrvPubKey()).encode())

    def insertUser(self, user):
        self.userConnMap[user.getUsername()] = user
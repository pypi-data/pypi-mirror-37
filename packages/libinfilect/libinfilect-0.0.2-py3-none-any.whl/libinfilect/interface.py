import json
import re
import time
import sys
import string
import socket
from os.path import abspath, dirname, join


class Server:
    def __init__(self,ip,port,queue_size=5,terminate_char=b'\n'):
        self.ip=ip
        self.port=port
        self.queue_size=queue_size
        self.terminate_char = terminate_char
    
    def create_socket(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.ip, self.port))
        self.serversocket.listen(self.queue_size)

    def start_listening(self):
        self.connection, addr = self.serversocket.accept()

        buffer = b''
        while True:
            data = self.connection.recv(1024*1000)
            buffer+=data
            if not data or data.endswith(self.terminate_char):
                break
        # print("Received",buffer)
        
        return buffer

    def respond(self,response):
        tosend = response+"\n"
        # print("Replying..",tosend)
        tosend = bytes(tosend.encode('utf-8'))
        self.connection.sendall(tosend)
        self.connection.close()
        return
    
    def __del__(self):
        print("closing socket")
        self.serversocket.close()
    

class Client:
    def __init__(self,ip,port,terminate_char=b'\n'):
        self.ip=ip
        self.port=port
        self.terminate_char = terminate_char
        
        
        
    def send_query_and_await_results(self,query):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientsocket.connect((self.ip, self.port))

        self.clientsocket.sendall(bytes(query+"\n",'UTF-8'))
        # print("Sent",query)
        buffer = b''
        while True:
            data = self.clientsocket.recv(1024*1000)
            buffer+=data
            if not data or data.endswith(self.terminate_char):
                break
        # print("Received",buffer)
        self.clientsocket.close()
        
        return buffer


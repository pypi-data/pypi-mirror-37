import json
import re
import time
import sys
import string
import socket
from os.path import abspath, dirname, join


def create_new_socket():
    """Creates a socket.

    Currently, it just creates a single type of socket.  Arguments can be added
    to create other types of sockets when they are required.

    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s

def read_from_socket(s, terminate_char=b'\n'):
    """Reads from a socket until we reach the end."""

    buf = b''
    while True:
        data = s.recv(1024 * 1000)
        buf += data
        if not data or data.endswith(terminate_char):
            break
    return buf


class Server:
    def __init__(self,ip,port,queue_size=5):
        self.ip=ip
        self.port=port
        self.queue_size=queue_size
    
    def create_socket(self):
        try:
            self.serversocket = create_new_socket()
        except socket.error as e:
            print("Error creating socket,",str(e))
            return
            
        self.serversocket.bind((self.ip, self.port))
        self.serversocket.listen(self.queue_size)


    
    def start_listening(self):
        self.connection, _ = self.serversocket.accept()
        try:
            query = read_from_socket(self.connection).decode('utf8').strip()
            # print("Received",query)
            return query
        except ValueError as e:
            print("Value error:",str(e))
            self.connection.close()
            raise e
        except Exception as e:
            print(str(e))
            self.connection.close()
            return

    def respond(self,response):
        tosend = response+"\n"
        # print("Replying..",tosend)
        tosend = bytes(tosend.encode('utf-8'))
        self.connection.send(tosend)
    

class Client:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port

    
    def create_socket(self):
        try:
            self.clientsocket = create_new_socket()
        except socket.error as e:
            print("Error creating socket,",str(e))
            return
        
        self.clientsocket.connect((self.ip, self.port))

    def send_query_and_await_results(self,query):
        self.clientsocket.send(bytes(query+"\n", 'UTF-8'))
        # print("Sent",query)
        response = read_from_socket(self.clientsocket).decode('utf-8').strip()
        # print("Received",response)
        return response



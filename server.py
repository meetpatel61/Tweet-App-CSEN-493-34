import socket       # Imports socket library
import threading    # Imports threading library
from colorama import Fore # what this library does is it allows you to use colors in the terminal

LOCK = threading.Lock()

from src.urls import functions
print(Fore.GREEN + 'Server has started listening' + Fore.WHITE)

# Use this class to create a new server.
class server:
    def __init__(self, connections, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)   
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, True)  
        self.sock.bind(("localhost", port)) 
        self.sock.listen(connections)
        self.threads = []          

    def start(self):
        while 1:
            LOCK.acquire()      # Obtain the lock if the main thread is unable to run.
            self.threads.append(self.thread())  # Opens a new thread for the client.

    @staticmethod
    def newThread(c, address):
        LOCK.release()      # When a new thread is initiated, the main thread is given control.
        try:
            data = c.recv(4096).decode().split()        # Max size of queries is 4KB.
            print(data)
            c.send(bytes(functions[data[0]](data[1:]), "utf-8"))     # Run the query command's associated function and return the result.
        except:
            pass
        return

    def thread(self):
        c,address = self.sock.accept()      # Makes a new thread after accepting a new connection.
        print(address)
        new = threading.Thread(server.newThread(c, address))  
        new.start()
        return new

Server = server(1000, 12345)  
Server.start()   # Starts a new server

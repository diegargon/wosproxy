#!/usr/bin/python3

import socket
from _thread import *
import threading

print_lock = threading.Lock()

def threaded(c):
    while True:
        data = c.recv(1024)
        if not data:
            print('no data')

            print_lock.release()
            break
        # reverse data = data[::~1]
    c.close()        


appname = "wosproxy"
host = ""
port = 12345
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.bind((host, port))
print("%s is listining on port %d", appname, port)

while True:
    c, addr = s.accept()

    print_lock.acquire()
    print('Connected to:', addr[0], ':', addr[1])
    
    start_new_thread(threaded,(c,))

s.close()
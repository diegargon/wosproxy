"""

Copyright (c) Diego Garcia
All rights reserved.

"""

import os
import socket
from _thread import *
import threading

socket_filename = '/var/run/wosproxy.socket'

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


def leave(s):
    s.close()
    if(os.path.exists(socket_filename)):
        os.remove(socket_filename)    

def wos_main(appname, logger):
    pid_filename = '/tmp/' + appname + '.pid'

    try:
        try:
            os.unlink(socket_filename)
        except OSError:
            if os.path.exists(socket_filename):
                print('socket exists')
                raise                

        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(socket_filename)
        os.chmod(socket_filename, 0o666)
        s.listen(20)
        print(appname, ' is listining on socket ', socket_filename)

        while True:
            c, addr = s.accept()
            print_lock.acquire()
            #print('Connected to:', addr[0], ':', addr[1])
            start_new_thread(threaded,(c,))

    except KeyboardInterrupt:
        #exit key
        leave(s)

    except SystemExit:
        #System exit
        leave(s)    

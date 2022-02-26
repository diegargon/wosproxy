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

def threaded(conn, logger):
    logger.debug('Thread starting with pid %d' % os.getpid())
    while True:
        data = conn.recv(1024)
        if not data:
            logger.debug('Received data: no data')
            break        
        logger.debug('Received data: %s' % data)        
        #break
    logger.debug('Thread end pid %d' % os.getpid())        
    conn.close()        


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
                logger.err(msg ='socket exists')                
                raise                

        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(socket_filename)
        os.chmod(socket_filename, 0o666)
        s.listen(20)        
        logger.info(appname + ' is listining on socket ' + socket_filename + ' pid %d' % os.getpid())
        while True:
            conn, addr = s.accept()      
            start_new_thread(threaded,(conn,logger,))

    except KeyboardInterrupt:
        #exit key
        leave(s)

    except SystemExit:
        #System exit
        leave(s)    

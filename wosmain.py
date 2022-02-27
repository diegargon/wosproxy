"""

Copyright (c) Diego Garcia
All rights reserved.

"""

from curses.ascii import EOT
import os
from pickle import FALSE
import socket
from _thread import *
import threading
from wosproto import WosProto
import subprocess

socket_filename = '/var/run/wosproxy.socket'
eot_flag = "\\r\\n\\r\\n"

print_lock = threading.Lock()

def run_command(cmd, parms):
    if parms == False:
        parms = ''
    result = subprocess.run([cmd, parms], stdout=subprocess.PIPE).stdout.decode('utf-8')
    #return '{"result":"true","data":"hello"}'
    #TODO check is valid json result
    #add result to data { result: true, data: result
    return result

def threaded(conn, logger):    
    logger.debug('Thread starting with pid %d' % os.getpid())
    wos = WosProto(conn,logger)
    recv = wos.receive()
    if 'result' in recv:
        reply = recv
    else:    
        cmd = recv['request']
        parms = False
        if 'parms' in recv:
            parms = recv['parms']
            
        reply = run_command(cmd, parms)

    wos.reply(reply)
    #while True:    
        #data = str(conn.recv(1024), encoding='UTF-8')
        #data = conn.recv(1024)
        #if not data:
        #    logger.debug('Receivedº data: no data')
        #    break        
        #logger.debug('Received data: \'%s\'' % data.strip())
        #if(data == eot_flag):
        #   print("Must break")
        #    break
        
    logger.debug('Thread end pid %d' % os.getpid())        
    conn.close()        


def leave(s, logger):
    logger.debug('Leaving..')
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
            conn.send
            start_new_thread(threaded,(conn,logger,))

    except KeyboardInterrupt:
        #exit key
        leave(s, logger)

    except SystemExit:
        #System exit
        leave(s, logger)    

"""

Copyright (c) Diego Garcia
All rights reserved.

"""

#from curses.ascii import EOT
#from pickle import FALSE
import os
import socket
from _thread import *
import threading
from wosproto import WosProto
import subprocess
import json

socket_filename = '/var/run/wosproxy.socket'
eot_flag = "\\r\\n\\r\\n"

print_lock = threading.Lock()

def run_command(cmd, parms):
    if parms == False:
        parms = ''
    result = subprocess.run([cmd, parms], stdout=subprocess.PIPE).stdout.decode('utf-8')

    return result

def threaded(conn, logger):    
    logger.debug('Thread starting with pid %d' % os.getpid())
    wos = WosProto(conn,logger)
    recv = wos.receive()
    data_reply = []
    json_reply = ''
    reply = {}

    if 'result' in recv: 
        reply = recv #receive error message
    else: 
        for request_cmd in recv['request']:
            cmd = request_cmd['cmd']
            if 'parms' in request_cmd:
                parms = request_cmd['parms']
            else:
                parms = False
            
            json_reply = run_command(cmd, parms)
            if 'noreply' not in recv:
                try:        
                    data_reply.extend(json.loads(json_reply)) #Json to list for extend the list (many cmds)
                except ValueError as e:
                    logger.warning('Request reply invalid json')
                    reply = {'result': False, 'error': 'Request reply invalid json', 'data': json_reply, 'end': 'end'}
                    break
        if not reply: #no error
            json_reply = json.dumps(data_reply)  #extended list to json for build the final reply
            json_reply = '{"result": "ok", "data":'+ json_reply +'}' #build json 
            reply = json.loads(json_reply)            
   
    if 'noreply' not in recv:
        wos.reply(reply)
    else:
        logger.debug('Request not want reply')

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

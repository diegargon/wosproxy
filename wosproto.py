"""

Copyright (c) Diego Garcia
All rights reserved.

    #jsondata= recibe()
    #true/false =valida(jsondata)
    #true/false = validate_request(request)
    #jsondatos = ejecuta(comando)
    #true/false = valid (jsondata)
    #retorna(datos)        

"""

import json
import os

class WosProto:

    def __init__(self, conn, logger):
        self.conn = conn
        self.logger = logger
        #self.bindir = '/usr/share/wosproxy/bin'
        self.bindir = '/home/diego/wosproxy/bin'
        self.eot_flag = "\\r\\n\\r\\n"
        self.eot_flag = "\\r"

    def receive(self):
        jsondata = self.recv()
        if not jsondata:
            reply = {'result': False, 'error': 'No data'}
            return reply
        
        dict_data =  self.is_valid_json(jsondata)
        if dict_data == False:
            reply = {'result': False, 'error': 'Invalid json receive'}
            return reply
        
        if 'request' not in dict_data or self.is_valid_request(dict_data) == False:
            reply = {'result': False, 'error': 'Invalid request receive'}
            return reply
        
        return  dict_data

    def recv(self):
        buff = ''
        while True:
            #data = self.conn.recv(1024)
            data = str(self.conn.recv(4096), 'utf-8')
            data = data.strip()
            if not data:
                self.logger.debug('Received data: no data')
                break
            elif (data == self.eot_flag):
                break
            else:
                self.logger.debug('Received data: \'%s\'' % data.strip())
                buff += data  
                                                 
        return buff

    def is_valid_json(self, jsondata):
        try:
            data = json.loads(jsondata)
        except ValueError as e:
            return False

        if 'request' in data:
            return data
        return False

    def is_valid_request(self, request_data): 
        if os.path.isfile(self.bindir + '/' + request_data['request']):
            request_data['request'] = self.bindir + '/' + request_data['request']
            return True
        
        return False
        
    def reply(self, reply):
        json_data = json.dumps(reply)
        self.conn.send(json_data.encode())
    
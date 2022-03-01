"""

Copyright (c) Diego Garcia
All rights reserved.

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
        jsondata = self.recv() #Sock Recv

        #Check valid json / request(if file exist)
        if not jsondata:
            reply = {'result': False, 'error': 'No data'}
            return reply
        
        dict_data =  self.validate_json(jsondata)
        if dict_data == False:
            reply = {'result': False, 'error': 'Invalid json receive'}
            return reply
        
        if 'request' not in dict_data or self.validate_request(dict_data) == False:
            reply = {'result': False, 'error': 'Invalid request receive'}
            return reply
        
        return  dict_data

    def recv(self):
        buff = ''
        while True:            
            data = str(self.conn.recv(4096), 'utf-8')
            data = data.strip()
            if not data:
                self.logger.debug('No data received')
                break
            elif (data == self.eot_flag):
                break
            else:
                self.logger.debug('Received data: \'%s\'' % data.strip())
                buff += data  
                                                 
        return buff

    # Check valid syntax & request field exists
    def validate_json(self, jsondata):
        try:
            data = json.loads(jsondata)
        except ValueError as e:
            return False

        if 'request' in data:
            return data

        return False

    # request contains the file to execute we add the bindir path and check
    # if file exists
    def validate_request(self, request_data): 
        request_data['request'] = self.bindir + '/' + request_data['request']
        if os.path.isfile(request_data['request']):
            if os.access(request_data['request'], os.X_OK):
                return True
            else:
                self.logger.error('File is not executable: %s' % request_data['request'])        
        return False
        
    def reply(self, reply):
        json_data = json.dumps(reply)
        self.conn.send(json_data.encode())
    
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
        #self.eot_flag = "\\r\\n\\r\\n"
        self.eot_flag = "\r\n\r\n"
        #self.eot_flag = "\\r"

    def receive(self):        
        jsondata = self.recv() #Sock Recv

        #Check valid json / request(if file exist)
        if not jsondata:
            reply = {'result': False, 'error': 'No data'}
            return reply
        
        self.logger.debug('json data receive: \'%s\'' % jsondata) 
        data_dct =  self.validate_json(jsondata)
        
        if data_dct == False:
            reply = {'result': False, 'error': 'Invalid json receive'}
            return reply
        
        if 'request' not in data_dct or self.validate_request(data_dct) == False:
            reply = {'result': False, 'error': 'Invalid request receive'}
            return reply
        
        return  data_dct

    def recv(self):
        buff = ''
        while True:            
            data = str(self.conn.recv(4096), 'utf-8')
            #data = data.strip()
            if not data:
                self.logger.debug('No data received: \'%s\'' % data) #data.strip())
                break                
            elif (self.eot_flag in data):
                self.logger.debug('Line Break received')
                buff += data.strip()
                break
            else:
                self.logger.debug('Received data: \'%s\'' % data ) #data.strip())
                buff += data.strip()
                                                 
        return buff

    # Check valid syntax & request field exists, return dict
    def validate_json(self, jsondata):
        try:
            data = json.loads(jsondata)
        except ValueError as e:
            return False

        if 'request' in data:
            return data

        return False

    # request contains the file to execute 
    # we add the bindir path and check if file exists
    def validate_request(self, request_data): 
        for i,request_value in enumerate(request_data['request']):
            script_request = self.bindir + '/' + request_value['cmd']
            request_data['request'][i]['cmd'] = script_request
            if not os.path.isfile(script_request):                
                self.logger.error('File is not executable: %s' % script_request)        
                return False
        return True
         
    def reply(self, reply):        
        json_data = json.dumps(reply)
        self.logger.debug('Reply data: \'%s\'' % reply)
        self.conn.send(json_data.encode())
    
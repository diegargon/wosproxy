"""

Copyright (c) Diego Garcia
All rights reserved.

"""

import logging
import logging.handlers

class Logger:
    
    def __init__(self, appname, loglevel='LOG_DEBUG'):        
        self.appname = appname
        self.devlog = '/dev/log'
        self.logger = logging.getLogger(self.appname)        
        self.handler = logging.handlers.SysLogHandler(address = self.devlog, facility=logging.handlers.SysLogHandler.LOG_DAEMON)
        self.logger.addHandler(self.handler)
        formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
        self.handler.setFormatter(formatter)
        self.console = False
        if loglevel == 'LOG_INFO':            
            self.logger.setLevel(logging.INFO)
        elif loglevel == 'LOG_WARNING':
            self.logger.setLevel(logging.WARNING)
        elif loglevel == 'LOG_ERR':
            self.logger.setLevel(logging.ERROR)
        else:            
            self.logger.setLevel(logging.DEBUG)

    def toConsole(self, set = True):
        self.console = set       
    def debug(self, msg):
        self.logger.debug(msg)        
        if self.console:
            print(msg)
    def info(self, msg):
        self.logger.info(msg)
        if self.console:
            print(msg)
    def warning(self, msg):
        self.logger.warning(msg)
        if self.console:
            print(msg)
    def err(self, msg):
        self.logger.error(msg)
        if self.console:
            print(msg)
            
#!/usr/bin/python3

"""

Copyright (c) Diego Garcia
All rights reserved.

"""

import sys, time
from daemon import Daemon
from wosmain import wos_main

#Overwrite daemon run method
class WosDaemon(Daemon):
        def run(self):
                wos_main()


if len(sys.argv) == 2 and sys.argv[1] == '-nd':
    wos_main()
elif len(sys.argv) == 3 and sys.argv[1] == '-d':      
    daemon = WosDaemon('/tmp/wosd.pid')
    if 'start' == sys.argv[2]:
        daemon.start()
    elif 'stop' == sys.argv[2]:
        daemon.stop()        
    elif 'restart' == sys.argv[2]:
        daemon.restart()
    else:
        print("Unknown option")
        sys.exit(2)
    sys.exit(0)
else:
    print ("Usage:")
    print ("%s -nd (No daemon)" % sys.argv[0])
    print ("%s -d start|stop|restart (daemon mode)" % sys.argv[0])
    sys.exit(2)    

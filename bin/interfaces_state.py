#!/usr/bin/python3
#
#

import json
import re
import os
import pprint
import socket

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

interfaces_dir_get = '/sys/class/net'

lista = []
static_list = {"id":"interfaces_state", "type": "array", "value":[]}

interfaces = []


flags = {
	'IFF_UP'		 :	1<<0,
	'IFF_BROADCAST'	 :	1<<1,
	'IFF_DEBUG'		 :	1<<2,
	'IFF_LOOPBACK'	 :	1<<3,
	'IFF_POINTOPOINT':  1<<4,
	'IFF_NOTRAILERS' :	1<<5,
	'IFF_RUNNING'	 :	1<<6, # why sys not return RUNNING?
	'IFF_NOARP'		 :	1<<7, 
	'IFF_PROMISC'	 :	1<<8,  
	'IFF_ALLMULTI'	 :	1<<9, 
	'IFF_MASTER'	 :	1<<10, 
	'IFF_SLAVE'		 :	1<<11,
	'IFF_MULTICAST'	 :	1<<12, 
	'IFF_PORTSEL'	 :	1<<13,
	'IFF_AUTOMEDIA'	 :	1<<14, 
	'IFF_DYNAMIC'	 :	1<<15,
	'IFF_LOWER_UP'	 :	1<<16,
	'IFF_DORMANT'	 :  1<<17, 
	'IFF_ECHO'  	 :  1<<18, 
}

def get_hflags(iface_flags):
    hflags = []
    for kflags, vflags in flags.items():
        if (int(iface_flags, 16) & vflags):
            hflags.append(kflags[4:])
    return hflags

def get_keyfiles_value(dir):
    keyvalue = {}
    basename = os.path.basename(dir)

    onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))] 
    for onefile in onlyfiles:
        #if basename not in keyvalue:
        #    keyvalue[basename] =  {'iface': basename}
        #print(dir + '/' +  onefile)
        readdir = dir + '/' +  onefile
        if os.access(readdir, os.R_OK):                        
            with open(readdir, 'r') as file:
                try:
                    data = file.readline().strip()
                    #change hex to dec   
                    keyvalue.update({onefile: data})
                    if onefile == 'flags':
                        hflags = get_hflags(data)
                        keyvalue.update({'hflags': hflags})
                except:
                    False
                
    #pprint.pprint(keyvalue)
    #pprint.pprint(onlyfiles)
    return keyvalue

def parse_interfaces_dir(interface_dir):
    False

interfaces_dirs = [ f.path for f in os.scandir(interfaces_dir_get) if f.is_dir() ]

_tmp = {}
for interface_dir in interfaces_dirs:    
    iface = os.path.basename(interface_dir)
    _tmp[iface] = {'iface': iface}
    _tmp[iface].update(get_keyfiles_value(interface_dir))
    #get stats
    interface_dir_stats = interface_dir + '/statistics'
    #print(interface_dir)
    _tmp[iface].update(get_keyfiles_value(interface_dir_stats))
    #_tmp = parse_interfaces_dir(interface_dir)


pprint.pprint(_tmp)
#pprint.pprint(interfaces)
#interfaces_state = parse_interfaces_dir(interfaces_state_dir)
#pprint.pprint(interfaces_state)

#lista.append(interfaces_state)
#print(json.dumps(lista))

#print hex
#print(format(flags['IFF_RUNNING'], '#X'))
#print(hex(flags['IFF_RUNNING']))

x = 0x1003 #wan0
x = "0x1043"
#x = 0x9 #lo
"""
print('RUNNING')
print(x & flags['IFF_RUNNING'])
print('UP')
print(x & flags['IFF_UP'] )
print('BROADCAST')
print(x & flags['IFF_BROADCAST'] ) 
print('MULTICAST')
print(x & flags['IFF_MULTICAST'] ) 
print('LOOPBACK')
print(x & flags['IFF_LOOPBACK'] ) 
print('PROMISC')
print(x & flags['IFF_PROMISC'] ) 
"""
"""
test = []
if (int(x, 16) & flags['IFF_UP']):
    test.append('IFF_IP')
    test.append('IFF_IP')

pprint.pprint(test)
"""
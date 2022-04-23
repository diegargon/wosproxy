#!/usr/bin/python3
#
#

import json
import re
import os
import pprint
import socket

import psutil

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


lista = []
interfaces_info = {"id":"interfaces_info", "type": "array", "value":[]}


addresses = psutil.net_if_addrs()
stats = psutil.net_if_stats()
pprint.pprint(addresses)
pprint.pprint(stats)
interfaces = {}


for iface, addr_list in addresses.items():
    interfaces[iface] = {'iface': iface, 'address': []}
    if iface in stats and stats[iface].isup == True:
        interfaces[iface].update({'up': 1})
        interfaces[iface].update({'mtu': stats[iface].mtu})
        interfaces[iface].update({'speed': stats[iface].speed})
    else: 
        interfaces[iface].update({'up': 0})    
    for addr in addr_list:        
        _dict_addr = {}
	    
        if ( addr.family == socket.AF_INET):
            _dict_addr.update({'family': 'AF_INET'})            
        elif addr.family == socket.AF_INET6:
            _dict_addr.update({'family': 'AF_INET6'})
        elif addr.family == psutil.AF_LINK:
            _dict_addr.update({'family': 'AF_LINK'})

        if (addr.address != None):
            _dict_addr.update({'address': getattr(addr, 'address')})
        if (addr.netmask != None):
            _dict_addr.update({'netmask': getattr(addr, 'netmask')})
        if (addr.broadcast != None):
            _dict_addr.update({'broadcast': getattr(addr, 'broadcast')})
        if (addr.ptp != None):
            _dict_addr.update({'ptp': getattr(addr, 'ptp')})            
        interfaces[iface]['address'].append(_dict_addr)


interfaces_info['value'].append(interfaces)
lista.append(interfaces_info)
print(json.dumps(lista))

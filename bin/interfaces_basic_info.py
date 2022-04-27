#!/usr/bin/python3
#
#

import json
import socket
import psutil
import os

lista = []
interfaces_info = {"id":"interfaces_info", "type": "array", "value":[]}


addresses = psutil.net_if_addrs()
stats = psutil.net_if_stats()

interfaces = {}


for iface, addr_list in addresses.items():
    interfaces[iface] = {'iface': iface, 'address': []}
    if iface in stats and stats[iface].isup == True:
        interfaces[iface].update({'up': 1})
        interfaces[iface].update({'mtu': stats[iface].mtu})
        interfaces[iface].update({'speed': stats[iface].speed})
    else: 
        interfaces[iface].update({'up': 0})    

    if os.path.isdir('/sys/devices/virtual/net/'+ iface):
        virtual = 1
    else:
        virtual = 0
    interfaces[iface].update({'virtual': virtual})
    devtype = 'unknown'
    with open('/sys/class/net/'+ iface + '/uevent') as f:
        dev = f.readline().strip()
        dev = dev.split('=')
        if dev[0] == 'INTERFACE' and virtual == 0:
            devtype = 'physical'
        elif dev[0] == 'DEVTYPE':
            devtype = dev[1]

    interfaces[iface].update({'devtype': devtype})

    for addr in addr_list:        
        _dict_addr = {}
	    
        if ( addr.family == socket.AF_INET):
            _dict_addr.update({'family': 2})
            _dict_addr.update({'family_h': 'ipv4'})            
        elif addr.family == socket.AF_INET6:
            _dict_addr.update({'family': 10})
            _dict_addr.update({'family_h': 'ipv6'})
        elif addr.family == psutil.AF_LINK:
            _dict_addr.update({'family': 17})
            _dict_addr.update({'family_h': 'mac'})

        if (addr.address != None):
            _dict_addr.update({'address': getattr(addr, 'address').replace('%'+ iface, '')})
        if (addr.netmask != None and addr.netmask != 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff' and addr.netmask != 'ffff:ffff:ffff:ffff::'):
            _dict_addr.update({'netmask': getattr(addr, 'netmask')})
        if (addr.broadcast != None):
            _dict_addr.update({'broadcast': getattr(addr, 'broadcast')})
        if (addr.ptp != None):
            _dict_addr.update({'ptp': getattr(addr, 'ptp')})            
        interfaces[iface]['address'].append(_dict_addr)


interfaces_info['value'].append(interfaces)
lista.append(interfaces_info)
print(json.dumps(lista))

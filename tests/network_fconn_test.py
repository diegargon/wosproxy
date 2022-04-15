#!/usr/bin/python3
#
#
# TODO: -filter udp,tcp,icmp
# TODO: -filter_st ?
# TODO: ipv6


import json
import re

nf_conn_file = '/proc/net/nf_conntrack'

def read_file(f):
    sockets = f.split('\n')
    return [line.strip() for line in sockets]

def hexaddr_to_ip(address):
    hex_addr, hex_port = address.split(':')
    addr_list = [hex_addr[i:i+2] for i in range(0, len(hex_addr), 2)]
    addr_list.reverse()
    addr = ".".join(map(lambda x: str(int(x, 16)), addr_list))
    return addr

def hexaddr_to_port(address):
    hex_addr, hex_port = address.split(':')
    return str(int(hex_port, 16))


def get_nfsocket_formated(lsocket):
    if not lsocket:
        return False    
    lsplit = re.split(r'\s+', lsocket)

    #print(lsocket)
    if lsplit[2] == "tcp":
        _tmp = {
            'layer': lsplit[0],
            'nlayer': lsplit[1],
            'stype': lsplit[2],
            'ntype': lsplit[3],
            'timeout': lsplit[4],
            'state': lsplit[5],
            'saddr': lsplit[6],
            'sport': lsplit[8],
            'daddr': lsplit[7],
            'dport': lsplit[9],
        }
    else:
        _tmp = {
            'layer': lsplit[0],
            'nlayer': lsplit[1],
            'stype': lsplit[2],
            'ntype': lsplit[3],
            'timeout': lsplit[4],
            'state': '',
            'saddr': lsplit[5],
            'sport': lsplit[7],
            'daddr': lsplit[6],
            'dport': lsplit[8],
        }
    return _tmp
###

lista = []

with open(nf_conn_file) as f:
    sockets = read_file(f.read())
for lsocket in sockets:
    fsocket = get_nfsocket_formated(lsocket)
    if fsocket:
        lista.append(fsocket)    
        print(fsocket)

#print(json.dumps(lista))
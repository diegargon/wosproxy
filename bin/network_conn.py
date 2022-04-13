#!/usr/bin/python3
#
#
# TODO: -filter udp,tcp,icmp
# TODO: -filter_st ?
# TODO: ipv6


import json
import re

tcp_file = '/proc/net/tcp'
udp_file = '/proc/net/udp'
icmp_file = '/proc/net/icmp'

def read_file(f):
    sockets = f.split('\n')[1:-1]
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


def get_socket_formated(lsocket, ipv, sock_type):
    lsplit = re.split(r'\s+', lsocket)
    seq = lsplit[0].replace(":", ''),
    _tmp = {
        'id': seq,
        'seq': seq,
        'stype': sock_type,
        'state': int(lsplit[3], 16),
        'laddr': hexaddr_to_ip(lsplit[1]),
        'lport': hexaddr_to_port(lsplit[1]),
        'raddr': hexaddr_to_ip(lsplit[2]),
        'rport': hexaddr_to_port(lsplit[2]),        
        'uid': lsplit[7],
        'timeout': lsplit[8],        
        'inode': lsplit[9],
        'nlayer': ipv,        
    } 
    return _tmp
###

lista = []
net_conn = {"id":"netconn_local", "type": "array", "value":[]}

with open(tcp_file) as f:
    sockets = read_file(f.read())
for lsocket in sockets:
    fsocket = get_socket_formated(lsocket, 'ipv4', 'tcp')
    net_conn['value'].append(fsocket)

with open(udp_file) as f:
    sockets = read_file(f.read())
for lsocket in sockets:
    fsocket = get_socket_formated(lsocket, 'ipv4', 'udp')
    net_conn['value'].append(fsocket)

with open(icmp_file) as f:
    sockets = read_file(f.read())
for lsocket in sockets:
    fsocket = get_socket_formated(lsocket, 'ipv4', 'udp')
    net_conn['value'].append(fsocket) 

lista.append(net_conn)

print(json.dumps(lista))
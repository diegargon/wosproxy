#!/usr/bin/python3
#
#
# TODO: -filter udp,tcp,icmp
# TODO: -filter_st ?
# TODO: ipv6

import json
import re
import socket
import pickle

tcp_file = '/proc/net/tcp'
udp_file = '/proc/net/udp'
icmp_file = '/proc/net/icmp'

resolv_cache = '/tmp/resolv-cache'

resolv = {
    "0.0.0.0": "default",
    "127.0.0.1":"localhost",
}

RESOLV_IP = True
# Avoid slow down limiting request without using resolv_cache
RESOLV_COUNT = 0 
MAX_RESOLV = 20


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
    global RESOLV_COUNT

    lsplit = re.split(r'\s+', lsocket)
    seq = lsplit[0].replace(":", '')
    laddr = hexaddr_to_ip(lsplit[1])
    raddr = hexaddr_to_ip(lsplit[2])
    lhost = ''
    rhost = ''

    if RESOLV_IP and RESOLV_COUNT <= MAX_RESOLV:
        if laddr in resolv:
            lhost = resolv[laddr]
        else:
            try:
                RESOLV_COUNT += 1
                lhost = socket.gethostbyaddr(laddr)[0]
                resolv[laddr] = lhost
            except:
                resolv[laddr] = laddr

        if raddr in resolv:
            rhost = resolv[raddr]
        else:
            try:
                RESOLV_COUNT += 1
                rhost = socket.gethostbyaddr(raddr)[0]
                resolv[raddr] = rhost
            except:                
                resolv[raddr] = raddr

    _tmp = {
        'id': seq,
        'seq': seq,
        'stype': sock_type,
        'state': int(lsplit[3], 16),
        'laddr': laddr,
        'lhost': lhost,
        'lport': hexaddr_to_port(lsplit[1]),
        'raddr': raddr,
        'rhost': rhost,
        'rport': hexaddr_to_port(lsplit[2]),        
        'uid': lsplit[7],
        'timeout': lsplit[8],        
        'inode': lsplit[9],
        'layer': ipv,        
    } 
    return _tmp
###

lista = []
net_conn = {"id":"netconn_local", "type": "array", "value":[]}

try:
    f_cache = open(resolv_cache, "rb")
    resolv = pickle.load(f_cache)
    f_cache.close()
except:
    False


with open(tcp_file) as f:
    sockets = read_file(f.read())
    for lsocket in sockets:
        fsocket = get_socket_formated(lsocket, 'ipv4', 'tcp')
        net_conn['value'].append(fsocket)
    f.close()

with open(udp_file) as f:
    sockets = read_file(f.read())
    for lsocket in sockets:
        fsocket = get_socket_formated(lsocket, 'ipv4', 'udp')
        net_conn['value'].append(fsocket)
    f.close()

with open(icmp_file) as f:
    sockets = read_file(f.read())
    for lsocket in sockets:
        fsocket = get_socket_formated(lsocket, 'ipv4', 'udp')
        net_conn['value'].append(fsocket) 
    f.close()

   
try:
    f_cache = open(resolv_cache, "wb")
    pickle.dump(resolv, f_cache)
    f_cache.close()
except:
    False

lista.append(net_conn)

print(json.dumps(lista))
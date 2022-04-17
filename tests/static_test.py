#!/usr/bin/python3
#
#

import json
import pickle
import re

static_file="/proc/net/route"
resolv_cache="/tmp/test"

RESOLV_IP = True

lista = []
static_list = {"id":"static_routes", "type": "array", "value":[]}


def read_file(f):
    sockets = f.split('\n')[1:-1]
    return [line.strip() for line in sockets]

def hexaddr_to_ip(address):
    hex_addr, hex_port = address.split(':')
    addr_list = [hex_addr[i:i+2] for i in range(0, len(hex_addr), 2)]
    addr_list.reverse()
    addr = ".".join(map(lambda x: str(int(x, 16)), addr_list))
    return addr


def hexaddr_to_ip(address):
    addr_list = [address[i:i+2] for i in range(0, len(address), 2)]
    addr_list.reverse()
    addr = ".".join(map(lambda x: str(int(x, 16)), addr_list))
    return addr

def parse_static_routes (line):
    line_split = re.split(r'\s+', line)

    _tmp = {
        'iface' : line_split[0],
        'destination' : hexaddr_to_ip(line_split[1]),
        'gateway' : hexaddr_to_ip(line_split[2]),
        'flags' : int(line_split[3], 16),
        'refcnt' : line_split[4],
        'use' : line_split[5],
        'metric' : line_split[6],
        'mask' : hexaddr_to_ip(line_split[7]),
        'mtu' : line_split[8],
        'window' : line_split[9],
        'irtt' : line_split[10],
    }
    
    return _tmp


try:
    f_cache = open(resolv_cache, "rb")
    resolv = pickle.load(f_cache)
    f_cache.close()
except:
    False

##

with open(static_file) as f:
    content = read_file(f.read())
    for line in content:
        f_static = parse_static_routes(line)
        static_list['value'].append(f_static)
    f.close()


##

try:
    f_cache = open(resolv_cache, "wb")
    pickle.dump(resolv, f_cache)
    f_cache.close()
except:
    False


print(static_list)
#lista.append(static_list)
#print(json.dumps(lista))
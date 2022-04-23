#!/usr/bin/python3
#
#
# TODO: -filter udp,tcp,icmp
# TODO: -filter_st ?

import json
import re
import socket
import pickle

#TODO to option
RESOLV_IP= True 
#RESOLV_IP = False

LOCALHOST_IGNORE = True

nf_conn_file = '/proc/net/nf_conntrack'

resolv_cache = '/tmp/resolv-cache'

resolv = {
    "0.0.0.0": "default",
    "127.0.0.1":"localhost",
}

idx = 1

# Avoid slow down limiting request without using resolv_cache
RESOLV_COUNT = 0 
MAX_RESOLV = 30

def read_file(f):
    sockets = f.split('\n')
    return [line.strip() for line in sockets]

def gethost(addr): 
    #TODO Timeout
    return socket.gethostbyaddr(addr)[0]

def get_nfsocket_formated(lsocket):
    global RESOLV_COUNT

    if not lsocket:
        return False            
    lsplit = re.split(r'\s+', lsocket)
    tcp_dst_idx = 10
    udp_dst_idx = 9             
    
    if "[UNREPLIED]" in lsplit[tcp_dst_idx]:
        tcp_dst_idx += 1
    if "[UNREPLIED]" in lsplit[udp_dst_idx]:       
        if lsplit[2] == "unknonwn":
            #udp_dst_idx += 2
            False
        else:
            udp_dst_idx += 1
    #print(lsocket)
    if lsplit[2] == "tcp":
        saddr = lsplit[6].replace('src=','').strip()
        daddr = lsplit[tcp_dst_idx].replace('src=','').strip()
        shost=''
        dhost=''
        if LOCALHOST_IGNORE:
            if saddr == "127.0.0.1" and daddr == "127.0.0.1":
                return False
        if RESOLV_IP:
            if saddr in resolv:                
                shost = resolv[saddr]
            elif  RESOLV_COUNT < MAX_RESOLV:                
                try:
                    RESOLV_COUNT += 1               
                    shost = gethost(saddr)
                    resolv[saddr] = shost
                except:
                    resolv[saddr] = saddr

            if daddr in resolv:
                dhost = resolv[daddr]
            elif RESOLV_COUNT < MAX_RESOLV:
                try:
                    RESOLV_COUNT += 1
                    dhost = gethost(daddr)
                    resolv[daddr] = dhost
                except:                
                    resolv[daddr] = daddr
    
        _tmp = {
            'id': idx,
            'stype': lsplit[2],
            'state': lsplit[5],
            'saddr': saddr,
            'shost': shost,
            'sport': lsplit[8].replace('sport=',''),
            'daddr': daddr,
            'dhost': dhost,
            'dport': lsplit[9].replace('dport=',''),
            'timeout': lsplit[4],
            'nlayer': lsplit[1],
            'layer': lsplit[0],
            'ntype': lsplit[3],
        }        
    elif lsplit[2] == "icmp":
        saddr = lsplit[5].replace('src=','').strip()
        daddr = lsplit[6].replace('dst=','').strip()
        shost=''
        dhost=''
        if LOCALHOST_IGNORE:
            if saddr == "127.0.0.1"  and daddr == "127.0.0.1":
                return False

        if RESOLV_IP:
            if saddr in resolv:
                shost = resolv[saddr]
            elif RESOLV_COUNT < MAX_RESOLV:
                try:
                    RESOLV_COUNT += 1
                    shost = gethost(saddr)
                    resolv[saddr] = shost
                except:
                    resolv[saddr] = saddr

            if daddr in resolv:
                dhost = resolv[daddr]
            elif RESOLV_COUNT < MAX_RESOLV:
                try:
                    RESOLV_COUNT += 1
                    dhost = gethost(daddr)
                    resolv[daddr] = dhost
                except:                
                    resolv[daddr] = daddr
    

        _tmp = {
            'id': idx,
            'stype': lsplit[2],
            'state': lsplit[7].replace('type=',''),
            'saddr': saddr,
            'shost': shost,
            'sport': '',
            'daddr': daddr,
            'dhost': dhost,
            'dport': '',
            'timeout': lsplit[4],
            'nlayer': lsplit[1],
            'layer': lsplit[0],            
            'ntype': lsplit[3],
        }

    else:

        saddr = lsplit[5].replace('src=','').strip()
        daddr = lsplit[udp_dst_idx].replace('src=','').strip()
        shost=''
        dhost=''

        if LOCALHOST_IGNORE:
            if saddr == "127.0.0.1"  and daddr == "127.0.0.1":
                return False
        
        if RESOLV_IP:
            if saddr in resolv:
                shost = resolv[saddr]
            elif  RESOLV_COUNT < MAX_RESOLV:
                try:
                    RESOLV_COUNT += 1                    
                    shost = gethost(saddr)
                    resolv[saddr] = shost
                except:
                    resolv[saddr] = saddr

            if daddr in resolv:
                dhost = resolv[daddr]
            elif  RESOLV_COUNT < MAX_RESOLV:
                try:
                    RESOLV_COUNT += 1
                    dhost = gethost(daddr)
                    resolv[daddr] = dhost
                except:                
                    resolv[daddr] = daddr
    
        _tmp = {
            'id': idx,
            'stype': lsplit[2],
            'state': '',
            'saddr': saddr,
            'shost': shost,
            'sport': lsplit[7].replace('sport=',''),
            'daddr': daddr,
            'dhost': dhost,
            'dport': lsplit[8].replace('dport=',''),
            'timeout': lsplit[4],
            'nlayer': lsplit[1],
            'layer': lsplit[0],           
            'ntype': lsplit[3],
        }

    return _tmp
###

lista = []
net_fconn = {"id":"netconn_forward", "type": "array", "value":[]}

try:
    f_cache = open(resolv_cache, "rb")
    resolv = pickle.load(f_cache)
    f_cache.close()
except:
    False


with open(nf_conn_file) as f:
    sockets = read_file(f.read())    
for lsocket in sockets:
    fsocket = get_nfsocket_formated(lsocket)
    if fsocket:
        net_fconn['value'].append(fsocket)
        idx += 1

try:
    f_cache = open(resolv_cache, "wb")
    pickle.dump(resolv, f_cache)
    f_cache.close()
except:
    False

net_fconn['value'] = sorted(net_fconn['value'], key=lambda d: d['saddr'])
lista.append(net_fconn)
print(json.dumps(lista))
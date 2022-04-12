#!/usr/bin/python3

import psutil
import json

network_lista = []

network = psutil.net_io_counters(pernic=True)

for net_if in network:

    a = {'net_device': net_if, 'net_bytes_sent': network[net_if].bytes_sent, 
    'net_bytes_recv': network[net_if].bytes_recv,
    'net_packets_sent': network[net_if].packets_sent,  
    'net_packets_recv': network[net_if].packets_recv,
    'net_err_in': network[net_if].errin,
    'net_err_out': network[net_if].errout,
    'net_drop_in': network[net_if].dropin,
    'net_drop_out': network[net_if].dropout,    
    }
    network_lista.append(a)

print(network_lista)
print(json.dumps(network_lista))
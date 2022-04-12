#!/usr/bin/python3
# Response:    [{"id": "network", "type": "text", "value": 
#                   [{"id": "lo", "net_device": "lo", "net_bytes_sent": "331.9 MB", ..., "net_drop_out": 0}, 
#                    {"id": "lan0", "net_device": "lan0", "net_bytes_sent": "605.46 GB",.. "net_drop_out": 0}
#                   ]
#              }]
import psutil
import json
import math
lista = []

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

network_lista = {"id":"network", "type": "text", "value":[]}

network = psutil.net_io_counters(pernic=True)

for net_if in network:
    a = {'id': net_if,
    'net_device': net_if, 
    'net_bytes_sent': convert_size(network[net_if].bytes_sent), 
    'net_bytes_recv': convert_size(network[net_if].bytes_recv),
    'net_packets_sent': network[net_if].packets_sent,  
    'net_packets_recv': network[net_if].packets_recv,
    'net_err_in': network[net_if].errin,
    'net_err_out': network[net_if].errout,
    'net_drop_in': network[net_if].dropin,
    'net_drop_out': network[net_if].dropout,    
    }
    network_lista['value'].append(a)

lista.append(network_lista)
#print(json.dumps(network_lista))
print(json.dumps(lista))
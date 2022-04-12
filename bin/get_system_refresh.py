#!/usr/bin/python3

import psutil
import json

lista = []

ram_usage = psutil.virtual_memory().percent
lista.append({"id": "ram_usage", "type": "text", "value": ram_usage})
lista.append({"id": "ram_usage_value", "type": "value", "value": ram_usage})
cpu_load = psutil.cpu_percent(interval=0.1, percpu=False)
lista.append({"id": "cpu_load", "type": "text", "value": cpu_load})
lista.append({"id": "cpu_load_value", "type": "value", "value": cpu_load})
load_avg = psutil.getloadavg()[0]
lista.append({"id": "load_avg", "type": "text", "value": load_avg})
lista.append({"id": "load_avg_value", "type": "value", "value": load_avg})

cpu_freq = psutil.cpu_freq() 
lista.append({"id": "cpu_freq", "type": "text", "value": cpu_freq})


#lista.append({"id": "partitions", "type": "text", "value": list(psutil.disk_partitions())})
#lista.append({"id": "disk_usage", "type": "text", "value": psutil.disk_usage('/') })
#lista.append({"id": "disks_io", "type": "text", "value": psutil.disk_io_counters(perdisk=True)})
#print(psutil.disk_io_counters(perdisk=True))
json_data = json.dumps(lista)
print (json_data)


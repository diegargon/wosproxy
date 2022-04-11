#!/usr/bin/python3

import psutil
import json

lista = []

lista.append({"id": "ram_usage", "type": "text", "value": psutil.virtual_memory().percent})
lista.append({"id": "cpu_load", "type": "text", "value": psutil.cpu_percent(interval=0.1, percpu=False)})
lista.append({"id": "load_avg", "type": "text", "value": psutil.cpu_freq()})
lista.append({"id": "ncpu", "type": "text", "value": psutil.cpu_count(logical=False)})
lista.append({"id": "nthreads", "type": "text", "value": psutil.cpu_count()})
lista.append({"id": "partitions", "type": "text", "value": psutil.disk_partitions()})
lista.append({"id": "disk_usage", "type": "text", "value": psutil.disk_usage('/') })
lista.append({"id": "disks_io", "type": "text", "value":  psutil.disk_io_counters(perdisk=True)})

json_data = json.dumps(lista)
print (json_data)

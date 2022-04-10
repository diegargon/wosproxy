#!/usr/bin/python3
# depends:  psutil (pip install psutils)
# Request:      { "request": "get_system.py" }
# Response:     { "data": [{"id":"html_id","value":"field_value"}] }
import json
from configparser import ConfigParser
import os.path
import socket
import datetime
import subprocess
import platform
import psutil


config = ConfigParser()

lista = []

if os.path.isfile('/etc/os-release'):
    with open("/etc/os-release") as fp_stream:
        config.read_string("[root]\n" + fp_stream.read())  # trick missing section [head]
    
    if(config.has_option('root', 'NAME')):
        lista.append({"id": "distro_name", "type": "text", "value": config['root']['NAME']})
    if(config.has_option('root', 'PRETTY_NAME')):
        lista.append({"id": "distro_fullname", "type": "text", "value": config['root']['PRETTY_NAME']})
    if(config.has_option('root', 'CODENAME')):
        lista.append({"id": "os_codename", "type": "text", "value": config['root']['CODENAME']})
    if(config.has_option('root', 'VERSION')):
        lista.append({"id": "os_version", "type": "text", "value": config['root']['VERSION']})

lista.append({"id": "os_company", "value": ''})
lista.append({"id": "plataform", "type": "text", "value": platform.system()})
lista.append({"id": "release", "type": "text", "value": platform.release()})
lista.append({"id": "machine", "type": "text", "value": platform.machine()})
lista.append({"id": "processor", "type": "text", "value": platform.processor()})
lista.append({"id": "ram_usage", "type": "text", "value": psutil.virtual_memory().percent})
lista.append({"id": "cpu_load", "type": "text", "value": psutil.cpu_percent(interval=0.1, percpu=False)})
lista.append({"id": "load_avg", "type": "text", "value": psutil.cpu_freq()})
lista.append({"id": "ncpu", "type": "text", "value": psutil.cpu_count(logical=False)})
lista.append({"id": "nthreads", "type": "text", "value": psutil.cpu_count()})
lista.append({"id": "partitions", "type": "text", "value": psutil.disk_partitions()})
lista.append({"id": "disk_usage", "type": "text", "value": psutil.disk_usage('/') })
lista.append({"id": "disks_io", "type": "text", "value":  psutil.disk_io_counters(perdisk=True)})



date_now = datetime.datetime.now()
str_time = str(date_now) #TODO Format

lista.append({"id": "hostname", "type": "text", "value": socket.gethostname()})
lista.append({"id": "system_time", "type": "text", "value": str_time})

json_data = json.dumps(lista)
print (json_data)


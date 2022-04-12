#!/usr/bin/python3
# depends:  psutil (pip install psutils)
# Request:      { "request": "get_system.py" }
# Response:     [{"id":"html_id","value":"field_value"}]
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


date_now = datetime.datetime.now()
str_time = str(date_now) #TODO Format
lista.append({"id": "system_time", "type": "text", "value": str_time})

#socket
lista.append({"id": "hostname", "type": "text", "value": socket.gethostname()})

###############
#psutil
lista.append({"id": "ncpu", "type": "text", "value": psutil.cpu_count(logical=False)})
lista.append({"id": "nthreads", "type": "text", "value": psutil.cpu_count()})


disk_lista = {"id":"disks", "type": "array", "value":[]}

for disk in psutil.disk_partitions():
    if disk.fstype:
        disk_details = psutil.disk_usage(disk.mountpoint)
        #print(disk.device, disk.mountpoint, disk.fstype, disk_details.percent)        
        #print(disk.device, psutil.disk_usage(disk.mountpoint))
        a = {'disk_device': disk.device, 'disk_mountpoint': disk.mountpoint, 
        'disk_fstype': disk.fstype, 'disk_total': disk_details.total, 'disk_free': disk_details.free, 
        'disk_used': disk_details.used, 'disk_used_percent': disk_details.percent
        }
        disk_lista['value'].append(a)

lista.append(disk_lista)

#############
json_data = json.dumps(lista)
print (json_data)


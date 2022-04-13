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
import math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

###
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

boot_time = psutil.boot_time()
boot_day = datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")
uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())

lista.append({"id": "uptime", "type": "text", "value": str(uptime).split('.')[0]})
lista.append({"id": "boot_day", "type": "text", "value": str(boot_day)})

#Disks
disk_lista = {"id":"disks", "type": "array", "value":[]}

for disk in psutil.disk_partitions():
    if disk.fstype:
        disk_details = psutil.disk_usage(disk.mountpoint)
        #print(disk.device, disk.mountpoint, disk.fstype, disk_details.percent)        
        #print(disk.device, psutil.disk_usage(disk.mountpoint))
        a = {
            'id': os.path.basename(disk.device),
            'disk_device': disk.device, 
            'disk_mountpoint': disk.mountpoint, 
            'disk_fstype': disk.fstype, 
            'disk_total': convert_size(disk_details.total), 
            'disk_free': convert_size(disk_details.free), 
            'disk_used': convert_size(disk_details.used), 
            'disk_used_percent': disk_details.percent
        }
        disk_lista['value'].append(a)

lista.append(disk_lista)

#############
json_data = json.dumps(lista)
print (json_data)


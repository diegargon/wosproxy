#!/usr/bin/python3

import psutil
import json


disk_lista = []

for disk in psutil.disk_partitions():
    if disk.fstype:
        disk_details = psutil.disk_usage(disk.mountpoint)
        #print(disk.device, disk.mountpoint, disk.fstype, disk_details.percent)        
        #print(disk.device, psutil.disk_usage(disk.mountpoint))
        a = {'disk_device': disk.device, 'disk_mountpoint': disk.mountpoint, 
        'disk_fstype': disk.fstype, 'disk_total': disk_details.total, 'disk_free': disk_details.free, 
        'disk_used': disk_details.used, 'disk_used_percent': disk_details.percent
        }
        disk_lista.append(a)

print(disk_lista)
print(json.dumps(disk_lista))
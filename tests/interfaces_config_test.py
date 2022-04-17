#!/usr/bin/python3
#
#
# TODO: interfaces.d/*
#

import json
import re
import os
import pprint

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

interfaces_file="/etc/network/interfaces"
#interfaces_file="./network_interfaces-test.file"

lista = []
static_list = {"id":"interfaces_config", "type": "array", "value":[]}


def parse_interfaces(file):
    #starts = ("iface", "mapping", "auto", "allow-")
    actions = ("up", "down", "pre-up", "pre-down", "map", "script")
    _tmp = {}


    with open(file) as f:
        entrys = {}
        iface_conf_sel = ''
        mapping_ifaces = []

        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('source'):
                #TODO load and parse
                continue
#            print(line)

            if line.startswith("auto"):
                #print("'"+ line + "'")
                auto_line = line.split()
                for iface in auto_line:
                    if iface != "auto":
                        _tmp[iface] = {'iface': iface, 'auto': 1}
                mapping_ifaces.clear()                       
            elif line.startswith("iface"):                
                iface_line = line.split()
                #print(iface_line)
                #pprint.pprint(_tmp)
                if iface_line[1] not in _tmp:                                        
                    iface = iface_line[1]                    
                    _tmp[iface] = {'iface': iface}
                iface_conf_sel = iface_line[1]
                del iface_line[0]
                del iface_line[0]
                for ifaces_opt in iface_line:
                    _tmp[iface_conf_sel].update({ifaces_opt:1})               
                mapping_ifaces.clear() 
            elif line.startswith("mapping"): 
                mapping_line = line.split()
                for mapping in mapping_line:                    
                    if mapping != "mapping":
                        if mapping not in _tmp:
                            _tmp[mapping] = {'iface': mapping}
                        _tmp[mapping].update({'mapping': 1})
                        mapping_ifaces.append(mapping)                 
            elif len(mapping_ifaces) > 0:
                for mapping_ifaces_sel in mapping_ifaces:
                    _action_list = []
                    options_line = line.split()
                    key = options_line[0]
                    del options_line[0]
                    options_str = ' '.join(options_line)         
                    #print(mapping_ifaces_sel)            
                    if key in _tmp[mapping_ifaces_sel]:                   
                        _action_list.extend(_tmp[mapping_ifaces_sel][key]) 
                    _action_list.append(options_str)
                    _tmp[mapping_ifaces_sel].update({key:_action_list})
            else:
                options_line = line.split()                
                if options_line[0].startswith(actions):
                    #_tmp_actions =
                    _action_list = []
                    key = options_line[0]
                    del options_line[0]
                    options_str = ' '.join(options_line)                    
                    if key in _tmp[iface_conf_sel]:
                        _action_list.extend(_tmp[iface_conf_sel][key])
                    _action_list.append(options_str)
                    _tmp[iface_conf_sel].update({key:_action_list})
                    #    print(_tmp[iface_conf_sel][key])
                    #_tmp[iface_conf_sel].update({key:[options_str]})
                else: 
                    #_tmp[iface_conf_sel].update({options_line[0]:options_line[1]})
                    
                    _action_list = []
                    key = options_line[0]
                    del options_line[0]
                    #options_str = ' '.join(options_line)                
                    if key in _tmp[iface_conf_sel]:
                        _action_list.extend(_tmp[iface_conf_sel][key])
                    _action_list.extend(options_line)
                    _tmp[iface_conf_sel].update({key:_action_list})
                    #    print(_tmp[iface_conf_sel][key])
                    #_tmp[iface_conf_sel].update({key:[options_str]})

                

#_tmp[iface].update({"test":"tost"})
               
                        
        return _tmp

interfaces_config = parse_interfaces(interfaces_file)

pprint.pprint(interfaces_config)

#lista.append(interfaces_config)

#print(json.dumps(lista))



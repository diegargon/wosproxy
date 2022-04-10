#!/usr/bin/python3
# Request:      { "request": "test.py" }
# Response:     { "data": [{"id":"html_id","value":"field_value"}] }

import json

#test1
#------------------------------------------------------
#print ('{"data":[{"id":"hostname", "value":"hostname.com"},{"id":"os", "value":"linux"}]}')

#test2
#------------------------------------------------------
lista = {
    "data": [
        {"id":"hostname","value":"hostname.com"},
        {"id":"os","value":"linux"}
        ]
    }

#test3
#------------------------------------------------------
lista2 = {"data":[]}
test2 = {"id":"hostname","value":"hostname2.com"}
lista2['data'].append(test2)
#test4
#------------------------------------------------------
hostname3="hostname3.com"
lista3 = {"data":[]}
test3 = {
    "id": "hostname",
    "value": hostname3
    }    
lista3['data'].append(test3)
#test5
#------------------------------------------------------
hostname4="hostname4.com"
os4="Debian linux 4"
lista4 = {"data":[]}

lista4['data'].append({"id": "hostname", "value": hostname4})
lista4['data'].append({"id": "os", "value": os4})
#------------------------------------------------------

json_data = json.dumps(lista4)
print (json_data)



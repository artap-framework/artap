import os
import sys
import json

if os.path.exists("enviroment_local.json"):
    file_name = "enviroment_local.json"
else:   
    file_name = "enviroment.json"

with open(file_name, 'r') as f:
    enviroment = json.load(f)


class Enviroment:
    path = __file__
    path = path.replace("enviroment.py", "")

    artap_root = path
    tests_root = os.path.abspath(path + "./tests/")    
            
    condor_host_ip = enviroment["condor_host_ip"]
    condor_host_login = enviroment["condor_host_login"]
                
    available_ssh_servers = enviroment["available_ssh_servers"]
    ssh_login = enviroment["ssh_login"]

    comsol_path = enviroment["comsol_path"]

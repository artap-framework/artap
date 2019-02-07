import os
import json

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

#  global enviroment
with open(dir_path + os.sep + "enviroment.json", 'r') as f:
    enviroment_global = json.load(f)

#  local enviroment
enviroment_local = dict()
if os.path.exists(dir_path + os.sep + "enviroment_localx.json"):
    with open(dir_path + os.sep + "enviroment_localx.json", 'r') as f:
        enviroment_local = json.load(f)

# update dicts
enviroment = {**enviroment_global, **enviroment_local}


class Enviroment:
    path = __file__
    path = path.replace("enviroment.py", "")

    artap_root = path
    tests_root = os.path.abspath(path + "." + os.sep + "tests" + os.sep)
            
    condor_host_ip = enviroment["condor_host_ip"]
    condor_host_login = enviroment["condor_host_login"]
                
    available_ssh_servers = enviroment["available_ssh_servers"]
    ssh_login = enviroment["ssh_login"]

    comsol_path = enviroment["comsol_path"]

    loopback_ip = enviroment["loopback_ip"]
    server_initial_port = enviroment["server_initial_port"]
    server_keep_live_delay = enviroment["server_keep_live_delay"]

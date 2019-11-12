import os
import json

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

#  global environment
with open(dir_path + os.sep + "environment.json", 'r') as f:
    environment_global = json.load(f)

#  local environment
environment_local = dict()
if os.path.exists(dir_path + os.sep + "environment_local.json"):
    with open(dir_path + os.sep + "environment_local.json", 'r') as f:
        environment_local = json.load(f)

# update dicts
environment = {**environment_global, **environment_local}


class Enviroment:
    path = __file__
    path = path.replace("environment.py", "")

    artap_root = path
    tests_root = os.path.abspath(path + "." + os.sep + "tests" + os.sep)
            
    condor_host = environment["condor_host"]
    condor_login = environment["condor_login"]
    # get system user name
    if condor_login is None:
        import getpass
        condor_login = getpass.getuser()

    comsol_path = environment["comsol_path"]

    loopback_ip = environment["loopback_ip"]
    server_initial_port = environment["server_initial_port"]
    server_keep_live_delay = environment["server_keep_live_delay"]

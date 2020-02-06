import os
import getpass
from appdirs import user_config_dir
import pathlib

# internal variables
__id__ = "artap"
path = str(pathlib.Path(__file__).parent.absolute())

artap_root = path
tests_root = os.path.abspath(path + os.sep + "tests" + os.sep)

# config
config = {}

# config["condor_host"] = "edison.fel.zcu.cz"
config["condor_host"] = None
# get system user name
config["condor_login"] = getpass.getuser()

config["comsol_path"] = ""

config["loopback_ip"] = "127.0.0.1"
config["server_initial_port"] = 8050
config["server_keep_live_delay"] = 0.1

# user config
fn = "{}/config.py".format(user_config_dir(__id__))
if os.path.exists(fn):
    exec(open(fn).read())
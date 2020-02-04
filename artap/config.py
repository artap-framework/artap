import os
import getpass
from appdirs import user_config_dir

# internal variables
__version__ = "2020.2.4"
__id__ = "artap"
__author__ = u"Artap Team"
__author_email__ = "artap.team@gmail.com"
__copyright__ = u"Copyright (c) 2018-2019, {} <{}>".format(__author__, __author_email__)
__website__ = "http://agros2d.org/artap"
__license__ = "License :: OSI Approved :: MIT License"
__status__ = "Development Status :: 3 - Alpha"

path = __file__
path = path.replace("config.py", "")

artap_root = path
tests_root = os.path.abspath(path + "." + os.sep + "tests" + os.sep)

__artap__root = ""

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


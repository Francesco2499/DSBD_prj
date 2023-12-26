# config.py
from jproperties import Properties
import os
configs = Properties()



script_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_path, 'config.properties')
with open(config_path, 'rb') as config_file:
   configs.load(config_file)

def get_configs():
    return configs

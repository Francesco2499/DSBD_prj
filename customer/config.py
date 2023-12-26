# config.py
from jproperties import Properties

configs = Properties()

with open('customer/config.properties', 'rb') as config_file:
    configs.load(config_file)

def get_configs():
    return configs

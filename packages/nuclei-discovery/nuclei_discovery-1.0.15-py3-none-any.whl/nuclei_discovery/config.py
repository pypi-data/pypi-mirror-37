import os
import configparser

# config related handling
def run_once(func):
    ''' a declare wrapper function to call only once, use @run_once declare keyword '''
    def wrapper(*args, **kwargs):
        if 'result' not in wrapper.__dict__:
            wrapper.result = func(*args, **kwargs)
        return wrapper.result
    return wrapper

@run_once
def read_config():
    conf = configparser.ConfigParser()
    candidates = [ 
        os.path.join(os.path.dirname(__file__), 'config_default.ini'),
        'config.ini'
    ]
    conf.read(candidates)
    return conf

config = read_config() # keep the line as top as possible
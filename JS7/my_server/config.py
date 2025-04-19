import os

class Config(object):
    SECRET_KEY = os.urandom(32).hex()
    DB_PATH = 'personal.db'
    


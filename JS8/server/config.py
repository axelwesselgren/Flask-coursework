import os

class Config:
    SECRET_KEY = os.urandom(32).hex()
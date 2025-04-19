import os

class Config:
    SECRET_KEY = os.urandom(32).hex()
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg']
    UPLOAD_PATH = '/static/uploads'
    MAX_CONTENT_LENGTH = 0.5 * 1024 * 1024
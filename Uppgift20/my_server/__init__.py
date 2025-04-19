from my_server.config import Config
from flask import Flask, app
app = Flask(__name__)
app.config.from_object(Config)

from my_server import routes, error

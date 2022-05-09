import socket

from flask import Flask
from os import environ

host = socket.gethostbyname(environ.get('ADDRESS'))

app = Flask(__name__)
app.run(host=host, port=environ.get('PORT'))
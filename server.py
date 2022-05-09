from os import environ
from flask import Flask

address = environ.get('ADDRESS')
port = environ.get('PORT')

app = Flask(__name__)
app.run(address=address, port=port)
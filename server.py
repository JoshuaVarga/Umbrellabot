from os import environ
from flask import Flask

app = Flask(__name__)
app.run(port=environ.get('PORT'))
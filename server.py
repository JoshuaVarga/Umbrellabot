from os import environ
from flask import Flask

port = environ.get('PORT')

print('Running on port --> ', port)

app = Flask(__name__)
app.run(port)
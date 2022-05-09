from os import environ
from flask import Flask

port = environ.get('PORT')

app = Flask(__name__)
app.run(port)
print('Running on port --> ', port)
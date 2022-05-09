from multiprocessing import process
from flask import Flask

port = process.env.PORT

app = Flask(__name__)
app.run(port)
print('Running on port', port)
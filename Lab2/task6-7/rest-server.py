import base64
import sqlite3
from flask import Flask, g, make_response, request, send_file
# from helper import write_file  # or keep write_file in the same file

app = Flask(__name__)

@app.route('/')
def hello():
    return make_response({'message': 'Hello World!'})

# 3. Launch the server on localhost:9000
if __name__ == '__main__':
    app.run(host="localhost", port=9000)
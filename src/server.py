from flask import Flask, request, make_response, jsonify
from database import *

app = Flask(__name__, static_url_path=('/static'))

@app.route('/')
def index():
    return app.send_static_file("index.html")
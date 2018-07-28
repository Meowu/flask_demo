#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify, make_response
from datetime import timedelta
from pprint import pprint
import json
import os
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

@app.route('/')
def server():
    return render_template('index.html')

@app.route('/files/<filename>')
def get_file(filename):
    print(filename)
    ext = os.path.splitext(filename)[1]
    print(ext)
    if ext != '.py':
        return err_message(1, 'invalid filename: .py ext required.', 422)
    elif not os.path.exists('./files/' + filename):
        return err_message(2, "file not found", 404)
    with open('files/' + filename, 'rt') as f:
        data = f.read()
        return valid_message(data)

@app.route('/files', methods=["GET", "PUT"])
def handle_files():
    method = request.method
    data = request.get_json()
    pprint(data)
    try:
        filename = data["filename"]
        print(filename)
    except KeyError as err:
        print(err)
        return err_message(1, "filename required.", 400)
    
    try:
        content = data["content"]
    except KeyError as err:
        return err_message(1, "content cannot be empty.", 400)

    if method == "PUT":
        # name = request.form["filename"]
        # content = request.form["content"]
        with open("files/" + filename, 'wt') as f:
            f.write(content)
            return valid_message({}, message="changes saved")
    if method == "GET":
        ext = os.path.splitext(filename)[1]
        if ext != '.py':
            return err_message(1, 'invalid filename: .py ext required.', 422)
        elif not os.path.exists('./files/' + filename):
            return err_message(2, "file not found", 404)
        with open('files/' + filename, 'rt') as f:
            data = f.read()
            return valid_message(data)
def err_message(code, meseage, status):
    msg = {
        "code": code,
        "message": meseage
    }
    return make_response(jsonify(msg), status)

def valid_message(data, message='OK', code=0):
    msg = {
        "code": code,
        "message": message,
        "data": data
    }
    return make_response(jsonify(msg))
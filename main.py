import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory


app = Flask(__name__)

UPLOAD_FOLDER = 'var/www/user/img'


@app.route("/")
def hello():
        return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        return render_template('index1.html', userimg=file)

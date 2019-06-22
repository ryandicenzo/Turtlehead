import os
import cv2
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

from PIL import Image

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

APP_ROOT = "D:/Projects/Turtlehead"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello():
        return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = 'static/img/userimg/' + file.filename
            file.save(filename)
            process_image(filename)

        return render_template('index1.html', imgsrc='img/userimg/' + file.filename)


def process_image(path):
    # Load turtlehead
    turt = Image.open("turtle-head.png")

    # Load image to be modified
    img = Image.open(path)
    
    # Resize image to desired width, maintaining aspect ratio
    width, height = img.size
    new_width  = 680
    new_height = new_width * height / width 
    scale_image(img, new_width, new_height)

    img.save(path)
    cv_img = cv2.imread(path) # Load image for use with OpenCV

    faces = detect_faces(cv_img)

    # For each face found, render turtle-head on top of it.
    for (x, y, w, h) in faces: 
        turt.thumbnail((w * 1.5, h * 1.5))
        img.paste(turt, (x,y), mask=turt)
    img.save(path)


def scale_image(image, width, height):
    image.thumbnail((width,height), Image.ANTIALIAS)


# Takes in an image, and returns a list of coordinates and size of detected faces in photo.
def detect_faces(img):
    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
            img,
            scaleFactor=1.1,
            minNeighbors=2,
            minSize=(30,30),
    )

    return faces
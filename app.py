from flask import Flask, render_template, request
import os
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    photo = request.files["room_photo"]
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    photo.save(save_path)

    dominant_color = get_dominant_color(save_path)

    return render_template("result.html",
                            image_file=photo.filename,
                            color=dominant_color)

def get_dominant_color(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (100, 100))
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    average_color = image.mean(axis=0)
    b, g, r = average_color

    return f"rgb({int(r)}, {int(g)}, {int(b)})"

if __name__ == "__main__":
    app.run(debug=True)
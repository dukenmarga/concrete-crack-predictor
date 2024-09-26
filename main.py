import io
import os

import requests
from flask import Flask, current_app, request, send_from_directory
from PIL import Image

from prediction import predict_concrete

app = Flask(__name__, static_folder="template/build")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


@app.route("/_app/<path:path>")
def resources(path: str):
    if app.static_folder:
        return send_from_directory(app.static_folder, f"_app/{path}")
    return "Resource not found", 500


@app.route("/favicon.png")
def icon():
    if app.static_folder:
        return current_app.send_static_file("favicon.png")
    return "Resource not found", 500


@app.route("/")
def index():
    if app.static_folder:
        return current_app.send_static_file("index.html")
    return "Template not found", 500


@app.route("/predict-from-upload", methods=["POST"])
def predict_from_upload():
    # Get the uploaded image from the request
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    # Make prediction
    try:
        image = Image.open(io.BytesIO(file.read()))
        source = f"Source: {file.filename}<br>"
        return predict_concrete(image) + source, 200
    except Exception as e:
        print(f"Error processing image: {file.name}: {str(e)}")
        return (
            "Error processing image: Please make sure that the image is in valid format",
            500,
        )


@app.route("/predict-from-url", methods=["POST"])
def predict_from_url():
    data = request.get_json()
    if "url" not in data:
        return "No url provided", 400
    image_url = data["url"]

    response = requests.get(image_url)

    if response.status_code == 200:
        # Open the downloaded image with PIL
        image = Image.open(io.BytesIO(response.content))
    else:
        print("Failed to download the image.")

    # Make prediction
    try:
        source = f"Source: {image_url}<br>"
        return predict_concrete(image) + source, 200
    except Exception as e:
        print(f"Error processing image: {image_url}: {str(e)}")
        return (
            "Error processing image: Please make sure that the image is in valid format",
            500,
        )

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# --- Model and Constants ---
REDNESS_MODEL_PATH = os.path.join("models", "redness_model.h5")
BLINK_MODEL_PATH = os.path.join("models", "blink_model.h5")
MYOPIA_MODEL_PATH = os.path.join("models", "myopia_model.h5")

redness_model = load_model(REDNESS_MODEL_PATH)
blink_model = load_model(BLINK_MODEL_PATH)
myopia_model = load_model(MYOPIA_MODEL_PATH)

IMAGE_SIZE = (150, 150)

# --- File Handling ---
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Prediction Functions ---
def predict_redness(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        image = image.resize(IMAGE_SIZE)
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0) / 255.0

        prediction = redness_model.predict(image)[0]
        predicted_index = np.argmax(prediction)
        confidence = float(prediction[predicted_index])
        condition = ["normal", "redness"][predicted_index]

        remedy = "Use lubricating eye drops and reduce screen time." if condition == "redness" else "No issue detected."

        return {
            "condition": condition,
            "confidence": confidence,
            "remedy": remedy,
        }
    except Exception as e:
        return {"error": str(e)}

def predict_blink_rate(video_path):
    # Placeholder for blink rate prediction
    return {"blink_rate": 20, "status": "normal"}

def predict_myopia(image_path):
    # Placeholder for myopia prediction
    return {"myopia_risk": "low", "confidence": 0.95}

# --- API Routes ---
@app.route("/api/predict/redness", methods=["POST"])
def upload_and_predict_redness():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(image_path)

    result = predict_redness(image_path)
    return jsonify(result)

@app.route("/api/predict/blink", methods=["POST"])
def upload_and_predict_blink():
    if "video" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["video"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(video_path)

    result = predict_blink_rate(video_path)
    return jsonify(result)

@app.route("/api/predict/myopia", methods=["POST"])
def upload_and_predict_myopia():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(image_path)

    result = predict_myopia(image_path)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

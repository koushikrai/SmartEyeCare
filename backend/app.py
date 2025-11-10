from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.image import img_to_array, load_img  # noqa: F401 (load_img not strictly needed)
except Exception:
    load_model = None
    img_to_array = None

app = Flask(__name__)
CORS(app)

# --- Model and Constants ---
REDNESS_MODEL_PATH = os.path.join("models", "redness_model.h5")
BLINK_MODEL_PATH = os.path.join("models", "blink_model.h5")
MYOPIA_MODEL_PATH = os.path.join("models", "myopia_model.h5")

redness_model = None
blink_model = None
myopia_model = None

# Lazy/robust model loading: do not crash if files are missing in MVP
if load_model is not None and os.path.exists(REDNESS_MODEL_PATH):
    try:
        redness_model = load_model(REDNESS_MODEL_PATH)
    except Exception:
        redness_model = None

if load_model is not None and os.path.exists(BLINK_MODEL_PATH):
    try:
        blink_model = load_model(BLINK_MODEL_PATH)
    except Exception:
        blink_model = None

if load_model is not None and os.path.exists(MYOPIA_MODEL_PATH):
    try:
        myopia_model = load_model(MYOPIA_MODEL_PATH)
    except Exception:
        myopia_model = None

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
        if img_to_array is not None and redness_model is not None:
            image_arr = img_to_array(image)
            image_arr = np.expand_dims(image_arr, axis=0) / 255.0
            prediction = redness_model.predict(image_arr)[0]
            predicted_index = int(np.argmax(prediction))
            confidence = float(prediction[predicted_index])
            condition = ["normal", "redness"][predicted_index]
        else:
            # MVP fallback (no model available)
            condition = "redness"  # dummy condition for demo
            confidence = 0.82

        remedy = "Use lubricating eye drops and reduce screen time." if condition == "redness" else "No issue detected."

        return {
            "condition": condition,
            "confidence": confidence,
            "remedy": remedy,
        }
    except Exception as e:
        return {"error": str(e)}

def predict_blink_rate(video_path):
    # Placeholder for blink rate prediction (MVP)
    return {"blink_rate": 20, "status": "normal"}

def predict_myopia(image_path):
    # Placeholder for myopia prediction (MVP)
    return {"myopia_risk": "low", "confidence": 0.95}

# --- Fusion Logic (MVP scaffold) ---
def combine_eye_health(redness_confidence: float, blink_rate: float):
    """
    Combine redness probability and blink rate to infer severity and myopia risk.
    Intended as a placeholder; replace with a trained classifier later.
    """
    redness_severe = redness_confidence >= 0.7
    blink_low = blink_rate < 12

    if redness_severe and blink_low:
        severity = "severe"
        myopia_risk = "high"
        myopia_confidence = 0.8
    elif redness_severe or blink_low:
        severity = "moderate"
        myopia_risk = "elevated"
        myopia_confidence = 0.65
    else:
        severity = "mild"
        myopia_risk = "low"
        myopia_confidence = 0.55

    return {
        "severity": severity,
        "myopia_risk": myopia_risk,
        "myopia_confidence": myopia_confidence
    }

# --- API Routes ---
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "redness_model_loaded": redness_model is not None,
        "blink_model_loaded": blink_model is not None,
        "myopia_model_loaded": myopia_model is not None
    })

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

@app.route("/api/predict/eyehealth", methods=["POST"])
def predict_eye_health():
    """
    Accepts image (required) and optional video to compute redness, blink, and fused myopia.
    For MVP, uses existing predictors and fallbacks.
    """
    if "image" not in request.files:
        return jsonify({"error": "No file part: image"}), 400

    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "No selected image"}), 400

    image_name = secure_filename(image_file.filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_name)
    image_file.save(image_path)

    # Optional video for blink
    blink_rate_value = 18  # default fallback
    blink_status = "normal"
    if "video" in request.files and request.files["video"].filename:
        video_file = request.files["video"]
        video_name = secure_filename(video_file.filename)
        video_path = os.path.join(app.config["UPLOAD_FOLDER"], video_name)
        video_file.save(video_path)
        blink_res = predict_blink_rate(video_path)
        blink_rate_value = blink_res.get("blink_rate", blink_rate_value)
        blink_status = blink_res.get("status", blink_status)

    # Redness prediction
    red_res = predict_redness(image_path)
    if "error" in red_res:
        return jsonify(red_res), 500
    condition = red_res.get("condition", "unknown")
    redness_confidence = float(red_res.get("confidence", 0.0))

    # Fusion
    fusion = combine_eye_health(redness_confidence, blink_rate_value)

    return jsonify({
        "redness": {
            "condition": condition,
            "confidence": redness_confidence,
            "remedy": red_res.get("remedy", "—")
        },
        "blink": {
            "blink_rate": blink_rate_value,
            "status": blink_status
        },
        "fusion": fusion
    })
if __name__ == "__main__":
    app.run(debug=True, port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys
import numpy as np
from PIL import Image
from dotenv import load_dotenv
from api.signup import signup_bp
from api.login import login_bp
from api.history import history_bp
from db import get_db
from bson import ObjectId

# Load environment variables from .env file
load_dotenv()

# Check Python version and warn if not 3.11
python_version = sys.version_info
if python_version.major != 3 or python_version.minor != 11:
    print(f"WARNING: You're using Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    print("MediaPipe requires Python 3.11. Please use the Python 3.11 virtual environment:")
    print("  backend\\venv311\\Scripts\\python.exe backend/app.py")
    print("Or use: npm start (which uses the correct Python)")
    print("")

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.image import img_to_array, load_img  # noqa: F401 (load_img not strictly needed)
except Exception:
    load_model = None
    img_to_array = None

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(history_bp)

# --- Model and Constants ---
# Get the directory where this script is located (backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REDNESS_MODEL_PATH = os.path.join(BASE_DIR, "models", "redness_model.h5")
BLINK_MODEL_PATH = os.path.join(BASE_DIR, "models", "blink_model.h5")
MYOPIA_MODEL_PATH = os.path.join(BASE_DIR, "models", "myopia_model.h5")

redness_model = None
blink_model = None
myopia_model = None

# Lazy model loading: load models only when first needed (speeds up startup)
def ensure_redness_model_loaded():
    global redness_model
    if redness_model is None and load_model is not None and os.path.exists(REDNESS_MODEL_PATH):
        try:
            print("Loading redness model...")
            redness_model = load_model(REDNESS_MODEL_PATH)
            print("Redness model loaded successfully")
        except Exception as e:
            print(f"Failed to load redness model: {e}")
            redness_model = None
    return redness_model is not None

def ensure_blink_model_loaded():
    global blink_model
    if blink_model is None and load_model is not None and os.path.exists(BLINK_MODEL_PATH):
        try:
            print("Loading blink model...")
            blink_model = load_model(BLINK_MODEL_PATH)
            print("Blink model loaded successfully")
        except Exception as e:
            print(f"Failed to load blink model: {e}")
            blink_model = None
    return blink_model is not None

def ensure_myopia_model_loaded():
    global myopia_model
    if myopia_model is None and load_model is not None and os.path.exists(MYOPIA_MODEL_PATH):
        try:
            print("Loading myopia model...")
            myopia_model = load_model(MYOPIA_MODEL_PATH)
            print("Myopia model loaded successfully")
        except Exception as e:
            print(f"Failed to load myopia model: {e}")
            myopia_model = None
    return myopia_model is not None

IMAGE_SIZE = (224, 224)

# --- File Handling ---
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Prediction Functions ---
def predict_redness(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        image = image.resize(IMAGE_SIZE)
        
        # Lazy load model on first use
        model_available = ensure_redness_model_loaded()
        
        if img_to_array is not None and model_available:
            # Use trained model if available
            image_arr = img_to_array(image)
            image_arr = np.expand_dims(image_arr, axis=0) / 255.0
            prediction = redness_model.predict(image_arr)[0]
            predicted_index = int(np.argmax(prediction))
            confidence = float(prediction[predicted_index])
            condition = ["normal", "redness"][predicted_index]
            # Save history if user_id provided in environment context (not available here)
        else:
            # Fallback: Basic color-based redness detection
            # Analyze the image for red/pink tones that might indicate eye redness
            img_array = np.array(image)
            
            # Calculate average RGB values
            avg_r = np.mean(img_array[:, :, 0])
            avg_g = np.mean(img_array[:, :, 1])
            avg_b = np.mean(img_array[:, :, 2])
            
            # Redness detection: check if red channel is significantly higher than green/blue
            # and if the overall redness ratio is high
            redness_ratio = avg_r / (avg_g + avg_b + 1)  # +1 to avoid division by zero
            red_dominance = avg_r / (avg_r + avg_g + avg_b + 1)
            
            # Thresholds for redness detection (tuned for eye images)
            # Higher redness_ratio and red_dominance indicate more redness
            is_red = redness_ratio > 1.15 or (red_dominance > 0.42 and avg_r > 140)
            
            if is_red:
                condition = "redness"
                # Confidence based on how strong the redness indicators are
                confidence = min(0.75 + (redness_ratio - 1.15) * 0.5, 0.92)
            else:
                condition = "normal"
                confidence = 0.70 + (1.0 - min(redness_ratio, 1.3)) * 0.15

        remedy = "Use lubricating eye drops and reduce screen time." if condition == "redness" else "No issue detected. Continue maintaining good eye care habits."

        return {
            "condition": condition,
            "confidence": confidence,
            "remedy": remedy,
        }
    except Exception as e:
        return {"error": str(e)}

def predict_blink_rate(video_path):
    """
    Predict blink rate from video using MediaPipe Face Mesh.
    Uses Eye Aspect Ratio (EAR) to detect blinks.
    """
    try:
        from utils.blink_rate_detector import detect_blink_rate
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        result = detect_blink_rate(video_path)
        
        # Ensure all required fields are present
        return {
            "blink_rate": result.get("blink_rate", 18),
            "status": result.get("status", "normal"),
            "blink_count": result.get("blink_count", 0),
            "video_duration_seconds": result.get("video_duration_seconds", 0),
            "frames_processed": result.get("frames_processed", 0)
        }
    except ImportError as e:
        # MediaPipe not installed
        print(f"Blink detection ImportError: {e}")
        import traceback
        traceback.print_exc()
        return {
            "blink_rate": 18,  # Fallback value
            "status": "normal",
            "blink_count": 0,
            "video_duration_seconds": 0,
            "frames_processed": 0,
            "error": f"MediaPipe is not installed or import failed: {str(e)}"
        }
    except Exception as e:
        print(f"Blink detection error: {e}")
        import traceback
        traceback.print_exc()
        # Fallback if detection fails
        return {
            "blink_rate": 18,
            "status": "normal",
            "blink_count": 0,
            "video_duration_seconds": 0,
            "frames_processed": 0,
            "error": f"Blink detection failed: {str(e)}"
        }

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
        "redness_model_available": os.path.exists(REDNESS_MODEL_PATH),
        "blink_model_loaded": blink_model is not None,
        "blink_model_available": os.path.exists(BLINK_MODEL_PATH),
        "myopia_model_loaded": myopia_model is not None,
        "myopia_model_available": os.path.exists(MYOPIA_MODEL_PATH)
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

    # Persist history if user_id provided in the form
    try:
        user_id = request.form.get('user_id')
        if user_id:
            db = get_db()
            try:
                uid = ObjectId(user_id) if ObjectId.is_valid(user_id) else user_id
            except Exception:
                uid = user_id
            db.history.insert_one({
                'user_id': uid,
                'kind': 'redness',
                'input': {'image_path': image_path, 'filename': filename},
                'result': result,
                'created_at': __import__('datetime').datetime.utcnow()
            })
    except Exception as e:
        print(f"Warning: could not save redness history: {e}")
    return jsonify(result)

@app.route("/api/predict/blink", methods=["POST"])
def upload_and_predict_blink():
    try:
        if "video" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["video"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        
        # Save the file
        try:
            file.save(video_path)
        except Exception as e:
            print(f"Error saving video file: {e}")
            return jsonify({"error": f"Failed to save video file: {str(e)}"}), 500

        # Process the video
        result = predict_blink_rate(video_path)

        # Persist history if user_id provided in the form
        try:
            user_id = request.form.get('user_id')
            if user_id:
                db = get_db()
                try:
                    uid = ObjectId(user_id) if ObjectId.is_valid(user_id) else user_id
                except Exception:
                    uid = user_id
                db.history.insert_one({
                    'user_id': uid,
                    'kind': 'blink',
                    'input': {'video_path': video_path, 'filename': filename},
                    'result': result,
                    'created_at': __import__('datetime').datetime.utcnow()
                })
        except Exception as e:
            print(f"Warning: could not save blink history: {e}")
        
        # Clean up the uploaded file after processing
        try:
            if os.path.exists(video_path):
                os.remove(video_path)
        except Exception as e:
            print(f"Warning: Could not delete temporary video file: {e}")
        
        return jsonify(result)
    except Exception as e:
        print(f"Error in upload_and_predict_blink: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to process video: {str(e)}"}), 500

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

    # Save combined history if user_id provided
    try:
        user_id = request.form.get('user_id')
        if user_id:
            db = get_db()
            try:
                uid = ObjectId(user_id) if ObjectId.is_valid(user_id) else user_id
            except Exception:
                uid = user_id
            db.history.insert_one({
                'user_id': uid,
                'kind': 'eyehealth',
                'input': {'image_path': image_path},
                'result': {
                    'redness': {
                        'condition': condition,
                        'confidence': redness_confidence
                    },
                    'blink': {
                        'blink_rate': blink_rate_value,
                        'status': blink_status
                    },
                    'fusion': fusion
                },
                'created_at': __import__('datetime').datetime.utcnow()
            })
    except Exception as e:
        print(f"Warning: could not save eyehealth history: {e}")

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
    # Disable the Werkzeug reloader on Windows to avoid socket errors
    # caused by the reloader restarting child threads/sockets.
    app.run(debug=True, port=5000, use_reloader=False)

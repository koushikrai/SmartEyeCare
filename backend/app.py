from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

# Import your redness API blueprint
from api.redness_detection import redness_api

app = Flask(__name__)
CORS(app)

# Register the blueprint
app.register_blueprint(redness_api)

# Folder to save uploaded images
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Optional: Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to handle image uploads for redness detection (if not handled in blueprint)
@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(image_path)

    # Import here if predict_redness is not needed elsewhere
    from backend.utils.train_redness_model import predict_redness
    result = predict_redness(image_path)

    return jsonify(result)


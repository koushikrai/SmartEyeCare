from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

# Assuming this is part of your Flask app
# You might need to adjust imports based on your project structure

# Make sure to import your prediction function
# Example:
# from ..utils.train_redness_model import predict_redness

# Define the blueprint
upload_bp = Blueprint("upload", __name__)

# Define the upload folder
UPLOAD_FOLDER = os.path.join("static", "uploads")

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Securely save the file
    filename = secure_filename(file.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(image_path)

    # Get the prediction
    # This assumes `predict_redness` is available and works as expected
    # You might need to adjust the import path for `predict_redness`
    try:
        # Example of how you might call your prediction function
        # from ..utils.train_redness_model import predict_redness
        # result = predict_redness(image_path)

        # For now, let's return a mock result
        result = {
            "disease": "Conjunctivitis",
            "confidence": 0.95,
            "remedy": "See a doctor for diagnosis and treatment.",
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

# backend/api/redness_detection.py

import os
import numpy as np
from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from PIL import Image
import io

redness_api = Blueprint('redness_api', __name__)

# Load the trained model
MODEL_PATH = os.path.join('models', 'redness_model.h5')
model = load_model(MODEL_PATH)

# Define target image size (based on training)
IMAGE_SIZE = (150, 150)  # same as in training

# Define class labels (adjust based on your dataset folders)
CLASS_NAMES = ['normal', 'redness']

@redness_api.route('/predict_redness', methods=['POST'])
def predict_redness():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    try:
        # Load image from request and preprocess
        image = Image.open(file).convert("RGB")
        image = image.resize(IMAGE_SIZE)
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0) / 255.0

        # Predict
        prediction = model.predict(image)[0]
        predicted_index = np.argmax(prediction)
        confidence = float(prediction[predicted_index])
        condition = CLASS_NAMES[predicted_index]

        # Custom remedy suggestions (optional)
        remedy = "Use lubricating eye drops and reduce screen time." if condition == "redness" else "No issue detected."

        return jsonify({
            "condition": condition,
            "confidence": confidence,
            "remedy": remedy
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

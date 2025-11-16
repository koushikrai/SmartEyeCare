from flask import Blueprint, request, jsonify
import bcrypt
from pymongo.errors import DuplicateKeyError
from db import get_db
import re

signup_bp = Blueprint('signup', __name__)

def is_valid_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@signup_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        # Validation
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400

        # Get database connection
        db = get_db()
        users_collection = db.users

        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return jsonify({"error": "Email already exists"}), 409

        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Create user document
        user_doc = {
            "email": email,
            "password": hashed_password.decode('utf-8'),  # Store as string
            "created_at": None  # Will be set by MongoDB
        }

        # Insert user into database
        result = users_collection.insert_one(user_doc)
        
        return jsonify({
            "message": "Signup successful",
            "user_id": str(result.inserted_id)
        }), 201

    except DuplicateKeyError:
        return jsonify({"error": "Email already exists"}), 409
    except Exception as e:
        print(f"Signup error: {e}")
        import traceback
        traceback.print_exc()
        error_msg = str(e)
        if "MongoDB" in error_msg or "Connection" in error_msg:
            return jsonify({"error": "Database connection failed. Please check if MongoDB is running."}), 500
        return jsonify({"error": f"An error occurred during signup: {error_msg}"}), 500

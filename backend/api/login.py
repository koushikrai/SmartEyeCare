from flask import Blueprint, request, jsonify
import bcrypt
from db import get_db

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        # Validation
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Get database connection
        db = get_db()
        users_collection = db.users

        # Find user by email
        user = users_collection.find_one({"email": email})
        
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        # Verify password
        stored_password = user.get("password", "")
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')
        
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Login successful
        return jsonify({
            "message": "Login successful",
            "user_id": str(user["_id"]),
            "email": user["email"]
        }), 200

    except Exception as e:
        print(f"Login error: {e}")
        import traceback
        traceback.print_exc()
        error_msg = str(e)
        if "MongoDB" in error_msg or "Connection" in error_msg:
            return jsonify({"error": "Database connection failed. Please check if MongoDB is running."}), 500
        return jsonify({"error": f"An error occurred during login: {error_msg}"}), 500

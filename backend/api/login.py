from flask import Blueprint, request, jsonify

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Replace with your actual authentication logic
    if username == "user" and password == "password":
        return jsonify({"token": "your_jwt_token"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

from flask import Blueprint, request, jsonify

signup_bp = Blueprint('signup', __name__)

@signup_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Replace with your actual user creation logic
    if email and password:
        # Here, you would typically save the new user to a database
        return jsonify({"message": "Signup successful"})
    else:
        return jsonify({"error": "Email and password are required"}), 400

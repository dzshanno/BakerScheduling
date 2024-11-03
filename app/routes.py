from flask import Blueprint, request, jsonify, render_template
from app import db, bcrypt, ma, socketio
from app.models import User, Role, Shift, ShiftAssignment
from sqlalchemy.orm import joinedload
from functools import wraps
import jwt
from datetime import datetime, timedelta
import os

main = Blueprint("main", __name__)

token_secret_key = os.getenv("TOKEN_SECRET_KEY", "supersecretkey")


# Utility function to verify token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            data = jwt.decode(token, token_secret_key, algorithms=["HS256"])
            current_user = (
                User.query.options(joinedload(User.role))
                .filter_by(user_id=data["user_id"])
                .first()
            )
        except:
            return jsonify({"message": "Token is invalid!"}), 403
        return f(current_user, *args, **kwargs)

    return decorated


# Example routes (you can add the rest here)
@main.route("/")
def home():
    return render_template("index.html")


@main.route("/users", methods=["GET"])
@token_required
def get_users(current_user):
    if current_user.role.role_name != "Admin":
        return (
            jsonify({"message": "Unauthorized. Only admins can view all users."}),
            403,
        )
    all_users = User.query.options(joinedload(User.role)).all()
    return jsonify(
        [
            {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "role_name": user.role.role_name if user.role else "No role assigned",
            }
            for user in all_users
        ]
    )

"""Auth routes - Signup & Login with JWT"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    if not all(k in data for k in ["email", "username", "password"]):
        return jsonify(error="Missing email, username, or password"), 400
    if User.query.filter((User.email == data["email"]) | (User.username == data["username"])).first():
        return jsonify(error="User already exists"), 409
    
    user = User(email=data["email"], username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User created", token=create_access_token(identity=user.id), user=user.to_dict()), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    if not all(k in data for k in ["email", "password"]):
        return jsonify(error="Missing email or password"), 400
    
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify(error="Invalid credentials"), 401
    return jsonify(token=create_access_token(identity=user.id), user=user.to_dict())

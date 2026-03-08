from datetime import datetime, timedelta, timezone
import jwt
from flask import Blueprint, current_app, request
from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__)

def create_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return {"message": "Name, email, and password are required."}, 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"message": "Email already exists."}, 409

    user = User(name=name, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    token = create_token(user.id)

    return {
        "token": token,
        "user": user.to_dict(),
    }, 201

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return {"message": "Email and password are required."}, 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"message": "Invalid email or password."}, 401

    token = create_token(user.id)

    return {
        "token": token,
        "user": user.to_dict(),
    }, 200

@auth_bp.get("/me")
def me():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return {"message": "Missing token."}, 401

    token = auth_header.split(" ", 1)[1]

    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET"],
            algorithms=["HS256"],
        )
        user_id = int(payload["sub"])
    except Exception:
        return {"message": "Invalid token."}, 401

    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found."}, 404

    return {"user": user.to_dict()}, 200
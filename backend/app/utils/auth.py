import jwt
from flask import current_app, request
from app.models import User


def get_current_user():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1]

    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET"],
            algorithms=["HS256"],
        )
        user_id = int(payload["sub"])
    except Exception:
        return None

    return User.query.get(user_id)
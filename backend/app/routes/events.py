from flask import Blueprint

events_bp = Blueprint("events", __name__)

@events_bp.get("/")
def list_events():
    return {"events": []}, 200
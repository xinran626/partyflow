from flask import Blueprint, request

from ..extensions import db
from ..models import Event, EventMember
from ..utils.auth import get_current_user

events_bp = Blueprint("events", __name__)


@events_bp.get("/")
def list_events():
    current_user = get_current_user()

    if not current_user:
        return {"message": "Unauthorized."}, 401

    memberships = EventMember.query.filter_by(user_id=current_user.id).all()
    event_ids = [membership.event_id for membership in memberships]

    if not event_ids:
        return {"events": []}, 200

    events = (
        Event.query
        .filter(Event.id.in_(event_ids))
        .order_by(Event.created_at.desc())
        .all()
    )

    return {
        "events": [event.to_dict() for event in events]
    }, 200


@events_bp.post("/")
def create_event():
    current_user = get_current_user()

    if not current_user:
        return {"message": "Unauthorized."}, 401

    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    date = data.get("date", "").strip()
    location = data.get("location", "").strip()

    if not name:
        return {"message": "Event name is required."}, 400

    event = Event(
        name=name,
        date=date or None,
        location=location or None,
        created_by=current_user.id,
    )

    db.session.add(event)
    db.session.flush()

    leader_membership = EventMember(
        event_id=event.id,
        user_id=current_user.id,
        role="team_leader",
    )

    db.session.add(leader_membership)
    db.session.commit()

    return {
        "message": "Event created successfully.",
        "event": event.to_dict(),
    }, 201


@events_bp.put("/<int:event_id>")
def update_event(event_id):
    current_user = get_current_user()

    if not current_user:
        return {"message": "Unauthorized."}, 401

    event = Event.query.get(event_id)
    if not event:
        return {"message": "Event not found."}, 404

    leader_membership = EventMember.query.filter_by(
        event_id=event.id,
        user_id=current_user.id,
        role="team_leader",
    ).first()

    if not leader_membership:
        return {"message": "Forbidden."}, 403

    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    date = data.get("date", "")
    location = data.get("location", "")

    if not name:
        return {"message": "Event name is required."}, 400

    event.name = name
    event.date = date or None
    event.location = location or None

    db.session.commit()

    return {
        "message": "Event updated successfully.",
        "event": event.to_dict(),
    }, 200


@events_bp.delete("/<int:event_id>")
def delete_event(event_id):
    current_user = get_current_user()

    if not current_user:
        return {"message": "Unauthorized."}, 401

    event = Event.query.get(event_id)
    if not event:
        return {"message": "Event not found."}, 404

    leader_membership = EventMember.query.filter_by(
        event_id=event.id,
        user_id=current_user.id,
        role="team_leader",
    ).first()

    if not leader_membership:
        return {"message": "Forbidden."}, 403

    db.session.delete(event)
    db.session.commit()

    return {"message": "Event deleted successfully."}, 200
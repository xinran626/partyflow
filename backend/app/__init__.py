from flask import Flask
from .config import Config
from .extensions import db, migrate
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://127.0.0.1:5173"
            ]
        }
    },
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )

    from .routes.auth import auth_bp
    from .routes.events import events_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(events_bp, url_prefix="/api/events")

    @app.get("/")
    def health_check():
        return {"message": "PartyFlow backend is running"}

    return app
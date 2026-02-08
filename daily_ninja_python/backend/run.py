"""Daily Ninja Backend - Flask REST API (Azure-compatible)"""
import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.core import config
from app.models import db
from app.api import auth_bp, tasks_bp, activity_bp


def create_app(config_name=None):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name or os.getenv("FLASK_ENV", "development")])
    
    # Init extensions & register routes
    db.init_app(app)
    JWTManager(app)
    CORS(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(activity_bp)
    
    @app.route("/health")
    def health():
        return jsonify(status="healthy", service="daily-ninja-api")
    
    with app.app_context():
        db.create_all()
    
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)

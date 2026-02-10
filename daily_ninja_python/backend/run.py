"""Daily Ninja Backend - Flask REST API"""
import os
import logging
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from app.core import config
from app.models import db
from app.api import auth_bp, tasks_bp, activity_bp

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """Application factory"""
    app = Flask(__name__)
    config_env = config_name or os.getenv("FLASK_ENV", "development")
    app.config.from_object(config[config_env])
    
    # Validate secrets in production
    if config_env == "production":
        if not os.getenv("SECRET_KEY") or os.getenv("SECRET_KEY").startswith("dev-"):
            raise ValueError("SECRET_KEY not configured for production")
        if not os.getenv("JWT_SECRET_KEY") or os.getenv("JWT_SECRET_KEY").startswith("jwt-"):
            raise ValueError("JWT_SECRET_KEY not configured for production")
    
    db.init_app(app)
    JWTManager(app)
    
    cors_origins = os.getenv("CORS_ORIGINS", "*")
    CORS(app) if cors_origins == "*" else CORS(app, origins=cors_origins.split(","))
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(activity_bp)
    
    @app.route("/")
    def index():
        return jsonify(
            service="Daily Ninja API",
            version="1.0.0",
            env=config_env,
            endpoints=["/health", "/auth/signup", "/auth/login", "/tasks", "/streak", "/heatmap"]
        )
    
    @app.route("/health")
    def health():
        return jsonify(status="healthy", service="daily-ninja-api")
    
    with app.app_context():
        db.create_all()
    
    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = app.config.get("DEBUG", False)
    app.run(host="0.0.0.0", port=port, debug=debug)

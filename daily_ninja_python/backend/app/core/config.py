"""Configuration for Daily Ninja Backend"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-only-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///daily_ninja.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = int(os.getenv("PORT", 5000))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    REDIS_URL = os.getenv("REDIS_URL", None)
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "")


def validate_required_env(config_env: str) -> None:
    required_by_env = {
        "production": ["SECRET_KEY", "JWT_SECRET_KEY", "DATABASE_URL"],
    }
    required_vars = required_by_env.get(config_env, [])
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(f"Missing required environment variables for {config_env}: {missing_str}")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

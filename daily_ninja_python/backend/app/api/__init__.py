"""API Routes for Daily Ninja Backend"""
from .auth import auth_bp
from .tasks import tasks_bp
from .activity import activity_bp

__all__ = ["auth_bp", "tasks_bp", "activity_bp"]

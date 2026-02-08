"""Task CRUD routes"""
from datetime import datetime, date, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Task, Activity, User

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def log_task_completion(user_id):
    """Log activity when task is completed - updates heatmap & streak."""
    today = date.today()
    
    # Update activity count for heatmap
    activity = Activity.query.filter_by(user_id=user_id, date=today).first()
    if activity:
        activity.count += 1
    else:
        activity = Activity(user_id=user_id, date=today, count=1)
        db.session.add(activity)
    
    # Update user streak
    user = User.query.get(user_id)
    yesterday = today - timedelta(days=1)
    
    if user.last_activity_date != today:
        if user.last_activity_date == yesterday:
            user.current_streak += 1
        else:
            user.current_streak = 1
        user.last_activity_date = today
        user.longest_streak = max(user.longest_streak, user.current_streak)
    
    db.session.commit()
    return activity.count


@tasks_bp.route("", methods=["GET"])
@jwt_required()
def get_tasks():
    tasks = Task.query.filter_by(user_id=get_jwt_identity()).order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])


@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    data = request.get_json() or {}
    if "title" not in data:
        return jsonify(error="Missing title"), 400
    
    user_id = get_jwt_identity()
    title = data["title"].strip()
    
    # Prevent duplicates (case-insensitive)
    existing = Task.query.filter_by(user_id=user_id).filter(
        db.func.lower(Task.title) == title.lower()
    ).first()
    if existing:
        return jsonify(error="Task already exists"), 409
    
    task = Task(user_id=user_id, title=title)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify(error="Task not found"), 404
    
    data = request.get_json() or {}
    was_done = task.done
    
    if "title" in data:
        task.title = data["title"]
    if "done" in data:
        task.done = data["done"]
        task.completed_at = datetime.utcnow() if data["done"] else None
        
        # Log activity when task is newly completed (for heatmap + streak)
        if data["done"] and not was_done:
            log_task_completion(user_id)
    
    db.session.commit()
    return jsonify(task.to_dict())


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=get_jwt_identity()).first()
    if not task:
        return jsonify(error="Task not found"), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify(message="Task deleted")
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

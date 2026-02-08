"""Activity routes - Streak tracking and heatmap"""
from datetime import date, timedelta
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Activity, User

activity_bp = Blueprint("activity", __name__)


@activity_bp.route("/activity", methods=["POST"])
@jwt_required()
def log_activity():
    """Log activity for today - updates heatmap count and streak."""
    user_id = get_jwt_identity()
    today = date.today()
    
    # Update activity count
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
    return jsonify(message="Activity logged", date=today.isoformat(), 
                   count=activity.count, current_streak=user.current_streak)


@activity_bp.route("/streak", methods=["GET"])
@jwt_required()
def get_streak():
    """Get current and longest streak from user record."""
    user = User.query.get(get_jwt_identity())
    return jsonify(current_streak=user.current_streak or 0, 
                   longest_streak=user.longest_streak or 0)


@activity_bp.route("/heatmap", methods=["GET"])
@jwt_required()
def get_heatmap():
    user_id = get_jwt_identity()
    today, start = date.today(), date.today() - timedelta(days=364)
    activity_map = {a.date.isoformat(): a.count for a in 
        Activity.query.filter(Activity.user_id == user_id, Activity.date >= start).all()}
    return jsonify([{"date": (start + timedelta(days=i)).isoformat(), 
                     "count": activity_map.get((start + timedelta(days=i)).isoformat(), 0)} 
                    for i in range(365)])

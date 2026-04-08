import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

# Ensure backend package imports resolve in tests
BACKEND_ROOT = Path(__file__).resolve().parents[2] / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from run import create_app  # noqa: E402
from app.models import db, User, Activity  # noqa: E402
from app.api import tasks as tasks_api  # noqa: E402


@pytest.fixture()
def app():
    app = create_app("testing")
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def user_id(app):
    with app.app_context():
        user = User(email="unit@example.com", username="unit-user")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        return user.id


def _freeze_today(monkeypatch, target_date):
    class FixedDate(date):
        @classmethod
        def today(cls):
            return target_date

    monkeypatch.setattr(tasks_api, "date", FixedDate)


def test_zero_streak_for_new_user(app, user_id):
    with app.app_context():
        user = db.session.get(User, user_id)
        assert user.current_streak == 0
        assert user.longest_streak == 0


def test_long_streak_increments_on_consecutive_days(app, user_id, monkeypatch):
    start = date(2026, 1, 1)

    with app.app_context():
        for offset in range(10):
            _freeze_today(monkeypatch, start + timedelta(days=offset))
            tasks_api.log_task_completion(user_id)

        user = db.session.get(User, user_id)
        assert user.current_streak == 10
        assert user.longest_streak == 10

        activities = Activity.query.filter_by(user_id=user_id).all()
        assert len(activities) == 10


def test_broken_streak_resets_to_one(app, user_id, monkeypatch):
    today = date(2026, 2, 10)

    with app.app_context():
        user = db.session.get(User, user_id)
        user.current_streak = 7
        user.longest_streak = 7
        user.last_activity_date = today - timedelta(days=3)
        db.session.commit()

        _freeze_today(monkeypatch, today)
        tasks_api.log_task_completion(user_id)

        db.session.refresh(user)
        assert user.current_streak == 1
        assert user.longest_streak == 7


def test_same_day_completion_increments_heatmap_not_streak(app, user_id, monkeypatch):
    today = date(2026, 2, 11)

    with app.app_context():
        user = db.session.get(User, user_id)
        user.current_streak = 4
        user.longest_streak = 5
        user.last_activity_date = today
        db.session.commit()

        _freeze_today(monkeypatch, today)
        first_count = tasks_api.log_task_completion(user_id)
        second_count = tasks_api.log_task_completion(user_id)

        db.session.refresh(user)
        assert first_count == 1
        assert second_count == 2
        assert user.current_streak == 4
        assert user.longest_streak == 5

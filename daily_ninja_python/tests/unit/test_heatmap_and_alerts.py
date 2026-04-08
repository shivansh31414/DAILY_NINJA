import importlib.util
import sys
import types
from datetime import datetime, timedelta
from pathlib import Path

import pytest


def _load_frontend_app_module(monkeypatch):
    captured_markdown = []

    st = types.ModuleType("streamlit")
    st.session_state = types.SimpleNamespace()

    def set_page_config(**_kwargs):
        return None

    def markdown(text, **_kwargs):
        captured_markdown.append(text)

    st.set_page_config = set_page_config
    st.markdown = markdown

    monkeypatch.setitem(sys.modules, "streamlit", st)

    module_path = Path(__file__).resolve().parents[2] / "frontend" / "app.py"
    spec = importlib.util.spec_from_file_location("frontend_app_for_tests", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    return module, st, captured_markdown


def _freeze_now(monkeypatch, module, target_datetime):
    class FixedDateTime(datetime):
        @classmethod
        def now(cls):
            return target_datetime

    monkeypatch.setattr(module, "datetime", FixedDateTime)


def test_heatmap_render_uses_mock_activity_data(monkeypatch):
    module, st, captured = _load_frontend_app_module(monkeypatch)
    today = datetime(2026, 3, 10)
    _freeze_now(monkeypatch, module, today)

    st.session_state.data = {
        "todos": [],
        "streak": 0,
        "last_date": None,
        "longest_streak": 0,
        "activity": {
            today.strftime("%Y-%m-%d"): 7,
            (today - timedelta(days=1)).strftime("%Y-%m-%d"): 3,
        },
    }

    module.render_heatmap()

    html = captured[-1]
    assert 'class="heatmap"' in html
    assert "#39d353" in html  # high contribution color
    assert "#006d32" in html  # medium contribution color


def test_weekly_stats_reports_missed_days(monkeypatch):
    module, st, _ = _load_frontend_app_module(monkeypatch)
    today = datetime(2026, 3, 10)
    _freeze_now(monkeypatch, module, today)

    active_dates = [
        today.strftime("%Y-%m-%d"),
        (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        (today - timedelta(days=3)).strftime("%Y-%m-%d"),
        (today - timedelta(days=6)).strftime("%Y-%m-%d"),
    ]

    st.session_state.data = {
        "activity": {d: 1 for d in active_dates},
        "todos": [],
        "streak": 0,
        "last_date": None,
        "longest_streak": 0,
    }

    weekly = module.get_weekly_stats()
    assert weekly["active_days"] == 4
    assert weekly["missed"] == 3


def test_alert_triggers_for_missed_days(monkeypatch):
    module, _, _ = _load_frontend_app_module(monkeypatch)

    kind, message = module.get_missed_days_alert(3)
    assert kind == "warning"
    assert "missed 3 days" in message

    kind, message = module.get_missed_days_alert(0)
    assert kind == "success"
    assert "Perfect week" in message

    kind, message = module.get_missed_days_alert(1)
    assert kind is None
    assert message is None

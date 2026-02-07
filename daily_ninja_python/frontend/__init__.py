"""
Streamlit Frontend Application
==============================

Daily Ninja - Productivity Assistant
A Streamlit-based productivity app featuring:
- Streak counter for tracking consecutive productive days
- Todo list with priorities and completion tracking
- GitHub-style activity heatmap visualization

Usage:
    streamlit run frontend/app.py
"""

from pathlib import Path

# Package metadata
__version__ = "1.0.0"
__author__ = "Daily Ninja Team"

# Expose main module path for convenience
APP_PATH = Path(__file__).parent / "app.py"
DATA_DIR = Path(__file__).parent / "data"

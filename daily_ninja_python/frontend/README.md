# Daily Ninja Frontend 🥷

A fully functional Streamlit-based productivity assistant with streak tracking, todo management, and activity visualization.

## Features

### 🔥 Streak Counter
- Track consecutive days of productivity
- Visual streak display with motivational messages
- One-click daily check-in
- Streak milestones with celebrations

### 📝 Todo List
- Add tasks with priority levels (High/Medium/Low)
- Mark tasks as complete/incomplete
- Delete individual tasks
- Clear all completed tasks
- Task statistics and progress tracking

### 📊 GitHub-Style Heatmap
- Visual representation of activity over the past year
- Color-coded activity intensity
- Current and longest streak metrics
- Activity rate percentage

## Installation

1. **Ensure dependencies are installed:**
   ```bash
   pip install -r requirements/base.txt
   ```

2. **Run the app:**
   ```bash
   cd daily_ninja_python
   streamlit run frontend/app.py
   ```

3. **Open in browser:**
   The app will automatically open at `http://localhost:8501`

## Usage

### Daily Check-In
1. Click the **"🎯 Check In Today"** button to mark your day as productive
2. Watch your streak grow!
3. The heatmap will update to show your activity

### Managing Tasks
1. Enter a task in the input field
2. Select a priority (Low/Medium/High)
3. Click **"➕ Add"** to add the task
4. Click the checkbox to mark as complete
5. Click 🗑️ to delete a task

### Demo Mode
- Use **"📥 Load Sample Data"** in the sidebar to populate with demo data
- Use **"🗑️ Clear All Data"** to reset everything

## Project Structure

```
frontend/
├── __init__.py      # Package initialization
├── app.py           # Main Streamlit application
├── README.md        # This file
└── data/            # Persisted user data (JSON)
    └── user_data.json
```

## Data Persistence

User data is automatically saved to `frontend/data/user_data.json` and persists across sessions. The data includes:
- Todo items with priorities and completion status
- Completed activity dates
- Streak information

## Customization

### Styling
Custom CSS is injected via `inject_custom_css()`. Modify this function to change:
- Color schemes
- Button styles
- Container styling
- Layout spacing

### Extending Features
The app is modular with separate functions for each component:
- `render_streak_counter()` - Streak display and check-in
- `render_todo_list()` - Todo management UI
- `render_heatmap()` - Activity visualization
- `render_sidebar()` - Settings and quick stats

## Dependencies

- `streamlit>=1.28.0` - Web framework
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical operations

## Screenshots

### Main Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│  🥷 Daily Ninja - Your Personal Productivity Assistant      │
├─────────────────────┬───────────────────────────────────────┤
│  🔥 Streak Counter  │  📊 Activity Heatmap                  │
│  ┌───────────────┐  │  ┌─────────────────────────────────┐  │
│  │      15      │  │  │ █ █ █   █ █ █ █   █ █ █ █ █    │  │
│  │  Days Streak │  │  │ █   █ █     █ █ █   █          │  │
│  └───────────────┘  │  │   █ █ █ █ █   █   █ █ █ █      │  │
│                     │  └─────────────────────────────────┘  │
│  📝 Todo List       │                                       │
│  🔴 Complete PR     │  Stats: 45 active days, 12% rate      │
│  🟡 Write tests     │                                       │
│  🟢 Update docs     │                                       │
└─────────────────────┴───────────────────────────────────────┘
```

## License

Part of the Daily Ninja project. See root LICENSE for details.

"""Daily Ninja - Productivity Assistant (Streamlit Frontend)"""
import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path

# Config
st.set_page_config(page_title="Daily Ninja 🥷", page_icon="🥷", layout="wide")
DATA_FILE = Path(__file__).parent / "data" / "user_data.json"

# Task categories with colors
CATEGORIES = {
    "work": {"emoji": "💼", "color": "#3b82f6"},
    "personal": {"emoji": "🏠", "color": "#8b5cf6"},
    "health": {"emoji": "💪", "color": "#10b981"},
    "learning": {"emoji": "📚", "color": "#f59e0b"},
}

# Streak milestones for badges
BADGES = [
    {"days": 7, "emoji": "🥉", "name": "Week Warrior"},
    {"days": 30, "emoji": "🥈", "name": "Monthly Master"},
    {"days": 100, "emoji": "🥇", "name": "Century Ninja"},
    {"days": 365, "emoji": "🏆", "name": "Legendary"},
]
DATA_FILE = Path(__file__).parent / "data" / "user_data.json"

# ============ CUSTOM CSS ============
st.markdown("""
<style>
/* Navbar */
.navbar { background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%); padding: 1rem 2rem;
    border-radius: 10px; margin-bottom: 2rem; display: flex; align-items: center; gap: 20px; }
.navbar h1 { color: #fff; margin: 0; font-size: 1.8rem; }
.navbar span { color: #8b949e; font-size: 0.9rem; }
/* Cards with hover */
.stat-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 1.5rem;
    transition: all 0.3s ease; text-align: center; }
.stat-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(57, 211, 83, 0.2);
    border-color: #39d353; }
.stat-card h2 { color: #39d353; font-size: 2.5rem; margin: 0; }
.stat-card p { color: #8b949e; margin: 0.5rem 0 0 0; }
/* Todo items */
.todo-item { background: #0d1117; border: 1px solid #21262d; border-radius: 8px; padding: 0.8rem 1rem;
    margin: 0.5rem 0; transition: all 0.2s ease; }
.todo-item:hover { background: #161b22; border-color: #39d353; }
/* Buttons */
.stButton > button { background: linear-gradient(90deg, #238636 0%, #2ea043 100%) !important;
    border: none !important; transition: all 0.3s ease !important; }
.stButton > button:hover { transform: scale(1.05) !important; box-shadow: 0 5px 20px rgba(46, 160, 67, 0.4) !important; }
/* Heatmap cells */
.cell { transition: all 0.2s ease; cursor: pointer; }
.cell:hover { transform: scale(1.5); z-index: 10; box-shadow: 0 0 10px rgba(57, 211, 83, 0.5); }
/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
/* Badges */
.badge { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 20px;
    background: linear-gradient(135deg, #1a1a2e, #16213e); border: 2px solid #39d353; margin: 4px; }
.badge.locked { opacity: 0.4; border-color: #30363d; }
.badge span { font-size: 1.2rem; }
.badge-name { color: #8b949e; font-size: 0.8rem; }
/* Category tags */
.category-tag { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; 
    font-weight: 500; margin-left: 8px; }
/* Ninja slash animation */
@keyframes ninjaSlash {
    0% { transform: scale(1) rotate(0deg); opacity: 1; }
    50% { transform: scale(1.5) rotate(180deg); opacity: 0.8; }
    100% { transform: scale(0) rotate(360deg); opacity: 0; }
}
.slash-effect { animation: ninjaSlash 0.5s ease-out; position: absolute; font-size: 2rem; }
/* Analytics cards */
.analytics-card { background: #0d1117; border: 1px solid #21262d; border-radius: 10px; padding: 1rem;
    text-align: center; }
.analytics-card h3 { color: #39d353; margin: 0; font-size: 1.5rem; }
.analytics-card p { color: #8b949e; margin: 0.5rem 0 0 0; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# ============ DATA FUNCTIONS ============
def load_data():
    """Load user data from JSON file with deduplication."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    defaults = {"todos": [], "activity": {}, "streak": 0, "last_date": None, "longest_streak": 0}
    if DATA_FILE.exists():
        data = json.loads(DATA_FILE.read_text())
        for key in defaults:
            if key not in data:
                data[key] = defaults[key]
        # Deduplicate todos on load
        seen, unique_todos = set(), []
        for todo in data.get("todos", []):
            task_key = todo.get("task", "").lower().strip()
            if task_key and task_key not in seen:
                seen.add(task_key)
                unique_todos.append(todo)
        if len(unique_todos) != len(data["todos"]):
            data["todos"] = unique_todos
            DATA_FILE.write_text(json.dumps(data, indent=2))
        return data
    return defaults

def save_data(data):
    """Save user data to JSON file."""
    DATA_FILE.write_text(json.dumps(data, indent=2))

def init_session():
    """Initialize session state from saved data."""
    if "data" not in st.session_state:
        st.session_state.data = load_data()

# ============ STREAK LOGIC ============
def log_activity():
    """Log activity for today (called when completing tasks or clicking Log Today)."""
    data = st.session_state.data
    today = datetime.now().strftime("%Y-%m-%d")
    data["activity"][today] = data["activity"].get(today, 0) + 1
    save_data(data)

def update_streak():
    """Recalculate streak based on consecutive days with activity."""
    data = st.session_state.data
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    if data["last_date"] == today:
        return
    
    if data["last_date"] == yesterday:
        data["streak"] += 1
    else:
        data["streak"] = 1
    
    # Track longest streak
    data["longest_streak"] = max(data.get("longest_streak", 0), data["streak"])
    data["last_date"] = today
    log_activity()

# ============ ANALYTICS ============
def get_weekly_stats():
    """Calculate stats for the last 7 days."""
    data = st.session_state.data
    today = datetime.now()
    week_dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    tasks_done = sum(data["activity"].get(d, 0) for d in week_dates)
    active_days = sum(1 for d in week_dates if data["activity"].get(d, 0) > 0)
    return {"tasks": tasks_done, "active_days": active_days, "missed": 7 - active_days}

def get_monthly_stats():
    """Calculate stats for the last 30 days."""
    data = st.session_state.data
    today = datetime.now()
    month_dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
    tasks_done = sum(data["activity"].get(d, 0) for d in month_dates)
    active_days = sum(1 for d in month_dates if data["activity"].get(d, 0) > 0)
    return {"tasks": tasks_done, "active_days": active_days, "missed": 30 - active_days}

def get_earned_badges(streak):
    """Get list of badges with earned/locked status."""
    return [{"badge": b, "earned": streak >= b["days"]} for b in BADGES]

# ============ HEATMAP ============
def render_heatmap():
    """Render GitHub-style contribution heatmap using HTML/CSS."""
    data = st.session_state.data
    today = datetime.now()
    
    # Generate last 365 days
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(364, -1, -1)]
    
    # Color scale (GitHub green palette)
    def get_color(count):
        if count == 0: return "#161b22"
        if count <= 2: return "#0e4429"
        if count <= 4: return "#006d32"
        if count <= 6: return "#26a641"
        return "#39d353"
    
    # Build grid cells
    cells = []
    for day in days:
        count = data["activity"].get(day, 0)
        color = get_color(count)
        cells.append(f'<div class="cell" style="background:{color}" title="{day}: {count}"></div>')
    
    # CSS + HTML for heatmap
    html = f"""
    <style>
    .heatmap {{ display: flex; flex-wrap: wrap; gap: 3px; max-width: 900px; }}
    .cell {{ width: 12px; height: 12px; border-radius: 2px; }}
    .legend {{ display: flex; gap: 4px; align-items: center; margin-top: 10px; color: #8b949e; font-size: 12px; }}
    </style>
    <div class="heatmap">{''.join(cells)}</div>
    <div class="legend">
        Less <div class="cell" style="background:#161b22"></div>
        <div class="cell" style="background:#0e4429"></div>
        <div class="cell" style="background:#006d32"></div>
        <div class="cell" style="background:#26a641"></div>
        <div class="cell" style="background:#39d353"></div> More
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ============ MAIN APP ============
def main():
    init_session()
    data = st.session_state.data
    
    # Custom Navbar
    st.markdown('''
    <div class="navbar">
        <h1>🥷 Daily Ninja</h1>
        <span>|</span>
        <span>📊 Dashboard</span>
        <span>|</span>
        <span>Your personal productivity tracker</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # --- Stats Row ---
    col1, col2, col3, col4 = st.columns(4)
    today = datetime.now().strftime("%Y-%m-%d")
    today_count = data["activity"].get(today, 0)
    
    with col1:
        st.markdown(f'<div class="stat-card"><h2>🔥 {data["streak"]}</h2><p>Day Streak</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><h2>✅ {today_count}</h2><p>Tasks Today</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><h2>🏆 {data.get("longest_streak", 0)}</h2><p>Best Streak</p></div>', unsafe_allow_html=True)
    with col4:
        if st.button("✅ Log Today", use_container_width=True):
            update_streak()
            st.rerun()
    
    st.write("")
    
    # --- Badges Section ---
    badges_html = "<div style='display:flex;flex-wrap:wrap;gap:8px;margin-bottom:1rem'>"
    for item in get_earned_badges(data["streak"]):
        b, earned = item["badge"], item["earned"]
        status = "" if earned else " locked"
        badges_html += f'<div class="badge{status}"><span>{b["emoji"]}</span><span class="badge-name">{b["name"]} ({b["days"]}d)</span></div>'
    badges_html += "</div>"
    st.markdown(badges_html, unsafe_allow_html=True)
    
    # --- Main Content ---
    tab1, tab2, tab3 = st.tabs(["📝 Tasks", "📊 Analytics", "🗓️ Heatmap"])
    
    # ===== TASKS TAB =====
    with tab1:
        col_form, col_list = st.columns([1, 2])
        
        with col_form:
            st.subheader("Add New Task")
            with st.form("add_task_form", clear_on_submit=True):
                new_task = st.text_input("Task", placeholder="What needs to be done?")
                category = st.selectbox("Category", list(CATEGORIES.keys()), format_func=lambda x: f"{CATEGORIES[x]['emoji']} {x.title()}")
                due_date = st.date_input("Due Date (optional)", value=None, min_value=datetime.now().date())
                submitted = st.form_submit_button("➕ Add Task", use_container_width=True)
                
                if submitted and new_task.strip():
                    existing = {t.get("task", "").lower().strip() for t in data["todos"]}
                    if new_task.lower().strip() not in existing:
                        data["todos"].append({
                            "task": new_task.strip(),
                            "done": False,
                            "category": category,
                            "due": due_date.isoformat() if due_date else None
                        })
                        save_data(data)
                        st.rerun()
                    else:
                        st.warning("Task already exists!")
        
        with col_list:
            st.subheader("Your Tasks")
            
            # Filter by category
            filter_cat = st.selectbox("Filter", ["all"] + list(CATEGORIES.keys()), 
                format_func=lambda x: "📋 All" if x == "all" else f"{CATEGORIES[x]['emoji']} {x.title()}")
            
            for i, todo in enumerate(data["todos"]):
                cat = todo.get("category", "personal")
                if filter_cat != "all" and cat != filter_cat:
                    continue
                    
                is_done = todo.get("done", False)
                task_text = todo.get("task", "")
                cat_info = CATEGORIES.get(cat, CATEGORIES["personal"])
                
                c1, c2, c3 = st.columns([0.5, 8, 1])
                with c1:
                    done = st.checkbox("done", is_done, key=f"chk_{i}", label_visibility="collapsed")
                    if done != is_done:
                        data["todos"][i]["done"] = done
                        if done and not is_done:
                            log_activity()
                            st.toast(f"⚔️ Ninja slash! Task completed!")
                        save_data(data)
                with c2:
                    style = "text-decoration: line-through; opacity: 0.5;" if is_done else ""
                    due = todo.get("due")
                    due_str = f" 📅 {due}" if due else ""
                    st.markdown(f'''<span style="{style}">{task_text}</span>
                        <span class="category-tag" style="background:{cat_info['color']}20;color:{cat_info['color']}">{cat_info['emoji']} {cat}</span>
                        <span style="color:#8b949e;font-size:0.8rem">{due_str}</span>''', unsafe_allow_html=True)
                with c3:
                    if st.button("🗑️", key=f"del_{i}"):
                        data["todos"].pop(i)
                        save_data(data)
                        st.rerun()
    
    # ===== ANALYTICS TAB =====
    with tab2:
        st.subheader("📈 Your Productivity Stats")
        
        weekly = get_weekly_stats()
        monthly = get_monthly_stats()
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="analytics-card"><h3>{weekly["tasks"]}</h3><p>Tasks This Week</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="analytics-card"><h3>{weekly["active_days"]}/7</h3><p>Active Days</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="analytics-card"><h3>{monthly["tasks"]}</h3><p>Tasks This Month</p></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="analytics-card"><h3>{monthly["active_days"]}/30</h3><p>Active Days</p></div>', unsafe_allow_html=True)
        
        st.write("")
        
        # Weekly breakdown chart
        st.subheader("📊 Last 7 Days")
        today_dt = datetime.now()
        week_data = []
        for i in range(6, -1, -1):
            d = (today_dt - timedelta(days=i)).strftime("%Y-%m-%d")
            week_data.append({"day": d[-5:], "tasks": data["activity"].get(d, 0)})
        
        st.bar_chart({d["day"]: d["tasks"] for d in week_data})
        
        # Missed days alert
        if weekly["missed"] > 2:
            st.warning(f"⚠️ You missed {weekly['missed']} days this week. Keep that streak going!")
        elif weekly["missed"] == 0:
            st.success("🎉 Perfect week! You logged activity every day!")
    
    # ===== HEATMAP TAB =====
    with tab3:
        total = sum(data["activity"].values())
        st.subheader(f"📊 {total} contributions in the last year")
        render_heatmap()

if __name__ == "__main__":
    main()

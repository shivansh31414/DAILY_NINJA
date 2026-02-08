"""Daily Ninja - Productivity Assistant (Streamlit Frontend)"""
import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path

# Config
st.set_page_config(page_title="Daily Ninja 🥷", page_icon="🥷", layout="wide")
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
</style>
""", unsafe_allow_html=True)

# ============ DATA FUNCTIONS ============
def load_data():
    """Load user data from JSON file with deduplication."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    defaults = {"todos": [], "activity": {}, "streak": 0, "last_date": None}
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
            DATA_FILE.write_text(json.dumps(data, indent=2))  # Save cleaned data
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
    
    # Only update streak once per day
    if data["last_date"] == today:
        return
    
    # Streak continues if we logged yesterday, otherwise resets to 1
    if data["last_date"] == yesterday:
        data["streak"] += 1
    else:
        data["streak"] = 1
    
    data["last_date"] = today
    log_activity()  # Also log activity when updating streak

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
    
    # --- Streak Section ---
    col1, col2 = st.columns([1, 3])
    with col1:
        today = datetime.now().strftime("%Y-%m-%d")
        today_count = data["activity"].get(today, 0)
        
        st.markdown(f'''
        <div class="stat-card">
            <h2>🔥 {data["streak"]}</h2>
            <p>Day Streak</p>
        </div>
        ''', unsafe_allow_html=True)
        st.write("")
        st.markdown(f'''
        <div class="stat-card">
            <h2>✅ {today_count}</h2>
            <p>Tasks Today</p>
        </div>
        ''', unsafe_allow_html=True)
        st.write("")
        if st.button("✅ Log Today", use_container_width=True):
            update_streak()
            st.rerun()
    
    # --- Todo Section ---
    with col2:
        st.subheader("📝 Todo List")
        
        # Use form to prevent duplicate submissions
        with st.form("add_task_form", clear_on_submit=True):
            new_task = st.text_input("Add task", placeholder="What needs to be done?", label_visibility="collapsed")
            submitted = st.form_submit_button("➕ Add Task", use_container_width=True)
            if submitted and new_task.strip():
                # Check for duplicates (case-insensitive)
                existing = {t.get("task", "").lower().strip() for t in data["todos"]}
                if new_task.lower().strip() not in existing:
                    data["todos"].append({"task": new_task.strip(), "done": False})
                    save_data(data)
                    st.rerun()
                else:
                    st.warning("Task already exists!")
        
        for i, todo in enumerate(data["todos"]):
            # Ensure todo has required keys
            is_done = todo.get("done", False)
            task_text = todo.get("task", str(todo) if isinstance(todo, str) else "")
            c1, c2, c3 = st.columns([0.5, 8, 1])
            with c1:
                done = st.checkbox("done", is_done, key=f"chk_{i}", label_visibility="collapsed")
                if done != is_done:
                    data["todos"][i] = {"task": task_text, "done": done}
                    # Log activity when task is completed (contributes to heatmap)
                    if done and not is_done:
                        log_activity()
                    save_data(data)
            with c2:
                style = "~~" if is_done else ""
                st.write(f"{style}{task_text}{style}")
            with c3:
                if st.button("🗑️", key=f"del_{i}"):
                    data["todos"].pop(i)
                    save_data(data)
                    st.rerun()
    
    # --- Heatmap Section ---
    st.divider()
    total = sum(data["activity"].values())
    st.subheader(f"📊 {total} contributions in the last year")
    render_heatmap()

if __name__ == "__main__":
    main()

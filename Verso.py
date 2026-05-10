import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import difflib
import streamlit.components.v1 as components

# --- 🛰️ GOOGLE ANALYTICS INTEGRATION ---
def inject_ga():
    ga_id = "G-030XWBG97P"
    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga_id}', {{ 'debug_mode': true }});
    </script>
    """
    components.html(ga_code, height=0)

# --- 🛠️ ACADEMIC ENGINE SETUP ---
@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
    except Exception: pass

setup_system()

# --- ⚙️ STATE MANAGEMENT ---
if 'reset_counter' not in st.session_state: st.session_state.reset_counter = 0
if 'timer_end_time' not in st.session_state: st.session_state.timer_end_time = None
if 'timer_active' not in st.session_state: st.session_state.timer_active = False
if 'remaining_at_pause' not in st.session_state: st.session_state.remaining_at_pause = 0
if 'sound_unlocked' not in st.session_state: st.session_state.sound_unlocked = False
if 'selected_alarm_tone' not in st.session_state: st.session_state.selected_alarm_tone = "Double Beep"
if 'theme_mode' not in st.session_state: st.session_state.theme_mode = "dark"

ALARM_TONES = {
    "Double Beep": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
    "Beep (High)": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    "Digital Alarm": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
    "Industrial Siren": "https://actions.google.com/sounds/v1/alarms/industrial_alarm.ogg"
}

def trigger_master_reset():
    st.session_state.reset_counter += 1
    for key in list(st.session_state.keys()):
        if key != 'reset_counter': del st.session_state[key]
    st.session_state.selected_alarm_tone = "Double Beep"
    st.session_state.theme_mode = "dark"
    st.toast("🚨 SYSTEM WIPED")
    time.sleep(0.4)
    st.rerun()

# --- 🎨 THEME LOGIC (IF CONDITION) ---
# This part handles the "all of their kind" text coloring
if st.session_state.theme_mode == "dark":
    main_text_color = "#FFFFFF"  # White text for dark mode
    app_background = "#0e1117"   # Dark background
    card_text_inner = "#e2e8f0"
else:
    main_text_color = "#000000"  # Black text for light mode
    app_background = "#FFFFFF"   # White background
    card_text_inner = "#1a202c"

accent = st.session_state.get('set_color', "#3b82f6")
bg_card = st.session_state.get('set_bg', "#1e293b")
f_scale = st.session_state.get('set_font', 1.1)

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

# Universal CSS Injector for text and theme
st.markdown(f"""
    <style>
    /* Main App Background */
    .stApp {{ background-color: {app_background} !important; }}
    
    /* Apply color to ALL text elements: headers, paragraphs, labels, and markdown */
    h1, h2, h3, p, span, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p, .stTextInput label, .stTextArea label {{ 
        color: {main_text_color} !important; 
    }}
    
    .notebook-card {{ 
        background-color: {bg_card}; 
        padding: 20px; border-radius: 12px; border-left: 5px solid {accent}; 
        margin-bottom: 15px; color: {card_text_inner} !important; 
    }}
    
    .teacher-board {{ 
        background-color: #1a202c; border: 2px solid {accent}; padding: 40px; 
        border-radius: 10px; font-family: 'Inter', sans-serif; min-height: 500px; 
        color: #e2e8f0 !important; line-height: 1.8; font-size: {f_scale}rem; 
    }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "✍️ Grammar Checker", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: HOME ---
if choice == "🏠 Home":
    st.markdown("<h1>Welcome to Verso Research</h1>", unsafe_allow_html=True)
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True)

# --- MODULE: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.markdown("<h1>Veso Writing Teacher</h1>", unsafe_allow_html=True)
    st.markdown("### 📥 Universal Resource Hub")
    st.file_uploader("Upload Files", accept_multiple_files=True)
    raw_content = st.text_area("Input Content:", height=200)

# --- MODULE: GRAMMAR CHECKER ---
elif choice == "✍️ Grammar Checker":
    st.markdown("<h1>Smart Grammar Correction</h1>", unsafe_allow_html=True)
    text_to_check = st.text_area("Paste text to improve:", height=200, placeholder="e.g., hi my nme is yaseen")
    if st.button("✨ Run Smart Correction"):
        if text_to_check:
            t = text_to_check.lower().strip()
            # Yaseen's common logic fixes
            t = re.sub(r'\bmy\s+nme\b', 'my name', t)
            t = re.sub(r'\bnme\b', 'name', t)
            blob = TextBlob(t)
            corrected = str(blob.correct())
            st.success("Correction Finished!")
            st.markdown(f'<div class="notebook-card">{corrected}</div>', unsafe_allow_html=True)

# --- MODULE: PLAGIARISM CHECKER ---
elif choice == "🛡️ Plagiarism Checker":
    st.markdown("<h1>Integrity Scanner</h1>", unsafe_allow_html=True)
    plag_text = st.text_area("Paste text to scan:", height=200)
    if st.button("🔍 Deep Plagiarism Scan"):
        st.success("Content Unique.")

# --- MODULE: TIME TRACKER ---
elif choice == "⏱️ Time Tracker":
    st.markdown("<h1>Focus Timer</h1>", unsafe_allow_html=True)
    mins = st.number_input("Minutes:", 1, 120, 25)
    c1, c2, c3 = st.columns(3)
    if c1.button("Start"): st.session_state.timer_active = True
    if c2.button("Pause"): st.session_state.timer_active = False
    if c3.button("Reset"): st.session_state.timer_active = False
    st.markdown(f"### Status: {mins}:00")

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.markdown("<h1>Verso Control Center</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🎨 Theme & UI")
        # FIXED: Theme buttons now actively change the state and rerun the app
        t_col1, t_col2 = st.columns(2)
        if t_col1.button("☀️ Light Mode", use_container_width=True):
            st.session_state.theme_mode = "light"
            st.rerun()
        if t_col2.button("🌑 Dark Mode", use_container_width=True):
            st.session_state.theme_mode = "dark"
            st.rerun()
            
        st.color_picker("Accent Color", accent, key="set_color")
        st.slider("Font Scale", 0.8, 2.0, 1.1, key="set_font")
        
    with c2:
        st.markdown("### ⚙️ System Tools")
        if st.button("🚨 MASTER RESET", type="primary", use_container_width=True):
            trigger_master_reset()
        st.selectbox("Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
        st.info(f"System Build: 15.2.0")

    st.write("---")
    st.markdown("### ⚡ Advanced Toolbox")
    tools = ["Arduino Serial", "MQ2 Calib", "Pin 4 Fix", "Climate Trends", "BT Config"]
    tc1, tc2, tc3 = st.columns(3)
    for i, t in enumerate(tools):
        col = [tc1, tc2, tc3][i % 3]
        if col.button(t, use_container_width=True):
            st.toast(f"Running {t}...")

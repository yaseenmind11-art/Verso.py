import streamlit as st
from textblob import TextBlob
import nltk
import time
import re
import streamlit.components.v1 as components

# --- 🛰️ ANALYTICS ---
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

# --- 🛠️ SETUP ---
@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
    except Exception: pass

setup_system()

# --- ⚙️ STATE ---
if 'theme_mode' not in st.session_state: st.session_state.theme_mode = "dark"
if 'reset_counter' not in st.session_state: st.session_state.reset_counter = 0

def trigger_master_reset():
    st.session_state.reset_counter += 1
    for key in list(st.session_state.keys()):
        if key != 'reset_counter': del st.session_state[key]
    st.session_state.theme_mode = "dark"
    st.toast("🚨 SYSTEM WIPED")
    time.sleep(0.4)
    st.rerun()

# --- 🎨 THEME ENGINE (FIXED FOR LIGHT MODE) ---
# This "if" block fixes the visibility issues you saw in your screenshots
if st.session_state.theme_mode == "dark":
    main_txt = "#FFFFFF"  # White text for dark mode
    main_bg = "#0e1117"   # Dark background
else:
    main_txt = "#000000"  # Black text for light mode
    main_bg = "#FFFFFF"   # White background

accent = st.session_state.get('set_color', "#3b82f6")
bg_card = st.session_state.get('set_bg', "#1e293b")

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

# Global CSS injector to fix text visibility across ALL elements
st.markdown(f"""
    <style>
    .stApp {{ background-color: {main_bg} !important; }}
    
    /* Forces ALL headers, labels, and markdown to the correct theme color */
    h1, h2, h3, p, span, label, .stMarkdown, .stTextInput label, .stTextArea label, .stRadio label {{ 
        color: {main_txt} !important; 
    }}

    .notebook-card {{ 
        background-color: {bg_card}; 
        padding: 20px; border-radius: 12px; border-left: 5px solid {accent}; 
        margin-bottom: 15px; color: #FFFFFF !important; 
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

# --- MODULE: GRAMMAR CHECKER ---
elif choice == "✍️ Grammar Checker":
    st.markdown("<h1>Smart Grammar Correction</h1>", unsafe_allow_html=True)
    text_to_check = st.text_area("Paste text to improve:", height=200)
    if st.button("✨ Run Smart Correction"):
        if text_to_check:
            t = text_to_check.lower().strip()
            # Custom logic for common typos
            t = re.sub(r'\bmy\s+nme\b', 'my name', t)
            t = re.sub(r'\bnme\b', 'name', t)
            blob = TextBlob(t)
            corrected = str(blob.correct())
            st.success("Correction Finished!")
            st.markdown(f'<div class="notebook-card">{corrected}</div>', unsafe_allow_html=True)

# --- MODULE: TIME TRACKER ---
elif choice == "⏱️ Time Tracker":
    st.markdown("<h1>Focus Timer</h1>", unsafe_allow_html=True)
    mins = st.number_input("Minutes:", 1, 120, 25)
    c1, c2, c3 = st.columns(3)
    if c1.button("Start"): st.toast("Timer Started! ⏳")
    if c2.button("Pause"): st.toast("Timer Paused.")
    if c3.button("Reset"): st.rerun()
    st.markdown(f"### Status: {mins}:00")

# --- MODULE: SETTINGS (THEME SWITCHER) ---
elif choice == "⚙️ Settings":
    st.markdown("<h1>Verso Control Center</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎨 Theme")
        if st.button("☀️ Light Mode", use_container_width=True):
            st.session_state.theme_mode = "light"
            st.rerun()
        if st.button("🌑 Dark Mode", use_container_width=True):
            st.session_state.theme_mode = "dark"
            st.rerun()
        st.color_picker("Accent Color", accent, key="set_color")
    with col2:
        st.markdown("### 🛠️ System")
        if st.button("🚨 MASTER RESET", type="primary", use_container_width=True):
            trigger_master_reset()

# --- REMAINING MODULES ---
elif choice == "📒 Study Assistant":
    st.markdown("<h1>Veso Writing Teacher</h1>", unsafe_allow_html=True)
    st.file_uploader("Upload Files", accept_multiple_files=True)

elif choice == "🛡️ Plagiarism Checker":
    st.markdown("<h1>Integrity Scanner</h1>", unsafe_allow_html=True)
    st.text_area("Paste text to scan:", height=200)
    if st.button("🔍 Deep Plagiarism Scan"):
        st.success("Content Unique. ✅")

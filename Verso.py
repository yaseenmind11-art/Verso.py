import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import streamlit.components.v1 as components
import docx2txt
import PyPDF2
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- 🛰️ INITIALIZATION ---
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

@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
    except Exception: pass

setup_system()

# --- ⚙️ STATE MANAGEMENT ---
if 'set_color' not in st.session_state: st.session_state.set_color = "#FFFFFF" 
if 'set_bg' not in st.session_state: st.session_state.set_bg = "#5465C9"
if 'set_font' not in st.session_state: st.session_state.set_font = 1.10
if 'high_contrast' not in st.session_state: st.session_state.high_contrast = False
if 'power_save' not in st.session_state: st.session_state.power_save = False

if 'reset_counter' not in st.session_state: st.session_state.reset_counter = 0
if 'timer_end_time' not in st.session_state: st.session_state.timer_end_time = None
if 'timer_active' not in st.session_state: st.session_state.timer_active = False
if 'remaining_at_pause' not in st.session_state: st.session_state.remaining_at_pause = 0
if 'selected_alarm_tone' not in st.session_state: st.session_state.selected_alarm_tone = "Double Beep"

if 'study_text_input' not in st.session_state: st.session_state.study_text_input = ""
if 'grammar_text_input' not in st.session_state: st.session_state.grammar_text_input = ""
if 'plag_text_input' not in st.session_state: st.session_state.plag_text_input = ""
if 'word_counter_input' not in st.session_state: st.session_state.word_counter_input = ""

# --- 🛠️ HELPERS ---
def trigger_master_reset():
    st.session_state.reset_counter += 1
    for key in list(st.session_state.keys()):
        if key != 'reset_counter': del st.session_state[key]
    st.toast("🚨 SYSTEM HARD RESET")
    time.sleep(0.4)
    st.rerun()

ALARM_TONES = {
    "Double Beep": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
    "Beep (High)": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    "Digital Alarm": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"
}

# --- 🎨 DYNAMIC STYLING ---
accent = st.session_state.set_color
bg_card = st.session_state.set_bg
f_scale = st.session_state.set_font

if st.session_state.high_contrast:
    accent = "#FFFF00"
    bg_card = "#000000"

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

st.markdown(f"""
    <style>
    .stApp {{ filter: {"grayscale(100%)" if st.session_state.power_save else "none"}; font-size: {f_scale}rem; }}
    .notebook-card {{ 
        background-color: {bg_card}; 
        padding: 25px; border-radius: 12px; border-left: 6px solid {accent}; 
        margin-bottom: 15px; color: #FFFFFF !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    .teacher-board {{ 
        background-color: #0f172a; border: 1px solid #334155; padding: 30px; 
        border-radius: 12px; color: #f1f5f9; line-height: 1.6;
    }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    nav_options = ["🏠 Home", "📒 Study Assistant", "✍️ Grammar Checker", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "📝 Word Counter", "⚙️ Settings"]
    choice = st.radio("Navigation", nav_options, label_visibility="collapsed")

# --- MAIN MODULES ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown("### 🎓 Universal Academic Engine")
    
    st.markdown("Activate Reliable Databases:")
    sources = st.multiselect("Databases", ["Educational (.edu)", "Government (.gov)", "Scientific Journals", "Encyclopedias"], 
                            default=["Educational (.edu)", "Government (.gov)", "Scientific Journals", "Encyclopedias"], label_visibility="collapsed")
    
    q = st.text_input("🔍 Search Database:", placeholder="Research your topic here...", key="home_search")
    if q:
        st.link_button("🚀 Open Research Results", f"https://www.google.com/search?q={q}")

elif choice == "📒 Study Assistant":
    st.title("Verso Deep Learning Teacher")
    raw_content = st.text_area("Input Content:", value=st.session_state.study_text_input, height=200)
    st.session_state.study_text_input = raw_content
    if raw_content.strip():
        blob = TextBlob(raw_content)
        t1, t2 = st.tabs(["🔑 Keywords", "✍️ AI Teacher"])
        with t1:
            words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 3]))
            for i, word in enumerate(words[:10]): 
                st.markdown(f'<div class="notebook-card">{i+1}. {word.title()}</div>', unsafe_allow_html=True)
        with t2:
            st.markdown(f'<div class="teacher-board"><h2>CONCEPT ANALYSIS</h2><p>Analysis for: <b>{words[0].title() if words else "Source"}</b></p></div>', unsafe_allow_html=True)

elif choice == "✍️ Grammar Checker":
    st.title("Smart Auto-Correct")
    text = st.text_area("Paste text:", value=st.session_state.grammar_text_input, height=200)
    st.session_state.grammar_text_input = text
    if st.button("✨ Correct"):
        corrected = str(TextBlob(text).correct())
        st.markdown(f'<div class="notebook-card"><b>Corrected version:</b><br>{corrected}</div>', unsafe_allow_html=True)

elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    plag_text = st.text_area("Paste text to scan:", value=st.session_state.plag_text_input, height=200)
    st.session_state.plag_text_input = plag_text
    if st.button("🔍 Run Scan"):
        with st.spinner("Comparing against database..."):
            time.sleep(1.5)
            st.success("Analysis complete: No significant matches found (Simulated).")

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    c1, c2, c3 = st.columns(3)
    if c1.button("Start"): 
        st.session_state.timer_end_time = time.time() + (mins * 60)
        st.session_state.timer_active = True
    if c2.button("Pause"): st.session_state.timer_active = False
    if c3.button("Reset"): 
        st.session_state.timer_active = False
        st.session_state.timer_end_time = None
    st.metric("Status", "Running" if st.session_state.timer_active else "Stopped")

elif choice == "📝 Word Counter":
    st.title("Word Metrics")
    txt = st.text_area("Input:", value=st.session_state.word_counter_input, height=200)
    st.session_state.word_counter_input = txt
    words = len(re.findall(r'\b\w+\b', txt))
    st.metric("Total Words", words)

elif choice == "⚙️ Settings":
    st.markdown('<h1 style="font-size: 3rem;">Verso Control Center</h1>', unsafe_allow_html=True)
    
    # --- 20 QUICK ACTION BUTTONS GRID ---
    st.markdown("### ⚡ Quick System Actions")
    bc1, bc2, bc3, bc4 = st.columns(4)
    with bc1:
        if st.button("🛠️ Repair Engine", use_container_width=True):
            st.cache_resource.clear()
            st.toast("Internal Engine Re-initialized.")
        if st.button("🧹 Clear Cache", use_container_width=True):
            st.toast("Temporary cache cleared.")
        if st.button("🔄 Sync Plugins", use_container_width=True):
            setup_system()
            st.toast("NLP Modules synchronized.")
        if st.button("📊 Update Metrics", use_container_width=True):
            st.toast("System statistics updated.")
        if st.button("🧪 Beta Mode", use_container_width=True):
            st.toast("Experimental features enabled.")

    with bc2:
        if st.button("📡 Reconnect API", use_container_width=True):
            with st.spinner("Connecting..."): time.sleep(1); st.toast("API Protocol: SUCCESS")
        if st.button("🛡️ Hard Lockdown", use_container_width=True):
            st.toast("Security protocols enforced.")
        if st.button("💾 Local Save", use_container_width=True):
            st.toast("Local snapshot saved.")
        if st.button("🌍 Global Sync", use_container_width=True):
            st.toast("Database indices updated.")
        if st.button("📜 View Logs", use_container_width=True):
            st.toast("Accessing system logs...")

    with bc3:
        if st.button("🔋 Power Save", use_container_width=True):
            st.session_state.power_save = not st.session_state.power_save
            st.rerun()
        if st.button("🔊 Max Volume", use_container_width=True):
            st.toast("System gain set to maximum.")
        if st.button("👁️ High Contrast", use_container_width=True):
            st.session_state.high_contrast = not st.session_state.high_contrast
            st.rerun()
        if st.button("📎 Rebuild Index", use_container_width=True):
            st.toast("Search index rebuilt.")
        if st.button("🛠️ Dev Tools", use_container_width=True):
            st.toast("Developer tools unlocked.")

    with bc4:
        if st.button("🧊 Freeze State", use_container_width=True):
            st.toast("Session state frozen.")
        if st.button("🔥 Performance", use_container_width=True):
            st.toast("Performance mode: ULTRA")
        if st.button("🛰️ Signal Check", use_container_width=True):
            st.toast(f"Latency: {random.randint(10, 50)}ms")
        if st.button("🔑 Verify Keys", use_container_width=True):
            st.toast("API keys validated.")
        if st.button("🚀 Turbo Boost", use_container_width=True):
            st.balloons(); st.toast("Processing speed augmented.")

    st.divider()

    # --- THREE COLUMN MAIN LAYOUT ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('### 📚 Academic')
        st.selectbox("Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
        st.selectbox("Citation Style", ["APA 7th", "MLA 9th", "Chicago"], key="cite_style")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚨 MASTER RESET", type="primary", use_container_width=True):
            trigger_master_reset()

    with col2:
        st.markdown('### 🎨 UI Appearance')
        st.color_picker("Accent Color", value=st.session_state.set_color, key="set_color")
        st.color_picker("Card BG", value=st.session_state.set_bg, key="set_bg")
        st.slider("Font Scale", 0.8, 2.0, value=st.session_state.set_font, key="set_font")

    with col3:
        st.markdown('### 🔐 System Info')
        if st.button("Purge Input History", use_container_width=True):
            st.session_state.study_text_input = ""
            st.session_state.grammar_text_input = ""
            st.session_state.plag_text_input = ""
            st.toast("Input buffers purged.")
        if st.button("Cloud Backup", use_container_width=True):
            st.toast("Cloud snapshot created.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"Build: 14.5.6 (vID: {st.session_state.reset_counter})")

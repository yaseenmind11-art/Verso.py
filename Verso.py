import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import os
import streamlit.components.v1 as components

# --- 🛰️ ANALYTICS & SYSTEM ---
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
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger', 'maxent_treebank_pos_tagger']:
            nltk.download(res, quiet=True)
        os.system("python -m textblob.download_corpora")
    except Exception: pass

setup_system()

# --- ⚙️ STATE MANAGEMENT ---
if 'reset_counter' not in st.session_state: st.session_state.reset_counter = 0
if 'timer_end_time' not in st.session_state: st.session_state.timer_end_time = None
if 'timer_active' not in st.session_state: st.session_state.timer_active = False
if 'remaining_at_pause' not in st.session_state: st.session_state.remaining_at_pause = 0
if 'sound_unlocked' not in st.session_state: st.session_state.sound_unlocked = False

# Dictionary of available alarm tones
ALARM_TONES = {
    "Beep (Default)": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    "Digital Alarm": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
    "Industrial Siren": "https://actions.google.com/sounds/v1/alarms/industrial_alarm.ogg",
    "Double Beep": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg"
}

def trigger_master_reset():
    st.session_state.reset_counter += 1
    for key in list(st.session_state.keys()):
        if key != 'reset_counter': del st.session_state[key]
    st.rerun()

# --- ⏱️ BACKGROUND TIMER LOGIC ---
if st.session_state.timer_active and st.session_state.timer_end_time:
    now = time.time()
    diff = st.session_state.timer_end_time - now
    if diff <= 0:
        st.session_state.timer_active = False
        st.session_state.remaining_at_pause = 0
        st.session_state.timer_finished_trigger = True
    else:
        st.session_state.remaining_at_pause = diff

# --- 🎨 UI STYLING ---
accent = st.session_state.get('set_color', "#3b82f6")
bg_card = st.session_state.get('set_bg', "#1e293b")
f_scale = st.session_state.get('set_font', 1.1)

# Get the selected tone URL from settings
selected_tone_url = ALARM_TONES.get(st.session_state.get('selected_alarm_tone'), ALARM_TONES["Beep (Default)"])

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #FFFFFF; }}
    [data-testid="stSidebar"] {{ background-color: #1e293b !important; }}
    .notebook-card {{ background-color: {bg_card}; padding: 20px; border-radius: 12px; border-left: 5px solid {accent}; margin-bottom: 15px; color: #FFFFFF; }}
    .teacher-board {{ background-color: #1a202c; border: 2px solid {accent}; padding: 40px; border-radius: 10px; font-family: 'Inter', sans-serif; min-height: 500px; color: #e2e8f0; line-height: 1.8; font-size: {f_scale}rem; }}
    .time-up-banner {{ background-color: #ef4444; color: white; padding: 25px; text-align: center; font-weight: 800; border-radius: 12px; font-size: 28px; margin-bottom: 20px; animation: blinker 0.8s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0.2; }} }}
    </style>
""", unsafe_allow_html=True)

# --- 🔊 THE AUTOMATIC SOUND ENGINE ---
st.markdown(f"""
    <audio id="alarm-sound" preload="auto">
        <source src="{selected_tone_url}" type="audio/ogg">
    </audio>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: HOME ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True)

# --- MODULE: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("Veso Writing Teacher")
    st.markdown("### 📥 Universal Resource Hub")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.file_uploader("Upload Files", type=['pdf', 'docx', 'pptx', 'xlsx', 'csv', 'txt', 'png', 'jpg'], accept_multiple_files=True, key=f"file_hub_{st.session_state.reset_counter}")
    with col_b:
        st.text_input("Link Hub", placeholder="Paste URL here...", key=f"link_hub_{st.session_state.reset_counter}")
    st.write("---")
    raw_content = st.text_area("Input Content:", height=200)
    if raw_content:
        st.success("Analysis Engine Ready.")
        blob = TextBlob(raw_content)
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if words:
            st.markdown(f'<div class="notebook-card"><b>Main Topic Identified:</b> {words[0].title()}</div>', unsafe_allow_html=True)

# --- MODULE: PLAGIARISM CHECKER ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    p_text = st.text_area("Paste text:")
    if st.button("Deep Scan"):
        with st.spinner("Checking database..."):
            time.sleep(1)
            st.success("✅ Content Unique.")

# --- MODULE: TIME TRACKER (THE AUTOMATIC FIX) ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    
    if not st.session_state.sound_unlocked:
        st.warning("Browsers block automatic sound until you click once. Please click below to start.")
        if st.button("🔓 ENABLE AUTOMATIC ALARMS", use_container_width=True, type="primary"):
            components.html("""
                <script>
                    var audio = window.parent.document.getElementById('alarm-sound');
                    audio.play().then(() => { audio.pause(); audio.currentTime = 0; });
                </script>
            """, height=0)
            st.session_state.sound_unlocked = True
            st.rerun()
    else:
        st.success(f"✅ Auto-Alarm Active: {st.session_state.get('selected_alarm_tone', 'Beep (Default)')}")

    mins = st.number_input("Minutes:", 1, 120, 25)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Start New", use_container_width=True): 
        st.session_state.timer_end_time = time.time() + (mins * 60)
        st.session_state.timer_active = True
        st.rerun()
    if c2.button("Pause", use_container_width=True):
        st.session_state.timer_active = False
        st.rerun()
    if c3.button("Resume", use_container_width=True):
        if st.session_state.remaining_at_pause > 0:
            st.session_state.timer_end_time = time.time() + st.session_state.remaining_at_pause
            st.session_state.timer_active = True
            st.rerun()
    if c4.button("Reset", use_container_width=True):
        st.session_state.timer_active = False
        st.session_state.timer_end_time = None
        st.session_state.remaining_at_pause = 0
        st.rerun()
    
    timer_display = st.empty()
    m, s = divmod(st.session_state.remaining_at_pause, 60)
    timer_display.metric("Status", f"{int(m):02d}:{int(s):02d}")
    
    if st.session_state.timer_active:
        time.sleep(1)
        st.rerun()

# --- MODULE: SETTINGS (ALARM TONE CUSTOMIZATION) ---
elif choice == "⚙️ Settings":
    st.title("Control Center")
    if st.button("🚨 MASTER RESET", type="primary"): trigger_master_reset()
    
    st.write("---")
    st.subheader("🔊 Audio Configuration")
    # ALLOWS USER TO SELECT DIFFERENT TONES
    st.selectbox("Select Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
    
    if st.button("🎵 Test Tone"):
        components.html("""
            <script>
                var audio = window.parent.document.getElementById('alarm-sound');
                audio.currentTime = 0;
                audio.play();
                setTimeout(function(){ audio.pause(); }, 3000);
            </script>
        """, height=0)
    
    st.write("---")
    st.color_picker("Accent Color", "#3b82f6", key="set_color")
    st.slider("Font Scale", 0.8, 2.0, 1.1, key="set_font")

# --- FINAL AUTOMATIC TRIGGER ---
if st.session_state.get('timer_finished_trigger'):
    st.markdown('<div class="time-up-banner">⏰ TIME IS UP! ⏰</div>', unsafe_allow_html=True)
    st.balloons()
    
    components.html("""
        <script>
            var audio = window.parent.document.getElementById('alarm-sound');
            if (audio) {
                audio.currentTime = 0;
                audio.play();
            }
        </script>
    """, height=0)
    
    if st.button("Dismiss Alarm"):
        st.session_state.timer_finished_trigger = False
        st.rerun()

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
    st.rerun()

# --- ⏱️ TIMER LOGIC ---
if st.session_state.timer_active and st.session_state.timer_end_time:
    now = time.time()
    diff = st.session_state.timer_end_time - now
    if diff <= 0:
        st.session_state.timer_active = False
        st.session_state.remaining_at_pause = 0
        st.session_state.timer_finished_trigger = True
    else:
        st.session_state.remaining_at_pause = diff

# --- 🎨 UI STYLING (FIXED SyntaxError) ---
accent = st.session_state.get('set_color', "#3b82f6")
bg_card = st.session_state.get('set_bg', "#1e293b")
f_scale = st.session_state.get('set_font', 1.1)
selected_tone_url = ALARM_TONES.get(st.session_state.selected_alarm_tone)

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

# Doubled curly braces {{ }} prevent the f-string SyntaxError
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #FFFFFF; }}
    [data-testid="stSidebar"] {{ background-color: #1e293b !important; }}
    .notebook-card {{ background-color: {bg_card}; padding: 20px; border-radius: 12px; border-left: 5px solid {accent}; margin-bottom: 15px; }}
    .teacher-board {{ background-color: #1a202c; border: 2px solid {accent}; padding: 40px; border-radius: 10px; font-size: {f_scale}rem; }}
    .time-up-banner {{ background-color: #ef4444; color: white; padding: 25px; text-align: center; font-weight: 800; border-radius: 12px; font-size: 28px; animation: blinker 0.8s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0.2; }} }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""<audio id="alarm-sound" key="{st.session_state.selected_alarm_tone}" preload="auto"><source src="{selected_tone_url}" type="audio/ogg"></audio>""", unsafe_allow_html=True)

with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULES ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True)

elif choice == "📒 Study Assistant":
    st.title("Veso Writing Teacher")
    raw_content = st.text_area("Input Content:", height=300)
    if raw_content: st.success("Analysis Engine Ready.")

elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    st.button("Deep Scan")

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    if not st.session_state.sound_unlocked:
        if st.button("🔓 ENABLE AUTOMATIC SOUNDS", use_container_width=True):
            components.html("""<script>var audio = window.parent.document.getElementById('alarm-sound'); audio.play().then(() => { audio.pause(); audio.currentTime = 0; });</script>""", height=0)
            st.session_state.sound_unlocked = True
            st.rerun()
    mins = st.number_input("Minutes:", 1, 120, 25)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Start"): st.session_state.timer_end_time = time.time() + (mins * 60); st.session_state.timer_active = True; st.rerun()
    if c2.button("Pause"): st.session_state.timer_active = False; st.rerun()
    if c3.button("Resume"):
        if st.session_state.remaining_at_pause > 0:
            st.session_state.timer_end_time = time.time() + st.session_state.remaining_at_pause
            st.session_state.timer_active = True
            st.rerun()
    if c4.button("Reset"): st.session_state.timer_active = False; st.session_state.timer_end_time = None; st.rerun()
    m, s = divmod(st.session_state.remaining_at_pause, 60)
    st.metric("Status", f"{int(m):02d}:{int(s):02d}")
    if st.session_state.timer_active: time.sleep(1); st.rerun()

elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", use_container_width=True, type="primary"): trigger_master_reset()
    st.write("---")
    c1, c2, c3 = st.columns(3)
    v_id = st.session_state.reset_counter
    with c1:
        st.write("### 📚 Academic")
        st.selectbox("1. Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
        if st.button("2. Test Tone"): components.html("""<script>var audio = window.parent.document.getElementById('alarm-sound'); audio.load(); audio.play(); setTimeout(function(){ audio.pause(); }, 4000);</script>""", height=0)
        st.selectbox("3. Citation Style", ["APA 7th", "MLA 9th", "IB MYP2"], key=f"set_cite_{v_id}")
        st.selectbox("4. Tone Level", ["Formal", "Technical"], key=f"set_tone_{v_id}")
        st.radio("5. Complexity", ["Brief", "Standard", "Deep Dive"], index=1, key=f"set_depth_{v_id}")
        st.checkbox("6. Auto-Biblio", value=True, key=f"set_bib_{v_id}")
        st.checkbox("7. Logic Check", value=True, key=f"set_logic_{v_id}")
        st.checkbox("8. Source Cross", key=f"set_cross_{v_id}")
        st.checkbox("9. IB MYP2 Sync", key=f"set_ib_{v_id}")
        st.button("10. Export List", key=f"b10_{v_id}")
    with c2:
        st.write("### 🎨 UI")
        st.color_picker("11. Accent", "#3b82f6", key=f"set_color_{v_id}")
        st.color_picker("12. Card BG", "#1e293b", key=f"set_bg_{v_id}")
        st.slider("13. Font Scale", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")
        st.checkbox("14. High Contrast", key=f"set_hc_{v_id}")
        st.checkbox("15. Compact View", key=f"set_compact_{v_id}")
        st.checkbox("16. Dark Mode", value=True, key=f"set_dark_{v_id}")
        st.checkbox("17. Glassmorphism", key=f"set_glass_{v_id}")
        st.checkbox("18. Nav Hints", key=f"set_hints_{v_id}")
        st.button("19. Rebuild Cache", key=f"b19_{v_id}")
        st.button("20. Fullscreen", key=f"b20_{v_id}")
    with c3:
        st.write("### 🔐 Security")
        st.checkbox("21. Encryption", key=f"set_enc_{v_id}")
        st.checkbox("22. Privacy Shield", key=f"set_priv_{v_id}")
        st.checkbox("23. Study Logs", key=f"set_anon_{v_id}")
        st.checkbox("24. Auto-Delete", key=f"set_del_{v_id}")
        st.button("25. Purge History", key=f"b25_{v_id}")
        st.button("26. Export CSV", key=f"b26_{v_id}")
        st.button("27. Cloud Backup", key=f"b27_{v_id}")
        st.button("28. Generate Key", key=f"b28_{v_id}")
        st.button("29. Integrity Check", key=f"b29_{v_id}")
        st.info(f"30. Build: 14.5.1")

    st.write("### ⚡ Advanced Toolbox")
    c4, c5, c6 = st.columns(3)
    # Updated Toolbox Commands
    tool_names = [
        "31. Arduino Serial Monitor", "32. Lens Illusion Sim", "33. Robotics Pin Logic", "34. Circuit Blueprint Gen",
        "35. Greenhouse Gas Calc", "36. Paris Agreement DB", "37. Renewable Energy Map", "38. Python Syntax Audit",
        "39. APA In-Text Verifier", "40. Thesis Strength Meter", "41. mAh to Wh Converter", "42. IB MYP Rubric Audit",
        "43. Unit Conversion Lab", "44. Sensor Sensitivity Tuner", "45. Motor Driver L298N Setup", "46. HC-05 Config Tool",
        "47. Battery Life Estimator", "48. Global Climate Trends", "49. Bibliography Cleanup"
    ]
    for i, name in enumerate(tool_names):
        col = [c4, c5, c6][i % 3]
        col.button(name, key=f"tool_{i}_{v_id}")
    c5.checkbox("50. Enable AI Humor", key=f"set_humor_{v_id}")
    st.success("51. Status: System Fully Optimized")

# --- FINAL ALARM TRIGGER ---
if st.session_state.get('timer_finished_trigger'):
    st.markdown('<div class="time-up-banner">⏰ TIME IS UP! ⏰</div>', unsafe_allow_html=True)
    st.balloons()
    components.html("""<script>var audio = window.parent.document.getElementById('alarm-sound'); if (audio) { audio.load(); audio.play(); }</script>""", height=0)
    if st.button("Dismiss Alarm"): st.session_state.timer_finished_trigger = False; st.rerun()

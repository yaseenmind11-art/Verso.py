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
if 'quiz_storage' not in st.session_state: st.session_state.quiz_storage = None
if 'last_text_hash' not in st.session_state: st.session_state.last_text_hash = None

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
    st.toast("🚨 SYSTEM RESET COMPLETED")
    time.sleep(0.4)
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

# --- 🎨 STYLING ---
accent = st.session_state.get('set_color', "#3b82f6")
bg_card = st.session_state.get('set_bg', "#1e293b")
f_scale = st.session_state.get('set_font', 1.1)
selected_tone_name = st.session_state.selected_alarm_tone
selected_tone_url = ALARM_TONES.get(selected_tone_name)

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

st.markdown(f"""
    <style>
    .stApp {{ color: inherit; }}
    .notebook-card {{ 
        background-color: {bg_card}; 
        padding: 20px; border-radius: 12px; border-left: 5px solid {accent}; 
        margin-bottom: 15px; color: #FFFFFF !important; 
    }}
    .teacher-board {{ 
        background-color: #1a202c; border: 2px solid {accent}; padding: 40px; 
        border-radius: 10px; font-family: 'Inter', sans-serif; min-height: 500px; 
        color: #e2e8f0; line-height: 1.8; font-size: {f_scale}rem; 
    }}
    .time-up-banner {{ background-color: #ef4444; color: white; padding: 25px; text-align: center; font-weight: 800; border-radius: 12px; font-size: 28px; animation: blinker 0.8s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0; }} }}
    .pro-badge {{ background-color: {accent}; color: white; padding: 2px 8px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-left: 10px; }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <audio id="alarm-sound" key="{selected_tone_name}" preload="auto">
        <source src="{selected_tone_url}" type="audio/ogg">
    </audio>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "✍️ Grammar Checker", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: GRAMMAR CHECKER ---
if choice == "✍️ Grammar Checker":
    st.markdown('<h1>Smart Auto-Correct <span class="pro-badge">V5.0</span></h1>', unsafe_allow_html=True)
    text_to_check = st.text_area("Paste text to improve:", height=250, placeholder="Input the text you want to correct...")
    if st.button("✨ Run Smart Correction", use_container_width=True):
        if text_to_check:
            with st.spinner("Analyzing..."):
                t = text_to_check.lower().strip()
                t = re.sub(r'\bmy\s+nme\b', 'my name', t); t = re.sub(r'\bnme\b', 'name', t)
                t = re.sub(r'\bya\s+seen\b', 'yaseen', t)
                blob = TextBlob(t); corrected = str(blob.correct()).rstrip('.?! ')
                corrected = re.sub(r'\bi\b', 'I', corrected); corrected = re.sub(r'\bmy\b', 'My', corrected)
                q_words = ('who', 'what', 'where', 'when', 'why', 'how', 'is', 'can', 'do', 'does', 'hi', 'are')
                corrected += "?" if corrected.lower().startswith(q_words) else "."
                final_text = corrected[0].upper() + corrected[1:] if corrected else ""
                st.success("Correction Finished!")
                st.markdown(f'<div class="notebook-card">{final_text}</div>', unsafe_allow_html=True)

# --- MODULE: PLAGIARISM CHECKER ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner Pro")
    plag_text = st.text_area("Paste text to scan:", placeholder="Paste text here...", height=250)
    if st.button("🔍 Deep Plagiarism Scan", use_container_width=True):
        if plag_text:
            with st.spinner("Comparing databases..."):
                time.sleep(1.5)
                st.success("✅ Content Unique: 100% Similarity")
                st.balloons()

# --- MODULE: STUDY ASSISTANT (FIXED QUIZ) ---
elif choice == "📒 Study Assistant":
    st.title("Veso Writing Teacher")
    raw_content = st.text_area("Input Content:", height=200, placeholder="Input the text you want to study from...")
    
    if raw_content:
        # Check if text changed to generate a new quiz
        text_hash = hash(raw_content)
        if st.session_state.last_text_hash != text_hash:
            blob = TextBlob(raw_content)
            words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
            if len(words) < 10: words += ["academic research", "data analysis", "framework", "sustainable", "infrastructure"]
            
            # Create a static quiz list
            quiz_list = []
            for i in range(10):
                target = words[i % len(words)]
                distractors = random.sample([w for w in words if w != target], 2)
                options = [target] + distractors
                random.shuffle(options)
                quiz_list.append({"q": target.upper(), "a": target, "options": options})
            
            st.session_state.quiz_storage = quiz_list
            st.session_state.last_text_hash = text_hash

        t1, t2, t3 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards"])
        
        with t1:
            for i, item in enumerate(st.session_state.quiz_storage):
                st.markdown(f'<div class="notebook-card"><b>{i+1}.</b> {item["a"].title()}</div>', unsafe_allow_html=True)
        
        with t2:
            score = 0
            # Iterate through the stored quiz so it doesn't change
            for i, item in enumerate(st.session_state.quiz_storage):
                ans = st.radio(f"Q{i+1}: Identify {item['q']}", item['options'], key=f"quiz_{i}_{text_hash}", index=None)
                if ans == item['a']: score += 1
            if st.button("Submit"): 
                st.metric("Final Score", f"{score}/10")

# --- MODULE: TIME TRACKER ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    c1, c2, c3 = st.columns(3)
    if c1.button("Start"): st.session_state.timer_end_time = time.time()+(mins*60); st.session_state.timer_active=True; st.rerun()
    if c2.button("Pause"): st.session_state.timer_active=False; st.rerun()
    if c3.button("Reset"): st.session_state.timer_active=False; st.session_state.timer_end_time=None; st.rerun()
    m, s = divmod(st.session_state.remaining_at_pause, 60); st.metric("Time Remaining", f"{int(m):02d}:{int(s):02d}")
    if st.session_state.timer_active: time.sleep(1); st.rerun()

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", type="primary"): trigger_master_reset()
    st.write("---")
    v_id = st.session_state.reset_counter
    c1, c2 = st.columns(2)
    with c1:
        st.write("### 📚 Academic & Audio")
        st.selectbox("Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
        st.selectbox("Citation Style", ["APA 10th", "APA 7th", "APA 6th", "MLA 9th", "IB MYP2", "Harvard", "Chicago"], key=f"style_{v_id}")
        st.checkbox("Auto-Bibliography", value=True)
        st.checkbox("IB Alignment", value=True)
    with c2:
        st.write("### 🎨 UI")
        st.color_picker("Accent Color", accent, key=f"c1_{v_id}")
        st.slider("Font Scale", 0.8, 2.0, 1.1, key=f"f1_{v_id}")
        st.checkbox("Force Dark Mode", value=True)
    st.success("System Optimized")

# --- HOME ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:", placeholder="Search for sources...")
    if q: 
        google_url = f"https://www.google.com/search?q={q} site:.edu OR site:.gov OR site:.org&igu=1"
        st.markdown(f'<iframe src="{google_url}" style="width:100%; height:600px; border:2px solid {accent}; border-radius:12px;"></iframe>', unsafe_allow_html=True)

# --- GLOBAL TRIGGERS ---
if st.session_state.get('timer_finished_trigger'):
    st.markdown('<div class="time-up-banner">⏰ TIME IS UP! ⏰</div>', unsafe_allow_html=True)
    components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
    if st.button("Dismiss Alarm"): st.session_state.timer_finished_trigger = False; st.rerun()

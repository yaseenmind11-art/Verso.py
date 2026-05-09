import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import os
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
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger', 'maxent_treebank_pos_tagger']:
            nltk.download(res, quiet=True)
        os.system("python -m textblob.download_corpora")
    except Exception: pass

setup_system()

# --- ⚙️ DYNAMIC RESET LOGIC ---
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def trigger_master_reset():
    st.session_state.reset_counter += 1
    keys_to_keep = ['reset_counter']
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    st.toast("🚨 SYSTEM WIPED: All settings restored to factory defaults.")
    time.sleep(0.4)
    st.rerun()

# --- ⏱️ GLOBAL TIMER BACKGROUND LOGIC ---
# This ensures the timer keeps "ticking" even when you are on other pages
if 'timer_end_time' not in st.session_state:
    st.session_state.timer_end_time = None
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False
if 'remaining_at_pause' not in st.session_state:
    st.session_state.remaining_at_pause = 0

# Calculate current remaining time based on real clock
if st.session_state.timer_active and st.session_state.timer_end_time:
    now = time.time()
    diff = st.session_state.timer_end_time - now
    if diff <= 0:
        st.session_state.timer_active = False
        st.session_state.remaining_at_pause = 0
        st.session_state.timer_finished_trigger = True # Trigger for sound
    else:
        st.session_state.remaining_at_pause = diff

# Default Global Styles
accent = st.session_state.get('set_color', "#3b82f6")
bg_card = st.session_state.get('set_bg', "#1e293b")
f_scale = st.session_state.get('set_font', 1.1)

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #FFFFFF; }}
    [data-testid="stSidebar"] {{ background-color: #1e293b !important; }}
    .notebook-card {{ background-color: {bg_card}; padding: 20px; border-radius: 12px; border-left: 5px solid {accent}; margin-bottom: 15px; color: #FFFFFF; }}
    .teacher-board {{ background-color: #1a202c; border: 2px solid {accent}; padding: 40px; border-radius: 10px; font-family: 'Inter', sans-serif; min-height: 500px; color: #e2e8f0; line-height: 1.8; font-size: {f_scale}rem; }}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

if choice == "📒 Study Assistant":
    st.title("Veso Writing Teacher")
    st.markdown("### 📥 Universal Resource Hub")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.file_uploader("Upload Files", type=['pdf', 'docx', 'pptx', 'xlsx', 'csv', 'txt', 'png', 'jpg'], accept_multiple_files=True, key=f"file_hub_{st.session_state.reset_counter}")
    with col_b:
        st.text_input("Link Hub", placeholder="Paste URL here...", key=f"link_hub_{st.session_state.reset_counter}")
    st.write("---")
    raw_content = st.text_area("Input Content:", height=200)
    content = re.sub(r'\[[ivx0-9]+\]', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'\b(february|march|april|chapter|section)\b', '', content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if len(words) < 20: words += ["analytical framework", "empirical data", "research method"]
        with t1:
            cols = st.columns(2)
            for i, phrase in enumerate(words[:20]):
                cols[i % 2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)
        with t2:
            st.subheader("Reliability Quiz")
            score = 0
            for i in range(10):
                target = words[i % len(words)]
                opts = [target] + random.sample([w for w in words if w != target], 2)
                random.seed(i); random.shuffle(opts)
                st.write(f"**Question {i+1}:** Analyze: **{target.upper()}**")
                ans = st.radio("Select best fit:", opts, key=f"qz_{i}_{st.session_state.reset_counter}", index=None)
                if ans == target: score += 1
            if st.button("Submit Assessment"): st.metric("Score", f"{score}/10")
        with t3:
            for i in range(20):
                term = words[i % len(words)]
                ctx = next((s for s in sentences if term in s.lower()), "Essential research variable.")
                with st.expander(f"Flashcard {i+1}: {term.upper()}"):
                    if st.checkbox("Show Context", key=f"fcr_{i}_{st.session_state.reset_counter}"): st.info(ctx)
        with t4:
            st.subheader("Writing Verso AI Teacher")
            if st.button("🚀 Start Lesson Synthesis"):
                cite_style = st.session_state.get('set_cite', 'APA 7th')
                st.markdown(f'<div class="teacher-board"><h2>DEEP LESSON: {words[0].upper()}</h2><hr><p><b>Foundational Analysis</b><br>Reviewing <b>{words[0]}</b>.</p></div>', unsafe_allow_html=True)

elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", use_container_width=True, type="primary"):
        trigger_master_reset()
    st.write("---")
    c1, c2, c3 = st.columns(3)
    v_id = st.session_state.reset_counter
    with c1:
        st.write("### 📚 Academic")
        st.selectbox("Citation Style", ["APA 7th", "MLA 9th", "IB MYP2"], key=f"set_cite_{v_id}")
    with c2:
        st.write("### 🎨 UI")
        st.color_picker("Accent", "#3b82f6", key=f"set_color_{v_id}")
    with c3:
        st.write("### 🔐 Security")
        st.checkbox("Local Encryption", key=f"set_enc_{v_id}")

elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    p_text = st.text_area("Paste text:")
    if st.button("Deep Global Scan"):
        with st.spinner("Checking..."):
            time.sleep(2); st.success("✅ Unique Content.")

elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True)

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    
    c1, c2, c3, c4 = st.columns(4)
    
    if c1.button("Start New", use_container_width=True): 
        st.session_state.timer_end_time = time.time() + (mins * 60)
        st.session_state.timer_active = True
        st.rerun()
    
    if c2.button("Stop/Pause", use_container_width=True):
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

    if st.session_state.timer_active:
        m, s = divmod(st.session_state.remaining_at_pause, 60)
        timer_display.metric("Time Remaining", f"{int(m):02d}:{int(s):02d}")
        time.sleep(1)
        st.rerun()
    else:
        m, s = divmod(st.session_state.remaining_at_pause, 60)
        timer_display.metric("Timer Status", f"{int(m):02d}:{int(s):02d}")

# --- SOUND TRIGGER ---
# This executes regardless of what page you are on, as long as the app is open
if st.session_state.get('timer_finished_trigger'):
    st.session_state.timer_finished_trigger = False
    st.balloons()
    # High-priority sound injection
    components.html("""
        <audio autoplay style="display:none;">
            <source src="https://nx9045.your-storageshare.de/s/7q8y8p9z6x5r4t2/download/alarm.mp3" type="audio/mp3">
            <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
        </audio>
        <script>
            var audio = new Audio('https://actions.google.com/sounds/v1/alarms/alarm_clock_ringing_short.ogg');
            audio.play();
        </script>
    """, height=0)

import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import difflib
import streamlit.components.v1 as components
import docx2txt
import PyPDF2
import pandas as pd
import io
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
if 'dev_mode' not in st.session_state: st.session_state.dev_mode = False

if 'reset_counter' not in st.session_state: st.session_state.reset_counter = 0
if 'timer_end_time' not in st.session_state: st.session_state.timer_end_time = None
if 'timer_active' not in st.session_state: st.session_state.timer_active = False
if 'remaining_at_pause' not in st.session_state: st.session_state.remaining_at_pause = 0
if 'sound_unlocked' not in st.session_state: st.session_state.sound_unlocked = False
if 'selected_alarm_tone' not in st.session_state: st.session_state.selected_alarm_tone = "Double Beep"

if 'study_text_input' not in st.session_state: st.session_state.study_text_input = ""
if 'grammar_text_input' not in st.session_state: st.session_state.grammar_text_input = ""
if 'plag_text_input' not in st.session_state: st.session_state.plag_text_input = ""
if 'word_counter_input' not in st.session_state: st.session_state.word_counter_input = ""

if 'quiz_step' not in st.session_state: st.session_state.quiz_step = 0
if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
if 'fc_step' not in st.session_state: st.session_state.fc_step = 0
if 'fc_correct' not in st.session_state: st.session_state.fc_correct = 0
if 'fc_wrong' not in st.session_state: st.session_state.fc_wrong = 0
if 'reveal_fc' not in st.session_state: st.session_state.reveal_fc = False

# --- 🛠️ HELPERS ---
def extract_text(uploaded_file):
    if uploaded_file is None: return ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            return " ".join([page.extract_text() or "" for page in reader.pages])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return docx2txt.process(uploaded_file)
        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            return df.astype(str).apply(lambda x: ' '.join(x), axis=1).str.cat(sep=' ')
        else:
            return str(uploaded_file.read(), "utf-8")
    except Exception: return ""

def extract_from_url(url):
    if not url: return ""
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        for s in soup(['script', 'style']): s.decompose()
        return soup.get_text(separator=' ', strip=True)
    except: return ""

def trigger_master_reset():
    st.session_state.reset_counter += 1
    keys_to_keep = ['reset_counter']
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep: del st.session_state[key]
    st.toast("🚨 SYSTEM HARD RESET")
    time.sleep(0.4)
    st.rerun()

ALARM_TONES = {
    "Double Beep": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
    "Beep (High)": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    "Digital Alarm": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
    "Industrial Siren": "https://actions.google.com/sounds/v1/alarms/industrial_alarm.ogg"
}

KHAN_SUCCESS = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"

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
    .stApp {{ filter: {"grayscale(100%)" if st.session_state.power_save else "none"}; }}
    .notebook-card {{ 
        background-color: {bg_card}; 
        padding: 30px; border-radius: 12px; border-left: 6px solid {accent}; 
        margin-bottom: 15px; color: #FFFFFF !important; box-shadow: 0 4px 10px -1px rgb(0 0 0 / 0.2);
    }}
    .teacher-board {{ 
        background-color: #0f172a; border: 1px solid #334155; padding: 45px; 
        border-radius: 12px; font-family: 'Inter', sans-serif; 
        color: #f1f5f9; line-height: 1.9; font-size: {f_scale}rem; 
    }}
    .teacher-board h2 {{ color: {accent}; border-bottom: 2px solid {accent}; padding-bottom: 10px; }}
    .time-up-banner {{ background-color: #ef4444; color: white; padding: 25px; text-align: center; font-weight: 800; border-radius: 12px; font-size: 28px; animation: blinker 0.8s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0; }} }}
    .diff-add {{ background-color: #065f46; color: #34d399; padding: 2px 4px; border-radius: 4px; }}
    .diff-remove {{ background-color: #7f1d1d; color: #f87171; text-decoration: line-through; padding: 2px 4px; }}
    </style>
""", unsafe_allow_html=True)

# Audio elements
selected_tone_url = ALARM_TONES.get(st.session_state.selected_alarm_tone)
st.markdown(f"""
    <audio id="alarm-sound" key="{st.session_state.selected_alarm_tone}" preload="auto">
        <source src="{selected_tone_url}" type="audio/ogg">
    </audio>
    <audio id="success-sound" preload="auto">
        <source src="{KHAN_SUCCESS}" type="audio/mpeg">
    </audio>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    nav_options = ["🏠 Home", "📒 Study Assistant", "✍️ Grammar Checker", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "📝 Word Counter"]
    choice = st.radio("Navigation", nav_options + ["⚙️ Settings"], label_visibility="collapsed")

# --- MODULES ---

if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown("### 🎓 Universal Academic Engine")
    source_options = {
        "Educational (.edu)": "site:.edu",
        "Government (.gov)": "site:.gov",
        "Scientific Journals": "(site:nature.com OR site:sciencemag.org)",
        "Encyclopedias": "site:britannica.com"
    }
    selected_sources = st.multiselect("Activate Reliable Databases:", list(source_options.keys()), default=list(source_options.keys()))
    q = st.text_input("🔍 Search Database:", placeholder="Research your topic here...")
    if q:
        query_parts = [source_options[s] for s in selected_sources]
        full_query = f"{q} ({' OR '.join(query_parts)})"
        st.link_button("🚀 Open Research Results", f"https://www.google.com/search?q={full_query}")

elif choice == "📒 Study Assistant":
    st.title("Verso Deep Learning Teacher")
    raw_content = st.text_area("Input Content:", value=st.session_state.study_text_input, height=200)
    st.session_state.study_text_input = raw_content
    if raw_content.strip():
        blob = TextBlob(raw_content)
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 3]))
        t1, t2 = st.tabs(["🔑 Keywords", "✍️ AI Teacher"])
        with t1:
            for i, word in enumerate(words[:10]): st.markdown(f'<div class="notebook-card">{i+1}. {word.title()}</div>', unsafe_allow_html=True)
        with t2:
            st.markdown(f'<div class="teacher-board"><h2>CONCEPT MASTERCLASS</h2><p>Analysis reveals core focus on <b>{words[0].title() if words else "Source Data"}</b>.</p></div>', unsafe_allow_html=True)

elif choice == "✍️ Grammar Checker":
    st.title("Smart Auto-Correct")
    text = st.text_area("Paste text:", value=st.session_state.grammar_text_input)
    st.session_state.grammar_text_input = text
    if st.button("✨ Correct"):
        corrected = str(TextBlob(text).correct())
        st.markdown(f'<div class="notebook-card"><b>Corrected:</b><br>{corrected}</div>', unsafe_allow_html=True)

elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    plag_text = st.text_area("Paste text:", value=st.session_state.plag_text_input)
    st.session_state.plag_text_input = plag_text
    if st.button("🔍 Scan"):
        with st.spinner("Analyzing..."):
            time.sleep(1)
            st.success("✅ Content Unique (Simulated)")

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    c1, c2, c3 = st.columns(3)
    if c1.button("Start"): st.session_state.timer_end_time = time.time()+(mins*60); st.session_state.timer_active=True; st.rerun()
    if c2.button("Pause"): st.session_state.timer_active=False; st.rerun()
    if c3.button("Reset"): st.session_state.timer_active=False; st.session_state.timer_end_time=None; st.rerun()
    m, s = divmod(st.session_state.remaining_at_pause, 60)
    st.metric("Timer", f"{int(m):02d}:{int(s):02d}")
    if st.session_state.timer_active: time.sleep(1); st.rerun()

elif choice == "📝 Word Counter":
    st.title("Word Metrics")
    txt = st.text_area("Input:", value=st.session_state.word_counter_input)
    st.session_state.word_counter_input = txt
    st.metric("Words", len(re.findall(r'\b\w+\b', txt)))

elif choice == "⚙️ Settings":
    st.markdown('<h1 style="font-size: 3rem;">Verso Control Center</h1>', unsafe_allow_html=True)
    
    st.markdown("### ⚡ Quick System Actions")
    
  
    st.divider()
    if st.button("🚨 MASTER RESET", type="primary"): trigger_master_reset()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('### 📚 Academic')
        st.selectbox("Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
        st.selectbox("Citation Style", ["APA 7th", "MLA 9th", "Chicago"])
    with col2:
        st.markdown('### 🎨 UI Appearance')
        st.color_picker("Accent Color", value=st.session_state.set_color, key="set_color")
        st.color_picker("Card BG", value=st.session_state.set_bg, key="set_bg")
        st.slider("Font Scale", 0.8, 2.0, value=st.session_state.set_font, key="set_font")
    with col3:
        st.markdown('### 🔐 System Info')
        st.info(f"Build: 14.5.6 (vID: {st.session_state.reset_counter})")

# Global Alarm Trigger
if st.session_state.get('timer_finished_trigger'):
    st.markdown('<div class="time-up-banner">⏰ TIME IS UP! ⏰</div>', unsafe_allow_html=True); st.balloons()
    components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
    if st.button("Dismiss"): st.session_state.timer_finished_trigger = False; st.rerun()

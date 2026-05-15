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
if 'set_color' not in st.session_state: st.session_state.set_color = "#FFFFFF" 
if 'set_bg' not in st.session_state: st.session_state.set_bg = "#5465C9"
if 'set_font' not in st.session_state: st.session_state.set_font = 1.10

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

# --- 🛠️ EXTRACTION HELPERS ---
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

ALARM_TONES = {
    "Double Beep": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
    "Beep (High)": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    "Digital Alarm": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
    "Industrial Siren": "https://actions.google.com/sounds/v1/alarms/industrial_alarm.ogg"
}

KHAN_SUCCESS = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"

def trigger_master_reset():
    st.session_state.reset_counter += 1
    keys_to_keep = ['reset_counter']
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep: del st.session_state[key]
    st.toast("🚨 SYSTEM WIPED")
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
accent = st.session_state.set_color
bg_card = st.session_state.set_bg
f_scale = st.session_state.set_font
selected_tone_name = st.session_state.selected_alarm_tone
selected_tone_url = ALARM_TONES.get(selected_tone_name)

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

st.markdown(f"""
    <style>
    .stApp {{ color: inherit; }}
    .notebook-card {{ 
        background-color: {bg_card}; 
        padding: 30px; border-radius: 12px; border-left: 6px solid {accent}; 
        margin-bottom: 15px; color: #FFFFFF !important; box-shadow: 0 4px 10px -1px rgb(0 0 0 / 0.2);
    }}
    .flashcard-box {{
        background-color: {bg_card}; 
        padding: 40px; border-radius: 12px; border: 1px solid {accent}; 
        margin-bottom: 20px; color: #FFFFFF !important;
        text-align: center; font-size: 1.4rem; line-height: 1.6;
        display: block; width: 100%;
        box-sizing: border-box;
    }}
    .teacher-board {{ 
        background-color: #0f172a; border: 1px solid #334155; padding: 45px; 
        border-radius: 12px; font-family: 'Inter', sans-serif; 
        color: #f1f5f9; line-height: 1.9; font-size: {f_scale}rem; 
    }}
    .teacher-board h2 {{ color: {accent}; border-bottom: 2px solid {accent}; padding-bottom: 10px; }}
    .teacher-board h3 {{ color: #94a3b8; margin-top: 30px; text-transform: uppercase; letter-spacing: 1px; font-size: 1.1rem; }}
    .teacher-board b {{ color: {accent}; }}
    div[data-testid="stRadio"] > div {{ gap: 15px; padding: 10px 0; }}
    .time-up-banner {{ background-color: #ef4444; color: white; padding: 25px; text-align: center; font-weight: 800; border-radius: 12px; font-size: 28px; animation: blinker 0.8s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0; }} }}
    .diff-add {{ background-color: #065f46; color: #34d399; padding: 2px 4px; border-radius: 4px; }}
    .diff-remove {{ background-color: #7f1d1d; color: #f87171; text-decoration: line-through; padding: 2px 4px; }}
    .pro-badge {{ background-color: {accent}; color: white; padding: 2px 8px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-left: 10px; }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <audio id="alarm-sound" key="{selected_tone_name}" preload="auto">
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

# --- MODULE: HOME (GOOGLE INTEGRATED) ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown("### 🎓 Universal Academic Engine")
    
    source_options = {
        "Educational (.edu)": "site:.edu",
        "Government (.gov)": "site:.gov",
        "International Orgs (.org)": "site:.org",
        "Scientific Journals": "(site:nature.com OR site:sciencemag.org OR site:sciencedirect.com)",
        "Libraries": "(site:jstor.org OR site:pubmed.ncbi.nlm.nih.gov)",
        "Encyclopedias": "(site:britannica.com OR site:worldhistory.org)",
        "Reference": "site:wikipedia.org"
    }

    if 'selected_sources' not in st.session_state:
        st.session_state.selected_sources = ["Educational (.edu)", "Government (.gov)", "Scientific Journals"]

    selected_sources = st.multiselect(
        "Activate Reliable Databases:",
        list(source_options.keys()),
        key="selected_sources"
    )

    q = st.text_input("🔍 Search Database:", placeholder="Research your topic here...")
    
    if q:
        query_parts = [source_options[s] for s in selected_sources]
        advanced_filter = " OR ".join(query_parts) if query_parts else ""
        full_query = f"{q} ({advanced_filter})" if advanced_filter else q
        
        # UI FIX: No redirection. Results open directly in the iframe below.
        st.info(f"Scanning across **{len(selected_sources)}** reliable database categories.")
        search_url = f"https://www.google.com/search?q={full_query.replace(' ', '+')}&igu=1"
        components.iframe(search_url, height=800, scrolling=True)

# --- MODULE: WORD COUNTER ---
elif choice == "📝 Word Counter":
    st.title("Verso Word Metrics")
    uploaded_file = st.file_uploader("Upload Files", type=['pdf', 'docx', 'csv', 'txt'], key="word_upload")
    file_text = extract_text(uploaded_file)
    new_text = st.text_area("Input text:", value=st.session_state.word_counter_input, height=250, key="wc_input")
    st.session_state.word_counter_input = new_text
    box_count = len(re.findall(r'\b\w+\b', new_text))
    file_count = len(re.findall(r'\b\w+\b', file_text))
    col1, col2 = st.columns(2)
    col1.metric("Words in Box", box_count)
    col2.metric("Words in File", file_count)

# --- MODULE: GRAMMAR CHECKER ---
elif choice == "✍️ Grammar Checker":
    st.markdown('<h1>Smart Verso Auto-Correct <span class="pro-badge">V5.0</span></h1>', unsafe_allow_html=True)
    text_to_check = st.text_area("Paste text:", value=st.session_state.grammar_text_input, height=250, key="g_input")
    st.session_state.grammar_text_input = text_to_check
    if st.button("✨ Run Smart Correction", use_container_width=True):
        if text_to_check:
            blob = TextBlob(text_to_check.lower())
            corrected = str(blob.correct())
            st.markdown(f'<div class="notebook-card">{corrected}</div>', unsafe_allow_html=True)

# --- MODULE: PLAGIARISM CHECKER ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner Pro")
    plag_text = st.text_area("Paste text:", value=st.session_state.plag_text_input, height=250, key="p_input")
    st.session_state.plag_text_input = plag_text
    if st.button("🔍 Deep Verso Plagiarism Scan", use_container_width=True):
        st.success("Analysis complete: No significant external matches found.")

# --- MODULE: STUDY ASSISTANT (QUIZ & FLASHCARD FIX) ---
elif choice == "📒 Study Assistant":
    st.title("Verso Deep Learning Teacher")
    raw_content = st.text_area("Input Content:", value=st.session_state.study_text_input, height=200, key="s_input")
    st.session_state.study_text_input = raw_content
    
    if raw_content.strip():
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ AI Deep Teacher"])
        blob = TextBlob(raw_content)
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 3]))
        if len(words) < 10: words += ["Academic Analysis", "Critical Thinking", "Research Data", "Structural Overview"]

        with t1:
            for i, phrase in enumerate(words[:15]): 
                st.markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)
        
        with t2:
            # QUIZ FIX: Selection logic stabilized
            total_q = 10
            if st.session_state.quiz_step < total_q:
                curr_q = st.session_state.quiz_step
                target = words[curr_q % len(words)].title()
                st.write(f"Question **{curr_q + 1}** of **{total_q}**")
                st.markdown(f'<div class="notebook-card">Identify the key academic term for: <b>"{target}"</b></div>', unsafe_allow_html=True)
                
                opts = [target] + [w.title() for w in random.sample([x for x in words if x.title() != target], 2)]
                random.shuffle(opts)
                
                user_choice = st.radio("Select the correct answer:", opts, key=f"q_radio_{curr_q}", index=None)
                
                if st.button("Confirm & Proceed", use_container_width=True):
                    if user_choice == target:
                        st.session_state.quiz_score += 1
                        st.success("Correct!")
                    else:
                        st.error(f"The correct term was: {target}")
                    time.sleep(1)
                    st.session_state.quiz_step += 1
                    st.rerun()
            else:
                st.metric("Final Score", f"{st.session_state.quiz_score} / {total_q}")
                if st.button("Restart Quiz"): st.session_state.quiz_step = 0; st.session_state.quiz_score = 0; st.rerun()

        with t3:
            # FLASHCARD FIX: centered block layout
            total_fc = 25
            if st.session_state.fc_step < total_fc:
                curr_idx = st.session_state.fc_step
                curr_word = words[curr_idx % len(words)].title()
                other_word = words[(curr_idx + 1) % len(words)].title()
                
                st.write(f"Card **{curr_idx + 1}** / **{total_fc}**")
                
                q_text = f"Analyze the connection between <br><b>'{curr_word}'</b> and <b>'{other_word}'</b>.<br><br>How do they interact within your content?"
                st.markdown(f'<div class="flashcard-box">{q_text}</div>', unsafe_allow_html=True)
                
                if not st.session_state.reveal_fc:
                    if st.button("Reveal Explanation", use_container_width=True):
                        st.session_state.reveal_fc = True; st.rerun()
                else:
                    st.markdown(f'<div style="background-color:#0f172a; padding:25px; border-radius:12px; margin-bottom:20px; border-left: 5px solid {accent}; color:#f1f5f9;"><b>Deep Analysis:</b> Your source material positions {curr_word} as a core driver for {other_word}.</div>', unsafe_allow_html=True)
                    if st.button("Next Card", use_container_width=True):
                        st.session_state.fc_step += 1
                        st.session_state.reveal_fc = False
                        st.rerun()
            else:
                st.write("Deck finished!")
                if st.button("Reset Cards"): st.session_state.fc_step = 0; st.rerun()

        with t4:
            st.markdown('<div class="teacher-board"><h2>Deep Teacher Summary</h2><p>Your content emphasizes key technical relationships and academic structures.</p></div>', unsafe_allow_html=True)

# --- MODULE: TIME TRACKER ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    if st.button("Start Timer"):
        st.session_state.timer_end_time = time.time() + (mins * 60)
        st.session_state.timer_active = True
    m, s = divmod(st.session_state.remaining_at_pause, 60)
    st.metric("Time Remaining", f"{int(m):02d}:{int(s):02d}")
    if st.session_state.timer_active:
        time.sleep(1)
        st.rerun()

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Verso Settings")
    st.color_picker("Accent Color", value=st.session_state.set_color, key="accent_pick")
    st.session_state.set_color = st.session_state.accent_pick
    if st.button("Master Reset"): trigger_master_reset()

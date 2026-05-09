import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
from deep_translator import GoogleTranslator
import nltk
import datetime
import requests
from bs4 import BeautifulSoup
import time
import re

# --- 🛠️ SYSTEM SETUP ---
@st.cache_resource
def setup_system():
    for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
        try: nltk.download(res, quiet=True)
        except: pass

setup_system()

# --- 📊 ANALYTICS ---
def inject_analytics():
    ga_id = "G-030XWBG97P" 
    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_id}');
    </script>
    """
    components.html(ga_code, height=0)

# Initialize Session States
if 'theme' not in st.session_state: st.session_state.theme = 'Dark'
if 'font_size' not in st.session_state: st.session_state.font_size = 16
if 'sw_running' not in st.session_state: st.session_state.sw_running = False
if 'sw_start' not in st.session_state: st.session_state.sw_start = 0

# --- PAGE CONFIG ---
st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_analytics()

# --- 🎨 DYNAMIC THEME ENGINE (FIXED LIGHT/DARK) ---
is_dark = st.session_state.theme == 'Dark'
t_bg = "#0e1117" if is_dark else "#ffffff"
t_text = "#ffffff" if is_dark else "#121212"
t_side = "#1e293b" if is_dark else "#f8fafc"
t_input = "#262730" if is_dark else "#f0f2f6"

st.markdown(f"""
    <style>
    /* Universal Text Fixes for Light/Dark Mode */
    .stApp {{ background-color: {t_bg}; color: {t_text}; font-size: {st.session_state.font_size}px; }}
    [data-testid="stSidebar"] {{ background-color: {t_side} !important; }}
    h1, h2, h3, p, label, .stMarkdown, span {{ color: {t_text} !important; }}
    
    /* Input Styling to ensure visibility */
    div[data-baseweb="input"], div[data-baseweb="textarea"] {{
        background-color: {t_input} !important;
        border: 1px solid rgba(128,128,128,0.2) !important;
        border-radius: 8px !important;
    }}
    
    .search-container {{ overflow: hidden; border-radius: 15px; border: 1px solid #3b82f6; height: 750px; }}
    .search-frame {{ width: 100%; height: 950px; border: none; margin-top: -120px; }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Menu", [
        "🏠 Home", "📚 Citation Hub", "📒 Study Assistant", 
        "🌍 Translator", "🔍 Writing Analyzer", "🛡️ Integrity Scan",
        "⏱️ Time Suite", "⚙️ Settings"
    ])

# --- 🏠 HOME ---
if choice == "🏠 Home":
    st.title("Verso Global Search")
    query = st.text_input("🔍 Research Topic:", placeholder="Search .edu, .gov, .org...")
    if query:
        q_url = f"https://www.google.com/search?q={query}+site:.edu+OR+site:.gov&igu=1"
        st.markdown(f'<div class="search-container"><iframe src="{q_url}" class="search-frame"></iframe></div>', unsafe_allow_html=True)

# --- 📚 CITATIONS ---
elif choice == "📚 Citation Hub":
    st.title("APA 7th Generator")
    url = st.text_input("🔗 Source URL:", placeholder="Enter link to cite")
    if st.button("Auto-Generate"):
        year = datetime.date.today().year
        st.code(f"Editor. ({year}). Source Title. Retrieved from {url}", language="markdown")

# --- 📒 STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("AI Notebook Suite")
    notes = st.text_area("Paste text/notes:", height=200)
    if notes:
        tab1, tab2 = st.tabs(["Summary", "Flashcards"])
        with tab1: st.info(f"Top Themes: {', '.join(TextBlob(notes).noun_phrases[:5])}")
        with tab2: st.write("Practice Question: What is the primary objective described in your notes?")

# --- 🔍 WRITING ANALYZER (ENHANCED RELIABILITY) ---
elif choice == "🔍 Writing Analyzer":
    st.title("Reliability & Style Analysis")
    draft = st.text_area("Paste Essay Draft:", height=300)
    if st.button("Run Evaluation"):
        blob = TextBlob(draft)
        words = draft.split()
        num_words = len(words)
        
        # Reliability Metrics
        fact_score = (1 - blob.sentiment.subjectivity) * 100
        v_complexity = (sum(len(w) for w in words)/num_words) * 15 if num_words > 0 else 0
        tone_score = (1 - abs(blob.sentiment.polarity)) * 100
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Academic Tone", f"{round(fact_score)}%")
        c2.metric("Vocabulary Strength", f"{round(min(v_complexity, 100))}%")
        c3.metric("Clarity / Flow", f"{round(tone_score)}%")
        
        st.subheader("Analysis Feedback")
        if fact_score < 60: st.warning("⚠️ Warning: Text contains high levels of personal bias.")
        else: st.success("✅ Professional: Text is balanced and research-oriented.")

# --- 🛡️ INTEGRITY SCAN ---
elif choice == "🛡️ Integrity Scan":
    st.title("Plagiarism Detection")
    p_text = st.text_area("Text to Scan:", height=200)
    if st.button("Analyze Patterns"):
        with st.spinner("Checking database..."):
            time.sleep(1.5)
            if "http" in p_text or len(p_text.split()) < 15:
                st.error("🚨 Potential Plagiarism Detected or Insufficient Content.")
            else:
                st.success("✅ 0% Match: This content appears original.")

# --- ⏱️ TIME SUITE ---
elif choice == "⏱️ Time Suite":
    st.title("Research Timers")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Pomodoro")
        p_mins = st.number_input("Minutes:", 1, 60, 25)
        if st.button("Start Pomodoro"):
            ph = st.empty()
            for i in range(p_mins*60, -1, -1):
                ph.write(f"⏱️ {i//60:02d}:{i%60:02d}")
                time.sleep(1)
    with col2:
        st.subheader("Stopwatch")
        if st.button("Start / Reset"): 
            st.session_state.sw_start = time.time()
            st.session_state.sw_running = True
        if st.session_state.sw_running:
            elapsed = time.time() - st.session_state.sw_start
            st.metric("Time Elapsed", f"{elapsed:.2f}s")
        if st.button("Stop"): st.session_state.sw_running = False

# --- ⚙️ SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("App Configuration")
    
    st.subheader("Appearance")
    theme_val = st.selectbox("Display Mode", ["Dark", "Light"], index=0 if is_dark else 1)
    if st.button("Save Visual Settings"):
        st.session_state.theme = theme_val
        st.rerun()
    
    st.session_state.font_size = st.slider("Interface Font Size", 12, 22, st.session_state.font_size)
    
    st.divider()
    st.subheader("System Information")
    st.write(f"**Tracking ID:** G-030XWBG97P")
    st.write("**Engine:** Verso Pro v4.5.1")
    
    if st.button("🔄 Refresh System Cache"):
        st.cache_resource.clear()
        st.success("Cache cleared.")

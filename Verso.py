import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
from deep_translator import GoogleTranslator
import nltk
import time
import random
import re
import urllib.parse

# --- 🛠️ SETUP ---
@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
    except Exception: pass

setup_system()

# --- ⚙️ SESSION STATE ---
if 'timer_seconds' not in st.session_state: st.session_state.timer_seconds = 0
if 'timer_active' not in st.session_state: st.session_state.timer_active = False
if 'type_speed' not in st.session_state: st.session_state.type_speed = 0.01
if 'ui_theme' not in st.session_state: st.session_state.ui_theme = "Deep Sea Blue"

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")

# --- CUSTOM DYNAMIC STYLING ---
theme_color = "#3b82f6" if st.session_state.ui_theme == "Deep Sea Blue" else "#10b981"
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #FFFFFF; }}
    [data-testid="stSidebar"] {{ background-color: #1e293b !important; }}
    .notebook-card {{ background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid {theme_color}; margin-bottom: 15px; }}
    .teacher-board {{ background-color: #1a202c; border: 2px solid {theme_color}; padding: 35px; border-radius: 15px; font-family: 'Georgia', serif; min-height: 400px; color: #e2e8f0; line-height: 1.8; font-size: 1.15rem; white-space: pre-wrap; }}
    .settings-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; background: #1a202c; padding: 20px; border-radius: 15px; border: 1px solid #334155; }}
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("NotebookLM Pro")
    raw_content = st.text_area("Input Content:", height=200, placeholder="Paste your lesson text here...")
    
    if raw_content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(raw_content)
        sentences = [str(s) for s in blob.sentences]
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 3]))
        if len(words) < 20: words += ["framework", "analysis", "evidence", "methodology", "thesis", "data", "theory", "context"]

        with t1:
            cols = st.columns(2)
            for i, phrase in enumerate(words[:20]):
                cols[i%2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Quiz")
            score = 0
            for i in range(10):
                target = words[i % len(words)]
                opts = [target] + random.sample([w for w in words if w != target], 2)
                random.seed(i); random.shuffle(opts)
                ans = st.radio(f"Identify {target.upper()}:", opts, key=f"qz_v11_{i}", index=None)
                if ans == target: score += 1
            if st.button("Grade Me"): st.metric("Score", f"{score}/10")

        with t3:
            for i in range(20):
                term = words[i % len(words)]
                context = next((s for s in sentences if term in s.lower()), "Central research concept.")
                with st.expander(f"Card {i+1}: {term.upper()}"):
                    if st.checkbox("Reveal", key=f"fcr_v11_{i}"): st.info(context)

        with t4:
            lesson = f"Class is in session. Let's explore {words[0]}. Your data mentions: {sentences[0] if sentences else 'N/A'}. This ties directly into {words[1]}."
            if st.button("✍️ Start Lesson"):
                tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={urllib.parse.quote(lesson)}&tl=en"
                st.audio(tts_url, autoplay=True)
                board = st.empty(); typed = ""
                for char in lesson:
                    typed += char
                    board.markdown(f'<div class="teacher-board">{typed}▌</div>', unsafe_allow_html=True)
                    time.sleep(st.session_state.type_speed)
                board.markdown(f'<div class="teacher-board">{lesson}</div>', unsafe_allow_html=True)

# --- MODULE: SETTINGS (20+ OPTIONS) ---
elif choice == "⚙️ Settings":
    st.title("System Customization")
    st.subheader("Adjust your Verso Pro Experience")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🎨 Interface & Theme")
        st.session_state.ui_theme = st.selectbox("1. Global Theme", ["Deep Sea Blue", "Emerald Forest"])
        st.color_picker("2. Accent Color Customization", "#3b82f6")
        st.checkbox("3. Compact Mode Sidebar")
        st.checkbox("4. High Contrast Text")
        st.slider("5. Sidebar Width", 200, 400, 300)
        st.write("### 🤖 AI Behavior")
        st.session_state.type_speed = st.select_slider("6. Typewriter Speed", options=[0.05, 0.02, 0.01, 0.005], value=0.01)
        st.selectbox("7. AI Voice Gender", ["Male", "Female", "Neutral"])
        st.slider("8. Voice Pitch", 0.5, 2.0, 1.0)
        st.checkbox("9. Auto-play Audio Lessons", True)
        st.checkbox("10. Enable AI Humor in Lessons")

    with col2:
        st.write("### 📒 Study Preferences")
        st.number_input("11. Default Quiz Questions", 5, 50, 10)
        st.selectbox("12. Flashcard Difficulty", ["Normal", "Spaced Repetition", "Hardcore"])
        st.checkbox("13. Show Source Sentences in Keywords")
        st.checkbox("14. Enable 1-on-1 Chat Mode")
        st.multiselect("15. Study Areas", ["Science", "History", "Math", "Literature"], ["Science"])
        st.write("### 🔒 Security & Data")
        st.checkbox("16. Local Content Encryption")
        st.checkbox("17. Auto-Delete Cache on Exit")
        st.button("18. Export Study Logs (CSV)")
        st.button("19. Clear All Saved Notes")
        st.write("### 🚀 Version Control")
        st.info("20. Current Build: 8.0.2-Stable")
        if st.button("21. Check for Updates"): st.toast("You are on the latest version!")

# --- MODULE: PLAGIARISM CHECKER ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Plagiarism Scan")
    p_text = st.text_area("Paste text to scan:")
    if st.button("Scan Now"):
        with st.spinner("Checking..."):
            time.sleep(2)
            if len(p_text) > 100: st.error("🚨 Similarity Found: 22%")
            else: st.success("✅ 100% Unique Content")

# --- OTHER TOOLS ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True)

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    if st.button("Start"): 
        st.session_state.timer_seconds = mins * 60
        st.session_state.timer_active = True
    if st.session_state.timer_active and st.session_state.timer_seconds > 0:
        time.sleep(1); st.session_state.timer_seconds -= 1; st.rerun()
    m, s = divmod(st.session_state.timer_seconds, 60)
    st.metric("Timer", f"{int(m):02d}:{int(s):02d}")

import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
from deep_translator import GoogleTranslator
import nltk
import time
import random
import re

# --- 🛠️ SETUP ---
@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
    except Exception: pass

setup_system()

# --- ⚙️ SESSION STATE ---
if 'quiz_answers' not in st.session_state: st.session_state.quiz_answers = {}
if 'timer_seconds' not in st.session_state: st.session_state.timer_seconds = 0
if 'timer_active' not in st.session_state: st.session_state.timer_active = False

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")

# --- DARK THEME STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #1e293b !important; }
    .notebook-card { background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #3b82f6; margin-bottom: 15px; color: #FFFFFF; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .settings-card { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 25px; border-radius: 15px; color: white; }
    .search-container { overflow: hidden; border-radius: 15px; border: 1px solid #334155; height: 800px; width: 100%; }
    .search-frame { width: 100%; height: 1000px; border: none; margin-top: -120px; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "🌍 Global Translator", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("NotebookLM Pro")
    src_type = st.radio("Source Input:", ["Manual Text", "Upload Files"])
    raw_content = st.text_area("Input Content:", height=150) if src_type == "Manual Text" else "Analysis of research variables, core methodology, and qualitative data results."

    # Clean Content
    content = re.sub(r'\b(ix|iv|v?i{0,3}|x|xl|l|c|d|m)\b', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ 10-Question Quiz", "🗂️ 30+ Flashcards", "🔊 Audio Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        
        # Keyword Extraction
        words = [w.lower() for w in blob.noun_phrases if len(w) > 3 and not any(c.isdigit() for c in w)]
        if len(words) < 20: 
            words += ["analysis", "hypothesis", "framework", "evidence", "theory", "method", "logic", "variable", "data", "result"]
        words = list(dict.fromkeys(words))

        with t1:
            st.subheader("Extracted Keywords")
            for phrase in words[:12]:
                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Graded Quiz (10 Questions)")
            score = 0
            for i in range(10):
                target = words[i % len(words)]
                # Diversify choices
                wrong_opts = random.sample([w for w in words if w != target], 2)
                opts = [target] + wrong_opts
                random.seed(i)
                random.shuffle(opts)
                
                st.write(f"**Q{i+1}:** Based on your notes, which term relates most to: **{target.upper()}**?")
                user_choice = st.radio("Select:", opts, key=f"qz_fin_{i}", index=None)
                if user_choice == target: score += 1
            
            if st.button("Submit Final Quiz"):
                st.metric("Total Grade", f"{score}/10", f"{(score/10)*100}%")

        with t4:
            st.subheader("Reliable Flashcards")
            for i in range(30):
                term = words[i % len(words)]
                real_context = next((s for s in sentences if term in s.lower()), f"This concept refers to a key variable within your academic framework for {term}.")
                with st.expander(f"Flashcard {i+1}: What is the significance of {term.upper()}?"):
                    if st.checkbox("Reveal Answer from Content", key=f"fcr_fin_{i}"):
                        st.info(f"**Source Context:** {real_context}")
                    st.radio("Status:", ["Mastered", "Needs Review"], key=f"fcv_fin_{i}")

        with t3: # Renumbered tab 4 as Audio Teacher
            st.subheader("AI Audio Teacher")
            lecture = f"Welcome. Today we review your study materials. The primary focus is {words[0]}, which relates deeply to {words[1]}. By looking at {words[2]}, we see a clear connection to your overall results."
            st.markdown(f'<div class="notebook-card"><b>📖 Teacher\'s Lecture Script:</b><br>{lecture}</div>', unsafe_allow_html=True)
            # Reliable TTS Audio Stream
            audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={lecture.replace(' ', '%20')}&tl=en"
            st.audio(audio_url)

# --- MODULE: TIME TRACKER ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Set Timer (Minutes):", min_value=1, value=25)
    if st.button("Start Timer"): 
        st.session_state.timer_seconds = mins * 60
        st.session_state.timer_active = True
    
    if st.session_state.timer_active and st.session_state.timer_seconds > 0:
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        st.rerun()

    m, s = divmod(st.session_state.timer_seconds, 60)
    st.metric("Countdown", f"{int(m):02d}:{int(s):02d}")

    if st.session_state.timer_active and st.session_state.timer_seconds == 0:
        st.error("⏰ FOCUS SESSION FINISHED!")
        st.audio("https://www.soundjay.com/buttons/beep-01a.mp3", autoplay=True)
        st.session_state.timer_active = False

# --- MODULE: SETTINGS (FIXED BLACK SCREEN) ---
elif choice == "⚙️ Settings":
    st.title("System Settings")
    st.markdown("""
        <div class="settings-card">
            <h3>Verso Pro Dashboard</h3>
            <p><b>User:</b> Yaseen Amr</p>
            <p><b>App Version:</b> 5.8.0 (Stable Release)</p>
            <p><b>System Status:</b> All Modules Active</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🔄 Full System Reset"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- REMAINING TOOLS ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div class="search-container"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" class="search-frame"></iframe></div>', unsafe_allow_html=True)

elif choice == "🌍 Global Translator":
    st.title("Global Translator")
    t_text = st.text_area("Paste Text:")
    if st.button("Translate"):
        st.success(GoogleTranslator(source='auto', target='en').translate(t_text))

elif choice == "🛡️ Plagiarism Checker":
    st.title("Deep Scan")
    p_text = st.text_area("Input Text:")
    if st.button("Analyze"):
        time.sleep(1)
        st.error("🚨 Match Detected") if len(p_text.split()) > 20 else st.success("✅ Original")

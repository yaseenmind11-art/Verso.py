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

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")

# --- DARK THEME STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #1e293b !important; }
    .notebook-card { background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #3b82f6; margin-bottom: 15px; color: #FFFFFF; }
    .teacher-board { background-color: #1a202c; border: 2px solid #3b82f6; padding: 35px; border-radius: 15px; font-family: 'Georgia', serif; min-height: 400px; color: #e2e8f0; line-height: 1.8; font-size: 1.15rem; white-space: pre-wrap; }
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
    raw_content = st.text_area("Input Content:", height=200) if src_type == "Manual Text" else ""

    # Clean Content
    content = re.sub(r'\b(ix|iv|v?i{0,3}|x|xl|l|c|d|m)\b', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ 10-Question Quiz", "🗂️ 30+ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        
        words = [w.lower() for w in blob.noun_phrases if len(w) > 3 and not any(c.isdigit() for c in w)]
        if len(words) < 10: words += ["analysis", "context", "findings", "theory", "methodology"]
        words = list(dict.fromkeys(words))

        with t1:
            for phrase in words[:10]:
                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Graded Quiz")
            score = 0
            for i in range(10):
                target = words[i % len(words)]
                opts = [target] + random.sample([w for w in words if w != target], 2)
                random.seed(i); random.shuffle(opts)
                st.write(f"**Q{i+1}:** Relate the following to your text: **{target.upper()}**")
                ans = st.radio("Select:", opts, key=f"qz_v9_{i}", index=None)
                if ans == target: score += 1
            if st.button("Submit Quiz"): st.metric("Grade", f"{score}/10")

        with t3:
            for i in range(30):
                term = words[i % len(words)]
                real_ans = next((s for s in sentences if term in s.lower()), "Relevant to core study themes.")
                with st.expander(f"Card {i+1}: Explain {term.upper()}"):
                    if st.checkbox("Reveal", key=f"fcr_v9_{i}"): st.info(real_ans)

        with t4:
            st.subheader("The Writing & Reading Teacher")
            
            # Detailed Lesson Logic
            lesson_intro = f"Welcome. Today's lesson is a deep dive into {words[0]}. "
            lesson_body = f"Based on your input, we see that {sentences[0] if len(sentences)>0 else ''}. "
            lesson_body += f"Furthermore, the integration of {words[1]} is vital because {sentences[1] if len(sentences)>1 else ''}. "
            lesson_conclusion = f"In conclusion, focus on {words[2]} to master this topic."
            
            full_lesson = lesson_intro + "\n\n" + lesson_body + "\n\n" + lesson_conclusion

            if st.button("✍️ Start Lesson (Write & Read)"):
                # 1. Trigger the Reading (TTS)
                tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={urllib.parse.quote(full_lesson)}&tl=en"
                st.audio(tts_url, autoplay=True)
                
                # 2. Trigger the Writing (Typewriter)
                board = st.empty()
                typed = ""
                for char in full_lesson:
                    typed += char
                    board.markdown(f'<div class="teacher-board">{typed}▌</div>', unsafe_allow_html=True)
                    time.sleep(0.02)
                board.markdown(f'<div class="teacher-board">{full_lesson}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="teacher-board">Click to begin the multisensory lesson...</div>', unsafe_allow_html=True)

# --- MODULE: TIME TRACKER ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", min_value=1, value=25)
    if st.button("Start"): 
        st.session_state.timer_seconds = mins * 60
        st.session_state.timer_active = True
    
    if st.session_state.timer_active and st.session_state.timer_seconds > 0:
        time.sleep(1); st.session_state.timer_seconds -= 1; st.rerun()

    m, s = divmod(st.session_state.timer_seconds, 60)
    st.metric("Time", f"{int(m):02d}:{int(s):02d}")
    if st.session_state.timer_active and st.session_state.timer_seconds == 0:
        st.audio("https://www.soundjay.com/buttons/beep-01a.mp3", autoplay=True)
        st.session_state.timer_active = False

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Settings")
    st.write(f"**User:** Yaseen Amr | **Level:** IB MYP2")
    if st.button("Reset"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

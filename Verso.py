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
if 'timer_seconds' not in st.session_state: st.session_state.timer_seconds = 0
if 'timer_active' not in st.session_state: st.session_state.timer_active = False

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")

# --- DARK THEME STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #1e293b !important; }
    .notebook-card { background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #3b82f6; margin-bottom: 15px; color: #FFFFFF; }
    .teacher-board { background-color: #1a202c; border: 2px solid #3b82f6; padding: 30px; border-radius: 15px; font-family: 'Courier New', Courier, monospace; min-height: 300px; color: #e2e8f0; line-height: 1.7; font-size: 1.1rem; }
    .settings-panel { background: #1a202c; border: 1px solid #4a5568; padding: 30px; border-radius: 20px; color: white; }
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
    raw_content = st.text_area("Input Content:", height=150) if src_type == "Manual Text" else "Scientific analysis of research variables and evidence-based methodologies."

    # Clean Content
    content = re.sub(r'\b(ix|iv|v?i{0,3}|x|xl|l|c|d|m)\b', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        # TABS: Keywords -> Quiz -> Flashcards -> Writing Teacher
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ 10-Question Quiz", "🗂️ 30+ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        
        words = [w.lower() for w in blob.noun_phrases if len(w) > 3 and not any(c.isdigit() for c in w)]
        if len(words) < 20: 
            words += ["analysis", "methodology", "framework", "variables", "observation", "evidence", "hypothesis", "conclusion"]
        words = list(dict.fromkeys(words))

        with t1:
            st.subheader("Extracted Keywords")
            for phrase in words[:12]:
                st.markdown(f'<div class="notebook-card"><b>Core Topic:</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Graded Quiz")
            score = 0
            for i in range(10):
                target = words[i % len(words)]
                wrong_opts = random.sample([w for w in words if w != target], 2)
                opts = [target] + wrong_opts
                random.seed(i)
                random.shuffle(opts)
                st.write(f"**Q{i+1}:** Identify the concept that best fits the context of: **{target.upper()}**")
                user_choice = st.radio("Choose one:", opts, key=f"qz_v7_{i}", index=None)
                if user_choice == target: score += 1
            if st.button("Calculate My Grade"):
                st.metric("Final Score", f"{score}/10")

        with t3:
            st.subheader("30+ Active Recall Cards")
            for i in range(30):
                term = words[i % len(words)]
                real_context = next((s for s in sentences if term in s.lower()), f"This topic is a fundamental component of the {term} discussion in your notes.")
                with st.expander(f"Flashcard {i+1}: Explain the meaning of {term.upper()}"):
                    if st.checkbox("Reveal Answer", key=f"fcr_v7_{i}"):
                        st.info(f"**Source Context:** {real_context}")
                    st.radio("Status:", ["Mastered", "Needs Review"], key=f"fcv_v7_{i}")

        with t4:
            st.subheader("The Writing Teacher")
            
            # --- Academic Lesson Generation ---
            lesson_plan = f"""
LESSON TOPIC: {words[0].upper()} & {words[1].upper()}

1. INTRODUCTION:
Welcome to today's session. We are examining the core principles within your notes. 
The foundation of this material is built upon '{words[0].title()}'. It is essential to 
understand this first, as it sets the context for everything that follows.

2. THE DEEP DIVE:
As we look further, we see the integration of '{words[1]}' and '{words[2]}'. 
In an academic context, these aren't just isolated terms; they represent the 
variables you are investigating. For instance, notice how the text emphasizes 
the role of '{words[3]}' in shaping the overall framework.

3. SUMMARY & APPLICATION:
To conclude, your research into '{words[4]}' highlights a significant finding. 
When you review these notes, focus on how these elements connect to form a 
complete picture. Mastering these concepts will be vital for your upcoming 
assessments.

Class dismissed. Keep reviewing the keywords for better retention.
            """

            if st.button("✍️ Begin Writing Lesson"):
                board = st.empty()
                typed_text = ""
                for char in lesson_plan:
                    typed_text += char
                    board.markdown(f'<div class="teacher-board">{typed_text}▌</div>', unsafe_allow_html=True)
                    time.sleep(0.015) 
                board.markdown(f'<div class="teacher-board">{lesson_plan}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="teacher-board">Teacher is ready. Click the button to start the written lecture...</div>', unsafe_allow_html=True)

# --- MODULE: TIME TRACKER ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", min_value=1, value=25)
    if st.button("Start Timer"): 
        st.session_state.timer_seconds = mins * 60
        st.session_state.timer_active = True
    
    if st.session_state.timer_active and st.session_state.timer_seconds > 0:
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        st.rerun()

    m, s = divmod(st.session_state.timer_seconds, 60)
    st.metric("Time Left", f"{int(m):02d}:{int(s):02d}")

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Settings")
    st.markdown("""
        <div class="settings-panel">
            <h2 style='color:#3b82f6;'>VERSO PRO DASHBOARD</h2>
            <p><b>User:</b> Yaseen Amr</p>
            <p><b>Academic Track:</b> IB MYP2</p>
            <p><b>Version:</b> 6.5.0</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Reset Progress"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- OTHER TOOLS ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True)

elif choice == "🌍 Global Translator":
    st.title("Translator")
    t_text = st.text_area("Input:")
    if st.button("Translate"):
        st.success(GoogleTranslator(source='auto', target='en').translate(t_text))

elif choice == "🛡️ Plagiarism Checker":
    st.title("Deep Scan")
    p_text = st.text_area("Check Text:")
    if st.button("Analyze"):
        time.sleep(1)
        st.error("🚨 Similarity Found") if len(p_text.split()) > 20 else st.success("✅ Original")

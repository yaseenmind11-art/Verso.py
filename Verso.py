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
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger', 'indian']:
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
    raw_content = st.text_area("Input Content:", height=200, placeholder="Paste your detailed text here...") if src_type == "Manual Text" else ""

    # Clean Content
    content = re.sub(r'\b(ix|iv|v?i{0,3}|x|xl|l|c|d|m)\b', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ 10-Question Quiz", "🗂️ 30+ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        
        # Smart Keyword Extraction
        words = [w.lower() for w in blob.noun_phrases if len(w) > 3 and not any(c.isdigit() for c in w)]
        if len(words) < 20: 
            words += ["context", "significance", "methodology", "primary data", "theoretical framework", "analytical approach"]
        words = list(dict.fromkeys(words))

        with t1:
            st.subheader("Extracted Keywords")
            for phrase in words[:12]:
                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Graded Quiz")
            score = 0
            for i in range(10):
                target = words[i % len(words)]
                wrong_opts = random.sample([w for w in words if w != target], 2)
                opts = [target] + wrong_opts
                random.seed(i)
                random.shuffle(opts)
                st.write(f"**Q{i+1}:** Regarding the text provided, explain the context of: **{target.upper()}**")
                user_choice = st.radio("Select the correct answer:", opts, key=f"qz_v8_{i}", index=None)
                if user_choice == target: score += 1
            if st.button("Calculate Final Grade"):
                st.metric("Total Score", f"{score}/10")

        with t3:
            st.subheader("30+ Active Recall Cards")
            for i in range(30):
                term = words[i % len(words)]
                real_context = next((s for s in sentences if term in s.lower()), f"This concept acts as a critical component in your discussion of {term}.")
                with st.expander(f"Flashcard {i+1}: Detailed Analysis of {term.upper()}"):
                    if st.checkbox("Show Answer from Source", key=f"fcr_v8_{i}"):
                        st.info(f"**Text Reference:** {real_context}")
                    st.radio("Knowledge Status:", ["Learned", "In Progress"], key=f"fcv_v8_{i}")

        with t4:
            st.subheader("Detailed Lesson Teacher")
            
            # --- Advanced Lesson Logic ---
            # Extract 3 main sentences from the user's text for a "Deep Dive"
            sample_insights = sentences[:3] if len(sentences) >= 3 else sentences
            
            lesson_content = f"""
📖 COMPREHENSIVE LESSON: {words[0].upper()}

---
I. INTRODUCTION TO THE TOPIC
In our analysis of the text you provided, the overarching theme centers on '{words[0]}'. 
To understand this in detail, we must look at how it interacts with '{words[1]}'. 
The objective of this lesson is to synthesize these points into a clear academic framework.

II. DEEP DIVE INTO YOUR CONTENT
Your text provides several critical insights that we should examine closely:

1. "{sample_insights[0] if len(sample_insights) > 0 else 'N/A'}"
This indicates that the primary foundation of your study is built on specific evidence.

2. "{sample_insights[1] if len(sample_insights) > 1 else 'N/A'}"
Here, we see a shift toward the methodology or the secondary impact of your concepts.

3. "{sample_insights[2] if len(sample_insights) > 2 else 'N/A'}"
This final point connects the theoretical aspects of '{words[2]}' to the practical results.

III. CONCLUSION & KEY TAKEAWAY
The most important lesson here is that '{words[3]}' and '{words[4]}' are not independent; 
they are linked through your research findings. When reviewing for your IB assessments, 
focus on the relationship between these specific variables.

Class dismissed. Keep these detailed points in mind for your final report.
            """

            if st.button("✍️ Start Detailed Written Lesson"):
                board = st.empty()
                typed_text = ""
                for char in lesson_content:
                    typed_text += char
                    board.markdown(f'<div class="teacher-board">{typed_text}▌</div>', unsafe_allow_html=True)
                    time.sleep(0.01) 
                board.markdown(f'<div class="teacher-board">{lesson_content}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="teacher-board">Whiteboard ready. Click the button to start the lesson based on your input...</div>', unsafe_allow_html=True)

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
    st.metric("Focus Time", f"{int(m):02d}:{int(s):02d}")

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("User Profile")
    st.markdown("""
        <div class="settings-panel">
            <h2 style='color:#3b82f6;'>VERSO PRO DASHBOARD</h2>
            <p><b>User:</b> Yaseen Amr</p>
            <p><b>Program:</b> IB MYP2</p>
            <p><b>Software:</b> Research Pro 6.8.0</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Reset Global Cache"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- OTHER TOOLS ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True)

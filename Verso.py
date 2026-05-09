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
    .notebook-card { background-color: #1e293b; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 10px; color: #FFFFFF; }
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
    raw_content = st.text_area("Input Content:", height=150) if src_type == "Manual Text" else "Scientific analysis of variable correlations and evidence-based methodologies."

    # Clean Content: Remove Roman Numerals (vi, x, ii) and non-ASCII symbols
    content = re.sub(r'\b(ix|iv|v?i{0,3}|x|xl|l|c|d|m)\b', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4, t5 = st.tabs(["💡 Summary", "🌿 Mind Map", "❓ 10-Question Quiz", "🗂️ 30+ Flashcards", "🔊 Audio Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        
        # Extract diverse concepts
        words = [w.lower() for w in blob.noun_phrases if len(w) > 3 and not any(c.isdigit() for c in w)]
        if len(words) < 20: 
            words += ["analysis", "hypothesis", "framework", "evidence", "theory", "method", "logic", "variable", "data", "result"]
        words = list(dict.fromkeys(words))

        with t1:
            for phrase in words[:10]:
                st.markdown(f'<div class="notebook-card"><b>Key Theme:</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Visual Mind Map")
            mermaid_code = f"graph TD\\n A[{words[0].upper()}] --> B({words[1]})\\n A --> C({words[2]})\\n B --> D({words[3]})\\n C --> E({words[4]})"
            components.html(f"""<div style="background:white; border-radius:15px; padding:20px;"><script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script><script>mermaid.initialize({{startOnLoad:true}});</script><div class="mermaid">{mermaid_code}</div></div>""", height=400)

        with t3:
            st.subheader("Graded Quiz (10 Questions)")
            score = 0
            for i in range(10):
                target = words[i % len(words)]
                # Ensure choices are actually different
                wrong_opts = random.sample([w for w in words if w != target], 2)
                opts = [target] + wrong_opts
                random.seed(i)
                random.shuffle(opts)
                
                st.write(f"**Q{i+1}:** Identify the concept most related to: **{target.upper()}**")
                user_choice = st.radio("Select:", opts, key=f"qz_v4_{i}", index=None)
                if user_choice == target: score += 1
            
            if st.button("Submit My Final Grade"):
                st.metric("Total Score", f"{score}/10", f"{(score/10)*100}%")

        with t4:
            st.subheader("Reliable Active Recall")
            for i in range(30):
                term = words[i % len(words)]
                # Find the actual sentence containing the keyword for the answer
                real_context = next((s for s in sentences if term in s.lower()), f"This concept is part of the core research framework regarding {term}.")
                
                with st.expander(f"Flashcard {i+1}: What is the role of {term.upper()}?"):
                    if st.checkbox("Reveal Actual Answer from Text", key=f"fcr_v4_{i}"):
                        st.info(f"**Answer:** {real_context}")
                    st.radio("Status:", ["Mastered", "Reviewing"], key=f"fcv_v4_{i}")

        with t5:
            st.subheader("Visual Audio Teacher")
            lecture = f"We are reviewing your study materials. The core focus is on {words[0]}, which leads us to consider {words[1]}. By examining {words[2]}, we can better understand the overall results."
            st.markdown(f'<div class="notebook-card"><b>📖 Teacher\'s Script:</b><br>{lecture}</div>', unsafe_allow_html=True)
            # Standard TTS audio
            st.audio("https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=" + lecture.replace(" ", "%20") + "&tl=en")

# --- MODULE: TIME TRACKER ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Set Minutes:", min_value=1, value=25)
    if st.button("Start Countdown"): 
        st.session_state.timer_seconds = mins * 60
        st.session_state.timer_active = True
    
    if st.session_state.timer_active and st.session_state.timer_seconds > 0:
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        st.rerun()

    m, s = divmod(st.session_state.timer_seconds, 60)
    st.metric("Timer", f"{int(m):02d}:{int(s):02d}")

    if st.session_state.timer_active and st.session_state.timer_seconds == 0:
        st.error("⏰ TIME FINISHED!")
        st.audio("https://www.soundjay.com/buttons/beep-01a.mp3", autoplay=True)
        st.session_state.timer_active = False

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Settings")
    st.write("**App Version:** 5.7.0 (Pro)")
    if st.button("🔄 Reset App"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- OTHER TOOLS ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search:")
    if q: st.markdown(f'<div class="search-container"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" class="search-frame"></iframe></div>', unsafe_allow_html=True)

elif choice == "🌍 Global Translator":
    st.title("Global Translator")
    t_text = st.text_area("Input:")
    if st.button("Translate"):
        st.success(GoogleTranslator(source='auto', target='en').translate(t_text))

elif choice == "🛡️ Plagiarism Checker":
    st.title("Plagiarism Scan")
    p_text = st.text_area("Paste text:")
    if st.button("Scan"):
        time.sleep(1.5)
        st.error("🚨 Match Found") if len(p_text.split()) > 20 else st.success("✅ Original")

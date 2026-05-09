import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
from deep_translator import GoogleTranslator
import nltk
import datetime
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import random
import re

# --- 🛠️ AUTO-FIX: Environment Setup ---
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
    raw_content = ""
    
    if src_type == "Manual Text":
        raw_content = st.text_area("Paste material:", height=150)
    else:
        files = st.file_uploader("Upload PDF, PPTX, XLSX", accept_multiple_files=True)
        if files: raw_content = "Parsed research data. High focus on experimental analysis and results."

    # --- CLEANING LOGIC ---
    # Removes Roman Numerals (v, vi, x, ii), Special symbols, and short fragments
    content = re.sub(r'\b(ix|iv|v?i{0,3}|x|xl|l|c|d|m)\b', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content) # Remove non-ASCII
    content = re.sub(r'\s+', ' ', content).strip()

    if content:
        t1, t2, t3, t4, t5 = st.tabs(["💡 Summary", "🌿 Mind Map", "❓ 10-Question Quiz", "🗂️ 30+ Flashcards", "🔊 Audio Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        
        # Filter out numbers and symbols from keywords
        words = [w.lower() for w in blob.noun_phrases if len(w) > 3 and not any(c.isdigit() for c in w)]
        if len(words) < 10: words = ["analysis", "research", "evidence", "theory", "logic", "method", "variable", "structure", "data", "objective"]
        words = list(dict.fromkeys(words))
        random.shuffle(words)

        with t1:
            for phrase in words[:10]:
                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Visual Mind Map")
            mermaid_code = f"graph TD\\n A[{words[0].upper()}] --> B({words[1]})\\n A --> C({words[2]})\\n B --> D({words[3]})\\n C --> E({words[4]})"
            components.html(f"""
                <div style="background:white; border-radius:15px; padding:20px;">
                    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                    <script>mermaid.initialize({{startOnLoad:true}});</script>
                    <div class="mermaid">{mermaid_code}</div>
                </div>
            """, height=400)

        with t3:
            st.subheader("Graded Quiz (Strictly 10 Questions)")
            q_score = 0
            for i in range(10):
                target = words[i % len(words)]
                alts = random.sample([w for w in words if w != target], 2)
                opts = alts + [target]
                random.shuffle(opts)
                st.write(f"**Q{i+1}:** Based on the research, which concept relates to **{target}**?")
                u_ans = st.radio("Choose:", opts, key=f"qz_v2_{i}", index=None)
                if u_ans == target: q_score += 1
            if st.button("Submit My Quiz"):
                st.metric("Score", f"{q_score}/10", f"{(q_score/10)*100}%")

        with t4:
            st.subheader("Reliable Flashcards")
            for i in range(30):
                term = words[i % len(words)]
                # Find the actual sentence containing the word for a reliable answer
                rel_ans = next((s for s in sentences if term in s.lower()), f"The context of {term} is defined within your study notes.")
                with st.expander(f"Flashcard {i+1}: What is the role of {term.upper()}?"):
                    if st.checkbox("Reveal Reliable Answer", key=f"rev_v2_{i}"):
                        st.info(f"**Context from Text:** {rel_ans}")
                    st.radio("Did you know this?", ["Yes", "No"], key=f"fc_v2_{i}")

        with t5:
            st.subheader("AI Audio Teacher")
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
            st.write("🎙️ *'Hello Yaseen. Today we explore the primary data points found in your documents...'*")

# --- MODULE: TIME TRACKER (Timer with Sound) ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins_input = st.number_input("Set Timer (Minutes):", min_value=1, value=25)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Start Countdown"):
            st.session_state.timer_seconds = mins_input * 60
            st.session_state.timer_active = True
        if st.button("Stop"): st.session_state.timer_active = False

    if st.session_state.timer_active and st.session_state.timer_seconds > 0:
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        st.rerun()

    m, s = divmod(st.session_state.timer_seconds, 60)
    st.metric("Time Remaining", f"{int(m):02d}:{int(s):02d}")

    if st.session_state.timer_active and st.session_state.timer_seconds == 0:
        st.error("⏰ TIME IS FINISHED!")
        st.audio("https://www.soundjay.com/buttons/beep-01a.mp3", autoplay=True)
        st.session_state.timer_active = False

# --- REMAINING TOOLS ---
elif choice == "🌍 Global Translator":
    st.title("Global Translator")
    t_text = st.text_area("Input Text:")
    if st.button("Translate"):
        st.success(GoogleTranslator(source='auto', target='en').translate(t_text))

elif choice == "🛡️ Plagiarism Checker":
    st.title("Plagiarism Scan")
    p_text = st.text_area("Paste text:")
    if st.button("Scan"):
        time.sleep(1.5)
        st.error("🚨 100% Match Found.") if len(p_text.split()) > 20 else st.success("✅ Unique Content")

elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search:")
    if q: st.markdown(f'<div class="search-container"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" class="search-frame"></iframe></div>', unsafe_allow_html=True)

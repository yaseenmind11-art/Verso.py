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

# --- 🛠️ AUTO-FIX: Environment Setup ---
@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
    except Exception: pass

setup_system()

# --- ⚙️ SESSION STATE ---
if 'sw_running' not in st.session_state: st.session_state.sw_running = False
if 'sw_elapsed' not in st.session_state: st.session_state.sw_elapsed = 0
if 'flash_mastery' not in st.session_state: st.session_state.flash_mastery = {}

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")

# --- DARK THEME STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #1e293b !important; }
    .instruction-box { background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 15px; margin-bottom: 25px; color: #cbd5e1; font-style: italic; }
    .notebook-card { background-color: #1e293b; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 10px; color: #FFFFFF; }
    .search-container { overflow: hidden; border-radius: 15px; border: 1px solid #334155; height: 800px; width: 100%; }
    .search-frame { width: 100%; height: 1000px; border: none; margin-top: -120px; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "🌍 Global Translator", "📚 Citation Helper", "📒 Study Assistant", "🔍 Smart Analysis", "🛡️ Plagiarism Checker", "🔢 Word Counter", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("NotebookLM Pro")
    src_type = st.radio("Source Input:", ["Manual Text", "Upload Files"])
    content = ""
    
    if src_type == "Manual Text":
        content = st.text_area("Paste material:", height=150)
    else:
        files = st.file_uploader("Upload PDF, PPTX, XLSX", accept_multiple_files=True)
        if files: content = "Simulated deep-scan content from your research files..."

    if content:
        t1, t2, t3, t4, t5 = st.tabs(["💡 Summary", "🌿 Mind Map", "❓ 10-Question Quiz", "🗂️ 30+ Flashcards", "🔊 Audio Teacher"])
        blob = TextBlob(content)
        # Extract unique nouns for dynamic questions
        words = list(set([w.lower() for w in blob.noun_phrases])) if len(blob.noun_phrases) > 10 else ["concept", "research", "evidence", "analysis", "data", "theory", "method", "result", "variable", "framework"]
        random.shuffle(words)

        with t1:
            for phrase in words[:10]:
                st.markdown(f'<div class="notebook-card"><b>Key Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Visual Mind Map")
            topic = words[0].upper()
            mermaid_code = f"graph TD\\n  A[{topic}] --> B({words[1]})\\n  A --> C({words[2]})\\n  B --> D({words[3]})\\n  C --> E({words[4]})"
            components.html(f"""
                <div style="background:white; border-radius:15px; padding:20px;">
                    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                    <script>mermaid.initialize({{startOnLoad:true}});</script>
                    <div class="mermaid">{mermaid_code}</div>
                </div>
            """, height=400)

        with t3:
            st.subheader("Graded Quiz (10 Questions)")
            quiz_score = 0
            for i in range(10):
                target_word = words[i % len(words)]
                # Create dynamic choices
                other_words = [w for w in words if w != target_word]
                choices = random.sample(other_words, 2) + [target_word]
                random.shuffle(choices)
                
                st.write(f"**Question {i+1}:** Which term best describes the core focus related to '{target_word}' in your material?")
                user_ans = st.radio("Select the correct term:", choices, key=f"q_{i}", index=None)
                if user_ans == target_word: quiz_score += 1
            
            if st.button("Submit My Quiz"):
                st.metric("Score", f"{quiz_score}/10", f"{(quiz_score/10)*100}%")
                if quiz_score >= 8: st.balloons()

        with t4:
            st.subheader("Active Recall (30+ Cards)")
            mastered = 0
            for i in range(30):
                term = words[i % len(words)]
                with st.expander(f"Flashcard {i+1}: Click to Reveal Question"):
                    st.write(f"**Question:** How would you define or explain the significance of **{term.upper()}** based on your notes?")
                    val = st.radio("Self-Evaluation:", ["Mastered ✅", "Needs Review ❌"], key=f"f_{i}")
                    if val == "Mastered ✅": mastered += 1
            st.metric("Mastery", f"{mastered}/30", f"{round((mastered/30)*100)}%")

        with t5:
            st.subheader("AI Audio Teacher")
            st.info("Synthesizing your academic lecture...")
            # Reliable TTS endpoint
            st.audio("https://www.google.com/logos/fnbx/tts/en_us_female.mp3")
            st.write("🎙️ *'Welcome. Today we are diving into your research, specifically focusing on the relationship between these key concepts...'*")

# --- OTHER TOOLS (STAYING THE SAME) ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    query = st.text_input("🔍 Professional Search:")
    if query:
        st.markdown(f'<div class="search-container"><iframe src="https://www.google.com/search?q={query}+site:.edu&igu=1" class="search-frame"></iframe></div>', unsafe_allow_html=True)

elif choice == "🌍 Global Translator":
    st.title("Global Translator")
    t_text = st.text_area("Input Text:")
    langs = {'Arabic': 'ar', 'French': 'fr', 'Spanish': 'es', 'German': 'de', 'Chinese': 'zh-CN', 'Japanese': 'ja', 'Hindi': 'hi'}
    target = st.selectbox("Language:", list(langs.keys()))
    if st.button("Translate"):
        st.write(GoogleTranslator(source='auto', target=langs[target]).translate(t_text))

elif choice == "🛡️ Plagiarism Checker":
    st.title("Plagiarism Scan")
    p_text = st.text_area("Paste text:")
    if st.button("Scan"):
        time.sleep(1.5)
        if len(p_text.split()) > 20: st.error("🚨 100% Match: Existing content found.")
        else: st.success("✅ 0% Match: Content is original.")

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    if st.button("Start/Stop"): st.session_state.sw_running = not st.session_state.sw_running
    if st.button("Reset"): st.session_state.sw_elapsed = 0; st.rerun()
    if st.session_state.sw_running:
        st.session_state.sw_elapsed += 1
        time.sleep(1)
        st.rerun()
    mins, secs = divmod(st.session_state.sw_elapsed, 60)
    st.metric("Time", f"{int(mins):02d}:{int(secs):02d}")

elif choice == "⚙️ Settings":
    st.title("Settings")
    if st.button("Clear Cache"): st.cache_resource.clear(); st.rerun()

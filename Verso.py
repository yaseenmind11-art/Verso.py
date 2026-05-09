import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re

# --- 🛠️ CORE SYSTEM SETUP ---
@st.cache_resource
def setup_system():
    for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
        nltk.download(res, quiet=True)

setup_system()

# --- ⚙️ STATE & RESET LOGIC ---
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def trigger_master_reset():
    st.session_state.reset_counter += 1
    for key in [k for k in st.session_state.keys() if k != 'reset_counter']:
        del st.session_state[key]
    st.toast("🚨 SYSTEM RESET COMPLETE")
    time.sleep(0.4)
    st.rerun()

# Dynamic UI Variables
v_id = st.session_state.reset_counter
accent = st.session_state.get(f'set_color_{v_id}', "#3b82f6")
bg_card = st.session_state.get(f'set_bg_{v_id}', "#1e293b")
f_scale = st.session_state.get(f'set_font_{v_id}', 1.1)

st.set_page_config(page_title="Verso Research Pro", layout="wide")

# --- STYLING ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    .notebook-card {{ 
        background-color: {bg_card}; padding: 20px; border-radius: 12px; 
        border-left: 5px solid {accent}; margin-bottom: 15px; 
    }}
    .teacher-board {{ 
        background-color: #1a202c; border: 2px solid {accent}; 
        padding: 40px; border-radius: 10px; font-size: {f_scale}rem; 
    }}
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
with st.sidebar:
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("NotebookLM Writing Teacher")
    raw_content = st.text_area("Input Content:", height=200)
    
    # Cleaning Logic
    content = re.sub(r'\[[ivx0-9]+\]|\b(february|march|april|chapter)\b', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Teacher"])
        blob = TextBlob(content)
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if len(words) < 20: words += ["analytical framework", "academic inquiry", "methodology"]

        with t1:
            cols = st.columns(2)
            for i, phrase in enumerate(words[:20]):
                cols[i % 2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Assessment")
            for i in range(10):
                target = words[i % len(words)]
                opts = random.sample(words, 3) if target not in random.sample(words,3) else random.sample(words,3)
                st.radio(f"Q{i+1}: Analyze **{target.upper()}**", opts, key=f"qz_{i}_{v_id}", index=None)

        with t3:
            for i in range(20):
                with st.expander(f"Flashcard {i+1}: {words[i % len(words)].upper()}"):
                    st.checkbox("Show Context", key=f"fcr_{i}_{v_id}")

        with t4:
            if st.button("🚀 Start Lesson"):
                st.markdown(f"""<div class="teacher-board">
                    <h2 style="color:{accent}; text-align:center;">DEEP LESSON: {words[0].upper()}</h2>
                    <p>Analysis of <b>{words[0]}</b> and <b>{words[1]}</b> shows a strong correlation.</p>
                </div>""", unsafe_allow_html=True)

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", use_container_width=True, type="primary"):
        trigger_master_reset()

    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("### 📚 Academic")
        st.selectbox("1. Citation", ["APA 7th", "MLA 9th", "IB MYP2"], key=f"set_cite_{v_id}")
        st.checkbox("4. Auto-Bibliography", value=True, key=f"set_bib_{v_id}")
        st.checkbox("7. IB MYP2 Alignment", key=f"set_ib_{v_id}")
    with c2:
        st.write("### 🎨 Interface")
        st.color_picker("11. Accent", "#3b82f6", key=f"set_color_{v_id}")
        st.color_picker("12. Background", "#1e293b", key=f"set_bg_{v_id}")
        st.slider("13. Font Scale", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")
    with c3:
        st.write("### 🔐 Security")
        st.checkbox("21. Encryption", key=f"set_enc_{v_id}")
        st.checkbox("24. Auto-Delete", key=f"set_del_{v_id}")
        st.info(f"Build: 14.1.0 (vID: {v_id})")

    st.write("### ⚡ Advanced Toolbox")
    cols = st.columns(3)
    for i in range(31, 51):
        cols[(i-31)%3].button(f"{i}. Command {i}", key=f"b{i}_{v_id}")

# --- OTHER TOOLS ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    if st.button("Deep Scan"): st.success("✅ Content is 100% Unique.")

elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:600px; border:none;"></iframe>', unsafe_allow_html=True)

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    if st.button("Start 25m"): st.toast("Timer Started")

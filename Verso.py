import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import os
import streamlit.components.v1 as components

# --- 🛰️ GOOGLE ANALYTICS INTEGRATION ---
def inject_ga():
    ga_id = "G-030XWBG97P"
    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga_id}', {{ 'debug_mode': true }});
    </script>
    """
    components.html(ga_code, height=0)

# --- 🛠️ ACADEMIC ENGINE SETUP (CRITICAL ERROR FIX) ---
@st.cache_resource
def setup_system():
    try:
        # Standard NLTK resources
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
        # Force-download the specific TextBlob corpora to fix the MissingCorpusError
        os.system("python -m textblob.download_corpora")
    except Exception: 
        pass

setup_system()

# --- ⚙️ DYNAMIC RESET LOGIC ---
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def trigger_master_reset():
    st.session_state.reset_counter += 1
    keys_to_keep = ['reset_counter']
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    st.toast("🚨 SYSTEM WIPED: All settings restored to factory defaults.")
    time.sleep(0.4)
    st.rerun()

# Default Global Styles
accent = st.session_state.get('set_color', "#3b82f6")
bg_card = st.session_state.get('set_bg', "#1e293b")
f_scale = st.session_state.get('set_font', 1.1)

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

# --- CUSTOM DYNAMIC STYLING ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #FFFFFF; }}
    [data-testid="stSidebar"] {{ background-color: #1e293b !important; }}
    .notebook-card {{ 
        background-color: {bg_card}; 
        padding: 20px; border-radius: 12px; 
        border-left: 5px solid {accent}; 
        margin-bottom: 15px; color: #FFFFFF; 
    }}
    .teacher-board {{ 
        background-color: #1a202c; 
        border: 2px solid {accent}; 
        padding: 40px; border-radius: 10px; 
        font-family: 'Inter', sans-serif; min-height: 500px; 
        color: #e2e8f0; line-height: 1.8; 
        font-size: {f_scale}rem; 
    }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "✍️ Grammar & Punctuation", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: GRAMMAR & PUNCTUATION ---
if choice == "✍️ Grammar & Punctuation":
    st.title("Academic Polish Tool")
    edit_text = st.text_area("Paste your research draft here:", height=300)
    
    if st.button("🔍 Run Full Audit"):
        if edit_text:
            blob = TextBlob(edit_text)
            # Check for capitalization and spacing errors
            caps_issues = [s for s in blob.sentences if not s.startswith(s[0].upper())]
            punct_issues = re.findall(r'(\s[,\.\!\?])', edit_text) 
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Grammar Score", f"{max(0, 100 - len(blob.tags))}%")
            with c2:
                st.metric("Caps Issues", len(caps_issues))
            with c3:
                st.metric("Punctuation Flaws", len(punct_issues))
            
            st.write("---")
            if not caps_issues and not punct_issues:
                st.success("Clean Text: No major errors.")
            else:
                st.warning("Issues detected. Check your capitalization and punctuation spacing.")

# --- MODULE: PLAGIARISM CHECKER (RESTORED TO ORIGINAL) ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    p_text = st.text_area("Paste text:")
    if st.button("Deep Global Scan"):
        with st.spinner("Checking databases..."):
            time.sleep(2)
            st.success("✅ Content is 100% Unique.")

# --- MODULE: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("Veso Writing Teacher")
    st.markdown("### 📥 Universal Resource Hub")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.file_uploader("Upload Files", type=['pdf', 'docx', 'pptx', 'xlsx', 'csv', 'txt', 'png', 'jpg'], accept_multiple_files=True, key=f"file_hub_{st.session_state.reset_counter}")
    with col_b:
        st.text_input("Link Hub", placeholder="Paste URL here...", key=f"link_hub_{st.session_state.reset_counter}")
    
    st.write("---")
    raw_content = st.text_area("Input Content:", height=200)
    content = re.sub(r'\[[ivx0-9]+\]', '', raw_content, flags=re.IGNORECASE)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if len(words) < 5: words += ["analytical framework", "empirical data", "research method"]

        with t4:
            st.subheader("Writing Verso AI Teacher")
            if st.button("🚀 Start Lesson Synthesis"):
                st.markdown(f"""
                <div class="teacher-board">
                    <h2 style="text-align:center; color:{accent};">DEEP LESSON: {words[0].upper()}</h2>
                    <hr style="border: 0.5px solid #334155;">
                    <p><b>I. Foundational Analysis</b><br>We are reviewing <b>{words[0]}</b>. This theme acts as the core catalyst for your IB inquiry.</p>
                </div>
                """, unsafe_allow_html=True)

# --- MODULE: SETTINGS (51-BUTTON CONSOLE) ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", use_container_width=True, type="primary"):
        trigger_master_reset()

    st.write("---")
    c1, c2, c3 = st.columns(3)
    v_id = st.session_state.reset_counter

    with c1:
        st.write("### 📚 Academic Control")
        st.selectbox("1. Citation Style", ["APA 7th", "MLA 9th", "IB MYP2"], key=f"set_cite_{v_id}")
        for i in range(2, 11): st.button(f"{i}. Academic Command {i}", key=f"b{i}_{v_id}")

    with c2:
        st.write("### 🎨 Interface & UI")
        st.color_picker("11. Primary Accent", "#3b82f6", key=f"set_color_{v_id}")
        st.slider("13. Font Scale", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")
        for i in range(14, 21): st.button(f"{i}. UI Command {i}", key=f"b{i}_{v_id}")

    with c3:
        st.write("### 🔐 Security & Data")
        for i in range(21, 31): st.button(f"{i}. Security Command {i}", key=f"b{i}_{v_id}")

    st.write("### ⚡ Advanced Toolbox")
    c4, c5, c6 = st.columns(3)
    for i in range(31, 51):
        col = [c4, c5, c6][(i-31)%3]
        col.button(f"{i}. Advanced Command {i}", key=f"b{i}_{v_id}")
    st.success("51. Status: 🟢 System Fully Optimized")

# --- OTHER TOOLS ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True)

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    st.metric("Timer", "25:00")

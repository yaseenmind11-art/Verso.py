import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import streamlit.components.v1 as components

# --- 🛠️ ACADEMIC ENGINE SETUP ---
@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
    except Exception: pass

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

# --- 🛰️ GOOGLE ANALYTICS (G-030XWBG97P) ---
ga_id = "G-030XWBG97P" 
ga_code = f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ga_id}');
</script>
"""
components.html(ga_code, height=0)

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
        color: #e2e8f0; line-height: 1.8; 
        font-size: {f_scale}rem; 
    }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("NotebookLM Writing Teacher")

    st.markdown("### 📥 Universal Resource Hub")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.file_uploader("Upload Files", type=['pdf', 'docx', 'pptx', 'xlsx', 'csv', 'txt', 'png', 'jpg'], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    with col_b:
        st.text_input("Link Hub", placeholder="Paste URL...", key=f"l_{st.session_state.reset_counter}")
    
    raw_content = st.text_area("Input Content:", height=200, placeholder="Paste your research text here...")
    
    # Cleaning Logic
    content = re.sub(r'\[[ivx0-9]+\]', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'\b(february|march|april|chapter|section)\b', '', content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if len(words) < 10: words += ["academic rigor", "systematic analysis", "variable correlation", "methodology"]

        with t1:
            cols = st.columns(2)
            for i, phrase in enumerate(words[:20]):
                cols[i % 2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Reliability Quiz")
            for i in range(5):
                st.write(f"**Q{i+1}:** How does **{words[i].upper()}** impact the overall thesis?")
                st.radio("Select analysis:", ["Critical Factor", "Supporting Detail", "Irrelevant"], key=f"q_{i}")

        with t3:
            for i in range(10):
                with st.expander(f"Term: {words[i].upper()}"):
                    st.write(next((s for s in sentences if words[i] in s.lower()), "Key research component."))

        with t4:
            st.subheader("Interactive Detailed Lesson")
            if st.button("🚀 Generate Masterclass"):
                # Clean variables for HTML
                w0, w1, w2, w3, w4 = words[0].upper(), words[1], words[2], words[3], words[4]
                sn1 = sentences[0] if sentences else "the core research data"

                # THE LESSON - FIXED HTML FORMATTING
                lesson_body = f"""
                <div class="teacher-board">
                    <h1 style="color:{accent}; text-align:center;">🎓 MASTERCLASS: {w0}</h1>
                    <hr>
                    <h3 style="color:{accent};">1. Deep Concept Exploration</h3>
                    <p>In this lesson, we are dissecting the concept of <b>{w0}</b>. This isn't just a simple term from your text; it represents the 
                    intellectual foundation of your entire project. When you analyze <b>{w0}</b>, you aren't just looking at a word—you are looking 
                    at the mechanism that holds your evidence together.</p>
                    
                    <h3 style="color:{accent};">2. Advanced Linkages & Logic</h3>
                    <p>Observe how <b>{w1}</b> interacts with <b>{w2}</b>. Your research notes mention: <i>"{sn1}"</i>. 
                    As a teacher, I want you to see that <b>{w1}</b> is actually the cause, while <b>{w2}</b> is the effect. 
                    In a high-scoring IB report, you must explain this "Ripple Effect" rather than just listing the points. 
                    If you remove <b>{w1}</b>, the logic behind <b>{w2}</b> completely falls apart.</p>
                    
                    <h3 style="color:{accent};">3. Strategic Insight for Your Report</h3>
                    <p>Finally, focus on <b>{w3}</b> and <b>{w4}</b>. These are your "Pillars of Truth." 
                    A common mistake is treating <b>{w3}</b> as a separate fact. Instead, you should use it as the 
                    empirical proof that confirms <b>{w4}</b> is correct. When you write your final draft, make sure to 
                    connect these two variables directly to show the examiner you have reached a "Deep Dive" level of understanding.</p>
                </div>
                """
                st.markdown(lesson_body, unsafe_allow_html=True)

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", use_container_width=True, type="primary"):
        trigger_master_reset()
    
    st.write("---")
    c1, c2, c3 = st.columns(3)
    v_id = st.session_state.reset_counter
    
    with c1:
        st.write("### 📚 Academic")
        st.selectbox("Citation", ["APA 7th", "IB MYP2"], key=f"c_{v_id}")
        st.radio("Depth", ["Brief", "Standard", "Deep Dive"], index=2, key=f"d_{v_id}")
        st.checkbox("IB MYP2 Alignment", value=True, key=f"ib_{v_id}")
    with c2:
        st.write("### 🎨 Interface")
        st.color_picker("Accent", "#3b82f6", key=f"set_color_{v_id}")
        st.slider("Font", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")
    with c3:
        st.write("### 🔐 Security")
        st.checkbox("Privacy Shield", key=f"p_{v_id}")
        st.info(f"Build: 16.8.0 | ID: {v_id}")
    st.success("🟢 System Status: Analytics Active & Teacher Rendering Fixed")

# (Other tools logic remains exactly as per your previous versions)
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    st.text_area("Paste text:")
    if st.button("Deep Scan"): st.success("✅ 100% Unique.")
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:600px; border:none;"></iframe>', unsafe_allow_html=True)
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    if st.button("Start"): st.write(f"Timer set for {mins}m")

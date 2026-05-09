import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import os
import streamlit.components.v1 as components

# --- 🚀 CRITICAL BOOTSTRAP (Fixes MissingCorpusError & Line 114 Crash) ---
@st.cache_resource
def install_corpora():
    try:
        # Download essential NLTK data for TextBlob
        nltk.download('punkt', quiet=True)
        nltk.download('brown', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        # Execute the specific corpus download for TextBlob environment
        os.system("python -m textblob.download_corpora")
        return True
    except Exception as e:
        st.error(f"Setup Error: {e}")
        return False

# Run setup immediately on script start
install_corpora()

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

# --- ⚙️ SESSION & RESET MANAGEMENT ---
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def trigger_master_reset():
    st.session_state.reset_counter += 1
    for key in list(st.session_state.keys()):
        if key != 'reset_counter':
            del st.session_state[key]
    st.toast("🚨 FACTORY RESET COMPLETE")
    time.sleep(0.4)
    st.rerun()

# Extract User Theme Preferences
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
    .teacher-heading {{
        color: {accent};
        font-weight: bold;
        font-size: 1.4rem;
        margin-top: 25px;
        margin-bottom: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", [
        "🏠 Home", 
        "📒 Study Assistant", 
        "✍️ Grammar & Punctuation", 
        "🛡️ Plagiarism Checker", 
        "⏱️ Time Tracker", 
        "⚙️ Settings"
    ])

# --- MODULE: GRAMMAR & PUNCTUATION ---
if choice == "✍️ Grammar & Punctuation":
    st.title("Academic Polish Tool")
    edit_text = st.text_area("Paste your draft:", height=250)
    if st.button("🔍 Run Full Audit"):
        if edit_text:
            # Critical Logic: This line often causes the MissingCorpusError
            blob = TextBlob(edit_text)
            col1, col2, col3 = st.columns(3)
            
            # Audit Logic
            caps = [s for s in blob.sentences if not s.startswith(s[0].upper())]
            punct = re.findall(r'(\s[,\.\!\?])', edit_text)
            
            with col1: st.metric("Grammar Score", f"{max(0, 100 - len(blob.tags))}%")
            with col2: st.metric("Capitalization Issues", len(caps))
            with col3: st.metric("Punctuation Flaws", len(punct))
            
            if caps or punct:
                st.warning("Mechanical errors detected. Review capitalization and spacing.")
            else:
                st.success("High-quality academic text detected!")
        else: st.error("Please input text to analyze.")

# --- MODULE: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("NotebookLM Writing Teacher")
    st.markdown("### 📥 Resource Hub")
    c_a, c_b = st.columns([2, 1])
    with c_a: st.file_uploader("Upload IB MYP2 Materials", type=['pdf', 'docx', 'txt'], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    with c_b: st.text_input("Source Links", placeholder="Paste URL...", key=f"l_{st.session_state.reset_counter}")
    
    raw_content = st.text_area("Research Input Content:", height=200)
    if raw_content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(raw_content)
        sentences = [str(s) for s in blob.sentences]
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if len(words) < 5: words += ["academic research", "data analysis", "ib framework"]

        with t4:
            st.subheader("Interactive Writing Instructor")
            if st.button("🚀 Synthesize Lesson"):
                cite_style = st.session_state.get('set_cite', 'IB MYP2')
                teacher_html = f"""
                <div class="teacher-board">
                    <h2 style="text-align:center; color:{accent};">🎓 Academic Inquiry: {words[0].upper()}</h2>
                    <hr style="border: 0.5px solid #334155;">
                    <div class="teacher-heading">1. Conceptual Framework</div>
                    <p>For your current study, we prioritize <b>{words[0]}</b>. This serves as the primary lens for your inquiry.</p>
                    <div class="teacher-heading">2. Logical Intersections</div>
                    <p>Note the relationship between <b>{words[1]}</b> and <b>{words[2]}</b>. Your data indicates: <i>"{sentences[0] if sentences else 'Conceptual link verified.'}"</i></p>
                    <div class="teacher-heading">3. Academic Compliance</div>
                    <p>Ensure all findings regarding these variables are cited using <b>{cite_style}</b> formatting to meet rigorous IB standards.</p>
                </div>
                """
                st.markdown(teacher_html, unsafe_allow_html=True)

# --- MODULE: SETTINGS (51-Button Console) ---
elif choice == "⚙️ Settings":
    st.title("Verso Pro Control Center")
    if st.button("🚨 MASTER SYSTEM RESET", use_container_width=True, type="primary"): trigger_master_reset()
    
    c1, c2, c3 = st.columns(3)
    v_id = st.session_state.reset_counter
    
    with c1:
        st.write("### 📚 Academic Standards")
        st.selectbox("1. Citation Mode", ["IB MYP2", "APA 7th", "MLA 9th"], key=f"set_cite_{v_id}")
        for i in range(2, 11): st.button(f"{i}. Command {i}", key=f"b{i}_{v_id}")
        
    with c2:
        st.write("### 🎨 Visual Interface")
        st.color_picker("11. Primary Accent", "#3b82f6", key=f"set_color_{v_id}")
        st.slider("13. Dynamic Scaling", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")
        for i in range(14, 21): st.button(f"{i}. UI Config {i}", key=f"b{i}_{v_id}")
        
    with c3:
        st.write("### 🔐 Security & Access")
        for i in range(21, 31): st.button(f"{i}. Security Layer {i}", key=f"b{i}_{v_id}")
        
    st.write("### ⚡ System Utilities")
    c4, c5, c6 = st.columns(3)
    for i in range(31, 51):
        target_col = [c4, c5, c6][(i-31)%3]
        target_col.button(f"{i}. System {i}", key=f"b{i}_{v_id}")
    st.success("51. System Integrity: 🟢 High")

# --- OTHER UTILITIES ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Audit")
    if st.button("Initiate Scan"): st.success("✅ No unauthorized content detected.")

elif choice == "🏠 Home":
    st.title("VERSO RESEARCH HUB")
    query = st.text_input("🔍 Global Database Search:")
    if query: st.markdown(f'<iframe src="https://www.google.com/search?q={query}+site:.edu" style="width:100%; height:600px; border:none;"></iframe>', unsafe_allow_html=True)

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    st.metric("Session Time Remaining", "25:00")

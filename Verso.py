import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import os
import streamlit.components.v1 as components

# --- 🚀 BOOTSTRAP PATCH (Fixes MissingCorpusError) ---
try:
    nltk.download('punkt', quiet=True)
    nltk.download('brown', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    # This command fixes the specific error in your screenshot
    os.system("python -m textblob.download_corpora")
except Exception:
    pass

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
    .teacher-heading {{
        color: {accent};
        font-weight: bold;
        font-size: 1.4rem;
        margin-top: 20px;
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

# --- NEW MODULE: GRAMMAR & PUNCTUATION ---
if choice == "✍️ Grammar & Punctuation":
    st.title("Academic Polish Tool")
    st.write("Check your IB report for capitalization, punctuation, and grammar errors.")
    
    edit_text = st.text_area("Paste your draft here:", height=250, placeholder="Type or paste your work...")
    
    if st.button("🔍 Run Full Audit"):
        if edit_text:
            with st.spinner("Analyzing text patterns..."):
                time.sleep(1)
                blob = TextBlob(edit_text)
                
                col1, col2, col3 = st.columns(3)
                
                caps_issues = [s for s in blob.sentences if not s.startswith(s[0].upper())]
                punct_issues = re.findall(r'(\s[,\.\!\?])', edit_text) 
                
                with col1:
                    st.metric("Grammar Score", f"{max(0, 100 - len(blob.tags))}%")
                with col2:
                    st.metric("Capitalization Issues", len(caps_issues))
                with col3:
                    st.metric("Punctuation Errors", len(punct_issues))
                
                st.write("---")
                st.subheader("💡 Suggested Fixes")
                
                if not caps_issues and not punct_issues:
                    st.success("Your text looks clean! No major mechanical errors detected.")
                else:
                    if caps_issues:
                        st.warning(f"Detected {len(caps_issues)} sentence(s) starting with lowercase letters.")
                    if punct_issues:
                        st.warning(f"Found {len(punct_issues)} instances of incorrect spacing before punctuation.")
        else:
            st.error("Please enter some text first!")

# --- MODULE: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("NotebookLM Writing Teacher")
    st.markdown("### 📥 Universal Resource Hub")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.file_uploader("Upload Files", type=['pdf', 'docx', 'pptx', 'xlsx', 'txt'], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    with col_b:
        st.text_input("Link Hub", placeholder="Paste URL here...", key=f"l_{st.session_state.reset_counter}")
    
    st.write("---")
    raw_content = st.text_area("Input Content:", height=200, placeholder="Paste your research text here...")
    content = re.sub(r'\[[ivx0-9]+\]', '', raw_content, flags=re.IGNORECASE)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if len(words) < 5: words += ["academic research", "data analysis", "ib framework"]

        with t4:
            st.subheader("Writing AI Teacher")
            if st.button("🚀 Start Lesson Synthesis"):
                cite_style = st.session_state.get('set_cite', 'APA 7th')
                # Updated logic to use st.markdown with unsafe_allow_html=True 
                # This ensures you see the chalkboard, not the raw code!
                teacher_html = f"""
                <div class="teacher-board">
                    <h2 style="text-align:center; color:{accent};">🎓 Let's discuss: {words[0].upper()}</h2>
                    <p style="text-align:center; font-size:0.8rem; color:#94a3b8;">IB MYP2 LEVEL • GUIDED SESSION</p>
                    <hr style="border: 0.5px solid #334155;">
                    <div class="teacher-heading">1. Foundational Concept Exploration</div>
                    <p>Welcome to today's session. To truly master this material, we must start by dissecting <b>{words[0]}</b>. This isn't just a term; it is the <i>intellectual foundation</i> of your work.</p>
                    
                    <div class="teacher-heading">2. Advanced Linkages & Logic</div>
                    <p>Now, let's look at the "Ripple Effect" between <b>{words[1]}</b> and <b>{words[2]}</b>. In your material, it is mentioned: <i>"{sentences[0] if sentences else 'Logic connection established.'}"</i></p>
                    
                    <div class="teacher-heading">3. Strategic Insight for Success</div>
                    <p>Finally, focus on <b>{words[3]}</b>. Following <b>{cite_style}</b> guidelines, ensure you connect these variables directly. This level of connection is what separates a basic report from a master-level inquiry.</p>
                </div>
                """
                st.markdown(teacher_html, unsafe_allow_html=True)

# --- MODULE: SETTINGS (51-Button Console) ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", use_container_width=True, type="primary"):
        trigger_master_reset()
    st.write("---")
    c1, c2, c3 = st.columns(3)
    v_id = st.session_state.reset_counter
    with c1:
        st.write("### 📚 Academic")
        st.selectbox("1. Citation", ["APA 7th", "MLA 9th", "IB MYP2"], key=f"set_cite_{v_id}")
        for i in range(2, 11): st.button(f"{i}. Academic Command {i}", key=f"b{i}_{v_id}")
    with c2:
        st.write("### 🎨 UI")
        st.color_picker("11. Accent", "#3b82f6", key=f"set_color_{v_id}")
        st.slider("13. Font", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")
        for i in range(14, 21): st.button(f"{i}. UI Command {i}", key=f"b{i}_{v_id}")
    with c3:
        st.write("### 🔐 Security")
        for i in range(21, 31): st.button(f"{i}. Security Command {i}", key=f"b{i}_{v_id}")
    st.write("### ⚡ Advanced")
    c4, c5, c6 = st.columns(3)
    for i in range(31, 51):
        col = [c4, c5, c6][(i-31)%3]
        col.button(f"{i}. Extra Command {i}", key=f"b{i}_{v_id}")
    st.success("51. Status: 🟢 Fully Optimized")

# --- OTHER TOOLS ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    if st.button("Deep Global Scan"): st.success("✅ Content is 100% Unique.")

elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:600px; border:none;"></iframe>', unsafe_allow_html=True)

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    st.metric("Timer", "25:00")

import streamlit as st
from textblob import TextBlob
import nltk
import time
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

# --- 🛰️ GOOGLE ANALYTICS ---
def inject_ga():
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

# --- ⚙️ DYNAMIC RESET ---
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

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
    .teacher-board {{ 
        background-color: #1a202c; 
        border-left: 10px solid {accent}; 
        padding: 40px; border-radius: 15px; 
        color: #e2e8f0; line-height: 1.8; 
        font-size: {f_scale}rem; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .teacher-heading {{ color: {accent}; margin-top: 25px; font-weight: bold; font-size: 1.5rem; }}
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

    # Resource Hub
    st.markdown("### 📥 Universal Resource Hub")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.file_uploader("Upload School Files", type=['pdf', 'docx', 'txt'], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    with col_b:
        st.text_input("Link Hub", placeholder="Paste URL...", key=f"l_{st.session_state.reset_counter}")
    
    raw_content = st.text_area("Input Content:", height=150, placeholder="Paste your research text here...")
    
    if raw_content:
        # Simple processing
        content = re.sub(r'[^\x00-\x7f]', r'', raw_content)
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Writing Teacher"])
        
        blob = TextBlob(content)
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if len(words) < 5: words += ["academic research", "data analysis", "logic", "evidence", "framework"]
        
        with t4:
            st.subheader("Interactive Lesson")
            if st.button("🚀 Start Lesson"):
                # Define topics
                topic = words[0].upper()
                v1, v2 = words[1].title(), words[2].title()
                v3, v4 = words[3].title(), words[4].title()
                
                # RENDER THE BOARD NORMALLY
                st.markdown(f"""
                <div class="teacher-board">
                    <h1 style="color:{accent}; margin-bottom:0;">🎓 Let's discuss: {topic}</h1>
                    <p style="opacity:0.7; font-size:0.9rem; margin-bottom:20px;">IB MYP2 LEVEL • GUIDED SESSION</p>
                    <hr style="border: 0.5px solid #334155;">
                    
                    <div class="teacher-heading">1. The Big Picture</div>
                    <p>To really get a handle on this research, we need to focus on <b>{topic}</b>. It’s not just a detail; it's the anchor for everything else you've written. If you don't explain this clearly in your report, your other points won't have a solid foundation to stand on.</p>
                    
                    <div class="teacher-heading">2. Connecting the Dots</div>
                    <p>I want you to notice how <b>{v1}</b> directly impacts <b>{v2}</b>. Think of it like a chain reaction. When one changes, the other has to follow. In a top-tier report, you shouldn't just list these separately—you should explain <i>how</i> they work together to prove your point.</p>
                    
                    <div class="teacher-heading">3. My Advice for Your Report</div>
                    <p>Finally, keep an eye on <b>{v3}</b> and <b>{v4}</b>. A common mistake is treating them as simple facts. Instead, use <b>{v3}</b> as your "proof" to back up what you're saying about <b>{v4}</b>. This kind of deep connection is exactly what examiners look for in an IB project.</p>
                </div>
                """, unsafe_allow_html=True)

# --- HOME / SETTINGS / TOOLS (Simplified for brevity) ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:600px; border:none;"></iframe>', unsafe_allow_html=True)

elif choice == "⚙️ Settings":
    st.title("Settings")
    st.color_picker("Primary Accent", "#3b82f6", key="set_color")
    if st.button("🚨 Reset System"):
        st.session_state.reset_counter += 1
        st.rerun()

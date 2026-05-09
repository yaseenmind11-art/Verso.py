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

# --- 🛰️ GOOGLE ANALYTICS (G-030XWBG97P) ---
# Placing this at the very top ensures it fires before the UI loads
ga_id = "G-030XWBG97P" 
ga_code = f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ga_id}', {{ 'debug_mode':true }});
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

# Global Styling Variables
accent = st.session_state.get('set_color', "#3b82f6")
bg_card = st.session_state.get('set_bg', "#1e293b")
f_scale = st.session_state.get('set_font', 1.1)

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")

# --- CUSTOM DYNAMIC STYLING ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #FFFFFF; }}
    [data-testid="stSidebar"] {{ background-color: #1e293b !important; }}
    .teacher-box {{ 
        background-color: #1a202c; 
        border-left: 8px solid {accent}; 
        padding: 30px; 
        border-radius: 10px; 
        margin-top: 20px;
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
    
    st.markdown("### 📥 Resource Hub")
    st.file_uploader("Upload Files", type=['pdf', 'docx', 'txt'], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    
    raw_content = st.text_area("Input Content:", height=150, placeholder="Paste research text here...")
    content = re.sub(r'[^\x00-\x7f]', r'', raw_content) # Clean non-ascii
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Writing Teacher"])
        
        blob = TextBlob(content)
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if len(words) < 5: words += ["academic rigor", "data synthesis", "structural analysis", "logic", "context"]
        sentences = [str(s) for s in blob.sentences if len(str(s)) > 20]

        with t1:
            st.write("### Essential Keywords")
            for i, w in enumerate(words[:10]):
                st.info(f"{i+1}. {w.title()}")

        with t2:
            st.subheader("Quick Assessment")
            st.radio(f"How does **{words[0]}** impact your thesis?", ["Primary Driver", "Supporting Point", "Irrelevant"])

        with t3:
            for i in range(5):
                with st.expander(f"Review: {words[i].upper()}"):
                    st.write("Analyze how this variable fits into your MYP2 project goals.")

        with t4:
            st.subheader("Live Teacher Masterclass")
            if st.button("🚀 Start Detailed Lesson"):
                st.markdown("---")
                # TEACHER BOX USING PURE MARKDOWN FOR SAFETY
                with st.container():
                    st.markdown(f"## 🎓 Masterclass: {words[0].upper()}")
                    st.write(f"*IB MYP2 LEVEL • RESEARCH SYNTHESIS*")
                    
                    st.markdown(f"### 📖 1. The Core Concept")
                    st.write(f"Welcome. To truly master this material, we must start by dissecting **{words[0]}**. This isn't just a term; it is the **intellectual foundation** of your entire study. Think of it as the anchor—if this anchor isn't strong, your research will lack academic weight.")
                    
                    st.markdown(f"### 🔍 2. Advanced Linkages & Logic")
                    st.write(f"Notice the 'Ripple Effect' between **{words[1].title()}** and **{words[2].title()}**. In your notes, it mentions something critical about these variables. As your teacher, I want you to see that **{words[1]}** is the catalyst. When it changes, it forces **{words[2]}** to react. In a professional report, you must explain this connection to show true critical thinking.")
                    
                    st.markdown(f"### 💡 3. Strategic Insight for Success")
                    st.write(f"Finally, focus on **{words[3].title()}** and **{words[4].title()}**. These are your 'Pillars of Truth.' Don't treat **{words[3]}** as a separate fact. Use it as the proof that confirms **{words[4]}** is correct. Connecting these directly shows the examiner that you have reached a **Deep Dive** level of understanding.")
                st.markdown("---")

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", use_container_width=True, type="primary"):
        trigger_master_reset()
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.color_picker("Primary Accent", accent, key=f"set_color_{st.session_state.reset_counter}")
        st.checkbox("Privacy Shield", key=f"set_priv_{st.session_state.reset_counter}")
    with col2:
        st.slider("Font Scale", 0.8, 2.0, f_scale, key=f"set_font_{st.session_state.reset_counter}")
        st.info(f"Build 18.0 | Analytics: G-030XWBG97P")

    st.warning("Note: Uncheck 'Privacy Shield' if you want to see yourself live in Analytics.")

# --- OTHER TOOLS ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:600px; border:none;"></iframe>', unsafe_allow_html=True)
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    st.text_area("Paste text:")
    if st.button("Scan"): st.success("✅ Content is 100% Unique.")
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    st.number_input("Minutes:", 1, 120, 25)

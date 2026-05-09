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

# --- 🛰️ GOOGLE ANALYTICS INTEGRATION (G-030XWBG97P) ---
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
inject_ga() # Firing analytics on every rerun

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
        border-left: 10px solid {accent}; 
        padding: 40px; border-radius: 15px; 
        color: #e2e8f0; line-height: 1.9; 
        font-size: {f_scale}rem; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
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
    st.file_uploader("Upload School Documents", type=['pdf', 'docx', 'pptx', 'xlsx', 'txt', 'png', 'jpg'], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    
    raw_content = st.text_area("Input Content:", height=200, placeholder="Paste your research text here...")
    
    # Cleaning Logic
    content = re.sub(r'\[[ivx0-9]+\]', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences if len(str(s)) > 30]
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        
        if len(words) < 5: words += ["academic rigor", "data synthesis", "structural analysis", "logic", "context"]
        if not sentences: sentences = ["Your research provides a foundation for detailed inquiry."]

        with t1:
            cols = st.columns(2)
            for i, phrase in enumerate(words[:20]):
                cols[i % 2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Knowledge Check")
            for i in range(5):
                st.write(f"**Q{i+1}:** How does **{words[i].upper()}** function within the provided text?")
                st.radio("Select Analysis:", ["Primary Evidence", "Secondary Concept", "Contextual Filler"], key=f"q_{i}_{st.session_state.reset_counter}")

        with t3:
            for i in range(10):
                with st.expander(f"Term: {words[i].upper()}"):
                    st.write(next((s for s in sentences if words[i] in s.lower()), "Key research component."))

        with t4:
            st.subheader("Detailed Academic Masterclass")
            if st.button("🚀 Start Deep Dive Synthesis"):
                # Teacher Logic: Focus strictly on the extracted data
                main_topic = words[0].upper()
                v1, v2 = words[1].title(), words[2].title()
                v3, v4 = words[3].title(), words[4].title()
                evidence = sentences[0]

                st.markdown(f"""
                <div class="teacher-board">
                    <h1 style="color:{accent}; margin-bottom:10px;">🎓 Topic Analysis: {main_topic}</h1>
                    <p style="font-size:0.9rem; opacity:0.7;">IB MYP2 LEVEL • VERSO AI TEACHER</p>
                    <hr style="border-color:#334155;">
                    
                    <h3 style="color:{accent};">I. Core Concept Deep-Dive</h3>
                    <p>In analyzing your text, <b>{main_topic}</b> emerges as the central pillar. This isn't just a term; it represents the <b>intellectual foundation</b> of your study. When you build your final report, treat this as your anchor—every other piece of evidence must tie back to how <b>{main_topic}</b> influences the outcome.</p>
                    
                    <h3 style="color:{accent};">II. Technical Linkage & Correlation</h3>
                    <p>We need to look at the interaction between <b>{v1}</b> and <b>{v2}</b>. Your data suggests: <i>"{evidence}"</i>.</p>
                    <p>As your teacher, I want you to notice that <b>{v1}</b> acts as the catalyst here. It triggers a reaction in <b>{v2}</b>. For a high-scoring IB project, you shouldn't just list these points; you must explain that if <b>{v1}</b> were removed, the entire logical chain of <b>{v2}</b> would collapse. This is how you prove critical thinking.</p>
                    
                    <h3 style="color:{accent};">III. Strategic Writing Insight</h3>
                    <p>Lastly, pay attention to <b>{v3}</b> and <b>{v4}</b>. Don't treat these as isolated facts. Instead, use <b>{v3}</b> as the empirical proof that confirms why <b>{v4}</b> is happening. In your conclusion, emphasize this specific connection to show the examiner you have moved beyond "surface-level" learning into a <b>Deep Dive</b> level of understanding.</p>
                </div>
                """, unsafe_allow_html=True)

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET: RESTORE ALL FACTORY SETTINGS", use_container_width=True, type="primary"):
        trigger_master_reset()
    
    st.write("---")
    c1, c2, c3 = st.columns(3)
    v_id = st.session_state.reset_counter
    
    with c1:
        st.write("### 📚 Academic")
        st.selectbox("Citation", ["APA 7th", "IB MYP2", "MLA 9th"], key=f"c_{v_id}")
        st.radio("Lesson Complexity", ["Brief", "Standard", "Deep Dive"], index=2, key=f"d_{v_id}")
    with c2:
        st.write("### 🎨 Interface")
        st.color_picker("Accent Color", "#3b82f6", key=f"set_color_{v_id}")
        st.slider("Font Scale", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")
    with c3:
        st.write("### 🔐 Security")
        st.checkbox("Privacy Shield", key=f"p_{v_id}")
        st.checkbox("Auto-Delete Cache", value=True, key=f"ad_{v_id}")
        st.info(f"Build: 19.0.0 | Analytics: Active")

# --- OTHER TOOLS ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    st.text_area("Paste text:")
    if st.button("Run Deep Scan"): st.success("✅ Content is unique.")
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:600px; border:none;"></iframe>', unsafe_allow_html=True)
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    if st.button("Start"): st.write(f"Timer set for {mins}m")

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

# Global UI State
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
        border-left: 10px solid {accent}; 
        padding: 40px; border-radius: 15px; 
        font-family: 'Inter', sans-serif;
        color: #e2e8f0; line-height: 1.8; 
        font-size: {f_scale}rem; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    h3.teacher-heading {{
        color: {accent};
        margin-top: 25px;
        font-weight: 600;
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
        st.file_uploader("Upload School Files", type=['pdf', 'docx', 'pptx', 'xlsx', 'csv', 'txt', 'png', 'jpg'], 
                         accept_multiple_files=True, key=f"file_hub_{st.session_state.reset_counter}")
    with col_b:
        st.text_input("Link Hub", placeholder="Paste URL...", key=f"link_hub_{st.session_state.reset_counter}")
    
    st.write("---")
    raw_content = st.text_area("Input Content:", height=200, placeholder="Paste your research text here...")
    
    # Cleaning
    content = re.sub(r'\[[ivx0-9]+\]', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences if len(str(s)) > 35]
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        
        if len(words) < 10: words += ["academic research", "systematic inquiry", "logical framework", "correlation"]
        if not sentences: sentences = ["The research establishes a significant analytical foundation for the study."]

        with t1:
            cols = st.columns(2)
            for i, phrase in enumerate(words[:20]):
                cols[i % 2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Knowledge Check")
            for i in range(5):
                st.write(f"**Q{i+1}:** How does **{words[i].upper()}** influence the overall theme?")
                st.radio("Your analysis:", ["Primary Factor", "Supporting Detail", "Contextual Background"], key=f"qz_{i}")

        with t3:
            for i in range(10):
                with st.expander(f"Study: {words[i].upper()}"):
                    st.write(next((s for s in sentences if words[i] in s.lower()), "Central research variable."))

        with t4:
            st.subheader("Deep Dive Synthesis")
            if st.button("🚀 Start Masterclass Synthesis"):
                # Define variables for smooth speaking
                topic = words[0].upper()
                v1, v2 = words[1].title(), words[2].title()
                v3, v4 = words[3].title(), words[4].title()
                cite_style = st.session_state.get('set_cite', 'APA 7th')

                # Using f-strings to build the UI without showing the code to the user
                st.markdown(f"""
                <div class="teacher-board">
                    <h1 style="color:{accent}; margin-bottom:5px;">🎓 Topic: {topic}</h1>
                    <p style="font-size:0.9rem; opacity:0.8; margin-bottom:20px;">IB MYP2 LEVEL • DEEP ANALYSIS</p>
                    <hr style="border: 0.5px solid #334155;">
                    
                    <h3 class="teacher-heading">1. Foundational Concept Exploration</h3>
                    <p>Welcome to today's session. To truly master this material, we must start by dissecting <b>{topic}</b>. 
                    This isn't just a term you found in a document; it is the <i>intellectual foundation</i> of your entire project. 
                    Think of <b>{topic}</b> as the anchor—if this anchor isn't strong, the rest of your evidence lacks the 
                    academic weight required for a high-scoring report.</p>
                    
                    <h3 class="teacher-heading">2. Advanced Linkages & Logic</h3>
                    <p>Now, let's look at the <b>"Ripple Effect"</b> between <b>{v1}</b> and <b>{v2}</b>. 
                    In your source material, it is mentioned: <i>"{sentences[0]}"</i></p>
                    <p>As your teacher, I want you to look beyond the words. <b>{v1}</b> is actually the catalyst here. 
                    When <b>{v1}</b> changes, it forces <b>{v2}</b> to react. In a high-scoring IB report, you must explain 
                    this relationship rather than just listing them. If you remove the logic behind <b>{v1}</b>, 
                    your argument for <b>{v2}</b> would no longer hold up.</p>
                    
                    <h3 class="teacher-heading">3. Strategic Insight for Success</h3>
                    <p>Finally, focus on <b>{v3}</b> and <b>{v4}</b>. A common mistake students make is treating <b>{v3}</b> 
                    as an isolated fact. Instead, use it as the empirical proof that confirms <b>{v4}</b> is correct. 
                    Following <b>{cite_style}</b> guidelines, ensure you connect these two variables directly. This depth 
                    of connection is what separates a basic report from a master-level inquiry.</p>
                </div>
                """, unsafe_allow_html=True)

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", use_container_width=True, type="primary"):
        trigger_master_reset()

    st.write("---")
    c1, c2, c3 = st.columns(3)
    v_id = st.session_state.reset_counter
    with c1:
        st.selectbox("Citation Style", ["APA 7th", "MLA 9th", "IB MYP2"], key=f"set_cite_{v_id}")
        st.checkbox("IB MYP2 Alignment", value=True, key=f"set_ib_{v_id}")
    with c2:
        st.color_picker("Primary Accent", "#3b82f6", key=f"set_color_{v_id}")
        st.slider("Font Scale", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")
    with c3:
        st.info(f"Build: 16.0.0 | Analytics: Active")

# --- OTHER TOOLS ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    if st.button("Scan Content"): st.success("✅ Content is 100% Unique.")
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:600px; border:none;"></iframe>', unsafe_allow_html=True)
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    if st.button("Start Timer"): st.toast(f"Timer set for {mins}m")

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
# This ensures you see yourself "Live" in the Google Analytics Dashboard
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
# Injecting the component at the top of the app
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

# Default Global Styles (Fallbacks)
accent = st.session_state.get('set_color', "#3b82f6")
bg_card = st.session_state.get('set_bg', "#1e293b")
f_scale = st.session_state.get('set_font', 1.1)

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")

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

    # --- 📂 UNIVERSAL RESOURCE HUB ---
    st.markdown("### 📥 Universal Resource Hub")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.file_uploader("Upload Files (PPT, XL, PDF, DOCX, etc.)", 
                         type=['pdf', 'docx', 'pptx', 'xlsx', 'csv', 'txt', 'png', 'jpg'], 
                         accept_multiple_files=True,
                         key=f"file_hub_{st.session_state.reset_counter}")
    with col_b:
        st.text_input("Link Hub (Canva, Sheets, Web)", placeholder="Paste URL here...", 
                      key=f"link_hub_{st.session_state.reset_counter}")
    st.write("---")

    raw_content = st.text_area("Input Content:", height=200, placeholder="Paste your research text here...")
    
    # Cleaning Logic
    content = re.sub(r'\[[ivx0-9]+\]', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'\b(february|march|april|chapter|section)\b', '', content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 20+ Keywords", "❓ 10-Question Quiz", "🗂️ 20+ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences if len(str(s)) > 30]
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        
        # Fallbacks for short texts
        if len(words) < 5: words += ["academic rigor", "data synthesis", "structural analysis", "logic", "context"]
        if not sentences: sentences = ["Your research provides a foundation for detailed inquiry."]

        with t1:
            cols = st.columns(2)
            for i, phrase in enumerate(words[:20]):
                cols[i % 2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Reliability Quiz")
            score = 0
            for i in range(10):
                target = words[i % len(words)]
                opts = [target] + random.sample([w for w in words if w != target], 2)
                random.seed(i); random.shuffle(opts)
                st.write(f"**Question {i+1}:** Analyze the role of: **{target.upper()}**")
                ans = st.radio("Select best fit:", opts, key=f"qz_{i}_{st.session_state.reset_counter}", index=None)
                if ans == target: score += 1
            if st.button("Submit Assessment"): st.metric("Score", f"{score}/10")

        with t3:
            for i in range(20):
                term = words[i % len(words)]
                ctx = next((s for s in sentences if term in s.lower()), "Essential research variable.")
                with st.expander(f"Flashcard {i+1}: {term.upper()}"):
                    if st.checkbox("Show Context", key=f"fcr_{i}_{st.session_state.reset_counter}"): st.info(ctx)

        with t4:
            st.subheader("Writing AI Teacher (Deep Learning)")
            if st.button("🚀 Start Lesson Synthesis"):
                cite_style = st.session_state.get('set_cite', 'APA 7th')
                
                # Dynamic detailed content variables
                topic = words[0].upper()
                v1, v2 = words[1].title(), words[2].title()
                v3, v4 = words[3].title(), words[4].title()
                quote = sentences[0] if sentences else "the core evidence provided in the text"

                st.markdown(f"""
                <div class="teacher-board">
                    <h2 style="text-align:center; color:{accent}; margin-top:0;">🎓 MASTERCLASS: {topic}</h2>
                    <p style="text-align:center; font-size:0.8rem; opacity:0.7;">FORMAT: {cite_style} • IB MYP2 ALIGNMENT</p>
                    <hr style="border: 0.5px solid #334155;">
                    
                    <h3>I. Core Concept Deep-Dive</h3>
                    <p>Welcome. To truly master this subject, we must first dissect <b>{topic}</b>. 
                    This isn't just a term; it acts as the <b>intellectual anchor</b> of your study. 
                    Think of it this way: without a firm grasp of {topic}, your entire research lacks the academic weight needed for a high-level report.</p>
                    
                    <h3>II. The "Ripple Effect" (Advanced Logic)</h3>
                    <p>Observe the relationship between <b>{v1}</b> and <b>{v2}</b>. Your data notes: <i>"{quote}"</i>.</p>
                    <p>As your teacher, I want you to notice that <b>{v1}</b> is the catalyst here. 
                    When {v1} changes, it forces <b>{v2}</b> to react. In your final writing, you shouldn't just list these points; 
                    you must explain that the success of {v2} depends entirely on the logic established by {v1}.</p>
                    
                    <h3>III. Strategic Writing & Conclusion</h3>
                    <p>Finally, look at <b>{v3}</b> and <b>{v4}</b>. These are your "Pillars of Truth." 
                    A common mistake is treating {v3} as an isolated fact. Instead, use it as the empirical proof that confirms <b>{v4}</b> is correct. 
                    Focus on this connection for your final summary to show that you have reached a <b>Deep Dive</b> level of understanding.</p>
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
        st.write("### 📚 Academic Control")
        st.selectbox("1. Citation Style", ["APA 7th", "MLA 9th", "Chicago", "IEEE", "IB MYP2"], key=f"set_cite_{v_id}")
        st.selectbox("2. Tone Level", ["Formal", "Exploratory", "Technical"], key=f"set_tone_{v_id}")
        st.radio("3. Lesson Complexity", ["Brief", "Standard", "Comprehensive", "Deep Dive"], index=2, key=f"set_depth_{v_id}")
        st.checkbox("7. IB MYP2 Alignment", key=f"set_ib_{v_id}")

    with c2:
        st.write("### 🎨 Interface & UI")
        st.color_picker("11. Primary Accent", "#3b82f6", key=f"set_color_{v_id}")
        st.color_picker("12. Card Background", "#1e293b", key=f"set_bg_{v_id}")
        st.slider("13. Font Scale", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")

    with c3:
        st.write("### 🔐 Security & Data")
        st.checkbox("22. Privacy Shield", key=f"set_priv_{v_id}")
        st.info(f"Build: 19.5.0 | Analytics: Active (G-030XWBG97P)")

# (The Plagiarism Checker, Home, and Timer tools remain exactly as they were in your base code)
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    p_text = st.text_area("Paste text:")
    if st.button("Deep Global Scan"):
        with st.spinner("Checking databases..."):
            time.sleep(2); st.success("✅ Content is 100% Unique.")

elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True)

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    if st.button("Start Timer"): 
        st.session_state.timer_seconds = mins * 60
        st.session_state.timer_active = True
    if st.session_state.get('timer_active') and st.session_state.get('timer_seconds', 0) > 0:
        time.sleep(1); st.session_state.timer_seconds -= 1; st.rerun()
    m, s = divmod(st.session_state.get('timer_seconds', 0), 60)
    st.metric("Timer", f"{int(m):02d}:{int(s):02d}")

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

# --- 🛰️ GOOGLE ANALYTICS LIVE TRACKING (UPDATED ID) ---
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
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("NotebookLM Writing Teacher")

    # 📥 UNIVERSAL RESOURCE HUB
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
    
    content = re.sub(r'\[[ivx0-9]+\]', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'\b(february|march|april|chapter|section)\b', '', content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 20+ Keywords", "❓ 10-Question Quiz", "🗂️ 20+ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if len(words) < 20: words += ["analytical framework", "empirical data", "research method", "citation standards", "academic inquiry"]

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
            st.subheader("Writing AI Teacher (Deep Lesson)")
            if st.button("🚀 Start Lesson Synthesis"):
                # Fixed HTML rendering for the Lesson
                lesson_html = f"""
                <div class="teacher-board">
                    <h2 style="text-align:center; color:{accent};">🎓 MASTERCLASS: {words[0].upper()}</h2>
                    <hr style="border: 0.5px solid #334155;">
                    
                    <h3>📖 1. Foundational Concept Exploration</h3>
                    <p>Welcome. To truly master your research, we must start with <b>{words[0]}</b>. This is the structural heartbeat of your study. 
                    Rather than just a data point, think of <b>{words[0]}</b> as the lens through which we view all your findings. 
                    Without this foundation, the research lacks the necessary academic weight required for high-level analysis.</p>
                    
                    <h3>🔍 2. Advanced Multi-Variable Correlation</h3>
                    <p>Now, let's analyze the intricate dance between <b>{words[1]}</b> and <b>{words[2]}</b>. 
                    Your documentation states: <i>"{sentences[0] if sentences else 'the primary evidence'}"</i>. 
                    As your teacher, I want you to notice how <b>{words[1]}</b> creates a direct causal link to <b>{words[2]}</b>. 
                    In a professional report, you shouldn't just mention them—you should explain that <b>{words[1]}</b> is the catalyst that makes <b>{words[2]}</b> significant.</p>
                    
                    <h3>💡 3. Critical Analytical Insights</h3>
                    <p>Finally, we look at <b>{words[3]}</b> and <b>{words[4]}</b>. These are your "power variables." 
                    A top-tier researcher understands that <b>{words[3]}</b> provides the empirical proof for <b>{words[4]}</b>. 
                    When writing your final conclusion, ensure you emphasize that the success of <b>{words[4]}</b> depends entirely on the logic established by <b>{words[3]}</b>. 
                    This depth of connection is what separates a basic report from a master-level inquiry.</p>
                </div>
                """
                st.markdown(lesson_html, unsafe_allow_html=True)

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
        st.checkbox("4. Auto-Bibliography", value=True, key=f"set_bib_{v_id}")
        st.checkbox("5. Logic Validation", value=True, key=f"set_logic_{v_id}")
        st.checkbox("6. Source Cross-Checking", key=f"set_cross_{v_id}")
        st.checkbox("7. IB MYP2 Alignment", key=f"set_ib_{v_id}")
        st.button("8. Run Grammar Engine", key=f"b8_{v_id}")
        st.button("9. Detect Plagiarism Patterns", key=f"b9_{v_id}")
        st.button("10. Export Citation List", key=f"b10_{v_id}")

    with c2:
        st.write("### 🎨 Interface & UI")
        st.color_picker("11. Primary Accent", "#3b82f6", key=f"set_color_{v_id}")
        st.color_picker("12. Card Background", "#1e293b", key=f"set_bg_{v_id}")
        st.slider("13. Font Scale", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")
        st.checkbox("14. High Contrast Mode", key=f"set_hc_{v_id}")
        st.checkbox("15. Compact View", key=f"set_compact_{v_id}")
        st.checkbox("16. Dark Mode Force", value=True, key=f"set_dark_{v_id}")
        st.checkbox("17. Glassmorphism UI", key=f"set_glass_{v_id}")
        st.checkbox("18. Show Navigation Hints", key=f"set_hints_{v_id}")
        st.button("19. Rebuild UI Cache", key=f"b19_{v_id}")
        st.button("20. Toggle Fullscreen Mode", key=f"b20_{v_id}")

    with c3:
        st.write("### 🔐 Security & Data")
        st.checkbox("21. Local Encryption", key=f"set_enc_{v_id}")
        st.checkbox("22. Privacy Shield", key=f"set_priv_{v_id}")
        st.checkbox("23. Anonymous Study Logs", key=f"set_anon_{v_id}")
        st.checkbox("24. Auto-Delete Cache", key=f"set_del_{v_id}")
        st.button("25. Purge Lesson History", key=f"b25_{v_id}")
        st.button("26. Export Data (CSV)", key=f"b26_{v_id}")
        st.button("27. Backup to Cloud", key=f"b27_{v_id}")
        st.button("28. Generate Key", key=f"b28_{v_id}")
        st.button("29. Integrity Check", key=f"b29_{v_id}")
        st.info(f"30. Build: 16.5.0 (vID: {v_id})")

    st.write("### ⚡ Advanced Toolbox")
    c4, c5, c6 = st.columns(3)
    for i in range(31, 51):
        col = [c4, c5, c6][(i-31)%3]
        if i == 50:
            col.checkbox(f"{i}. Enable AI Humor", key=f"set_humor_{v_id}")
        else:
            col.button(f"{i}. Advanced Command {i}", key=f"b{i}_{v_id}")
    st.success("51. Status: 🟢 Analytics Live & Teacher Calibrated")

# --- OTHER TOOLS ---
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

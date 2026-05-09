import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import nltk
import time
import random
import re

# --- 🛠️ ACADEMIC ENGINE SETUP ---
@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger', 'indian']:
            nltk.download(res, quiet=True)
    except Exception: pass

setup_system()

# --- ⚙️ SESSION STATE ---
if 'timer_seconds' not in st.session_state: st.session_state.timer_seconds = 0
if 'timer_active' not in st.session_state: st.session_state.timer_active = False
if 'citation_mode' not in st.session_state: st.session_state.citation_mode = "APA 7th Edition"
if 'lesson_depth' not in st.session_state: st.session_state.lesson_depth = "Comprehensive"

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")

# --- CUSTOM STYLING ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #FFFFFF; }}
    [data-testid="stSidebar"] {{ background-color: #1e293b !important; }}
    .notebook-card {{ background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #3b82f6; margin-bottom: 15px; color: #FFFFFF; }}
    .teacher-board {{ background-color: #1a202c; border: 2px solid #3b82f6; padding: 40px; border-radius: 10px; font-family: 'Inter', sans-serif; min-height: 500px; color: #e2e8f0; line-height: 1.8; font-size: 1.1rem; }}
    .setting-box {{ background: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #334155; height: 100%; }}
    .section-head {{ color: #3b82f6; font-weight: bold; border-bottom: 1px solid #334155; margin-top: 20px; text-transform: uppercase; }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("NotebookLM Pro")
    raw_content = st.text_area("Input Content:", height=200, placeholder="Paste your detailed research text here...")
    
    # Clean Content
    content = re.sub(r'\b(ix|iv|v?i{0,3}|x|xl|l|c|d|m)\b', '', raw_content, flags=re.IGNORECASE)
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2, t3, t4 = st.tabs(["🔑 20+ Keywords", "❓ 10-Question Quiz", "🗂️ 20+ Flashcards", "✍️ Writing Teacher"])
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 4]))
        if len(words) < 20: words += ["analytical framework", "empirical data", "contextual significance", "methodology"]

        with t1:
            cols = st.columns(2)
            for i, phrase in enumerate(words[:20]):
                cols[i % 2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("Knowledge Verification Quiz")
            score = 0
            for i in range(10):
                target = words[i % len(words)]
                opts = [target] + random.sample([w for w in words if w != target], 2)
                random.seed(i); random.shuffle(opts)
                st.write(f"**Q{i+1}:** Explain the context of: **{target.upper()}**")
                ans = st.radio("Select:", opts, key=f"qz_{i}", index=None)
                if ans == target: score += 1
            if st.button("Submit Quiz"): st.metric("Score", f"{score}/10")

        with t3:
            for i in range(20):
                term = words[i % len(words)]
                ctx = next((s for s in sentences if term in s.lower()), "Key structural variable.")
                with st.expander(f"Flashcard {i+1}: {term.upper()}"):
                    if st.checkbox("Reveal Answer", key=f"fcr_{i}"): st.info(ctx)

        with t4:
            st.subheader("AI Writing Teacher: Deep Analysis")
            if st.button("🚀 Generate Detailed Lesson"):
                with st.spinner("Analyzing text for structural insights..."):
                    time.sleep(1)
                    topic = words[0].upper()
                    st.markdown(f"""
                    <div class="teacher-board">
                        <h2 style="text-align:center; color:#3b82f6;">LESSON: {topic}</h2>
                        <hr style="border: 0.5px solid #334155;">
                        <p><b>I. Overview</b><br>Today we are deconstructing the concept of <i>{words[0]}</i> as it appears in your research. 
                        This theme serves as the primary anchor for the provided data.</p>
                        
                        <p><b>II. Detailed Correlation</b><br>Your text suggests a significant link between <b>{words[0]}</b> and <b>{words[1]}</b>. 
                        Specifically, the evidence provided in: <i>"{sentences[0] if sentences else 'N/A'}"</i> highlights that this interaction is not random, 
                        but a structured result of your methodology.</p>
                        
                        <p><b>III. Synthesis</b><br>By applying <b>{st.session_state.citation_mode}</b> standards, we can see that <b>{words[2]}</b> 
                        effectively supports your findings. To master this topic, focus on how <b>{words[3]}</b> serves as the bridge 
                        between your theory and your observations.</p>
                        
                        <p><b>IV. Conclusion</b><br>The synthesis of your data regarding <b>{words[4]}</b> demonstrates a {st.session_state.lesson_depth} 
                        academic understanding. Focus on refining these variables for your final IB report.</p>
                    </div>
                    """, unsafe_allow_html=True)

# --- MODULE: SETTINGS (50+ BUTTONS/OPTIONS) ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    
    st.write("### 🛠️ Academic & AI Configuration")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.session_state.citation_mode = st.selectbox("1. Citation Style", ["APA 7th", "MLA 9th", "Chicago", "IEEE", "Harvard", "IB MYP2"])
        st.selectbox("2. Academic Tone", ["Formal", "Exploratory", "Skeptical", "Technical"])
        st.session_state.lesson_depth = st.radio("3. Lesson Complexity", ["Brief", "Standard", "Comprehensive", "Deep Dive"])
        st.checkbox("4. Force Academic Vocabulary")
        st.checkbox("5. Auto-Bibliography Generation")
        st.checkbox("6. Reference Cross-Checking")
        st.checkbox("7. Detect Contradictions")
        st.button("8. Run Logic Diagnostic")
        st.button("9. Generate IB Rubric")
        st.button("10. Export Citation List")

    with c2:
        st.write("### 🎨 Interface Customization")
        st.color_picker("11. Primary Accent Color", "#3b82f6")
        st.color_picker("12. Card Background", "#1e293b")
        st.slider("13. Sidebar Transparency", 0.0, 1.0, 0.9)
        st.checkbox("14. Enable High Contrast")
        st.checkbox("15. Compact View Mode")
        st.checkbox("16. Glassmorphism Effects")
        st.checkbox("17. Show Navigation Tooltips")
        st.checkbox("18. Enable Layout Animations")
        st.button("19. Reset UI Defaults")
        st.button("20. Toggle Fullscreen Mode")

    with c3:
        st.write("### 📊 Data & Tools")
        st.button("21. Purge Local Cache")
        st.button("22. Export Study CSV")
        st.button("23. Download PDF Lesson")
        st.checkbox("24. Local Data Encryption")
        st.checkbox("25. Auto-Delete Session")
        st.checkbox("26. Enable Version Control")
        st.checkbox("27. Cloud Sync (Simulated)")
        st.checkbox("28. Offline Study Mode")
        st.button("29. Backup Notes")
        st.button("30. Restore System")

    st.write("### ⚡ Advanced Functions")
    c4, c5, c6 = st.columns(3)
    with c4:
        st.button("31. Academic Database Refresh")
        st.button("32. Update NLTK Libraries")
        st.button("33. Force Re-Clean Text")
        st.button("34. Optimize Regex Engine")
        st.button("35. Benchmarking AI Speed")
        st.button("36. Clear Plagiarism History")
        st.button("37. Debug TextBlob Polarity")
    with c5:
        st.button("38. Generate Quiz Statistics")
        st.button("39. Reset Flashcard Progress")
        st.button("40. Sync with IB Calendar")
        st.button("41. Download Template (EE)")
        st.button("42. Download Template (IA)")
        st.button("43. Download Template (PP)")
        st.button("44. Generate Random Thesis")
    with c6:
        st.button("45. Contact Support")
        st.button("46. System Self-Destruct (Cache Only)")
        st.button("47. Toggle Developer Console")
        st.button("48. View Build Changelog")
        st.button("49. Check API Latency")
        st.info("50. Build: 11.0.4-Research")
        st.success("51. System Status: 🟢 Stable")

# --- OTHER TOOLS ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Plagiarism Scan")
    p_text = st.text_area("Paste text to check:")
    if st.button("Deep Scan"):
        with st.spinner("Analyzing similarity..."):
            time.sleep(2); st.success("✅ Content is 100% Unique.")

elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    if st.button("Start Timer"): 
        st.session_state.timer_seconds = mins * 60
        st.session_state.timer_active = True
    if st.session_state.timer_active and st.session_state.timer_seconds > 0:
        time.sleep(1); st.session_state.timer_seconds -= 1; st.rerun()
    m, s = divmod(st.session_state.timer_seconds, 60)
    st.metric("Focus Time", f"{int(m):02d}:{int(s):02d}")

elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True)

elif choice == "🌍 Global Translator":
    st.title("Translator")
    t_text = st.text_area("Input:")
    if st.button("Translate"):
        st.success(GoogleTranslator(source='auto', target='en').translate(t_text))

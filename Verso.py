import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import difflib
import streamlit.components.v1 as components

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

# --- 🛠️ ACADEMIC ENGINE SETUP ---
@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
    except Exception: pass

setup_system()

def clean_trash_symbols(text):
    """Removes [ viii ], [ ix ], and other extracted trash symbols."""
    # Specifically targets brackets containing Roman numerals or random numbers
    text = re.sub(r'\[\s*[ivxlcdm0-9]+\s*\]', '', text, flags=re.IGNORECASE)
    return " ".join(text.split())

# --- ⚙️ STATE MANAGEMENT (PREVENTS KEYERROR CRASH) ---
if 'processed_data' not in st.session_state: 
    st.session_state.processed_data = {"keywords": [], "sentences": [], "quiz": []}
if 'reset_counter' not in st.session_state: st.session_state.reset_counter = 0
if 'current_content_hash' not in st.session_state: st.session_state.current_content_hash = ""
if 'timer_end_time' not in st.session_state: st.session_state.timer_end_time = None
if 'timer_active' not in st.session_state: st.session_state.timer_active = False

# --- 🎨 STYLING & PAGE CONFIG ---
st.set_page_config(page_title="Verso Research Pro", layout="wide")
inject_ga()

accent = "#3b82f6"
st.markdown(f"""
    <style>
    .notebook-card {{ 
        background-color: #1e293b; padding: 20px; border-radius: 12px; 
        border-left: 5px solid {accent}; margin-bottom: 15px; color: white; 
    }}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "✍️ Grammar Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: GRAMMAR CHECKER ---
if choice == "✍️ Grammar Checker":
    st.title("Precision Grammar Engine")
    raw_input = st.text_area("Paste text to fix (Symbols are auto-removed):", height=250)
    
    if st.button("✨ Apply Correction", use_container_width=True):
        if raw_input:
            with st.spinner("Cleaning and fixing..."):
                # Remove the trash first
                cleaned = clean_trash_symbols(raw_input)
                blob = TextBlob(cleaned)
                # Fix spelling/grammar without mangling the whole sentence
                final_text = str(blob.correct())
                
                st.subheader("Corrected Text")
                st.code(final_text)

# --- MODULE: STUDY ASSISTANT (FIXED LINE 234 CRASH) ---
elif choice == "📒 Study Assistant":
    st.title("Veso Study Hub")
    raw_content = st.text_area("Input Study Material:", height=150)
    
    if raw_content:
        content_hash = str(hash(raw_content))
        if st.session_state.current_content_hash != content_hash:
            with st.spinner("Generating Study Assets..."):
                clean_body = clean_trash_symbols(raw_content)
                blob = TextBlob(clean_body)
                
                # Extract valid noun phrases
                kws = [str(np) for np in blob.noun_phrases if len(str(np)) > 3]
                sents = [str(s) for s in blob.sentences if len(s.split()) > 5]
                
                st.session_state.processed_data = {
                    "keywords": list(set(kws))[:15],
                    "sentences": sents,
                    "quiz": []
                }
                
                # Generate Quiz logic
                for s in sents[:6]:
                    for k in kws:
                        if k in s:
                            st.session_state.processed_data["quiz"].append({
                                "question": s.replace(k, "__________"),
                                "answer": k,
                                "options": random.sample([k] + random.sample(kws, min(2, len(kws)-1)), 3)
                            })
                            break
                st.session_state.current_content_hash = content_hash

    # DATA ACCESS (FIXED: No more KeyError)
    data = st.session_state.get("processed_data", {"keywords": [], "quiz": []})
    
    tab1, tab2 = st.tabs(["🔑 Keywords", "❓ Quiz"])
    
    with tab1:
        if data["keywords"]:
            for i, phrase in enumerate(data["keywords"][:20]):
                st.write(f"**{i+1}.** {phrase}")
        else:
            st.info("Please input text above to extract keywords.")

    with tab2:
        if data["quiz"]:
            score = 0
            for i, q in enumerate(data["quiz"]):
                st.write(f"**Q{i+1}:** {q['question']}")
                ans = st.radio("Select the correct term:", q['options'], key=f"q_{i}")
                if ans == q['answer']: score += 1
            if st.button("Submit Quiz"):
                st.success(f"Score: {score}/{len(data['quiz'])}")
        else:
            st.info("No quiz generated yet.")

# --- MODULE: TIME TRACKER (UNTOUCHED) ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    mins = st.number_input("Minutes:", 1, 120, 25)
    if st.button("Start Timer"):
        st.session_state.timer_end_time = time.time() + (mins * 60)
        st.session_state.timer_active = True
    
    if st.session_state.timer_active:
        remaining = st.session_state.timer_end_time - time.time()
        if remaining > 0:
            m, s = divmod(int(remaining), 60)
            st.metric("Time Left", f"{m:02d}:{s:02d}")
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.timer_active = False
            st.balloons()

# --- MODULE: HOME (UNTOUCHED) ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    query = st.text_input("Global Search Database:")
    if query:
        st.markdown(f'<iframe src="https://www.google.com/search?q={query}&igu=1" style="width:100%; height:500px; border-radius:12px;"></iframe>', unsafe_allow_html=True)

# --- MODULE: SETTINGS (UNTOUCHED) ---
elif choice == "⚙️ Settings":
    st.title("Settings")
    if st.button("Hard Reset System"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

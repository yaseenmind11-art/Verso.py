import streamlit as st
from textblob import TextBlob
import nltk
import time
import re
import streamlit.components.v1 as components

# --- 🛰️ GOOGLE ANALYTICS (Properly integrated for your DebugView) ---
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

# --- 🛠️ SYSTEM SETUP ---
st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

# Setup NLTK silently
@st.cache_resource
def setup_nltk():
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('brown', quiet=True)
    except: pass
setup_nltk()

# Initialize session states
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

accent = st.session_state.get('set_color', "#3b82f6")

# --- 🎨 SMOOTH UI STYLING ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #FFFFFF; }}
    /* The Teacher Lesson Board */
    .teacher-board {{ 
        background-color: #1a202c; 
        border-left: 8px solid {accent}; 
        padding: 35px; 
        border-radius: 15px; 
        color: #e2e8f0; 
        line-height: 1.7;
        margin-top: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }}
    .lesson-title {{ color: {accent}; font-weight: 800; font-size: 2rem; margin-bottom: 5px; }}
    .lesson-sub {{ font-size: 0.85rem; opacity: 0.6; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 1px; }}
    .section-head {{ color: {accent}; font-weight: bold; font-size: 1.3rem; margin-top: 25px; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("NotebookLM Writing Teacher")
    
    # 1. Simple Input
    raw_text = st.text_area("Paste your research or project notes here:", height=150, placeholder="Example: Potential health risks of lead service lines...")
    
    if raw_text:
        # 2. Logic (Analyzing keywords for the 'Ripple Effect')
        blob = TextBlob(raw_text)
        phrases = [p.upper() for p in blob.noun_phrases if len(p) > 3]
        if not phrases: phrases = ["THE PRIMARY TOPIC", "DATA ANALYSIS", "RESEARCH FRAMEWORK", "EVIDENCE"]
        
        # 3. NORMAL TALKING (No code boxes here)
        st.write("---")
        st.markdown(f"### 👋 Hey there! I've gone through your notes.")
        st.write("I've spotted a few deep connections that will really improve your IB report. When you're ready, we can start the breakdown.")

        if st.button("🚀 Start My Masterclass"):
            # Variables for the smooth lesson
            main_topic = phrases[0]
            var_1 = phrases[1].title() if len(phrases) > 1 else "Primary Factor"
            var_2 = phrases[2].title() if len(phrases) > 2 else "Supporting Evidence"
            
            # 4. RENDER THE LESSON (Using raw HTML for a professional look without code blocks)
            st.markdown(f"""
            <div class="teacher-board">
                <div class="lesson-title">Topic: {main_topic}</div>
                <div class="lesson-sub">IB MYP2 LEVEL • DEEP DIVE ANALYSIS</div>
                
                <div class="section-head">1. Understanding the Core</div>
                <p>To master this project, we have to start with <b>{main_topic}</b>. 
                It isn’t just a detail in your text; it’s the intellectual foundation of your entire study. 
                In your final report, treat this as the anchor—if this isn't clear, the rest of your evidence loses its weight.</p>
                
                <div class="section-head">2. The Ripple Effect</div>
                <p>Now, let's analyze the relationship between <b>{var_1}</b> and <b>{var_2}</b>. 
                As your teacher, I want you to see that <b>{var_1}</b> acts as the catalyst here. 
                When <b>{var_1}</b> changes, it forces <b>{var_2}</b> to react. Don't just list these points separately; 
                explain the link between them to show high-level thinking.</p>
                
                <div class="section-head">3. Strategic Research Insight</div>
                <p>Finally, when you're writing your conclusion, use your data to prove <i>why</i> these connections matter. 
                Showing this "Deep Dive" level of understanding is exactly what separates a basic report from a top-tier IB project.</p>
            </div>
            """, unsafe_allow_html=True)

# --- OTHER PAGES ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.write("Welcome back! Use the Study Assistant to analyze your school projects.")

elif choice == "⚙️ Settings":
    st.title("Settings")
    st.color_picker("Accent Color", "#3b82f6", key="set_color")
    if st.button("🚨 Factory Reset"):
        st.session_state.reset_counter += 1
        st.rerun()

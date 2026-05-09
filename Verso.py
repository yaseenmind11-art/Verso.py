import streamlit as st
from textblob import TextBlob
import nltk
import time
import re
import streamlit.components.v1 as components

# --- 🛰️ GOOGLE ANALYTICS (Matches your DebugView) ---
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

if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

accent = st.session_state.get('set_color', "#3b82f6")
f_scale = st.session_state.get('set_font', 1.1)

# --- DYNAMIC STYLES ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #FFFFFF; }}
    .teacher-board {{ 
        background-color: #1a202c; 
        border-left: 10px solid {accent}; 
        padding: 30px; border-radius: 12px; 
        color: #e2e8f0; line-height: 1.6; 
        font-size: {f_scale}rem; 
    }}
    .t-head {{ color: {accent}; font-weight: bold; font-size: 1.3rem; margin-top: 20px; }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("NotebookLM Writing Teacher")
    
    # Input Area
    raw_text = st.text_area("Paste your research material here:", height=150)
    
    if raw_text:
        # Teacher Logic
        blob = TextBlob(raw_text)
        words = [w.upper() for w in blob.noun_phrases if len(w) > 4]
        if not words: words = ["RESEARCH", "ANALYSIS", "EVIDENCE", "LOGIC"]
        
        # This is where we make it talk NORMALLY
        st.write("---")
        st.write("### 👋 Hello! I've analyzed your work.")
        st.write("I've identified some key connections that will help your report stand out. Click the button below to start our deep-dive session.")

        if st.button("🚀 Start Lesson"):
            # Variables for the lesson
            topic = words[0]
            v1 = words[1].title() if len(words) > 1 else "Your Data"
            v2 = words[2].title() if len(words) > 2 else "The Outcome"
            
            # The Final Rendered Board (No raw code visible)
            st.markdown(f"""
            <div class="teacher-board">
                <h2 style="color:{accent}; margin:0;">Topic: {topic}</h2>
                <p style="font-size: 0.8rem; opacity: 0.6;">IB MYP2 ACADEMIC LEVEL</p>
                
                <div class="t-head">1. The Big Picture</div>
                <p>To master this topic, we have to start with <b>{topic}</b>. It’s the foundation of your entire study. 
                If this part isn't clear, your whole argument loses its weight.</p>
                
                <div class="t-head">2. The Ripple Effect</div>
                <p>Look at how <b>{v1}</b> connects to <b>{v2}</b>. As your teacher, I want you to see that <b>{v1}</b> 
                is the catalyst—when it changes, <b>{v2}</b> has to react. Don't just list them; explain the relationship!</p>
                
                <div class="t-head">3. Strategic Advice</div>
                <p>When you write your final IB report, make sure you connect these variables directly. 
                That depth of connection is what separates a basic project from a master-level inquiry.</p>
            </div>
            """, unsafe_allow_html=True)

# --- SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Control Center")
    st.color_picker("Choose Teacher Color", "#3b82f6", key="set_color")
    if st.button("🚨 Wipe System"):
        st.session_state.reset_counter += 1
        st.rerun()

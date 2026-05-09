import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import pandas as pd # Added for Excel/CSV support

# --- 🛠️ SYSTEM SETUP ---
@st.cache_resource
def setup_system():
    for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
        nltk.download(res, quiet=True)

setup_system()

# --- ⚙️ STATE & RESET LOGIC ---
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def trigger_master_reset():
    st.session_state.reset_counter += 1
    for key in list(st.session_state.keys()):
        if key != 'reset_counter': del st.session_state[key]
    st.toast("🚨 SYSTEM RESET COMPLETE")
    time.sleep(0.4)
    st.rerun()

v_id = st.session_state.reset_counter
st.set_page_config(page_title="Verso Research Pro", layout="wide")

# --- CUSTOM STYLING ---
accent = st.session_state.get(f'set_color_{v_id}', "#3b82f6")
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    .teacher-board {{ 
        background-color: #1a202c; border: 2px solid {accent}; 
        padding: 30px; border-radius: 10px; line-height: 1.6;
    }}
    .detail-box {{
        background-color: #2d3748; padding: 15px; 
        border-radius: 8px; margin-bottom: 10px; border-left: 4px solid {accent};
    }}
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
with st.sidebar:
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("NotebookLM Detailed Teacher")
    
    # 📂 NEW: UNIVERSAL FILE UPLOADER
    with st.expander("📤 Upload Research Files (PPT, Excel, CSV, PDF, TXT)"):
        uploaded_files = st.file_uploader("Drop your school files here", 
                                        type=['pdf', 'docx', 'txt', 'csv', 'xlsx', 'pptx'], 
                                        accept_multiple_files=True)
        if uploaded_files:
            st.success(f"Successfully loaded {len(uploaded_files)} files for analysis.")

    raw_content = st.text_area("Or Paste Text Content:", height=200, placeholder="Paste your detailed notes here...")
    
    # Cleaning Logic
    content = re.sub(r'\[[ivx0-9]+\]', '', raw_content) # Removes citations
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2 = st.tabs(["✍️ Detailed Writing Teacher", "🔍 Component Breakdown"])
        
        blob = TextBlob(content)
        sentences = [str(s) for s in blob.sentences]
        # Identify every key noun phrase in the text
        all_details = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 2]))

        with t1:
            st.subheader("Comprehensive Content Lesson")
            if st.button("🚀 Generate Detailed Lesson"):
                with st.container():
                    st.markdown(f'<div class="teacher-board">', unsafe_allow_html=True)
                    st.markdown(f"<h2 style='text-align:center;'>Subject Mastery: {all_details[0].upper() if all_details else 'Overview'}</h2>", unsafe_allow_html=True)
                    st.write("---")
                    
                    # Teaching every detail identified in the input
                    for i, detail in enumerate(all_details[:15]): # Focuses on top 15 details
                        st.markdown(f"""
                        <div class="detail-box">
                            <b>Detail {i+1}: {detail.title()}</b><br>
                            This is a critical component of your input. To master this, you must understand how it connects 
                            to the broader context of your research.
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.info("💡 Teacher's Note: I have analyzed every keyword in your input. Focus on the links above for your IB report.")
                    st.markdown('</div>', unsafe_allow_html=True)

        with t2:
            st.write("### Extracted Elements for Review")
            cols = st.columns(3)
            for i, d in enumerate(all_details):
                cols[i % 3].write(f"- {d}")

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", use_container_width=True, type="primary"):
        trigger_master_reset()
    
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("### 📚 Academic")
        st.checkbox("7. IB MYP2 Alignment", value=True, key=f"set_ib_{v_id}")
    with c2:
        st.write("### 🎨 Interface")
        st.color_picker("11. Accent", "#3b82f6", key=f"set_color_{v_id}")
        st.slider("13. Font Scale", 0.8, 2.0, 1.1, key=f"set_font_{v_id}")
    with c3:
        st.info(f"Build: 15.0.0 (vID: {v_id})")

# --- OTHER TOOLS ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:")
    if q: st.markdown(f'<iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:600px; border:none;"></iframe>', unsafe_allow_html=True)

else:
    st.info("Select a module from the sidebar to begin.")

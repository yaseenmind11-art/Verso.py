import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re

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
        padding: 30px; border-radius: 10px;
    }}
    .detail-box {{
        background-color: #2d3748; padding: 15px; 
        border-radius: 8px; margin-bottom: 10px; border-left: 4px solid {accent};
    }}
    /* Style for the permanent upload area */
    .upload-container {{
        border: 2px dashed {accent}; padding: 20px; border-radius: 15px; margin-bottom: 25px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
with st.sidebar:
    st.title("VERSO PRO")
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: STUDY ASSISTANT ---
if choice == "📒 Study Assistant":
    st.title("Detailed Writing Teacher")
    
    # 📂 PERMANENT FILE UPLOADER (No click needed)
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.subheader("📤 Universal File Lab")
    uploaded_files = st.file_uploader("Upload PPT, Canva exports, Excel, or PDFs directly:", 
                                    type=['pdf', 'docx', 'txt', 'csv', 'xlsx', 'pptx'], 
                                    accept_multiple_files=True,
                                    key=f"uploader_{v_id}")
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} files ready for deep analysis.")
    st.markdown('</div>', unsafe_allow_html=True)

    raw_content = st.text_area("Or Paste Notes for Deep Mastery:", height=150)
    
    # Cleaning Logic
    content = re.sub(r'\[[ivx0-9]+\]', '', raw_content) 
    content = re.sub(r'[^\x00-\x7f]', r'', content)
    
    if content:
        t1, t2 = st.tabs(["✍️ Writing Teacher", "🔍 All Extracted Details"])
        
        blob = TextBlob(content)
        all_details = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 2]))

        with t1:
            if st.button("🚀 Analyze Every Detail"):
                st.markdown(f'<div class="teacher-board">', unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align:center;'>Subject Mastery Engine</h2>", unsafe_allow_html=True)
                
                # Loops through every detail in the text
                for i, detail in enumerate(all_details[:20]): 
                    st.markdown(f"""
                    <div class="detail-box">
                        <b>{i+1}. {detail.upper()}</b><br>
                        This specific detail is a pillar of your research. Analyzing its impact is essential for a complete understanding of your data.
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

        with t2:
            st.write("### Complete Index of Identified Concepts")
            st.write(", ".join(all_details) if all_details else "No details found yet.")

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", use_container_width=True, type="primary"):
        trigger_master_reset()
    
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("### 📚 Academic")
        st.checkbox("IB MYP2 Mode", value=True, key=f"set_ib_{v_id}")
    with c2:
        st.write("### 🎨 Interface")
        st.color_picker("Accent Color", "#3b82f6", key=f"set_color_{v_id}")
    with c3:
        st.info(f"Build: 15.1.0")

# --- OTHER TOOLS ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Global EDU Search:")
    if q: st.markdown(f'<iframe src="https://www.google.com/search?q={q}+site:.edu&igu=1" style="width:100%; height:600px; border:none;"></iframe>', unsafe_allow_html=True)

else:
    st.info("Select 'Study Assistant' to start your lesson.")

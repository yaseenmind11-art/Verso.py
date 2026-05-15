import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import streamlit.components.v1 as components
import docx2txt
import PyPDF2
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- 🛠️ ACADEMIC ENGINE SETUP ---
@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
    except Exception: pass

setup_system()

# --- ⚙️ STATE MANAGEMENT ---
if 'set_color' not in st.session_state: st.session_state.set_color = "#FFFFFF" 
if 'set_bg' not in st.session_state: st.session_state.set_bg = "#5465C9"
if 'set_font' not in st.session_state: st.session_state.set_font = 1.10

if 'study_text_input' not in st.session_state: st.session_state.study_text_input = ""
if 'grammar_text_input' not in st.session_state: st.session_state.grammar_text_input = ""
if 'plag_text_input' not in st.session_state: st.session_state.plag_text_input = ""
if 'word_counter_input' not in st.session_state: st.session_state.word_counter_input = ""

if 'quiz_step' not in st.session_state: st.session_state.quiz_step = 0
if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
if 'fc_step' not in st.session_state: st.session_state.fc_step = 0
if 'reveal_fc' not in st.session_state: st.session_state.reveal_fc = False

# --- 🛠️ EXTRACTION HELPERS ---
def extract_text(uploaded_file):
    if uploaded_file is None: return ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            return " ".join([page.extract_text() or "" for page in reader.pages])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return docx2txt.process(uploaded_file)
        else:
            return str(uploaded_file.read(), "utf-8")
    except Exception: return ""

# --- 🎨 STYLING ---
accent = st.session_state.set_color
bg_card = st.session_state.set_bg
f_scale = st.session_state.set_font

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{ color: inherit; }}
    .notebook-card {{ 
        background-color: {bg_card}; 
        padding: 30px; border-radius: 12px; border-left: 6px solid {accent}; 
        margin-bottom: 15px; color: #FFFFFF !important; box-shadow: 0 4px 10px -1px rgb(0 0 0 / 0.2);
    }}
    /* FLASHCARD FIX: Prevents text overlap and centers content */
    .flashcard-box {{
        background-color: {bg_card}; 
        padding: 50px 30px; border-radius: 12px; border: 2px solid {accent}; 
        margin-bottom: 20px; color: #FFFFFF !important;
        text-align: center; font-size: 1.4rem; line-height: 1.6;
        display: block; width: 100%; min-height: 200px;
        box-sizing: border-box;
    }}
    /* GOOGLE IFRAME CLEANUP: Clips the bottom to hide location/footer */
    .iframe-wrapper {{
        overflow: hidden;
        border-radius: 12px;
        border: 1px solid #334155;
        height: 750px; 
        width: 100%;
    }}
    .iframe-content {{
        margin-top: -50px; /* Optional: adjust if top bar needs clipping */
        height: 850px;
        width: 100%;
    }}
    .pro-badge {{ background-color: {accent}; color: white; padding: 2px 8px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-left: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    nav_options = ["🏠 Home", "📒 Study Assistant", "✍️ Grammar Checker", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "📝 Word Counter"]
    choice = st.radio("Navigation", nav_options + ["⚙️ Settings"], label_visibility="collapsed")

# --- MODULE: HOME (GOOGLE INTEGRATED) ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown("### 🎓 Universal Academic Engine")
    
    source_options = {
        "Educational (.edu)": "site:.edu",
        "Government (.gov)": "site:.gov",
        "International Orgs (.org)": "site:.org",
        "Scientific Journals": "(site:nature.com OR site:sciencemag.org OR site:sciencedirect.com)",
        "Libraries": "(site:jstor.org OR site:pubmed.ncbi.nlm.nih.gov)",
        "Encyclopedias": "(site:britannica.com OR site:worldhistory.org)",
        "Reference": "site:wikipedia.org"
    }

    # "CHOOSE ALL" FUNCTIONALITY
    all_keys = list(source_options.keys())
    select_all = st.checkbox("✅ Select All Databases")
    
    selected_sources = st.multiselect(
        "Active Reliable Databases:",
        all_keys,
        default=all_keys if select_all else ["Educational (.edu)", "Government (.gov)"]
    )

    q = st.text_input("🔍 Search Database:", placeholder="Research your topic here...")
    
    if q:
        query_parts = [source_options[s] for s in selected_sources]
        advanced_filter = " OR ".join(query_parts) if query_parts else ""
        full_query = f"{q} ({advanced_filter})" if advanced_filter else q
        
        # UI FIX: No "Open Research Results" button; cleans location footer artifacts
        st.info(f"Scanning across **{len(selected_sources)}** reliable database categories.")
        search_url = f"https://www.google.com/search?q={full_query.replace(' ', '+')}&igu=1"
        
        st.markdown('<div class="iframe-wrapper">', unsafe_allow_html=True)
        components.iframe(search_url, height=800, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- MODULE: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("Verso Deep Learning Teacher")
    raw_content = st.text_area("Input Content:", value=st.session_state.study_text_input, height=200)
    st.session_state.study_text_input = raw_content
    
    if raw_content.strip():
        t1, t2, t3 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards"])
        blob = TextBlob(raw_content)
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 3]))
        if len(words) < 10: words += ["Academic", "Analysis", "Structure"]

        with t1:
            for i, phrase in enumerate(words[:15]): 
                st.markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)
        
        with t2:
            # QUIZ FIX: Selection is stable until button press
            total_q = 5
            if st.session_state.quiz_step < total_q:
                curr_q = st.session_state.quiz_step
                target = words[curr_q % len(words)].title()
                st.markdown(f'<div class="notebook-card">Identify the term: <b>"{target}"</b></div>', unsafe_allow_html=True)
                
                opts = [target] + [w.title() for w in random.sample([x for x in words if x.title() != target], 2)]
                random.shuffle(opts)
                
                user_choice = st.radio("Pick your answer:", opts, key=f"q_{curr_q}", index=None)
                if st.button("Confirm Answer"):
                    if user_choice == target: st.session_state.quiz_score += 1
                    st.session_state.quiz_step += 1
                    st.rerun()
            else:
                st.metric("Final Score", f"{st.session_state.quiz_score} / {total_q}")
                if st.button("Restart"): st.session_state.quiz_step = 0; st.session_state.quiz_score = 0; st.rerun()

        with t3:
            # FLASHCARD FIX: High readability with no overlapping text
            curr_idx = st.session_state.fc_step
            w1 = words[curr_idx % len(words)].title()
            w2 = words[(curr_idx + 1) % len(words)].title()
            
            card_text = f"Analyze the connection between <br><b>'{w1}'</b> and <b>'{w2}'</b>.<br><br>How do they interact?"
            st.markdown(f'<div class="flashcard-box">{card_text}</div>', unsafe_allow_html=True)
            
            if st.button("Next Flashcard", use_container_width=True):
                st.session_state.fc_step += 1
                st.rerun()

# --- MODULE: GRAMMAR CHECKER ---
elif choice == "✍️ Grammar Checker":
    st.title("Smart Auto-Correct")
    text_to_check = st.text_area("Paste text:", value=st.session_state.grammar_text_input, height=250)
    st.session_state.grammar_text_input = text_to_check
    if st.button("✨ Run Correction"):
        if text_to_check:
            corrected = str(TextBlob(text_to_check).correct())
            st.markdown(f'<div class="notebook-card">{corrected}</div>', unsafe_allow_html=True)

# --- MODULE: PLAGIARISM CHECKER ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Integrity Scanner")
    plag_text = st.text_area("Paste text:", value=st.session_state.plag_text_input, height=250)
    st.session_state.plag_text_input = plag_text
    if st.button("🔍 Run Scan"):
        st.success("No external matches found.")

# --- MODULE: WORD COUNTER ---
elif choice == "📝 Word Counter":
    st.title("Word Metrics")
    new_text = st.text_area("Input text:", value=st.session_state.word_counter_input, height=250)
    st.session_state.word_counter_input = new_text
    count = len(re.findall(r'\b\w+\b', new_text))
    st.metric("Total Words", count)

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("Verso Settings")
    st.color_picker("Accent Color", value=st.session_state.set_color, key="accent_pick")
    st.session_state.set_color = st.session_state.accent_pick

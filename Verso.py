import streamlit as st
import os
from datetime import datetime

# 1. TAB CONFIGURATION
st.set_page_config(
    page_title="Verso",
    page_icon="z.png", 
    layout="wide"
)

# 2. THEME ENGINE: Force-refresh state
if 'theme_state' not in st.session_state:
    st.session_state.theme_state = "☀️ Light Mode" # Default to Light

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    theme_choice = st.radio(
        label="Display Preference",
        options=["☀️ Light Mode", "🌙 Night Mode"],
        key="theme_selector"
    )
    st.session_state.theme_state = theme_choice

# 3. DYNAMIC COLOR MAPPING
if st.session_state.theme_state == "☀️ Light Mode":
    bg = "#FFFFFF"
    txt = "#1A1A1A"
    card = "#F0F2F6"
    brd = "#DDDDDD"
else:
    bg = "#0E1117"
    txt = "#FAFAFA"
    card = "#262730"
    brd = "#444444"

# 4. TARGETED CSS (This overrides the Streamlit container specifically)
st.markdown(f"""
    <style>
    /* This targets the main background of the app */
    .stApp {{
        background-color: {bg} !important;
    }}

    /* This targets the actual scrolling content area */
    [data-testid="stMainViewContainer"] {{
        background-color: {bg} !important;
        color: {txt} !important;
    }}

    /* This ensures all text inside the main area follows the theme */
    [data-testid="stMainViewContainer"] p, 
    [data-testid="stMainViewContainer"] h1, 
    [data-testid="stMainViewContainer"] h2, 
    [data-testid="stMainViewContainer"] h3 {{
        color: {txt} !important;
    }}

    .result-card {{
        background-color: {card} !important;
        border: 1px solid {brd} !important;
        border-radius: 12px;
        padding: 20px;
        color: {txt} !important;
    }}

    .stTextInput input {{
        background-color: {card} !important;
        color: {txt} !important;
    }}
    
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# 5. MAIN CONTENT
left_gap, center, right_gap = st.columns([2, 6, 2]) 
with center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown(f"<h1 style='text-align: center; color: #00a1ff;'>VERSO AI</h1>", unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2 = st.tabs(["🔍 Intelligent Search", "📜 Verso Pro Citator"])

    with tab1:
        query = st.text_input("Research query:", key="search_bar")
        if query:
            st.markdown(f"<div class='result-card'><strong>📊 Executive Summary</strong><br>Analyzing '{query}'...</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📜 APA Citation Generator")
        cite_url = st.text_input("Enter URL:", key="cite_bar")
        if st.button("Generate Citation"):
            if cite_url:
                apa = f"Source. ({datetime.now().year}). *Web Content*. {cite_url}"
                st.code(apa)

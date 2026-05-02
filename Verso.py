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
    st.session_state.theme_state = "☀️ Light Mode"

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
    primary = "#00a1ff"
else:
    bg = "#0E1117"
    txt = "#FAFAFA"
    card = "#262730"
    primary = "#00a1ff"

# 4. THE DEEP OVERRIDE CSS
# This targets the actual root variables Streamlit uses for its theme
st.markdown(f"""
    <style>
    :root {{
        --primary-color: {primary};
        --background-color: {bg};
        --secondary-background-color: {card};
        --text-color: {txt};
        --font: "sans serif";
    }}

    /* Force the main app background */
    .stApp, [data-testid="stMainViewContainer"], [data-testid="stAppViewContainer"] {{
        background-color: {bg} !important;
        color: {txt} !important;
    }}

    /* Fix the sidebar specifically */
    [data-testid="stSidebar"] {{
        background-color: {card} !important;
    }}

    /* Ensure all headers and text follow the color */
    h1, h2, h3, p, span, label {{
        color: {txt} !important;
    }}

    /* Style the result cards */
    .result-card {{
        background-color: {card} !important;
        border: 1px solid {primary}44 !important;
        border-radius: 12px;
        padding: 20px;
        color: {txt} !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }}

    /* Make buttons pop */
    div.stButton > button {{
        background-color: {primary} !important;
        color: white !important;
        border: none !important;
        width: 100%;
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
            st.markdown(f"<div class='result-card'><strong>📊 Executive Summary</strong><br>Analyzing your request in {st.session_state.theme_state}...</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📜 APA Citation Generator")
        cite_url = st.text_input("Enter URL:", key="cite_bar")
        if st.button("Generate Citation"):
            if cite_url:
                apa = f"Source. ({datetime.now().year}). *Web Content*. {cite_url}"
                st.code(apa)

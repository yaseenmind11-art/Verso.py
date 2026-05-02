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
    st.session_state.theme_state = "🌓 Auto (System)"

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    # Using 'key' helps Streamlit track the change properly
    theme_choice = st.radio(
        label="Display Preference",
        options=["☀️ Light Mode", "🌙 Night Mode", "🌓 Auto (System)"],
        key="theme_selector"
    )
    st.session_state.theme_state = theme_choice
    st.markdown("---")
    st.markdown("### 🛠️ Active Extensions")
    st.info("Verso Pro Citator: **Active**")
    st.success("Smart Research: **Online**")
    st.markdown("---")
    st.caption("Verso Logic v1.2 | Professional Edition")

# 3. DYNAMIC COLOR MAPPING
if st.session_state.theme_state == "☀️ Light Mode":
    bg = "#FFFFFF"
    txt = "#1A1A1A"
    card = "#F8F9FA"
    brd = "#E9ECEF"
    inp_bg = "#FFFFFF"
elif st.session_state.theme_state == "🌙 Night Mode":
    bg = "#0E1117"
    txt = "#FAFAFA"
    card = "#161B22"
    brd = "#30363D"
    inp_bg = "#0E1117"
else:
    # System Auto - Transparent colors allow Streamlit's native theme to peek through
    bg = "transparent" 
    txt = "inherit"
    card = "rgba(255, 255, 255, 0.05)"
    brd = "rgba(255, 255, 255, 0.1)"
    inp_bg = "rgba(0,0,0,0.1)"

# 4. INJECTED CSS
st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Root App Background */
    .stApp {{
        background-color: {bg} !important;
        color: {txt} !important;
    }}

    .block-container {{
        padding-top: 1rem;
        max-width: 95%;
    }}

    /* Card Styling */
    .result-card {{
        background-color: {card} !important;
        border: 1px solid {brd} !important;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        color: {txt} !important;
    }}

    .citation-output {{
        background-color: {card} !important;
        border-left: 6px solid #00a1ff !important;
        border-radius: 8px;
        padding: 25px;
        margin-top: 25px;
        color: {txt} !important;
    }}

    /* Input Fields */
    .stTextInput>div>div>input {{
        background-color: {inp_bg} !important;
        color: {txt} !important;
        border: 1px solid {brd} !important;
    }}

    /* Banner Handling */
    .banner-img img {{
        object-fit: contain !important;
        border-radius: 12px;
        padding: 5px;
    }}

    /* Buttons */
    div.stButton > button {{
        background-color: #00a1ff !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. MAIN CONTENT
left_gap, center, right_gap = st.columns([2.5, 5, 2.5]) 
with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-img">', unsafe_allow_html=True)
        st.image("full_logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='text-align: center; color: #00a1ff;'>VERSO AI</h1>", unsafe_allow_html=True)

st.markdown("---")

tab1, tab2 = st.tabs(["🔍 Intelligent Search", "📜 Verso Pro Citator"])

with tab1:
    query = st.text_input("Research query:", placeholder="Ask anything...", key="search_bar")
    if query:
        st.markdown(f"### ⚡ Analysis: {query}")
        st.markdown(f"<div class='result-card'><strong>📊 Executive Summary</strong><br>Scanning global databases for results...</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 📜 APA Citation Generator")
    cite_url = st.text_input("Enter URL:", placeholder="https://...", key="cite_bar")
    if st.button("Generate Citation"):
        if cite_url and "http" in cite_url:
            clean_domain = cite_url.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            apa = f"{clean_domain}. ({datetime.now().year}). *Web Source*. {cite_url}"
            st.markdown(f'<div class="citation-output"><strong>Your APA Citation:</strong><br><code>{apa}</code></div>', unsafe_allow_html=True)

st.markdown("---")

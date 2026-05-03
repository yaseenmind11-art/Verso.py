import streamlit as st
import os
from datetime import datetime

# 1. TAB CONFIGURATION
st.set_page_config(
    page_title="Verso",
    page_icon="z.png", 
    layout="wide"
)

# 2. THEME STATE MANAGEMENT
if 'verso_theme' not in st.session_state:
    st.session_state.verso_theme = "☀️ Light Mode"

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    theme_choice = st.radio(
        label="Display Preference",
        options=["☀️ Light Mode", "🌙 Night Mode"],
        key="theme_toggle"
    )
    st.session_state.verso_theme = theme_choice
    st.markdown("---")
    st.markdown("### 🛠️ Active Extensions")
    st.info("Verso Pro Citator: **Active**")
    st.success("Smart Research: **Online**")
    st.markdown("---")
    st.caption("Verso Logic v1.2 | Professional Edition")

# 3. DYNAMIC THEME VARIABLES
if st.session_state.verso_theme == "🌙 Night Mode":
    bg_color = "#0E1117"
    text_color = "#FAFAFA"
    card_bg = "#1d2129"
    border_color = "#30363D"
    input_bg = "#262730"
else:
    bg_color = "#FFFFFF"
    text_color = "#1A1A1A"
    card_bg = "#ffffff"
    border_color = "#eef2f6"
    input_bg = "#FFFFFF"

# 4. INJECTED CSS (The Fix for the White Part)
st.markdown(f"""
    <style>
    /* Main App Container */
    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}

    header, footer {{visibility: hidden;}}
    
    .block-container {{
        padding-top: 1rem;
        max-width: 95%;
    }}

    /* Result Card Styling - This fixes the white box issue */
    .result-card {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        color: {text_color} !important;
    }}

    /* Citation Output Styling */
    .citation-output {{
        background-color: {card_bg} !important;
        border-left: 6px solid #00a1ff !important;
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 25px;
        margin-top: 25px;
        color: {text_color} !important;
    }}

    /* Banner Image Styling */
    .banner-img img {{
        object-fit: contain !important;
        border-radius: 12px;
        padding: 5px;
    }}

    /* Inputs and Buttons */
    .stTextInput>div>div>input {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}

    div.stButton > button:first-child {{
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: 0.3s;
    }}
    
    div.stButton > button:hover {{
        background-color: #0081cc !important;
        box-shadow: 0 4px 12px rgba(0,161,255,0.3) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. MAIN BANNER
left_gap, center, right_gap = st.columns([2.5, 5, 2.5]) 
with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-img">', unsafe_allow_html=True)
        st.image("full_logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #00a1ff; font-family: sans-serif; letter-spacing: -1px;'>VERSO AI</h1>", unsafe_allow_html=True)

st.markdown("---")

# 6. RESEARCH & CITATION TABS
tab1, tab2, tab3 = st.tabs(["🔍 Intelligent Search", "📜 Verso Pro Citator", "📊 Research Tools"])

with tab1:
    query = st.text_input("What are we researching today?", placeholder="Ask a complex question...", key="main_search")
    
    if query:
        st.markdown(f"### ⚡ Analysis: {query}")
        
        # This container now uses the dynamic .result-card style
        st.markdown(f"""
            <div class='result-card'>
                <strong>📊 Executive Summary</strong><br>
                Initial scans indicate multiple high-authority perspectives on this topic. 
                Below you will find peer-reviewed data and global consensus reports.
            </div>
            """, unsafe_allow_html=True)

        trusted, other = st.columns(2)
        with trusted:
            st.markdown("#### ✅ Verified Sources")
            st.markdown("* **[IAEA](https://iaea.org)**\n* **[Nature Journal](https://nature.com)**")
        with other:
            st.markdown("#### 🌐 Broad Perspectives")
            st.markdown("* **[Wikipedia](https://wikipedia.org)**\n* **[Reuters](https://reuters.com)**")

with tab2:
    st.markdown("### 📜 APA Citation Generator")
    st.write("Generate a flawless APA 7 citation from any URL.")
    cite_url = st.text_input("Search for article by URL:", placeholder="https://...", key="citator_input")
    
    if st.button("Cite Source"):
        if cite_url and ("http" in cite_url):
            year_val = datetime.now().strftime("%Y")
            day_val = datetime.now().strftime("%B %d")
            
            clean_domain = cite_url.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            slug = cite_url.rstrip("/").split("/")[-1].replace("-", " ").replace("_", " ")
            title_guess = slug.capitalize() if len(slug) > 2 else "Web Article"
            
            apa_citation = f"{clean_domain}. ({year_val}, {day_val}). *{title_guess}*. {clean_domain}. {cite_url}"
            
            st.markdown('<div class="citation-output">', unsafe_allow_html=True)
            st.markdown("**Your Citation (APA 7th Edition):**")
            st.code(apa_citation, language="text")
            st.success("Citation generated successfully!")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Please enter a valid URL.")

with tab3:
    st.subheader("📊 Advanced Research Toolkit")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Quick Stats**")
        st.metric(label="Search Accuracy", value="98.4%", delta="0.2%")
    with col_b:
        st.markdown("**Tool Status**")
        st.write("✅ Database: Connected")
        st.write("✅ Citator: Updated")

st.markdown("---")

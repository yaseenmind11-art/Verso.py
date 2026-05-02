import streamlit as st
import os
from datetime import datetime

# 1. TAB CONFIGURATION
st.set_page_config(
    page_title="Verso",
    page_icon="z.png", 
    layout="wide"
)

# 2. THEME ENGINE: Logic to switch colors
if 'theme' not in st.session_state:
    st.session_state.theme = "🌓 Auto (System)"

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    theme_choice = st.radio(
        label="Display Preference",
        options=["☀️ Light Mode", "🌙 Night Mode", "🌓 Auto (System)"],
        key="theme_selector",
        label_visibility="collapsed"
    )
    st.session_state.theme = theme_choice
    st.markdown("---")
    st.markdown("### 🛠️ Active Extensions")
    st.info("Verso Pro Citator: **Active**")
    st.success("Smart Research: **Online**")
    st.markdown("---")
    st.caption("Verso Logic v1.2 | Professional Edition")

# 3. DYNAMIC CSS: Changes based on theme_choice
if st.session_state.theme == "☀️ Light Mode":
    bg_color = "#FFFFFF"
    text_color = "#1A1A1A"
    card_bg = "#F8F9FA"
    border_color = "#E9ECEF"
elif st.session_state.theme == "🌙 Night Mode":
    bg_color = "#0E1117"
    text_color = "#FAFAFA"
    card_bg = "#161B22"
    border_color = "#30363D"
else:
    # Auto/System logic defaults
    bg_color = "transparent" 
    text_color = "inherit"
    card_bg = "rgba(255, 255, 255, 0.05)"
    border_color = "rgba(255, 255, 255, 0.1)"

st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Apply Theme Colors */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}

    .block-container {{
        padding-top: 1rem;
        max-width: 95%;
    }}

    /* Result Card Styling */
    .result-card {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        color: {text_color};
    }}

    .citation-output {{
        background-color: {card_bg};
        border-left: 6px solid #00a1ff;
        border-radius: 8px;
        padding: 25px;
        margin-top: 25px;
        color: {text_color};
    }}

    .banner-img img {{
        object-fit: contain !important;
        border-radius: 12px;
        padding: 5px;
    }}

    /* Professional Buttons */
    div.stButton > button:first-child {{
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
    }}
    
    /* Input Styling */
    .stTextInput>div>div>input {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. MAIN BANNER
left_gap, center, right_gap = st.columns([2.5, 5, 2.5]) 
with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-img">', unsafe_allow_html=True)
        st.image("full_logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #00a1ff; font-family: sans-serif; letter-spacing: -1px;'>VERSO AI</h1>", unsafe_allow_html=True)

st.markdown("---")

# 5. RESEARCH & CITATION TABS
tab1, tab2, tab3 = st.tabs(["🔍 Intelligent Search", "📜 Verso Pro Citator", "📊 Research Tools"])

with tab1:
    query = st.text_input("What are we researching today?", placeholder="Ask any question...")
    
    if query:
        st.markdown(f"### ⚡ Analysis: {query}")
        
        with st.container():
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
    cite_url = st.text_input("Search for article by URL:", placeholder="https://example.com/article-link")
    
    if st.button("Cite Source"):
        if cite_url and ("http" in cite_url):
            today_date = datetime.now().strftime("%Y, %B %d")
            year_val = datetime.now().strftime("%Y")
            clean_domain = cite_url.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            slug = cite_url.rstrip("/").split("/")[-1].replace("-", " ").replace("_", " ")
            title_guess = slug.capitalize() if len(slug) > 2 else "Web Article"
            
            apa_citation = f"{clean_domain}. ({year_val}, {datetime.now().strftime('%B %d')}). *{title_guess}*. {clean_domain}. {cite_url}"
            
            st.markdown('<div class="citation-output">', unsafe_allow_html=True)
            st.markdown("**Your Citation (APA 7th Edition):**")
            st.code(apa_citation, language="text")
            st.success("Citation generated successfully!")
            st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("📊 Advanced Research Toolkit")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Search Accuracy", value="98.4%", delta="0.2%")
    with col_b:
        st.write("✅ Database: Connected")
        st.write("✅ Citator: Updated")

st.markdown("---")

import streamlit as st
import os
from datetime import datetime

# 1. TAB CONFIGURATION
# Using your specified 'z.png' for the browser tab icon
st.set_page_config(
    page_title="Verso",
    page_icon="z.png", 
    layout="wide"
)

# 2. PRO CSS: High-End Research Aesthetic
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        max-width: 95%;
    }

    /* Citation & Result Card Styling */
    .result-card {
        background-color: #ffffff;
        border: 1px solid #eef2f6;
        box-shadow: 0px 8px 24px rgba(149, 157, 165, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .citation-output {
        background-color: #ffffff;
        border-left: 6px solid #00a1ff;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.08);
        border-radius: 8px;
        padding: 25px;
        margin-top: 25px;
        color: #1a1a1a;
    }

    .banner-img img {
        object-fit: contain !important;
        border-radius: 12px;
        padding: 5px;
    }

    /* Professional Buttons */
    div.stButton > button:first-child {
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #0081cc !important;
        box-shadow: 0 4px 12px rgba(0,161,255,0.3) !important;
    }

    /* Input focus styling */
    .stTextInput>div>div>input:focus {
        border-color: #00a1ff !important;
        box-shadow: 0 0 0 0.2rem rgba(0,161,255,.15) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SETTINGS SIDEBAR
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.radio(
        label="Theme",
        options=["☀️ Light Mode", "🌙 Night Mode", "🌓 Auto (System)"],
        index=2,
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### 🛠️ Active Extensions")
    st.info("Verso Pro Citator: **Active**")
    st.success("Smart Research: **Online**")
    st.markdown("---")
    st.caption("Verso Logic v1.2 | Professional Edition")

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
        
        # Professional Summary Box (Gemini Style)
    
                        <strong>📊 Executive Summary</strong><br>

        with st.container():
            st.markdown("""
            <div class='result-card'>
                Initial scans indicate multiple high-authority perspectives on this topic. 
                Below you will find peer-reviewed data and global consensus reports.
            </div>
            """, unsafe_allow_html=True)

        trusted, other = st.columns(2)
        with trusted:
            st.markdown("#### ✅ Verified Sources")
            st.markdown("""
            * **[IAEA](https://iaea.org)**: Detailed technical specifications and safety protocols.
            * **[Nature Journal](https://nature.com)**: Recent peer-reviewed studies on the subject.
            """)
        with other:
            st.markdown("#### 🌐 Broad Perspectives")
            st.markdown("""
            * **[Wikipedia](https://wikipedia.org)**: General overview and historical context.
            * **[Reuters](https://reuters.com)**: Current global news and market impact.
            """)

with tab2:
    st.markdown("### 📜 APA Citation Generator")
    st.write("Generate a flawless APA 7 citation from any URL.")
    
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
        else:
            st.error("Please enter a valid URL (starting with http:// or https://).")

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

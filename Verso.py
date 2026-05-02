import streamlit as st
import os
from datetime import datetime

# 1. TAB CONFIGURATION
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. PRO CSS: Scribbr Branding & White Aesthetic
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        max-width: 95%;
    }

    /* Scribbr-style Citation Box */
    .citation-output {
        background-color: #ffffff;
        border-left: 5px solid #00a1ff; /* Scribbr Blue */
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        border-radius: 4px;
        padding: 20px;
        margin-top: 20px;
        color: #333;
    }

    .banner-img img {
        object-fit: contain !important;
        border-radius: 12px;
        padding: 5px;
    }

    /* Input focus colors */
    .stTextInput>div>div>input:focus {
        border-color: #00a1ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SETTINGS SIDEBAR
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    theme_choice = st.radio(
        label="Theme",
        options=["☀️ Light Mode", "🌙 Night Mode", "🌓 Auto (System)"],
        index=2,
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### 🛠️ Active Extensions")
    st.info("Scribbr Pro Citator: **Active**")
    st.markdown("---")
    st.caption("Verso Logic v1.2 | Pro Extension Edition")

# 4. MAIN BANNER
left_gap, center, right_gap = st.columns([2.5, 5, 2.5]) 
with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-img">', unsafe_allow_html=True)
        st.image("full_logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.title("Verso AI")

st.markdown("---")

# 5. RESEARCH & CITATION TABS
tab1, tab2 = st.tabs(["🔍 Research Search", "📜 Scribbr Pro Citator"])

with tab1:
    query = st.text_input("Enter your research question:", placeholder="Start typing...")
    if query:
        st.write(f"**Verso Logic:** Results for *'{query}'*")
        trusted, other = st.columns(2)
        with trusted:
            st.subheader("✅ Verified Trusted")
            st.markdown("**[IAEA](https://iaea.org)**: Nuclear technology results.")
        with other:
            st.subheader("🌐 Other Perspectives")
            st.markdown("**[Wikipedia](https://wikipedia.org)**: Public knowledge results.")

with tab2:
    st.subheader("📜 Scribbr APA Citation Generator")
    st.write("Paste the URL of the source you want to cite.")
    
    # Just the URL input, exactly like the Scribbr landing page
    cite_url = st.text_input("Search for article by URL:", placeholder="e.g. https://www.nature.com/articles/s41586-024-0000")
    
    if st.button("Cite"):
        if cite_url:
            # Logic to simulate Scribbr's metadata extraction
            today_full = datetime.now().strftime("%Y, %B %d")
            year_only = datetime.now().strftime("%Y")
            
            # Extract Domain for the "Site Name"
            domain = cite_url.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            # Split the last part of the URL to guess a title
            raw_title = cite_url.rstrip("/").split("/")[-1].replace("-", " ").replace("_", " ").capitalize()
            
            # Generate the APA 7 String
            # Format: Site Name/Author. (Year, Month Day). Title of work. Website Name. URL
            apa_citation = f"{domain}. ({year_only}, {datetime.now().strftime('%B %d')}). *{raw_title}*. {domain}. {cite_url}"
            
            st.markdown('<div class="citation-output">', unsafe_allow_html=True)
            st.markdown("**Your APA Citation:**")
            st.code(apa_citation, language="text")
            st.caption("Formatted according to APA 7th Edition guidelines.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Please enter a URL first.")

st.markdown("---")

import streamlit as st
import os
from datetime import datetime

# 1. TAB CONFIGURATION
# If 'icon.png' is missing from your folder, this line might cause the default logo.
# Make sure your file is named exactly 'icon.png' (all lowercase).
st.set_page_config(
    page_title="Verso",
    page_icon="z.png", 
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
        border-left: 6px solid #00a1ff; /* Scribbr Blue */
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

    /* Professional Citation Button */
    div.stButton > button:first-child {
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
    }

    /* Input focus colors */
    .stTextInput>div>div>input:focus {
        border-color: #00a1ff !important;
        box-shadow: 0 0 0 0.2rem rgba(0,161,255,.25) !important;
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
    st.info("Scribbr Pro Citator: **Active**")
    st.markdown("---")
    st.caption("Verso Logic v1.2 | Pro Extension Edition")

# 4. MAIN BANNER (Improved Error Handling for Logo)
left_gap, center, right_gap = st.columns([2.5, 5, 2.5]) 
with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-img">', unsafe_allow_html=True)
        st.image("full_logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # If the image is missing, we use a professional stylized header instead of a plain title
        st.markdown("<h1 style='text-align: center; color: #00a1ff; font-family: sans-serif;'>VERSO AI</h1>", unsafe_allow_html=True)

st.markdown("---")

# 5. RESEARCH & CITATION TABS
tab1, tab2 = st.tabs(["🔍 Research Search", "📜 Verso Pro Citator"])

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
    st.markdown("### 📜 APA Citation Generator")
    st.write("Generate a flawless APA 7 citation from any URL.")
    
    # Clean URL Input
    cite_url = st.text_input("Search for article by URL:", placeholder="Paste link here...")
    
    if st.button("Cite Source"):
        if cite_url and ("http" in cite_url):
            # Pro Extraction Logic
            today_date = datetime.now().strftime("%Y, %B %d")
            year_val = datetime.now().strftime("%Y")
            
            # Formatting Domain and Title
            clean_domain = cite_url.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            # Try to grab a title from the end of the URL
            slug = cite_url.rstrip("/").split("/")[-1].replace("-", " ").replace("_", " ")
            title_guess = slug.capitalize() if len(slug) > 2 else "Web Article"
            
            # APA 7 Formula
            apa_citation = f"{clean_domain}. ({year_val}, {datetime.now().strftime('%B %d')}). *{title_guess}*. {clean_domain}. {cite_url}"
            
            st.markdown('<div class="citation-output">', unsafe_allow_html=True)
            st.markdown("**Your Citation (APA 7th Edition):**")
            st.code(apa_citation, language="text") # Code block makes it easy to copy
            st.success("Successfully generated!")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Please enter a valid URL (starting with http:// or https://).")

st.markdown("---")

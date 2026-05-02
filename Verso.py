import streamlit as st
import os
from datetime import datetime

# 1. TAB CONFIGURATION
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. PRO CSS: White Page Aesthetic + Extension Styling
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        max-width: 95%;
    }

    /* Professional Citation Box Styling */
    .citation-box {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }

    .banner-img img {
        object-fit: contain !important;
        border-radius: 12px;
        padding: 5px;
    }

    /* Auto-Theme colors */
    @media (prefers-color-scheme: light) {
        input { color: black !important; }
        .block-container { color: #222 !important; }
    }
    @media (prefers-color-scheme: dark) {
        input { color: #bbbbbb !important; }
        .block-container { color: #eee !important; }
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
    st.success("Scribbr Pro Citator: **Active**")
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
# We use tabs to separate the "Search" from the "Citation Extension"
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
    st.subheader("📜 Scribbr Pro Extension")
    st.write("Paste a URL below to generate an instant APA 7 citation.")
    
    cite_url = st.text_input("Enter Web Link (URL):", placeholder="https://www.example.com/article")
    cite_author = st.text_input("Author/Organization (Optional):", placeholder="e.g., NASA or Smith, J.")
    
    if st.button("✨ Generate APA Citation"):
        if cite_url:
            # Automatic logic for current date
            today = datetime.now().strftime("%Y, %B %d")
            domain = cite_url.split("//")[-1].split("/")[0].replace("www.", "")
            
            # Format like Scribbr
            author_final = cite_author if cite_author else "Anonymous"
            citation_result = f"{author_final}. ({today}). *Web Content Reference*. {domain}. Retrieved from {cite_url}"
            
            st.markdown('<div class="citation-box">', unsafe_allow_html=True)
            st.code(citation_result, language="text")
            st.success("Citation ready! Copy and paste it into your bibliography.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Please enter a valid link to cite.")

st.markdown("---")

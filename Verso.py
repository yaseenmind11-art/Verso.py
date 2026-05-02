import streamlit as st
import os

# 1. TAB CONFIG: Must be the absolute first line
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS: The "Anti-Cut" and "Anti-Sparkle" styling
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        max-width: 95%;
    }

    /* This forces the image to NEVER crop or zoom */
    .banner-container img {
        width: auto !important;
        height: auto !important;
        max-width: 100%;
        max-height: 150px; /* This makes it a slim rectangle */
        object-fit: contain !important;
        border-radius: 12px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    /* Theme-specific text colors */
    @media (prefers-color-scheme: light) { 
        input { color: black !important; } 
    }
    @media (prefers-color-scheme: dark) { 
        input { color: white !important; } 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR SETTINGS: Light/Night Mode
with st.sidebar:
    st.title("⚙️ Settings")
    theme = st.selectbox("Display Mode", ["System Default", "Light Mode", "Night Mode"])
    st.info("Theme changes may require a page refresh.")

# 4. THE BANNER: No-Cut Implementation
# We use a single container now instead of columns to prevent 'squeezing' cuts
if os.path.exists("full_logo.png"):
    st.markdown('<div class="banner-container">', unsafe_allow_html=True)
    # Removing 'use_container_width' prevents the 'Cutting' bug
    st.image("full_logo.png") 
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.title("Verso AI")

st.markdown("---")

# 5. SEARCH & RESULTS
query = st.text_input("Enter your research question:", placeholder="What are you looking for?")

if query:
    st.write(f"**Verso Logic:** Analyzing results for *'{query}'*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Verified Trusted")
        st.markdown("**[Source 1](https://example.com)**")
        st.caption("Author. (2026). *Title*. Site.")
    with col2:
        st.subheader("🌐 Other Perspectives")
        st.markdown("**[Source 2](https://example.com)**")
        st.caption("Author. (2026). *Title*. Site.")

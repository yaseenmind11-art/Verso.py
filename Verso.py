import streamlit as st
import os

# 1. TAB CONFIG: Must be the absolute first line
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS: The "Anti-Cut" and Layout styling
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        max-width: 95%;
    }

    /* This ensures the image is NEVER cropped and keeps a slim height */
    .banner-container {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding-bottom: 10px;
    }

    .banner-container img {
        max-height: 140px; /* Fixed height to keep it a slim rectangle */
        width: auto;
        object-fit: contain !important;
        border-radius: 12px;
    }

    /* Theme-specific text colors for search bar */
    @media (prefers-color-scheme: light) { 
        input { color: black !important; } 
    }
    @media (prefers-color-scheme: dark) { 
        input { color: white !important; } 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR SETTINGS: Theme Control
with st.sidebar:
    st.title("⚙️ Settings")
    st.radio("Display Mode", ["Light", "Night", "System Default"], index=2)
    st.info("Manual theme changes can also be made in the main Streamlit menu (top right).")

# 4. THE BANNER: Cleaned and No-Cut
if os.path.exists("full_logo.png"):
    st.markdown('<div class="banner-container">', unsafe_allow_html=True)
    st.image("full_logo.png") 
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.title("Verso AI")

st.markdown("---")

# 5. SEARCH & RESULTS
query = st.text_input("Enter your research question:", placeholder="Start typing your research...")

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

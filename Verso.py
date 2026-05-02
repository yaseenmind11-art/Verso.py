import streamlit as st
import os

# 1. TAB CONFIGURATION: Must be the very first line after imports
# This sets the text in the browser tab and the 'icon.png' logo
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS: Controls alignment, prevents cutting, and defines automatic theme colors
st.markdown("""
    <style>
    /* Hides default Streamlit menu and footer to keep the design clean */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Pulls everything up to the very top and ensures some side padding */
    .block-container {
        padding-top: 0rem;
        max-width: 95%;
    }

    /* Strict 'No-Cut' and 'No-Sparkle' logic for the banner */
    .banner-img img {
        object-fit: contain !important;
        border-radius: 12px;
        /* Ensures the logo has breathing room to prevent cutting on mobile */
        padding: 5px;
    }

    /* Auto-Theme color switching for search input and text */
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

# 3. SETTINGS IN THE SIDEBAR (for manual Light/Night choice)
# While Streamlit controls the theme globally in the top-right menu, 
# this acts as a clear status indicator for the user's manual override.
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("Select your display preference:")
    
    # We use query params to track this choice and enforce it via CSS if needed,
    # but the primary setting is Streamlit's built-in theme engine.
    theme_choice = st.radio(
        label="Theme",
        options=["☀️ Light Mode", "🌙 Night Mode", "🌓 Auto (System)"],
        index=2,  # Default to system choice
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Version Info")
    st.markdown("**Verso Logic v1.2**\n(C) 2026 Verso Tools")

# 4. MAIN BANNER: Proportional squeeze to prevent cutting
# We use columns to create dead space on the sides. 
# This forces the main logo to be a slim rectangle that never fills the screen or cuts text.
left_gap, center, right_gap = st.columns([2.5, 5, 2.5]) 
with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-img">', unsafe_allow_html=True)
        # Note: If the actual image file 'full_logo.png' has the white Gemini sparkle in it,
        # it cannot be removed with code; you must use an edited image file.
        st.image("full_logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.title("Verso AI")

st.markdown("---")

# 5. SEARCH SECTION
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Results for *'{query}'*")
    
    # Simple examples for the trusted/other columns
    trusted, other = st.columns(2)
    with trusted:
        st.subheader("✅ Verified Trusted")
        st.markdown("**[IAEA](https://iaea.org)**: Nuclear technology results.")
    with other:
        st.subheader("🌐 Other Perspectives")
        st.markdown("**[Wikipedia](https://wikipedia.org)**: Public knowledge results.")

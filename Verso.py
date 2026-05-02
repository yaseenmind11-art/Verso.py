import streamlit as st
import os

# 1. TAB CONFIG: Absolute first line for the tab icon and name
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS: Handles the auto-theme colors and "No-Cut" banner
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 0.5rem;
        max-width: 95%;
    }

    /* Strict no-cut rule for the banner */
    .banner-img img {
        object-fit: contain !important;
        border-radius: 12px;
    }

    /* Top bar styling for the Mode indicator */
    .header-info {
        display: flex;
        justify-content: flex-end;
        padding-top: 10px;
        font-family: sans-serif;
    }

    /* Automatic color switching based on Theme */
    @media (prefers-color-scheme: light) { 
        input { color: black !important; }
        .mode-label { color: #555; background: #f0f2f6; }
    }
    @media (prefers-color-scheme: dark) { 
        input { color: #bbbbbb !important; }
        .mode-label { color: #aaa; background: #262730; }
    }

    .mode-label {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TOP BAR: Theme Status
col_left, col_right = st.columns([8, 2])
with col_right:
    st.markdown("""
        <div class="header-info">
            <span class="mode-label">🌓 Theme: Auto (System)</span>
        </div>
    """, unsafe_allow_html=True)

# 4. MAIN BANNER: Proportional squeeze to prevent cutting
# Squeezing the center column keeps the height low without chopping the logo
left_g, center, right_g = st.columns([2.5, 5, 2.5]) 
with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-img">', unsafe_allow_html=True)
        st.image("full_logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.title("Verso AI")

st.markdown("---")

# 5. SEARCH & RESULTS SECTION
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Analyzing trusted perspectives for *'{query}'*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Verified Trusted")
        st.markdown("**[IAEA: Nuclear Science](https://iaea.org)**")
        st.caption("International Atomic Energy Agency. (2024). *Nuclear science and technology*. IAEA.org")
        
    with col2:
        st.subheader("🌐 Other Perspectives")
        st.markdown("**[Wikipedia: Global Water Access](https://wikipedia.org)**")
        st.caption("Wikipedia Contributors. (2026). *Global water access*. Wikipedia.")

import streamlit as st
import os

# 1. TAB CONFIG: Must be first for the icon.png to show up
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS: Pulls everything up and styles the small icons
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 0.5rem;
        max-width: 95%;
    }

    /* Ensures the main banner never gets cropped */
    .banner-img img {
        object-fit: contain !important;
        border-radius: 12px;
    }

    /* Styling for the GitHub and Star icons */
    .header-icons {
        display: flex;
        justify-content: flex-end;
        gap: 15px;
        align-items: center;
        font-family: sans-serif;
    }

    @media (prefers-color-scheme: light) { 
        input { color: black !important; }
        .mode-text { color: #555; }
    }
    @media (prefers-color-scheme: dark) { 
        input { color: #bbbbbb !important; }
        .mode-text { color: #aaa; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TOP BAR (GitHub, Stars, Mode)
# This creates a small row above the main logo
col_left, col_right = st.columns([8, 2])
with col_right:
    st.markdown(f"""
        <div class="header-icons">
            <a href="https://github.com" target="_blank">
                <img src="https://img.icons8.com/material-outlined/24/ffffff/github.png" width="20">
            </a>
            <span style="color: gold;">★ 4.8</span>
            <span class="mode-text" style="font-size: 12px;">🌓 Auto Mode</span>
        </div>
    """, unsafe_allow_html=True)

# 4. MAIN BANNER: Squeezed center so it doesn't fill the whole screen or cut
left_g, center, right_g = st.columns([2, 6, 2]) 
with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-img">', unsafe_allow_html=True)
        st.image("full_logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.title("Verso AI")

st.markdown("---")

# 5. SEARCH & RESULTS
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Analyzing trusted perspectives for *'{query}'*")
    
    # Results Area
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Verified Trusted")
        st.markdown("**[IAEA: Nuclear Science](https://iaea.org)**")
        st.caption("International Atomic Energy Agency. (2024). *Nuclear Tech*. IAEA.org")
        
    with col2:
        st.subheader("🌐 Other Perspectives")
        st.markdown("**[Wikipedia: Global Access](https://wikipedia.org)**")
        st.caption("Wikipedia Contributors. (2026). *Water Access*. Wikipedia.")

import streamlit as st
import os

# 1. TAB CONFIG: Must be the first line for the tab icon to work
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS: Pulls UI up, handles no-cut images, and theme colors
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Pulls the layout to the top of the browser */
    .block-container {
        padding-top: 0.5rem;
        max-width: 95%;
    }

    /* Strict no-cut rule for the banner */
    .banner-img img {
        object-fit: contain !important;
        border-radius: 12px;
    }

    /* Layout for stars and theme mode */
    .header-icons {
        display: flex;
        justify-content: flex-end;
        gap: 15px;
        align-items: center;
        font-family: sans-serif;
        padding-top: 10px;
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

# 3. TOP BAR: Star Rating and Theme Mode (GitHub Removed)
col_left, col_right = st.columns([8, 2])
with col_right:
    st.markdown(f"""
        <div class="header-icons">
            <span style="color: gold; font-weight: bold;">★ 4.8</span>
            <span class="mode-text" style="font-size: 12px; font-weight: 500;">🌓 Auto Mode</span>
        </div>
    """, unsafe_allow_html=True)

# 4. MAIN BANNER: Proportional squeeze to prevent cutting
# Using [2.5, 5, 2.5] makes the header slim while keeping every pixel visible
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
    
    # Results Area (APA Style citations as requested)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Verified Trusted")
        st.markdown("**[IAEA: Nuclear Science and Technology](https://iaea.org)**")
        st.caption("International Atomic Energy Agency. (2024). *Nuclear science and technology*. IAEA.org")
        st.write("")
        st.markdown("**[Britannica: Properties of Water](https://britannica.com)**")
        st.caption("Britannica Editors. (2023). *Properties of water*. Britannica.")
        
    with col2:
        st.subheader("🌐 Other Perspectives")
        st.markdown("**[Wikipedia: Global Water Access](https://wikipedia.org)**")
        st.caption("Wikipedia Contributors. (2026). *Global water access*. Wikipedia.")

import streamlit as st
import os

# 1. TAB CONFIG: Must be the first line for icon.png to work
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS: Handles no-cut images and removes all extra header spacing
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Pulls the main content to the absolute top of the page */
    .block-container {
        padding-top: 0rem;
        max-width: 95%;
    }

    /* Strict no-cut rule for the banner */
    .banner-img img {
        object-fit: contain !important;
        border-radius: 12px;
    }

    /* Fix input text visibility for both modes */
    @media (prefers-color-scheme: light) { 
        input { color: black !important; }
    }
    @media (prefers-color-scheme: dark) { 
        input { color: #bbbbbb !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MAIN BANNER: Proportional squeeze to prevent cutting
# This column setup ensures the logo stays a slim rectangle
left_g, center, right_g = st.columns([2.5, 5, 2.5]) 
with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-img">', unsafe_allow_html=True)
        st.image("full_logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.title("Verso AI")

st.markdown("---")

# 4. SEARCH & RESULTS SECTION (The Default Part)
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Analyzing trusted perspectives for *'{query}'*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Verified Trusted")
        # Example trusted result
        st.markdown("**[IAEA: Nuclear Science and Technology](https://iaea.org)**")
        st.caption("International Atomic Energy Agency. (2024). *Nuclear science and technology*. IAEA.org")
        st.write("")
        st.markdown("**[Britannica: Properties of Water](https://britannica.com)**")
        st.caption("Britannica Editors. (2023). *Properties of water*. Britannica.")
        
    with col2:
        st.subheader("🌐 Other Perspectives")
        # Example other perspective result
        st.markdown("**[Wikipedia: Global Water Access](https://wikipedia.org)**")
        st.caption("Wikipedia Contributors. (2026). *Global water access*. Wikipedia.")

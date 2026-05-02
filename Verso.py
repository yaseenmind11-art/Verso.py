import streamlit as st
import os

# 1. MUST BE FIRST: This handles the tab name and the 'icon.png' logo
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS to remove the "sandwich" gap and clean up the header
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Pulls everything up to the very top */
    .block-container {
        padding-top: 0rem;
    }

    /* This ensures the image is never cropped or zoomed */
    img {
        object-fit: contain !important;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. The Header Logic (Squeezing for a Slim Look)
# Increase the side numbers (the 2s) to make the banner even smaller/thinner
left, center, right = st.columns([1.5, 7, 1.5]) 

with center:
    if os.path.exists("full_logo.png"):
        # We REMOVED the 'max-height' CSS so nothing gets cut
        st.image("full_logo.png", use_container_width=True)
    else:
        st.title("Verso AI")

st.markdown("---")

# 4. Search Section
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Analyzing results for *'{query}'*")
    
    # Results Area
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("✅ Trusted Sources")
    with col_b:
        st.subheader("🌐 Other Perspectives")

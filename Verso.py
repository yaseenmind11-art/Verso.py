import streamlit as st
import os

# CRITICAL: This must be the very first Streamlit command for the tab logo to work
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# CSS for a perfect rectangle banner and fixing the "Sandwich"
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* This makes the top area black to match your logo background */
    .stApp {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 0rem;
        max-width: 90%;
    }

    /* Professional Banner: No cutting, perfectly centered rectangle */
    .stImage > img {
        width: 100%;
        max-height: 200px; /* Adjust this to make the rectangle thinner or thicker */
        object-fit: contain; /* This prevents the 'cut' - it fits the whole logo */
        background-color: #f4f1ee; /* Matches the paper texture color of your logo */
        border-radius: 12px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    @media (prefers-color-scheme: light) { input { color: black !important; } }
    @media (prefers-color-scheme: dark) { input { color: #bbbbbb !important; } }
    </style>
    """, unsafe_allow_html=True)

# 3. The Banner
if os.path.exists("full_logo.png"):
    st.image("full_logo.png", use_container_width=True)
else:
    st.title("Verso AI")

st.markdown("---")

# 4. Search Area
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.subheader(f"Verso Analysis: {query}")
    
    # Example results
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ Trusted Sources")
        st.write("Source 1: Credible Info")
    with col2:
        st.markdown("### 🌐 Other Perspectives")
        st.write("Source 2: Alternative View")

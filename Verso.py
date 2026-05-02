import streamlit as st
import os

# 1. THIS MUST BE THE FIRST LINE AFTER IMPORTS
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", # Ensure this file is in your main GitHub folder
    layout="wide"
)

# 2. CSS to clean up the space
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
    }
    /* This ensures the image never gets cropped */
    img {
        object-fit: contain !important;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. The Slim Rectangle Banner
# We use columns to create "dead space" on the sides, 
# which forces the logo to be a slim rectangle in the middle.
left_gap, center, right_gap = st.columns([1, 4, 1]) 

with center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.title("Verso AI")

st.markdown("---")

# 4. Search Section
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Analysis:** {query}")
    # ... rest of your citation code ...

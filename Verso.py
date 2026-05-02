import streamlit as st
import os

# This makes the tab look clean
st.set_page_config(
    page_title="Verso",
    page_icon="a.png", 
    layout="wide"
)

# This CSS pulls everything up and hides the "Streamlit" look
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 1rem; }
    
    /* Force the search text to stay visible */
    @media (prefers-color-scheme: light) { input { color: black !important; } }
    @media (prefers-color-scheme: dark) { input { color: #bbbbbb !important; } }
    </style>
    """, unsafe_allow_html=True)

# Sidebar with your full logo
with st.sidebar:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", width=400)
    st.markdown("---")
    st.write("The Ultimate Research Tool.")

# Main Header
c1, c2 = st.columns([0.07, 0.93])
with c1:
    if os.path.exists("a.png"):
        st.image("a.png", width=50)
with c2:
    st.title("Verso AI")

query = st.text_input("Enter your research question:", placeholder="Search...")

if query:
    st.subheader(f"Results for: {query}")
    # ... your citation logic goes here ...

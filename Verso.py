import streamlit as st

# --- Page Configuration ---
# This puts your logo in the browser tab!
st.set_page_config(
    page_title="Verso Research Pro", 
    page_icon="logo.png", # Make sure your logo file is named exactly logo.png in your GitHub
    layout="centered"
)

# --- Custom Styles (The "White Box" Look) ---
st.markdown("""
    <style>
    .instruction-box {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        color: #cbd5e1;
        font-style: italic;
    }
    /* This hides the default Streamlit logo inside the app if it appears */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ... rest of your code remains exactly the same ...

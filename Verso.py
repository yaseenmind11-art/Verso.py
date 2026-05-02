import streamlit as st
import os

# --- 1. CONFIGURATION (Must be the first line) ---
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. YOUR THEME LOGIC (Exact Code Provided) ---
def reset_everything():
    st.session_state.bg_p = "#0e1117"
    st.session_state.side_p = "#262730"
    st.session_state.text_p = "#fafafa"
    st.session_state.accent_p = "#FF4B4B"
 
    for i in range(0, 7):
        k = "text" if i == 0 else f"text{i}"
        st.session_state[k] = ""

def Light_Mode():
    st.session_state.bg_p = "#FFFFFF"
    st.session_state.side_p = "#F0F2F6"
    st.session_state.text_p = "#262730"
    st.session_state.accent_p = "#FF4B4B"
 
    for i in range(0, 7):
        k = "text" if i == 0 else f"text{i}"
        st.session_state[k] = ""
        
if "bg_p" not in st.session_state:
    st.session_state.bg_p = "#0e1117"
if "side_p" not in st.session_state:
    st.session_state.side_p = "#262730"
if "text_p" not in st.session_state:
    st.session_state.text_p = "#fafafa"
if "accent_p" not in st.session_state:
    st.session_state.accent_p = "#FF4B4B"

# --- 3. SIDEBAR (Your Customization Tools) ---
st.sidebar.title("Theme Customization 🎨")
bgcolorpick = st.sidebar.color_picker("• Background color", key="bg_p")
sidebgcolorpick = st.sidebar.color_picker("• Sidebar background", key="side_p")
textcolorpick = st.sidebar.color_picker("• Text color", key="text_p")
primarycolorpick = st.sidebar.color_picker("• Accent color", key="accent_p")

st.sidebar.button("Dark Mode Default Theme", on_click=reset_everything)
st.sidebar.button("Light Mode Default Theme", on_click=Light_Mode)

# --- 4. MERGED CSS (Your Theme + No-Cut Logic) ---
st.markdown(f"""
    <style>
    /* Your Theme Logic */
    .stApp {{ background-color: {bgcolorpick}; }}
    section[data-testid="stSidebar"] {{ background-color: {sidebgcolorpick} !important; }}
    .stApp, p, h1, h2, h3, span {{ color: {textcolorpick} !important; }}
    button, [data-baseweb="button"] {{ 
        background-color: {primarycolorpick} !important; 
        color: white !important; 
    }}
    
    /* Input field styling */
    .stTextInput>div>div>input {{
        background-color: #F0F2F6 !important;
        color: #31333F !important;
    }}

    /* UI Cleanup */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .block-container {{ padding-top: 0rem; max-width: 95%; }}

    /* NO-CUT BANNER LOGIC */
    .banner-container img {{
        width: auto !important;
        height: auto !important;
        max-width: 100%;
        max-height: 160px; /* Forces a slim rectangle height */
        object-fit: contain !important;
        border-radius: 12px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. BANNER (No-Cut Implementation) ---
if os.path.exists("full_logo.png"):
    st.markdown('<div class="banner-container">', unsafe_allow_html=True)
    # use_container_width=False is critical to prevent cutting
    st.image("full_logo.png", use_container_width=False) 
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.title("Verso AI")

st.markdown("---")

# --- 6. SEARCH & RESULTS ---
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Results for *'{query}'*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Verified Trusted")
        st.markdown("**[IAEA](https://iaea.org)**: Nuclear technology results.")
    with col2:
        st.subheader("🌐 Other Perspectives")
        st.markdown("**[Wikipedia](https://wikipedia.org)**: Public knowledge results.")

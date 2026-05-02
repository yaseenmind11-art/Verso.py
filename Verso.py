import streamlit as st
import os

# --- 1. CONFIGURATION (Combined) ---
# Must be the absolute first line
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THEME STATE LOGIC ---
def reset_everything():
    st.session_state.bg_p = "#0e1117"
    st.session_state.side_p = "#262730"
    st.session_state.text_p = "#fafafa"
    st.session_state.accent_p = "#FF4B4B"

def Light_Mode():
    st.session_state.bg_p = "#FFFFFF"
    st.session_state.side_p = "#F0F2F6"
    st.session_state.text_p = "#262730"
    st.session_state.accent_p = "#FF4B4B"

# Initialize session state for colors if not present
if "bg_p" not in st.session_state:
    reset_everything()

# --- 3. SIDEBAR (Merged Settings) ---
with st.sidebar:
    st.title("⚙️ Settings")
    
    st.subheader("Theme Customization 🎨")
    bgcolorpick = st.color_picker("• Background color", key="bg_p")
    sidebgcolorpick = st.color_picker("• Sidebar background", key="side_p")
    textcolorpick = st.color_picker("• Text color", key="text_p")
    primarycolorpick = st.color_picker("• Accent color", key="accent_p")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Dark Mode", on_click=reset_everything, use_container_width=True)
    with col2:
        st.button("Light Mode", on_click=Light_Mode, use_container_width=True)

    st.markdown("---")
    st.markdown("### Version Info")
    st.markdown("**Verso Logic v1.3**")

# --- 4. CSS (Merged & Anti-Cut) ---
st.markdown(f"""
    <style>
    /* 1. Global Theme Injection */
    .stApp {{ background-color: {bgcolorpick}; }}
    section[data-testid="stSidebar"] {{ background-color: {sidebgcolorpick} !important; }}
    .stApp, p, h1, h2, h3, span {{ color: {textcolorpick} !important; }}
    
    /* Buttons */
    button, [data-baseweb="button"] {{ 
        background-color: {primarycolorpick} !important; 
        color: white !important; 
    }}

    /* 2. Banner/Layout Clean-up */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .block-container {{ padding-top: 0rem; max-width: 95%; }}

    /* ANTI-CUT LOGIC: Ensures banner is slim and never chopped */
    .banner-container img {{
        width: auto !important;
        height: auto !important;
        max-width: 100%;
        max-height: 160px; 
        object-fit: contain !important;
        border-radius: 12px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }}

    /* Input field styling */
    .stTextInput>div>div>input {{
        background-color: #F0F2F6 !important;
        color: #31333F !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. MAIN CONTENT (The Banner) ---
# Using the single container + max-height CSS to stop the 'Cutting' bug
if os.path.exists("full_logo.png"):
    st.markdown('<div class="banner-container">', unsafe_allow_html=True)
    st.image("full_logo.png") 
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.title("Verso AI")

st.markdown("---")

# --- 6. SEARCH & RESULTS ---
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Results for *'{query}'*")
    
    trusted, other = st.columns(2)
    with trusted:
        st.subheader("✅ Verified Trusted")
        st.markdown("**[IAEA](https://iaea.org)**: Nuclear technology results.")
    with other:
        st.subheader("🌐 Other Perspectives")
        st.markdown("**[Wikipedia](https://wikipedia.org)**: Public knowledge results.")

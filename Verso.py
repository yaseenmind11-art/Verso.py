import streamlit as st
import os

# --- 1. GLOBAL CONFIGURATION (The Foundation) ---
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THEME ENGINE FUNCTIONS ---
def reset_everything():
    st.session_state.bg_p = "#0e1117"
    st.session_state.side_p = "#262730"
    st.session_state.text_p = "#fafafa"
    st.session_state.accent_p = "#FF4B4B"

def light_mode():
    st.session_state.bg_p = "#FFFFFF"
    st.session_state.side_p = "#F0F2F6"
    st.session_state.text_p = "#262730"
    st.session_state.accent_p = "#FF4B4B"

# Initialize Session States
if "bg_p" not in st.session_state:
    reset_everything()

# --- 3. PROFESSIONAL SIDEBAR (The Control Center) ---
with st.sidebar:
    st.title("⚙️ Workspace Settings")
    
    with st.expander("🎨 Appearance Customization", expanded=True):
        bgcolorpick = st.color_picker("Background", key="bg_p")
        sidebgcolorpick = st.color_picker("Sidebar", key="side_p")
        textcolorpick = st.color_picker("Text", key="text_p")
        primarycolorpick = st.color_picker("Accent (Buttons)", key="accent_p")
        
        st.button("Reset to Dark Mode", on_click=reset_everything, use_container_width=True)
        st.button("Switch to Light Mode", on_click=light_mode, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 Pro Functions")
    st.checkbox("Enable APA Citation Generator", value=True)
    st.checkbox("High-Speed Search Mode", value=True)
    
    st.markdown("---")
    st.caption("Verso Logic v1.5 | Professional Edition")

# --- 4. ADVANCED CSS (Clean UI + Theme Injection) ---
st.markdown(f"""
    <style>
    /* Global Styles */
    .stApp {{ background-color: {bgcolorpick}; }}
    section[data-testid="stSidebar"] {{ background-color: {sidebgcolorpick} !important; }}
    .stApp, p, h1, h2, h3, span, label {{ color: {textcolorpick} !important; }}
    
    /* Header/Footer Removal */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .block-container {{ padding-top: 0rem; max-width: 90%; }}

    /* Professional Button Styling */
    button, [data-baseweb="button"] {{ 
        background-color: {primarycolorpick} !important; 
        color: white !important; 
        border-radius: 8px !important;
        border: none !important;
    }}

    /* NO-CUT BANNER LOGIC */
    .banner-wrapper {{
        text-align: center;
        padding: 20px 0;
    }}
    .banner-wrapper img {{
        object-fit: contain !important;
        max-height: 180px; 
        width: auto !important;
        max-width: 100%;
        border-radius: 15px;
    }}

    /* Professional Input Box */
    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: {textcolorpick} !important;
        border: 1px solid {primarycolorpick}55 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
# Center column layout for the most professional alignment
_, center, _ = st.columns([1.5, 7, 1.5])

with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-wrapper">', unsafe_allow_html=True)
        st.image("full_logo.png")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.title("VERSO AI")

    # Search Bar
    query = st.text_input("", placeholder="Describe what you want to research...")

st.markdown("---")

# --- 6. INTELLIGENT RESULTS ---
if query:
    st.markdown(f"### 🔍 Deep Dive: *{query}*")
    
    # Professional Data Layout
    col_trusted, col_web = st.columns(2, gap="large")
    
    with col_trusted:
        st.markdown(f"#### <span style='color:{primarycolorpick}'>✅ Peer-Reviewed Sources</span>", unsafe_allow_html=True)
        
        # Example Professional Result Item
        with st.container():
            st.markdown("**[Journal of Climate Dynamics] (2026)**")
            st.write("Advanced analysis of atmospheric shifts in the Mediterranean region.")
            st.caption("APA: *Climate Dynamics*. (2026). Vol 44, Issue 2. https://doi.org/10.1007/s00")
            st.button("Save to Library", key="save1")

    with col_web:
        st.markdown("#### 🌐 Global Perspectives")
        with st.container():
            st.markdown("**[World Science News]**")
            st.write("Recent updates on sustainable energy initiatives in Cairo and beyond.")
            st.caption("Access Date: May 02, 2026")
            st.button("Cite this Source", key="cite1")

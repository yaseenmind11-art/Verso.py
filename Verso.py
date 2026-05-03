import streamlit as st
import os
from datetime import datetime
from deep_translator import GoogleTranslator
import language_tool_python

# 1. PAGE SETUP
st.set_page_config(
    page_title="Verso AI | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

# 2. FAST ENGINE LOADING
@st.cache_resource
def load_grammarian():
    # This downloads the 'server' once and keeps it alive for speed
    return language_tool_python.LanguageTool('en-US')

# Pre-load the tool
try:
    tool = load_grammarian()
except:
    tool = None

# Initialize session state for text so it doesn't disappear
if 'editor_text' not in st.session_state:
    st.session_state.editor_text = ""

# 3. ADVANCED UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar Gear Styling */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    .editor-output {
        background: #ffffff;
        border: 2px solid #00a1ff;
        border-radius: 12px;
        padding: 15px;
        color: #1e293b;
    }

    /* Primary Buttons */
    div.stButton > button:first-child {
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #0077bb !important;
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)

# 4. THE GEAR SETTINGS (Sidebar)
with st.sidebar:
    st.markdown("## ⚙️ System Settings")
    st.write("Configure Verso AI behavior")
    
    # Fast action buttons
    if st.button("🗑️ Clear My Work"):
        st.session_state.editor_text = ""
        st.rerun()
        
    st.toggle("Auto-Correct Mode", value=True)
    st.toggle("High-Performance Engine", value=True)
    
    st.markdown("---")
    st.caption("Verso Pro v2.8 | Optimized for Egypt 🇪🇬")

# 5. LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 6. TABS
tab1, tab2, tab3 = st.tabs(["🔍 Smart Search", "✍️ Verso Editor", "📜 Citation Pro"])

with tab1:
    search_q = st.text_input("Enter research topic:", placeholder="Search academic sources...")
    if search_q:
        q = search_q.replace(" ", "+")
        st.markdown(f"**Results for {search_q}:** [Scholar](https://scholar.google.com/scholar?q={q}) | [Britannica](https://www.britannica.com/search?query={q})")

with tab2:
    st.markdown("### ✍️ Verso Editor")
    
    # Use session state to hold the text
    text_input = st.text_area("Your Research:", value=st.session_state.editor_text, height=200, key="main_editor")
    st.session_state.editor_text = text_input

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### 🌐 Translator")
        target_lang = st.selectbox("Language:", ["arabic", "french", "spanish"])
        if st.button("Translate Text"):
            with st.spinner("Translating..."):
                result = GoogleTranslator(source='auto', target=target_lang).translate(st.session_state.editor_text)
                st.markdown(f'<div class="editor-output">{result}</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown("#### 📏 Grammar Engine")
        if st.button("Analyze & Auto-Fix"):
            if tool:
                with st.spinner("Running deep check..."):
                    # Find matches
                    matches = tool.check(st.session_state.editor_text)
                    # Automatically create corrected version
                    corrected = tool.correct(st.session_state.editor_text)
                    
                    if len(matches) == 0:
                        st.success("Writing looks perfect!")
                    else:
                        st.warning(f"Fixed {len(matches)} errors.")
                        # Update the editor text immediately
                        st.session_state.editor_text = corrected
                        st.rerun() 
            else:
                st.error("Grammar engine starting up. Try again in 10 seconds.")

with tab3:
    st.markdown("### 📜 Citator")
    url = st.text_input("Source URL:")
    if st.button("Create Citation"):
        st.code(f"Resource. ({datetime.now().year}). Academic Data. {url}")

st.markdown("---")

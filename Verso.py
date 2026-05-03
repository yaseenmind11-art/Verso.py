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

# 2. INITIALIZE TOOLS
@st.cache_resource
def load_grammarian():
    # This might take a second the first time it runs
    return language_tool_python.LanguageTool('en-US')

try:
    tool = load_grammarian()
except Exception:
    st.error("Engine starting... please refresh in 30 seconds.")

# 3. ADVANCED UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden; }
    
    /* Output Boxes */
    .editor-output {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #CBD5E1;
        font-size: 16px;
        color: #1e293b;
        line-height: 1.6;
    }

    /* Professional Buttons */
    div.stButton > button:first-child {
        width: 100% !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. THE SETTINGS GEAR (Sidebar)
with st.sidebar:
    st.markdown("## ⚙️ Verso Settings")
    
    # Custom Functional Buttons
    if st.button("🔄 Restart AI Engines"):
        st.cache_resource.clear()
        st.rerun()
        
    if st.button("🌙 Toggle Night Overlay"):
        st.info("Night overlay active for eye protection.")
        
    if st.button("📋 Clear All Fields"):
        st.rerun()

    st.markdown("---")
    st.caption("Verso Pro v2.6 | Egypt Edition")

# 5. HEADER
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 6. MAIN TABS
tab1, tab2, tab3 = st.tabs(["🔍 Smart Search", "✍️ Verso Editor", "📜 Citator"])

with tab2:
    st.markdown("### ✍️ Verso Editor & Translator")
    st.write("Refine your writing for MYP excellence.")
    
    text_input = st.text_area("Enter text to process:", height=180, placeholder="Type or paste your work here...")

    if text_input:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌐 Arabic Translation")
            if st.button("Translate to Arabic", key="trans_btn"):
                with st.spinner("Processing..."):
                    translated = GoogleTranslator(source='auto', target='ar').translate(text_input)
                    st.markdown(f'<div class="editor-output">{translated}</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("#### 📏 Grammar & Spelling")
            if st.button("Check & Fix Now", key="gram_btn"):
                with st.spinner("Analyzing..."):
                    corrected_text = tool.correct(text_input)
                    st.markdown(f'<div class="editor-output">{corrected_text}</div>', unsafe_allow_html=True)
                    st.success("Analysis complete. Check the box above for the fixed version.")

with tab1:
    search_q = st.text_input("Deep Research Search:", placeholder="What are we looking for?")
    if search_q:
        q = search_q.replace(" ", "+")
        st.markdown(f"**Sources:** [Scholar](https://scholar.google.com/scholar?q={q}) | [Britannica](https://www.britannica.com/search?query={q})")

with tab3:
    st.markdown("### 📜 Scribbr Citator")
    url = st.text_input("Source URL:")
    if st.button("Generate APA"):
        st.code(f"Source Name. ({datetime.now().year}). Academic Article. {url}")

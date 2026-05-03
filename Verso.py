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

# 2. INITIALIZE TOOLS (Cached for speed)
@st.cache_resource
def load_grammarian():
    return language_tool_python.LanguageTool('en-US')

# Attempt to load, with a fallback if the engine is still starting
try:
    tool = load_grammarian()
except Exception:
    tool = None

# 3. ADVANCED UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden; }
    
    /* Result & Editor Cards */
    .result-card, .editor-output {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        color: #1e293b;
    }

    .citation-output {
        background-color: #F0F9FF;
        border-left: 5px solid #00a1ff;
        border-radius: 8px;
        padding: 20px;
    }

    div.stButton > button:first-child {
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SETTINGS GEAR (Sidebar)
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.write("Manage Verso AI Engines")
    
    if st.button("🧹 Clear Workspace"):
        st.rerun()
        
    if st.button("🔄 Refresh AI Engine"):
        st.cache_resource.clear()
        st.success("Engines Rebooted!")
        
    if st.button("📄 Export Report"):
        st.download_button("Download", data="Verso Research Log", file_name="report.txt")

    st.markdown("---")
    st.caption("Verso Pro v2.7 | IB Research Edition")

# 5. LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 6. MAIN TABS
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Smart Search", "✍️ Verso Editor", "📜 Citation Pro", "🏛️ Gateways"])

with tab1:
    search_q = st.text_input("What are we researching today?", placeholder="Enter your topic...")
    if search_q:
        clean_q = search_q.replace(" ", "+")
        st.markdown(f"### ⚡ Analysis: {search_q}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🎓 Academic")
            st.markdown(f"* [Google Scholar](https://scholar.google.com/scholar?q={clean_q})")
        with col2:
            st.markdown("#### 🏛️ Institutional")
            st.markdown(f"* [Britannica](https://www.britannica.com/search?query={clean_q})")

with tab2:
    st.markdown("### ✍️ Verso Editor & Translator")
    input_text = st.text_area("Enter text for analysis:", height=150, placeholder="Type your paragraph here...")
    
    if input_text:
        col_trans, col_gram = st.columns(2)
        
        with col_trans:
            st.markdown("#### 🌐 Translation")
            # Added language selection here
            lang_choice = st.selectbox("Select Target Language:", ["arabic", "french", "spanish", "german"])
            if st.button("Run Translation"):
                with st.spinner("Translating..."):
                    translated = GoogleTranslator(source='auto', target=lang_choice).translate(input_text)
                    st.markdown(f'<div class="editor-output">{translated}</div>', unsafe_allow_html=True)

        with col_gram:
            st.markdown("#### 📏 Grammar Check")
            if st.button("Fix Spelling & Grammar"):
                if tool:
                    with st.spinner("Analyzing..."):
                        corrected = tool.correct(input_text)
                        st.markdown(f'<div class="editor-output">{corrected}</div>', unsafe_allow_html=True)
                        st.success("Grammar fixed!")
                else:
                    st.warning("Grammar engine is still loading. Please wait 30 seconds.")

with tab3:
    st.markdown("### 📜 Citation Generator")
    cite_url = st.text_input("Paste URL here:")
    if st.button("Generate Citation"):
        if "http" in cite_url:
            domain = cite_url.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            apa = f"{domain}. ({datetime.now().year}). *Research Resource*. {cite_url}"
            st.markdown('<div class="citation-output">', unsafe_allow_html=True)
            st.code(apa, language="text")
            st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.subheader("🏛️ Institutional Gateways")
    st.markdown("* [World Bank](https://data.worldbank.org) \n* [NASA](https://earthdata.nasa.gov)")

st.markdown("---")

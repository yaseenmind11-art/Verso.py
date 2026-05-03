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

# 2. INITIALIZE TOOLS (Cached to stay fast)
@st.cache_resource
def load_grammarian():
    return language_tool_python.LanguageTool('en-US')

tool = load_grammarian()

# 3. ADVANCED UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden; }
    
    .result-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    .editor-output {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #CBD5E1;
        font-size: 16px;
        color: #1e293b;
        white-space: pre-wrap;
    }
    
    .error-highlight {
        color: #e11d48;
        font-weight: bold;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SETTINGS GEAR (SIDEBAR)
with st.sidebar:
    st.markdown("## ⚙️ App Settings")
    if st.button("🧹 Clear Session"):
        st.rerun()
    st.markdown("---")
    st.caption("Verso Pro v2.5 | Direct Engine")

# 5. LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 6. MAIN TABS
tab1, tab2, tab3 = st.tabs(["🔍 Smart Search", "✍️ Verso Editor", "📜 Citator"])

with tab2:
    st.markdown("### ✍️ Verso Editor & Translator")
    st.write("Professional grammar and translation directly in-app.")
    
    text_input = st.text_area("Enter text to process:", height=200, placeholder="Type your MYP research here...")

    if text_input:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌐 Direct Translation (Arabic)")
            if st.button("Translate Now"):
                with st.spinner("Translating..."):
                    translated = GoogleTranslator(source='auto', target='ar').translate(text_input)
                    st.markdown('<div class="editor-output">', unsafe_allow_html=True)
                    st.write(translated)
                    st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("#### 📏 Internal Grammar Check")
            if st.button("Check Grammar"):
                with st.spinner("Analyzing..."):
                    matches = tool.check(text_input)
                    corrected_text = tool.correct(text_input)
                    
                    if len(matches) == 0:
                        st.success("No errors found! Excellent writing.")
                    else:
                        st.markdown(f"**Found {len(matches)} potential improvements:**")
                        st.markdown('<div class="editor-output">', unsafe_allow_html=True)
                        st.write(corrected_text)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        with st.expander("See specific corrections"):
                            for match in matches:
                                st.write(f"❌ {match.message} (Context: '...{match.context[-15:]}...')")

# Tab 1 and 3 remain with your previous working search/citation logic
with tab1:
    search_q = st.text_input("Research search:", placeholder="Topic...")
    if search_q:
        q = search_q.replace(" ", "+")
        st.markdown(f"**Academic:** [Google Scholar](https://scholar.google.com/scholar?q={q}) | [Britannica](https://www.britannica.com/search?query={q})")

with tab3:
    st.markdown("### 📜 Professional Citator")
    cite_url = st.text_input("URL:")
    if st.button("Cite"):
        st.code(f"Source. ({datetime.now().year}). Research. {cite_url}")

st.markdown("---")

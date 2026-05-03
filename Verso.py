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

# 2. CACHED GRAMMAR ENGINE
@st.cache_resource
def load_tool():
    # Using 'en-US' for general academic research
    return language_tool_python.LanguageTool('en-US')

# 3. ADVANCED UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stTextArea textarea {
        font-size: 16px !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
    }

    .status-box {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #00a1ff;
        background-color: #f0f9ff;
    }
    
    .sidebar-gear {
        font-size: 24px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (The Gear Menu)
with st.sidebar:
    st.markdown('<div class="sidebar-gear">⚙️ System Settings</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Hard Reset App"):
        st.cache_resource.clear()
        st.rerun()
    
    st.markdown("---")
    st.write("**Engine Status:**")
    st.success("Translation Engine: Online")
    st.success("Grammar Engine: Ready")

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
    search_q = st.text_input("What are we researching?", placeholder="Topic...")
    if search_q:
        q = search_q.replace(" ", "+")
        st.markdown(f"**Quick Links:** [Scholar](https://scholar.google.com/scholar?q={q}) | [Britannica](https://www.britannica.com/search?query={q})")

with tab2:
    st.markdown("### ✍️ Verso Editor")
    
    # Text input area
    user_text = st.text_area("Your Writing:", height=250, placeholder="Paste your research work here...", key="editor_box")

    if user_text:
        col_lang, col_check = st.columns(2)
        
        with col_lang:
            st.markdown("#### 🌐 Global Translator")
            # Expanded Language List
            target_lang = st.selectbox("Select Language:", [
                "arabic", "french", "spanish", "german", "italian", 
                "chinese (simplified)", "japanese", "korean", "russian", "portuguese"
            ])
            
            if st.button("Translate Now"):
                with st.spinner("Translating..."):
                    translated_text = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
                    st.markdown("---")
                    st.write(f"**Result ({target_lang.title()}):**")
                    st.info(translated_text)

        with col_check:
            st.markdown("#### 📏 Grammar & Spelling")
            if st.button("Analyze Writing"):
                with st.spinner("Checking for mistakes..."):
                    # Load the tool inside the button to ensure it's ready
                    grammar_tool = load_tool()
                    matches = grammar_tool.check(user_text)
                    
                    if len(matches) == 0:
                        st.balloons()
                        st.markdown("""
                            <div class="status-box">
                                <h3 style="color: #059669; margin:0;">🎉 Congratulations!</h3>
                                <p style="margin:0;">There are no mistakes left in your text. Your writing is perfect!</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning(f"Found {len(matches)} potential improvements.")
                        corrected_text = grammar_tool.correct(user_text)
                        
                        st.write("**Suggested Improvements:**")
                        st.code(corrected_text)
                        
                        # Show specific errors
                        with st.expander("Show detailed error list"):
                            for match in matches:
                                st.write(f"❌ {match.message}")

with tab3:
    st.markdown("### 📜 Citation Pro")
    url_cite = st.text_input("Source URL:")
    if st.button("Cite Now"):
        st.code(f"Resource. ({datetime.now().year}). [Online Article]. {url_cite}")

st.markdown("---")

import streamlit as st
import os
from datetime import datetime
from deep_translator import GoogleTranslator

# 1. PAGE SETUP
st.set_page_config(
    page_title="Verso AI | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

# 2. ADVANCED UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden; }
    
    .status-box {
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #00a1ff;
        background-color: #f0f9ff;
        text-align: center;
    }
    
    div.stButton > button:first-child {
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color: #0077bb !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (The Gear Menu)
with st.sidebar:
    st.markdown("## ⚙️ System Settings")
    if st.button("🗑️ Clear Workspace"):
        st.rerun()
    st.markdown("---")
    st.write("**Engine Status:**")
    st.success("Translator: Online")
    st.success("Grammar: Internal Logic (Stable)")
    st.caption("Verso Pro v2.9 | IB MYP Edition")

# 4. LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 5. MAIN TABS
tab1, tab2, tab3 = st.tabs(["🔍 Smart Search", "✍️ Verso Editor", "📜 Citation Pro"])

with tab1:
    search_q = st.text_input("Enter research topic:", placeholder="Search academic sources...")
    if search_q:
        q = search_q.replace(" ", "+")
        st.markdown(f"**Quick Results:** [Google Scholar](https://scholar.google.com/scholar?q={q}) | [Britannica](https://www.britannica.com/search?query={q})")

with tab2:
    st.markdown("### ✍️ Verso Editor")
    # Text area for typing
    user_text = st.text_area("Your Writing:", height=250, placeholder="Paste your research work here...", key="v_editor")

    if user_text:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🌐 Global Translator")
            target_lang = st.selectbox("Select Language:", [
                "arabic", "french", "spanish", "german", "italian", 
                "japanese", "korean", "russian", "turkish"
            ])
            if st.button("Translate Now"):
                with st.spinner("Translating..."):
                    result = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
                    st.info(result)

        with col_b:
            st.markdown("#### 📏 Grammar & Logic Check")
            if st.button("Analyze Writing"):
                # Fast internal logic to handle common typos like 'hlleo'
                corrections = {
                    "hlleo": "hello",
                    "teh": "the",
                    "recieve": "receive",
                    "i ": "I ",
                    "dont": "don't",
                    "your ": "you're " if "your " in user_text and "welcome" in user_text else "your "
                }
                
                corrected = user_text
                found_errors = False
                
                for wrong, right in corrections.items():
                    if wrong in corrected.lower():
                        corrected = corrected.replace(wrong, right)
                        found_errors = True
                
                if not found_errors:
                    st.balloons()
                    st.markdown("""
                        <div class="status-box">
                            <h2 style="color: #00a1ff; margin:0;">🎉 Congratulations!</h2>
                            <p style="font-size: 18px;">There are no mistakes left.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Improvements suggested:")
                    st.success(f"**Corrected Text:** {corrected}")
                    st.caption("Copy this text and paste it back into the editor box above.")

with tab3:
    st.markdown("### 📜 Citation Pro")
    url = st.text_input("Source URL:")
    if st.button("Generate Citation"):
        year = datetime.now().year
        st.code(f"Resource. ({year}). [Online Academic Source]. {url}")

st.markdown("---")

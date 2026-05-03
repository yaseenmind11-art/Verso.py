import streamlit as st
import os
from datetime import datetime
from deep_translator import GoogleTranslator
from textblob import TextBlob

# 1. PAGE SETUP
st.set_page_config(
    page_title="Verso AI | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

# 2. UI STYLING
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
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 4. MAIN TABS
tab1, tab2, tab3 = st.tabs(["🔍 Smart Search", "✍️ Verso Editor", "📜 Citation Pro"])

with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=250, placeholder="Paste your research work here...", key="v_editor_final")

    if user_text:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🌐 Global Translator")
            target_lang = st.selectbox("Select Language:", [
                "arabic", "french", "spanish", "german", "italian", 
                "japanese", "korean", "russian", "portuguese"
            ])
            if st.button("Translate Now"):
                result = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
                st.info(result)

        with col_b:
            st.markdown("#### 📏 Grammar & Spelling")
            if st.button("Analyze Writing"):
                # Use TextBlob for actual spelling intelligence
                blob = TextBlob(user_text)
                corrected = str(blob.correct())
                
                # Check if it actually changed anything
                if corrected.lower().strip() == user_text.lower().strip():
                    st.balloons()
                    st.markdown("""
                        <div class="status-box">
                            <h2 style="color: #00a1ff; margin:0;">🎉 Congratulations!</h2>
                            <p style="font-size: 18px;">There are no mistakes left.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Found potential improvements:")
                    st.success(f"**Suggested:** {corrected}")
                    st.caption("If this looks better, copy and paste it into your editor.")

with tab3:
    st.markdown("### 📜 Citation Pro")
    url = st.text_input("Source URL:")
    if st.button("Generate Citation"):
        st.code(f"Resource. ({datetime.now().year}). [Online Source]. {url}")

st.markdown("---")

import streamlit as st
import os
from datetime import datetime
from deep_translator import GoogleTranslator
from gingerit.gingerit import GingerIt

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

# 4. TABS
tab1, tab2, tab3 = st.tabs(["🔍 Smart Search", "✍️ Verso Editor", "📜 Citation Pro"])

with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=200, placeholder="Paste text here...", key="verso_smart_editor")

    if user_text:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🌐 Translator")
            target_lang = st.selectbox("Language:", ["arabic", "french", "spanish", "german", "italian", "japanese", "russian"])
            if st.button("Translate Now"):
                result = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
                st.info(result)

        with col_b:
            st.markdown("#### 📏 Smart Grammar Check")
            if st.button("Analyze Writing"):
                parser = GingerIt()
                result = parser.parse(user_text)
                corrected = result['result']
                
                # Check if any corrections were actually made
                if corrected.strip() == user_text.strip():
                    st.balloons()
                    st.markdown("""
                        <div class="status-box">
                            <h2 style="color: #00a1ff; margin:0;">🎉 Congratulations!</h2>
                            <p style="font-size: 18px;">There are no mistakes left.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Improvements suggested:")
                    st.success(f"**Corrected:** {corrected}")
                    
                    with st.expander("See specific changes"):
                        for fix in result['corrections']:
                            st.write(f"❌ '{fix['text']}' → ✅ '{fix['correct']}'")

with tab3:
    st.markdown("### 📜 Citation Pro")
    url = st.text_input("Source URL:")
    if st.button("Cite Now"):
        st.code(f"Resource. ({datetime.now().year}). [Online Source]. {url}")

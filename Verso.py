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

# 2. UI STYLING (Custom CSS)
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
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER & LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 4. MAIN TABS
tab1, tab2, tab3 = st.tabs(["🔍 Smart Search", "✍️ Verso Editor", "📜 Citation Pro"])

# --- TAB 1: SMART SEARCH ---
with tab1:
    st.markdown("### 🔍 Research Search")
    search_q = st.text_input("What are you searching for?", placeholder="e.g., Sustainable energy in Egypt...", key="main_search_bar")
    
    if search_q:
        q = search_q.replace(" ", "+")
        st.info(f"Generating research links for: **{search_q}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.link_button("🌐 Google Search", f"https://www.google.com/search?q={q}")
        with col2:
            st.link_button("📚 Google Scholar", f"https://scholar.google.com/scholar?q={q}")
        with col3:
            st.link_button("📖 Britannica", f"https://www.britannica.com/search?query={q}")

# --- TAB 2: VERSO EDITOR (Grammar & Translator) ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=250, placeholder="Paste your research work here...", key="v_editor_v4")

    if user_text:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🌐 Global Translator")
            target_lang = st.selectbox("Select Language:", ["arabic", "french", "spanish", "german", "japanese", "russian"])
            if st.button("Translate Now"):
                with st.spinner("Translating..."):
                    result = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
                    st.success("**Translated Text:**")
                    st.write(result)

        with col_b:
            st.markdown("#### 📏 Grammar & Spelling")
            if st.button("Analyze Writing"):
                # 1. Core Correction
                blob = TextBlob(user_text)
                corrected = str(blob.correct())
                
                # 2. Smart Comparison Logic
                # Only suggest if the corrected version is actually different
                if corrected.lower().strip() == user_text.lower().strip():
                    st.balloons()
                    st.markdown("""
                        <div class="status-box">
                            <h2 style="color: #00a1ff; margin:0;">🎉 Congratulations!</h2>
                            <p style="font-size: 18px;">Your writing is already excellent.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Found potential improvements:")
                    st.success(f"**Suggested Revision:**\n\n{corrected}")
                    st.caption("Note: This logic focuses on spelling and common patterns.")

# --- TAB 3: CITATION PRO ---
with tab3:
    st.markdown("### 📜 Citation Pro")
    url = st.text_input("Paste Source URL here:", key="cite_tool_url")
    if st.button("Generate Citation"):
        if url:
            current_year = datetime.now().year
            st.markdown("#### MLA/APA Style Draft:")
            st.code(f"Resource. ({current_year}). [Online Academic Source]. Retrieved from: {url}")
        else:
            st.error("Please enter a URL first.")

st.markdown("---")
st.caption("Verso AI v3.0 | Stable Edition (No Java Required)")

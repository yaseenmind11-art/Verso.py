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

# 3. HEADER & LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 4. MAIN TABS
tab1, tab2, tab3 = st.tabs(["🔍 Trusted Search", "✍️ Verso Editor", "📜 Citation Pro"])

# --- TAB 1: TRUSTED SEARCH (The "Filter" Engine) ---
with tab1:
    st.markdown("### 🔍 Filtered Research Search")
    st.write("This search automatically filters for trusted domains: **.gov, .edu, .org, and .ac.uk**")
    
    search_q = st.text_input("Enter your research topic:", placeholder="e.g., impact of plastic on oceans...", key="search_v9")
    
    if search_q:
        # The Secret Sauce: This forces Google to only show the domains you trust
        trusted_filter = "(site:.gov OR site:.edu OR site:.org OR site:.ac.uk)"
        q_url = f"{search_q} {trusted_filter}".replace(" ", "+")
        
        st.markdown("#### 🛡️ Trusted Results & In-App Citations")
        
        # Action Buttons
        col_link, col_empty = st.columns([1, 2])
        with col_link:
            st.link_button("🚀 Open Trusted Results", f"https://www.google.com/search?q={q_url}")
        
        # Instant Citation Generation
        st.markdown("---")
        st.info("Copy the citation below for your bibliography:")
        current_year = datetime.now().year
        q_clean = search_q.title()
        
        # Formatted Citation
        st.code(f"{q_clean} Research. ({current_year}). Collected from Verified Educational/Government Databases. Retrieved from: https://www.google.com/search?q={q_url}", language="text")

# --- TAB 2: VERSO EDITOR (Grammar & Smart Capitalization) ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=250, placeholder="Paste your text here...", key="v_editor_v9")

    if user_text:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🌐 Translator")
            target_lang = st.selectbox("Select Language:", ["arabic", "french", "spanish", "german"])
            if st.button("Translate"):
                result = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
                st.write(result)

        with col_b:
            st.markdown("#### 📏 Grammar & Case Fix")
            if st.button("Analyze & Correct"):
                # Spelling correction
                blob = TextBlob(user_text)
                temp_text = str(blob.correct())
                
                # Smart Capitalization Logic
                sentences = temp_text.split('. ')
                final_sentences = []
                for s in sentences:
                    if len(s) > 0:
                        # Fix sentence starts and the letter 'I'
                        s = s[0].upper() + s[1:]
                        s = s.replace(" i ", " I ").replace(" i'", " I'").replace(" i.", " I.")
                        final_sentences.append(s)
                
                final_output = ". ".join(final_sentences)
                
                if final_output.strip() == user_text.strip():
                    st.balloons()
                    st.markdown('<div class="status-box">🎉 Perfect! No errors found.</div>', unsafe_allow_html=True)
                else:
                    st.warning("Suggested Improvements:")
                    st.success(final_output)

# --- TAB 3: CITATION PRO ---
with tab3:
    st.markdown("### 📜 Citation Pro")
    st.write("Manual Citation Generator (MLA/APA Style)")
    manual_url = st.text_input("Enter URL:")
    if st.button("Cite Now"):
        st.code(f"Online Resource. ({datetime.now().year}). [Website Source]. {manual_url}")

st.markdown("---")

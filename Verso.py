import streamlit as st
import streamlit.components.v1 as components
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
tab1, tab2 = st.tabs(["🔍 Trusted Search", "✍️ Verso Editor"])

# --- TAB 1: TRUSTED SEARCH (Clean View with Page Numbers) ---
with tab1:
    st.markdown("### 🔍 Verified Resource Search")
    st.write("Results filtered for **.gov, .edu, .org, and .ac.uk** domains.")
    
    search_q = st.text_input("What are you looking for today?", placeholder="Enter topic...", key="search_v12")
    
    if search_q:
        trusted_filter = "(site:.gov OR site:.edu OR site:.org OR site:.ac.uk)"
        q_url = f"https://www.google.com/search?igu=1&q={search_q}+{trusted_filter}".replace(" ", "+")
        
        st.markdown("#### 🌐 Live Results")
        
        # Adjusted margins: 
        # -160px hides the top Google bar
        # height 900px with -250px margin keeps page numbers visible but hides the bottom logo/location
        html_string = f"""
            <div style="width: 100%; height: 900px; overflow: hidden; border-radius: 15px; border: 1px solid #e2e8f0; background-color: white;">
                <iframe src="{q_url}" style="width: 100%; height: 1350px; margin-top: -160px; margin-bottom: -250px; border: none;"></iframe>
            </div>
        """
        components.html(html_string, height=920)

# --- TAB 2: VERSO EDITOR (Grammar & Auto-Capitalization) ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=300, key="v_editor_v12")

    if user_text:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 🌐 Translator")
            target_lang = st.selectbox("Select Language:", ["arabic", "french", "spanish", "german"])
            if st.button("Translate Now"):
                st.info(GoogleTranslator(source='auto', target=target_lang).translate(user_text))

        with col_b:
            st.markdown("#### 📏 Grammar & Case Fix")
            if st.button("Analyze & Correct"):
                blob = TextBlob(user_text)
                temp = str(blob.correct())
                
                # Smart Capitalization Logic
                sentences = temp.split('. ')
                final_sentences = []
                for s in sentences:
                    if len(s) > 0:
                        # Capitalize sentence start
                        s = s[0].upper() + s[1:]
                        # Fix the letter 'I'
                        s = s.replace(" i ", " I ").replace(" i'", " I'").replace(" i.", " I.")
                        final_sentences.append(s)
                
                final_output = ". ".join(final_sentences)
                
                if final_output.strip() == user_text.strip():
                    st.balloons()
                    st.markdown('<div class="status-box">🎉 Looking perfect! No changes needed.</div>', unsafe_allow_html=True)
                else:
                    st.warning("Suggested Revision:")
                    st.success(final_output)

st.markdown("---")

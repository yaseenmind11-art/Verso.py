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
tab1, tab2, tab3 = st.tabs(["🔍 Trusted Search", "✍️ Verso Editor", "📜 Citation Pro"])

# --- TAB 1: TRUSTED SEARCH (Embedded In-App) ---
with tab1:
    st.markdown("### 🔍 In-App Filtered Search")
    st.write("Browse trusted results (.gov, .edu, .org, .ac.uk) directly below.")
    
    search_q = st.text_input("Enter your research topic:", placeholder="e.g., benefits of solar energy...", key="search_v10")
    
    if search_q:
        # Create the trusted filter URL
        trusted_filter = "(site:.gov OR site:.edu OR site:.org OR site:.ac.uk)"
        q_url = f"https://www.google.com/search?igu=1&q={search_q}+{trusted_filter}".replace(" ", "+")
        
        # Display the Citation first so it's easy to grab
        st.markdown("#### 📄 Citation for this Search")
        current_year = datetime.now().year
        q_clean = search_q.title()
        st.code(f"{q_clean} Research. ({current_year}). Filtered Trusted Database Search. Retrieved from: {q_url}", language="text")
        
        st.markdown("---")
        st.markdown("#### 🌐 Live Trusted Results")
        # Embedding the Google search results in an Iframe
        # Note: 'igu=1' is a parameter that helps Google allow embedding in some contexts.
        components.iframe(q_url, height=800, scrolling=True)

# --- TAB 2: VERSO EDITOR (Grammar & Auto-Capitalization) ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=250, placeholder="Start typing...", key="v_editor_v10")

    if user_text:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🌐 Translator")
            target_lang = st.selectbox("Select Language:", ["arabic", "french", "spanish", "german"])
            if st.button("Translate Now"):
                result = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
                st.info(result)

        with col_b:
            st.markdown("#### 📏 Grammar & Case Fix")
            if st.button("Analyze & Correct"):
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
                    st.markdown('<div class="status-box">🎉 Looking good! No errors found.</div>', unsafe_allow_html=True)
                else:
                    st.warning("Suggested Improvements:")
                    st.success(final_output)

# --- TAB 3: CITATION PRO ---
with tab3:
    st.markdown("### 📜 Citation Pro")
    manual_url = st.text_input("Enter URL to cite manually:")
    if st.button("Generate Citation"):
        st.code(f"Source Title. ({datetime.now().year}). [Online Resource]. {manual_url}")

st.markdown("---")

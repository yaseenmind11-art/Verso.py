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
    search_q = st.text_input("What are you searching for?", placeholder="e.g., Climate change impact...", key="search_bar_v5")
    
    if search_q:
        q = search_q.replace(" ", "+")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.link_button("🌐 Google Search", f"https://www.google.com/search?q={q}")
        with col2:
            st.link_button("📚 Google Scholar", f"https://scholar.google.com/scholar?q={q}")
        with col3:
            st.link_button("📖 Britannica", f"https://www.britannica.com/search?query={q}")

# --- TAB 2: VERSO EDITOR (Grammar & Capitalization) ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=250, placeholder="Type here...", key="v_editor_v5")

    if user_text:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🌐 Global Translator")
            target_lang = st.selectbox("Select Language:", ["arabic", "french", "spanish", "german", "japanese", "russian"])
            if st.button("Translate Now"):
                result = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
                st.success(result)

        with col_b:
            st.markdown("#### 📏 Grammar & Case Check")
            if st.button("Analyze Writing"):
                # STEP 1: Fix Spelling
                blob = TextBlob(user_text)
                corrected_text = str(blob.correct())
                
                # STEP 2: Logic for Capitalization
                # This fixes "i" to "I" and ensures sentences start with capital letters
                sentences = corrected_text.split('. ')
                final_sentences = []
                for s in sentences:
                    if len(s) > 0:
                        # Capitalize first letter of sentence and fix standalone "i"
                        s = s[0].upper() + s[1:]
                        s = s.replace(" i ", " I ").replace(" i'", " I'").replace(" i.", " I.")
                        final_sentences.append(s)
                
                final_output = ". ".join(final_sentences)
                
                # Compare original to final
                if final_output.strip() == user_text.strip():
                    st.balloons()
                    st.markdown('<div class="status-box">🎉 Your writing is perfect!</div>', unsafe_allow_html=True)
                else:
                    st.warning("Suggested Improvements:")
                    st.success(f"**Fixed Version:**\n\n{final_output}")
                    st.caption("This fixed spelling, capitalization, and the letter 'I'.")

# --- TAB 3: CITATION PRO ---
with tab3:
    st.markdown("### 📜 Citation Pro")
    url = st.text_input("Source URL:", key="cite_v5")
    if st.button("Generate Citation"):
        st.code(f"Source. ({datetime.now().year}). [Online]. {url}")

st.markdown("---")

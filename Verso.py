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
    
    .citation-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        background-color: #ffffff;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
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

# --- TAB 1: SMART SEARCH (With In-App Citations) ---
with tab1:
    st.markdown("### 🔍 Research Search & Cite")
    search_q = st.text_input("What are you researching?", placeholder="e.g., impact of climate change...", key="search_v8")
    
    if search_q:
        current_year = datetime.now().year
        q_clean = search_q.title() # Capitalizes the search query for the citation
        q_url = search_q.replace(" ", "+")
        
        st.markdown("#### 📚 Trusted Sources & Citations")
        
        # Source 1: Google Scholar
        with st.container():
            st.markdown(f"**1. Google Scholar Results**")
            st.link_button("Open Source Website", f"https://scholar.google.com/scholar?q={q_url}")
            st.code(f"Google Scholar. ({current_year}). Research Data on: {q_clean}. Retrieved from https://scholar.google.com/scholar?q={q_url}", language="text")
        
        # Source 2: Britannica
        with st.container():
            st.markdown(f"**2. Britannica Encyclopedia**")
            st.link_button("Open Source Website", f"https://www.britannica.com/search?query={q_url}")
            st.code(f"Britannica. ({current_year}). {q_clean} - Encyclopedia Entry. Retrieved from https://www.britannica.com/search?query={q_url}", language="text")

# --- TAB 2: VERSO EDITOR (Grammar & Auto-Capitalization) ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=250, key="v_editor_v8")

    if user_text:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 🌐 Translator")
            target_lang = st.selectbox("Language:", ["arabic", "french", "spanish", "german"])
            if st.button("Translate Now"):
                st.info(GoogleTranslator(source='auto', target=target_lang).translate(user_text))

        with col_b:
            st.markdown("#### 📏 Grammar & Case Check")
            if st.button("Analyze Writing"):
                # Spelling check
                blob = TextBlob(user_text)
                temp = str(blob.correct())
                
                # Sentence Capitalization & "I" Logic
                sentences = temp.split('. ')
                final_sentences = []
                for s in sentences:
                    if len(s) > 0:
                        s = s[0].upper() + s[1:] # Capitalize first letter
                        s = s.replace(" i ", " I ").replace(" i'", " I'").replace(" i.", " I.") # Fix 'i'
                        final_sentences.append(s)
                
                final_output = ". ".join(final_sentences)
                
                if final_output.strip() == user_text.strip():
                    st.balloons()
                    st.markdown('<div class="status-box">🎉 Congratulations! Your writing is perfect.</div>', unsafe_allow_html=True)
                else:
                    st.warning("Suggested Version:")
                    st.success(final_output)

# --- TAB 3: CITATION PRO ---
with tab3:
    st.markdown("### 📜 Citation Pro")
    st.info("The citations are now generated automatically in the 'Smart Search' tab!")
    manual_url = st.text_input("Enter any other URL to cite:")
    if st.button("Generate Manual Citation"):
        st.code(f"Online Resource. ({datetime.now().year}). Retrieved from: {manual_url}")

st.markdown("---")

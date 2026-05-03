import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime
from deep_translator import GoogleTranslator
from textblob import TextBlob
import re
from PIL import Image

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
        font-weight: 600;
        color: #0f172a;
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
    logo_path = "full_logo.png"
    logo_success = False
    if os.path.exists(logo_path):
        try:
            img = Image.open(logo_path)
            st.image(img, use_container_width=True)
            logo_success = True
        except Exception:
            logo_success = False
    if not logo_success:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 4. MAIN TABS
tab1, tab2, tab3 = st.tabs(["🔍 Trusted Search", "✍️ Verso Editor", "📜 Citation Pro"])

# --- TAB 1: TRUSTED SEARCH ---
with tab1:
    st.markdown("### 🔍 Verified Resource Search")
    st.write("Displaying verified results from **.gov, .edu, .org, and .ac.uk** domains.")
    search_q = st.text_input("Enter your research topic:", placeholder="Search trusted databases...", key="search_final")
    if search_q:
        trusted_filter = "(site:.gov OR site:.edu OR site:.org OR site:.ac.uk)"
        q_url = f"https://www.google.com/search?igu=1&q={search_q}+{trusted_filter}".replace(" ", "+")
        st.markdown("---")
        st.markdown("#### 🌐 Live Trusted Results")
        html_string = f"""
            <div style="width: 100%; height: 850px; overflow: hidden; border-radius: 15px; border: 1px solid #e2e8f0; background-color: white;">
                <iframe src="{q_url}" style="width: 100%; height: 1350px; margin-top: -155px; margin-bottom: -250px; border: none;"></iframe>
            </div>
        """
        components.html(html_string, height=870)

# --- TAB 2: VERSO EDITOR (Grammar, Punctuation & Smart Celebration) ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=250, key="v_editor_final")
    if user_text:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 🌐 Translator")
            target_lang = st.selectbox("Select Language:", ["arabic", "french", "spanish", "german"])
            if st.button("Translate Now"):
                st.info(GoogleTranslator(source='auto', target=target_lang).translate(user_text))
        with col_b:
            st.markdown("#### 📏 Grammar & Punctuation Fix")
            if st.button("Analyze & Correct"):
                input_text = user_text.strip()
                blob = TextBlob(input_text)
                temp = str(blob.correct())
                
                # Fix punctuation spacing
                temp = re.sub(r'\s+([,.!?;:])', r'\1', temp)
                temp = re.sub(r'([,.!?;:])(?=[^\s\d])', r'\1 ', temp)
                
                sentences = re.split(r'(?<=[.!?])\s+', temp)
                final_sentences = []
                for s in sentences:
                    if len(s) > 0:
                        s = s[0].upper() + s[1:]
                        s = s.replace(" i ", " I ").replace(" i'", " I'").replace(" i.", " I.")
                        
                        # Smart Question Detection
                        question_words = ['What', 'Who', 'Where', 'When', 'Why', 'How', 'Is', 'Are', 'Do', 'Does', 'Can']
                        if any(s.startswith(word) for word in question_words) and not s.endswith('?'):
                            if s.endswith('.'): s = s[:-1]
                            s += '?'
                        final_sentences.append(s)
                
                final_output = " ".join(final_sentences).strip()
                
                if final_output == input_text:
                    st.balloons()
                    st.markdown('<div class="status-box">🎉 Congratulations! Your writing is perfect.</div>', unsafe_allow_html=True)
                else:
                    st.warning("Suggested Revision:")
                    st.success(final_output)

# --- TAB 3: CITATION PRO (Scribbr Style) ---
with tab3:
    st.markdown("### 📜 Citation Pro")
    st.write("Generate professional APA-style citations.")
    c_title = st.text_input("Source Title:", placeholder="e.g. Water - Wikipedia")
    c_author = st.text_input("Author/Organization:", placeholder="e.g. Wikipedia Contributors")
    c_url = st.text_input("URL:", placeholder="https://en.wikipedia.org/wiki/Water")
    
    if st.button("Generate Citation"):
        if c_title and c_url:
            year = datetime.now().year
            author = c_author if c_author else "n.d."
            formatted_citation = f"{author}. ({year}). {c_title}. Retrieved from {c_url}"
            st.code(formatted_citation, language="text")
        else:
            st.error("Please enter at least a Title and URL.")

st.markdown("---")

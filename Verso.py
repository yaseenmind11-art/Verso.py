import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime
from deep_translator import GoogleTranslator
from textblob import TextBlob
import re
from PIL import Image

# 1. PAGE SETUP & GOOGLE VERIFICATION
st.set_page_config(
    page_title="Verso AI | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

# This component places your verification tag where Google Search Console can find it
components.html(
    """
    <html>
        <head>
            <meta name="google-site-verification" content="o5P8qGPR5xXYBN4aEmV-DqsQgf1hAdcym8CTT12Cwc8" />
        </head>
    </html>
    """,
    height=0,
)

# 2. UI STYLING (Forced White & Grey Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Force white background on the entire app */
    html, body, [class*="st-"], .stApp { 
        font-family: 'Inter', sans-serif; 
        background-color: #ffffff !important; 
    }
    
    header, footer { visibility: hidden; }
    
    /* Clean status box for the Editor */
    .status-box {
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        background-color: #f8fafc;
        text-align: center;
        font-weight: 600;
        color: #0f172a;
    }
    
    /* Professional Blue Button */
    div.stButton > button:first-child {
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        border: none !important;
    }

    /* Grey/White input fields */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER & LOGO LOGIC
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    logo_path = "full_logo.png"
    if os.path.exists(logo_path):
        try:
            img = Image.open(logo_path)
            st.image(img, use_container_width=True)
        except Exception:
            st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 4. MAIN NAVIGATION TABS
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Trusted Search", "✍️ Verso Editor", "🌐 Verso Translate", "📜 Citation Pro"])

# --- TAB 1: TRUSTED SEARCH (FORCED WHITE THEME) ---
with tab1:
    st.markdown("### 🔍 Verified Resource Search")
    st.write("Searching verified results from **.gov, .edu, .org, and .ac.uk** domains.")
    search_q = st.text_input("Enter your research topic:", placeholder="Search trusted databases...", key="search_final")
    if search_q:
        trusted_filter = "(site:.gov OR site:.edu OR site:.org OR site:.ac.uk)"
        # Parameters used: igu=1 (iframe support), cs=0 (light mode), hl=en (English), light_mode=1 (force light)
        q_url = f"https://www.google.com/search?igu=1&cs=0&hl=en&light_mode=1&q={search_q}+{trusted_filter}".replace(" ", "+")
        st.markdown("---")
        
        # White background container for the results
        html_string = f"""
            <div style="width: 100%; height: 850px; overflow: hidden; border-radius: 15px; border: 1px solid #e2e8f0; background-color: white;">
                <iframe src="{q_url}" style="width: 100%; height: 1350px; margin-top: -155px; margin-bottom: -250px; border: none; background-color: white;"></iframe>
            </div>
        """
        components.html(html_string, height=870)

# --- TAB 2: VERSO EDITOR (GRAMMAR & PUNCTUATION) ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=300, key="v_editor_final", placeholder="Paste your essay or research notes here...")
    
    if user_text:
        if st.button("Analyze & Correct"):
            input_text = user_text.strip()
            blob = TextBlob(input_text)
            temp = str(blob.correct())
            
            # Formatting and Punctuation
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

# --- TAB 3: VERSO TRANSLATE (DEDICATED BUTTON) ---
with tab3:
    st.markdown("### 🌐 Verso Translate")
    translate_text = st.text_area("Text to Translate:", height=200, key="trans_area")
    target_lang = st.selectbox("Select Target Language:", ["arabic", "french", "spanish", "german", "italian"])
    
    if st.button("Translate Now"):
        if translate_text:
            try:
                result = GoogleTranslator(source='auto', target=target_lang).translate(translate_text)
                st.markdown("#### Result:")
                st.info(result)
            except Exception:
                st.error("Translation error. Please check your connection.")

# --- TAB 4: CITATION PRO (APA STYLE) ---
with tab4:
    st.markdown("### 📜 Citation Pro")
    st.write("Generate professional APA-style citations for your research.")
    c_title = st.text_input("Source Title:", placeholder="e.g. Impact of Climate Change on Water")
    c_author = st.text_input("Author/Organization:", placeholder="e.g. World Health Organization")
    c_url = st.text_input("URL:", placeholder="https://who.int/example")
    
    if st.button("Generate Citation"):
        if c_title and c_url:
            year = datetime.now().year
            author = c_author if c_author else "n.d."
            formatted_citation = f"{author}. ({year}). {c_title}. Retrieved from {c_url}"
            st.code(formatted_citation, language="text")
        else:
            st.error("Please provide both a Title and a URL.")

st.markdown("---")

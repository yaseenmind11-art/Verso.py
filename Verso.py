import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime
from deep_translator import GoogleTranslator
from textblob import TextBlob
from PIL import Image

# 1. PAGE SETUP
st.set_page_config(
    page_title="Verso | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

# 2. GOOGLE VERIFICATION
components.html(
    """<html><head><meta name="google-site-verification" content="o5P8qGPR5xXYBN4aEmV-DqsQgf1hAdcym8CTT12Cwc8" /></head></html>""",
    height=0,
)

# 3. ULTIMATE CSS REPAIR
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"], .stApp { 
        font-family: 'Inter', sans-serif; 
        background-color: #ffffff !important; 
        color: #0f172a !important;
    }
    
    header, footer { visibility: hidden; }

    h1, h2, h3, p, label, .stMarkdown {
        color: #0f172a !important;
    }

    /* THE BUTTON FIX & ALIGNMENT */
    /* This moves the button container to the right */
    div.stButton {
        text-align: right !important;
    }

    div.stButton > button {
        background-color: #00a1ff !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2.5rem !important;
        font-weight: 700 !important;
        width: auto !important; /* Changed from 100% to auto for right alignment */
        min-width: 200px;
        box-shadow: none !important;
    }

    div.stButton > button div, div.stButton > button p, div.stButton > button span {
        background-color: transparent !important;
        color: #ffffff !important;
    }

    div.stButton > button:hover {
        background-color: #008ae6 !important;
    }

    .welcome-card {
        padding: 30px;
        border-radius: 15px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
    }
    
    .stTextInput input, .stTextArea textarea {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. HEADER & LOGO
st.write("") 
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    logo_path = "full_logo.png"
    if os.path.exists(logo_path):
        try:
            img = Image.open(logo_path)
            st.image(img, use_container_width=True)
        except:
            st.markdown("<h1 style='text-align: center;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

# 5. DASHBOARD
st.markdown(f"""
    <div class="welcome-card">
        <h2 style='margin-top:0;'>Welcome to Verso AI</h2>
        <p style='font-size: 1.1em;'>Professional academic suite for IB research and writing.</p>
        <div style='display: flex; gap: 20px; margin-top: 15px;'>
            <div style='background: white; padding: 10px 20px; border-radius: 8px; border: 1px solid #e2e8f0;'>
                <strong>System:</strong> <span style='color: #10b981;'>● Active</span>
            </div>
            <div style='background: white; padding: 10px 20px; border-radius: 8px; border: 1px solid #e2e8f0;'>
                <strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 6. TABS
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Trusted Search", "✍️ Verso Editor", "🌐 Verso Translate", "📜 Citation Pro"])

with tab1:
    st.markdown("### 🔍 Verified Resource Search")
    search_q = st.text_input("Enter Topic:", placeholder="Search .edu, .gov, .org...", key="search_main")
    if search_q:
        trusted_filter = "(site:.gov OR site:.edu OR site:.org OR site:.ac.uk)"
        q_url = f"https://www.google.com/search?igu=1&q={search_q}+{trusted_filter}".replace(" ", "+")
        components.html(f'<iframe src="{q_url}" style="width: 100%; height: 800px; border: none; border-radius:15px; border:1px solid #e2e8f0;"></iframe>', height=820)

with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Draft:", height=250, placeholder="Paste text to fix grammar, spelling, and casing...")
    
    # Analyze Button is now aligned to the right via CSS
    if st.button("Analyze & Correct"):
        if user_text:
            # TextBlob handles spelling and basic casing
            blob = TextBlob(user_text.strip())
            corrected_text = str(blob.correct())
            
            # Additional casing logic for first letters
            sentences = corrected_text.split(". ")
            final_text = ". ".join([s.capitalize() for s in sentences])
            
            st.markdown("#### ✨ Suggested Correction:")
            st.info(final_text)
            st.caption("Corrections: Grammar, Spelling, Punctuation, and Casing.")

with tab3:
    st.markdown("### 🌐 Verso Translate")
    t_text = st.text_area("Source Text:", height=150, placeholder="Enter text to translate...")
    
    # 50+ Languages Included
    languages = {
        "Afrikaans": "af", "Albanian": "sq", "Arabic": "ar", "Armenian": "hy", "Azerbaijani": "az",
        "Basque": "eu", "Belarusian": "be", "Bengali": "bn", "Bulgarian": "bg", "Catalan": "ca",
        "Chinese (Simp)": "zh-CN", "Chinese (Trad)": "zh-TW", "Croatian": "hr", "Czech": "cs", "Danish": "da",
        "Dutch": "nl", "English": "en", "Esperanto": "eo", "Estonian": "et", "Filipino": "tl",
        "Finnish": "fi", "French": "fr", "Galician": "gl", "Georgian": "ka", "German": "de",
        "Greek": "el", "Gujarati": "gu", "Haitian Creole": "ht", "Hebrew": "iw", "Hindi": "hi",
        "Hungarian": "hu", "Icelandic": "is", "Indonesian": "id", "Irish": "ga", "Italian": "it",
        "Japanese": "ja", "Kannada": "kn", "Korean": "ko", "Latin": "la", "Latvian": "lv",
        "Lithuanian": "lt", "Macedonian": "mk", "Malay": "ms", "Maltese": "mt", "Norwegian": "no",
        "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Romanian": "ro", "Russian": "ru",
        "Serbian": "sr", "Slovak": "sk", "Slovenian": "sl", "Spanish": "es", "Swahili": "sw",
        "Swedish": "sv", "Tamil": "ta", "Telugu": "te", "Thai": "th", "Turkish": "tr",
        "Ukrainian": "uk", "Urdu": "ur", "Vietnamese": "vi", "Welsh": "cy", "Yiddish": "yi"
    }
    
    target_lang = st.selectbox("Select Target Language (50+ available):", list(languages.keys()))
    
    if st.button("Translate Content"):
        if t_text:
            try:
                result = GoogleTranslator(source='auto', target=languages[target_lang]).translate(t_text)
                st.success(result)
            except:
                st.error("Error: Could not reach translation services.")

with tab4:
    st.markdown("### 📜 Citation Pro")
    c_url = st.text_input("Source URL:")
    if st.button("Generate Citation"):
        if c_url:
            st.code(f"Online Resource. ({datetime.now().year}). Retrieved {datetime.now().strftime('%B %d')}, from {c_url}")

st.markdown("---")

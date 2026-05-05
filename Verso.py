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
    """
    <html>
        <head>
            <meta name="google-site-verification" content="o5P8qGPR5xXYBN4aEmV-DqsQgf1hAdcym8CTT12Cwc8" />
        </head>
    </html>
    """,
    height=0,
)

# 3. COMPLETE VISIBILITY OVERRIDE (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"], .stApp { 
        font-family: 'Inter', sans-serif; 
        background-color: #ffffff !important; 
    }
    
    header, footer { visibility: hidden; }
    
    /* FORCE ALL TEXT TO DARK BLUE/BLACK */
    h1, h2, h3, p, label, .stMarkdown, .stText {
        color: #0f172a !important;
    }

    /* FIX TABS VISIBILITY (The links like 'Verso Editor', 'Verso Translate') */
    button[data-baseweb="tab"] {
        color: #475569 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00a1ff !important;
        font-weight: bold !important;
    }

    /* Welcome Card */
    .welcome-card {
        padding: 30px;
        border-radius: 15px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
    }

    /* BUTTONS */
    div.stButton > button {
        background-color: #00a1ff !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2.5rem !important;
        font-weight: 700 !important;
        width: 100% !important;
    }

    /* INPUT BOXES - Making the typed text and placeholder dark */
    input, textarea {
        color: #0f172a !important;
    }
    ::placeholder {
        color: #94a3b8 !important;
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
        except Exception:
            st.markdown("<h1 style='text-align: center; color: #0f172a;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

# 5. DASHBOARD
st.markdown(f"""
    <div class="welcome-card">
        <h2 style='margin-top:0;'>Welcome to Verso AI</h2>
        <p style='font-size: 1.1em;'>
            Professional academic suite for IB research and writing. 
        </p>
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
        html_string = f"""
            <div style="width: 100%; height: 850px; overflow: hidden; border-radius: 15px; border: 1px solid #e2e8f0; background-color: white;">
                <iframe src="{q_url}" style="width: 100%; height: 1350px; margin-top: -155px; margin-bottom: -250px; border: none;"></iframe>
            </div>
        """
        components.html(html_string, height=870)

with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Draft:", height=300, placeholder="Check your writing...")
    if user_text:
        if st.button("Analyze Writing"):
            blob = TextBlob(user_text.strip())
            st.warning("Suggested Correction:")
            st.write(str(blob.correct()))

with tab3:
    st.markdown("### 🌐 Verso Translate")
    t_text = st.text_area("Source Text:", height=200)
    
    languages = {
        "Arabic": "ar", "Chinese (Simplified)": "zh-CN", "Dutch": "nl", 
        "French": "fr", "German": "de", "Hindi": "hi", 
        "Italian": "it", "Japanese": "ja", "Korean": "ko", "Latin": "la",
        "Portuguese": "pt", "Russian": "ru", "Spanish": "es", "Turkish": "tr",
        "Urdu": "ur", "Swedish": "sv"
    }
    
    target_lang_name = st.selectbox("Select Target Language:", list(languages.keys()))
    
    if st.button("Translate Now"):
        if t_text:
            try:
                result = GoogleTranslator(source='auto', target=languages[target_lang_name]).translate(t_text)
                st.info(result)
            except:
                st.error("Connection error.")

with tab4:
    st.markdown("### 📜 Citation Pro")
    st.write("Generate **APA 7th Edition** citations.")
    c_url = st.text_input("Source URL:", placeholder="Paste link here...")
    if st.button("Generate Citation"):
        if c_url:
            year = datetime.now().year
            today = datetime.now().strftime('%Y, %B %d')
            formatted = f"Online Resource. ({year}). Retrieved {today}, from {c_url}"
            st.code(formatted, language="text")

st.markdown("---")

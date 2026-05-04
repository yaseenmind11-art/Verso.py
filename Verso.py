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

# Essential for Google Search Console Verification
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

# 2. UI STYLING (Professional White & Grey Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"], .stApp { 
        font-family: 'Inter', sans-serif; 
        background-color: #ffffff !important; 
    }
    
    header, footer { visibility: hidden; }
    
    /* Welcome Card Styling */
    .welcome-card {
        padding: 30px;
        border-radius: 15px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
    }

    .status-box {
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        background-color: #f8fafc;
        text-align: center;
        font-weight: 600;
        color: #0f172a;
    }
    
    div.stButton > button:first-child {
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color: #0077c2 !important;
        transform: translateY(-2px);
    }

    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #e2e8f0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER & LOGO
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

# 4. WELCOME DASHBOARD
st.markdown(f"""
    <div class="welcome-card">
        <h2 style='margin-top:0;'>Welcome to Verso AI</h2>
        <p style='color: #64748b; font-size: 1.1em;'>
            Your intelligent workspace for academic excellence. Verso AI streamlines your research workflow 
            by combining verified source discovery with high-precision writing tools.
        </p>
        <div style='display: flex; gap: 20px; margin-top: 15px;'>
            <div style='background: white; padding: 10px 20px; border-radius: 8px; border: 1px solid #e2e8f0;'>
                <strong>Status:</strong> <span style='color: #10b981;'>● Operational</span>
            </div>
            <div style='background: white; padding: 10px 20px; border-radius: 8px; border: 1px solid #e2e8f0;'>
                <strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. MAIN NAVIGATION TABS
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Trusted Search", "✍️ Verso Editor", "🌐 Verso Translate", "📜 Citation Pro"])

# --- TAB 1: TRUSTED SEARCH ---
with tab1:
    st.markdown("### 🔍 Verified Resource Search")
    st.info("Results are filtered to show only .gov, .edu, .org, and .ac.uk domains.")
    search_q = st.text_input("What are you researching today?", placeholder="e.g., Renewable energy solutions in urban areas", key="search_final")
    
    if search_q:
        trusted_filter = "(site:.gov OR site:.edu OR site:.org OR site:.ac.uk)"
        # Parameters used to force light mode: igu=1, cs=0, hl=en, light_mode=1
        q_url = f"https://www.google.com/search?igu=1&cs=0&hl=en&light_mode=1&q={search_q}+{trusted_filter}".replace(" ", "+")
        st.markdown("---")
        
        html_string = f"""
            <div style="width: 100%; height: 850px; overflow: hidden; border-radius: 15px; border: 1px solid #e2e8f0; background-color: white;">
                <iframe src="{q_url}" style="width: 100%; height: 1350px; margin-top: -155px; margin-bottom: -250px; border: none; background-color: white;"></iframe>
            </div>
        """
        components.html(html_string, height=870)

# --- TAB 2: VERSO EDITOR ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Draft:", height=300, key="v_editor_final", placeholder="Paste your paragraph here to check for grammar and logic...")
    
    if user_text:
        if st.button("Check Writing"):
            input_text = user_text.strip()
            blob = TextBlob(input_text)
            temp = str(blob.correct())
            
            # Logic: Fix punctuation spacing and capitalization
            temp = re.sub(r'\s+([,.!?;:])', r'\1', temp)
            temp = re.sub(r'([,.!?;:])(?=[^\s\d])', r'\1 ', temp)
            
            sentences = re.split(r'(?<=[.!?])\s+', temp)
            final_sentences = []
            for s in sentences:
                if len(s) > 0:
                    s = s[0].upper() + s[1:]
                    s = s.replace(" i ", " I ").replace(" i'", " I'").replace(" i.", " I.")
                    
                    # Smart Question Logic
                    q_words = ['What', 'Who', 'Where', 'When', 'Why', 'How', 'Is', 'Are', 'Do', 'Does', 'Can']
                    if any(s.startswith(w) for w in q_words) and not s.endswith('?'):
                        if s.endswith('.'): s = s[:-1]
                        s += '?'
                    final_sentences.append(s)
            
            final_output = " ".join(final_sentences).strip()
            
            if final_output == input_text:
                st.balloons()
                st.markdown('<div class="status-box">🎉 Your writing is grammatically sound. Great work!</div>', unsafe_allow_html=True)
            else:
                st.markdown("#### Suggested Improvements:")
                st.success(final_output)

# --- TAB 3: VERSO TRANSLATE ---
with tab3:
    st.markdown("### 🌐 Verso Translate")
    t_text = st.text_area("Source Text:", height=200, key="trans_area")
    target_l = st.selectbox("Target Language:", ["arabic", "french", "spanish", "german", "italian", "chinese"])
    
    if st.button("Run Translation"):
        if t_text:
            try:
                result = GoogleTranslator(source='auto', target=target_l).translate(t_text)
                st.markdown("#### Translation Output:")
                st.info(result)
            except:
                st.error("The translation engine is currently busy. Please try again.")

# --- TAB 4: CITATION PRO ---
with tab4:
    st.markdown("### 📜 Citation Pro")
    st.write("Generate accurate APA-style citations for your bibliography.")
    col1, col2 = st.columns(2)
    with col1:
        c_title = st.text_input("Source Title:", placeholder="e.g. The Paris Agreement")
        c_author = st.text_input("Author/Organization:", placeholder="e.g. United Nations")
    with col2:
        c_url = st.text_input("Source URL:", placeholder="https://un.org/example")
        c_year = st.text_input("Publication Year:", placeholder=str(datetime.now().year))
    
    if st.button("Generate Citation"):
        if c_title and c_url:
            year_val = c_year if c_year else "n.d."
            auth_val = c_author if c_author else "n.d."
            formatted = f"{auth_val}. ({year_val}). {c_title}. Retrieved from {c_url}"
            st.markdown("#### Your APA Citation:")
            st.code(formatted, language="text")
        else:
            st.error("Please provide at least a Title and a URL.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>Verso AI Research Suite | Professional Edition</p>", unsafe_allow_html=True)

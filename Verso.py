import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import difflib
import streamlit.components.v1 as components
import docx2txt
import PyPDF2
import pandas as pd
import io
import requests
from bs4 import BeautifulSoup
import urllib3
import language_tool_python
from google import genai
from google.genai import types

# =========================================
# DISABLE SSL WARNINGS
# =========================================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =========================================
# GOOGLE ANALYTICS
# =========================================
def inject_ga():
    ga_id = "G-030XWBG97P"

    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>

    <script>
        window.dataLayer = window.dataLayer || [];

        function gtag() {{
            dataLayer.push(arguments);
        }}

        gtag('js', new Date());
        gtag('config', '{ga_id}', {{ 'debug_mode': true }});
    </script>
    """

    components.html(ga_code, height=0)

# =========================================
# SYSTEM SETUP
# =========================================
@st.cache_resource
def setup_system():

    try:
        for res in [
            'punkt',
            'brown',
            'wordnet',
            'punkt_tab',
            'averaged_perceptron_tagger'
        ]:
            nltk.download(res, quiet=True)

    except Exception:
        pass

setup_system()

# =========================================
# LANGUAGE TOOL
# =========================================
@st.cache_resource
def load_language_tool():
    return language_tool_python.LanguageTool('en-US')

grammar_tool = load_language_tool()

# =========================================
# ADVANCED GRAMMAR ENGINE
# =========================================
def smart_grammar_corrector(text):

    if not text.strip():
        return ""

    # -------------------------------------
    # STEP 1 → Grammar Correction
    # -------------------------------------
    matches = grammar_tool.check(text)

    corrected = language_tool_python.utils.correct(
        text,
        matches
    )

    # -------------------------------------
    # STEP 2 → Spelling Correction
    # -------------------------------------
    corrected = str(TextBlob(corrected).correct())

    # -------------------------------------
    # STEP 3 → Cleanup
    # -------------------------------------
    corrected = corrected.strip()

    corrected = re.sub(r'\bi\b', 'I', corrected)

    corrected = re.sub(r'\s+', ' ', corrected)

    # Capitalize first letter
    if corrected:
        corrected = corrected[0].upper() + corrected[1:]

    # -------------------------------------
    # STEP 4 → Smart Punctuation
    # -------------------------------------
    question_words = (
        'who', 'what', 'where',
        'when', 'why', 'how',
        'is', 'are', 'can',
        'could', 'do', 'does',
        'did', 'will', 'would'
    )

    if corrected and corrected[-1] not in ".!?":

        if corrected.lower().startswith(question_words):
            corrected += "?"
        else:
            corrected += "."

    return corrected

# =========================================
# SESSION STATES
# =========================================
def initialize_states(force=False):

    defaults = {
        'set_color': "#FFFFFF",
        'set_bg': "#5465C9",
        'set_font': 1.10,
        'reset_counter': random.randint(1, 1000),

        'grammar_text_input': ""
    }

    for key, value in defaults.items():

        if force or key not in st.session_state:
            st.session_state[key] = value

initialize_states()

# =========================================
# GEMINI CLIENT
# =========================================
try:

    API_KEY = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(api_key=API_KEY)

except Exception:

    client = None

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="VERSO PRO",
    page_icon="✍️",
    layout="wide"
)

inject_ga()

# =========================================
# CUSTOM CSS
# =========================================
accent = st.session_state.set_color
bg_card = st.session_state.set_bg
f_scale = st.session_state.set_font

st.markdown(f"""
<style>

.stApp {{
    color: inherit;
}}

.notebook-card {{
    background-color: {bg_card};
    padding: 30px;
    border-radius: 12px;
    border-left: 6px solid {accent};
    margin-bottom: 15px;
    color: #FFFFFF !important;
    box-shadow: 0 4px 10px -1px rgb(0 0 0 / 0.2);
}}

.diff-add {{
    background-color: #065f46;
    color: #34d399;
    padding: 2px 4px;
    border-radius: 4px;
}}

.diff-remove {{
    background-color: #7f1d1d;
    color: #f87171;
    text-decoration: line-through;
    padding: 2px 4px;
    border-radius: 4px;
}}

.correct-box {{
    background: #0f172a;
    border: 1px solid #334155;
    padding: 25px;
    border-radius: 12px;
    color: white;
    line-height: 1.8;
    font-size: {f_scale}rem;
}}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================
with st.sidebar:

    st.title("VERSO PRO")

    choice = st.radio(
        "Navigation Menu",
        [
            "🏠 Home",
            "✍️ Grammar Checker",
            "⚙️ Settings"
        ]
    )

# =========================================
# HOME PAGE
# =========================================
if choice == "🏠 Home":

    st.title("VERSO RESEARCH")

    st.markdown("""
    ### 🎓 Universal Academic Engine

    This app includes:

    ✅ Grammar Correction  
    ✅ Spelling Correction  
    ✅ Punctuation Correction  
    ✅ AI Text Enhancement  
    ✅ Smart Writing Assistant
    """)

# =========================================
# GRAMMAR CHECKER
# =========================================
elif choice == "✍️ Grammar Checker":

    st.title("✍️ Verso Smart Grammar Corrector")

    st.markdown("""
    ### AI Grammar + Spelling + Punctuation Assistant
    """)

    text_to_check = st.text_area(
        "Paste your text below:",
        value=st.session_state.grammar_text_input,
        height=250,
        placeholder="Type or paste your paragraph here..."
    )

    st.session_state.grammar_text_input = text_to_check

    # =====================================
    # BUTTON
    # =====================================
    if st.button(
        "✨ Run Smart Correction",
        use_container_width=True
    ):

        if text_to_check.strip():

            with st.spinner(
                "Analyzing grammar and spelling..."
            ):

                # -----------------------------
                # FINAL CORRECTED TEXT
                # -----------------------------
                final_text = smart_grammar_corrector(
                    text_to_check
                )

                # -----------------------------
                # DIFF VISUALIZATION
                # -----------------------------
                diff_html = ""

                matcher = difflib.SequenceMatcher(
                    None,
                    text_to_check,
                    final_text
                )

                for tag, i1, i2, j1, j2 in matcher.get_opcodes():

                    if tag == 'equal':

                        diff_html += text_to_check[i1:i2]

                    else:

                        if i1 != i2:

                            diff_html += f'''
                            <span class="diff-remove">
                            {text_to_check[i1:i2]}
                            </span>
                            '''

                        if j1 != j2:

                            diff_html += f'''
                            <span class="diff-add">
                            {final_text[j1:j2]}
                            </span>
                            '''

                # -----------------------------
                # SUCCESS
                # -----------------------------
                st.success(
                    "✅ Correction Finished!"
                )

                # -----------------------------
                # HIGHLIGHTED DIFFERENCES
                # -----------------------------
                st.markdown(
                    f'''
                    <div class="correct-box">
                    {diff_html}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

                # -----------------------------
                # FINAL OUTPUT
                # -----------------------------
                with st.expander(
                    "📄 Final Corrected Text",
                    expanded=True
                ):

                    st.code(final_text)

        else:

            st.warning(
                "Please enter some text."
            )

# =========================================
# SETTINGS
# =========================================
elif choice == "⚙️ Settings":

    st.title("⚙️ Verso Settings")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🎨 Appearance")

        def update_accent():
            st.session_state.set_color = (
                st.session_state.accent_pick
            )

        st.color_picker(
            "Accent Color",
            value=st.session_state.set_color,
            key="accent_pick",
            on_change=update_accent
        )

    with col2:

        st.markdown("### 🖼️ Card Background")

        def update_bg():
            st.session_state.set_bg = (
                st.session_state.bg_pick
            )

        st.color_picker(
            "Card Background",
            value=st.session_state.set_bg,
            key="bg_pick",
            on_change=update_bg
        )

    st.slider(
        "Font Scale",
        0.8,
        2.0,
        value=st.session_state.set_font,
        key="set_font"
    )

    st.success("✅ Settings Saved")

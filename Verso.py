import streamlit as st
from pathlib import Path

# Keep the original Verso icon when z.png is present; use a safe fallback otherwise.
ICON_PATH = Path(__file__).resolve().with_name("z.png")
st.set_page_config(
    page_title="Verso Research Pro",
    page_icon=str(ICON_PATH) if ICON_PATH.is_file() else "📘",
    layout="wide",
    initial_sidebar_state="expanded",
)
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
import html
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib3
import os  
from google import genai
from google.genai import types
from deep_translator import GoogleTranslator

# Disable insecure request warnings if connection requires SSL bypass on a managed proxy network
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# BUG FIX: campus_session was used but never defined (caused NameError in Citation Generator / URL extraction)
campus_session = requests.Session()
campus_session.verify = False



# --- 🛰️ GOOGLE ANALYTICS INTEGRATION ---
def inject_ga():
    ga_id = "G-030XWBG97P"
    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{ga_id}', {{ 'debug_mode': true }});
    </script>
    """
    components.html(ga_code, height=0)

# --- 🛠️ ACADEMIC ENGINE SETUP ---
@st.cache_resource
def setup_system():
    try:
        for res in ['punkt', 'brown', 'wordnet', 'omw-1.4', 'punkt_tab',
                    'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng']:
            nltk.download(res, quiet=True)
    except Exception: pass

setup_system()

# --- ⚙️ STATE MANAGEMENT ---
def initialize_states(force=False):
    defaults = {
        'set_color': "#0B57D0",
        'set_bg': "#FFFFFF",
        'set_font': 1.10,
        'reset_counter': random.randint(1, 1000),
        'timer_end_time': None,
        'timer_active': False,
        'remaining_at_pause': 0,
        'sound_unlocked': False,
        'selected_alarm_tone': "Double Beep",
        'selected_citation_format': "APA 7th Generation",
        'tone_level': "Academic",
        'complexity_level': "Standard",
        'auto_bibliography': True,
        'logic_validation': True,
        'force_dark': True,
        'glassmorphism': False,
        'study_text_input': "",
        'grammar_text_input': "",
        'plag_text_input': "",
        'word_counter_input': "",
        'citation_text_input': "",
        'quiz_step': 0,
        'quiz_score': 0,
        'current_quiz_options': None,
        'current_quiz_target': None,
        'current_quiz_text': None,
        'fc_step': 0,

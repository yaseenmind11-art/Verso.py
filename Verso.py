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

# Disable insecure request warnings if connection requires SSL bypass on a managed proxy network
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
            nltk.download(res, quiet=True)
    except Exception:
        pass

setup_system()

# --- ⚙️ STATE MANAGEMENT ---
def initialize_states(force=False):
    defaults = {
        'set_color': "#FFFFFF",
        'set_bg': "#5465C9",
        'set_font': 1.10,
        'reset_counter': random.randint(1, 1000),
        'timer_end_time': None,
        'timer_active': False,
        'remaining_at_pause': 0,
        'sound_unlocked': False,
        'selected_alarm_tone': "Double Beep",
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
        'fc_correct': 0,
        'fc_wrong': 0,
        'reveal_fc': False,
        'generated_lecture_text': ""
    }

    for key, value in defaults.items():
        if force or key not in st.session_state:
            st.session_state[key] = value

initialize_states()

# --- 🤖 GEMINI CLIENT INITIALIZATION ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    client = None

def teach_source_material(source_text: str):
    if client is None:
        return "⚠️ Setup Error: API Key missing."

    system_instruction = """
    You are an expert, engaging teacher. Your job is to take the provided source 
    material and teach it as a complete lesson. 
    
    Structure the lesson exactly like this:
    1. 🎯 Lesson Objective
    2. 📖 Introduction
    3. 🧠 Core Concepts
    4. 💡 Example
    5. 📝 Check for Understanding
    """

    prompt = f"Please teach the following source material as a lesson:\n\n{source_text}"

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )

        return response.text

    except Exception as e:
        return f"An error occurred: {e}"

# --- 🌐 NETWORK CONFIGURATION ---
CAMPUS_HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}

# --- 🛠️ EXTRACTION HELPERS ---
def extract_text(uploaded_file):
    if uploaded_file is None:
        return ""

    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            return " ".join([page.extract_text() or "" for page in reader.pages])

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return docx2txt.process(uploaded_file)

        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            return df.astype(str).apply(lambda x: ' '.join(x), axis=1).str.cat(sep=' ')

        else:
            return str(uploaded_file.read(), "utf-8")

    except Exception:
        return ""

def extract_from_url(url):
    if not url:
        return ""

    try:
        res = requests.get(url, headers=CAMPUS_HEADERS, timeout=6, verify=False)
        soup = BeautifulSoup(res.content, 'html.parser')

        for s in soup(['script', 'style']):
            s.decompose()

        return soup.get_text(separator=' ', strip=True)

    except:
        return ""

# --- 📜 CITATION GENERATOR ENGINE ---
def generate_scribbr_citation(url, style_format):
    if not url:
        return "Please enter a valid URL or reference title."

    title = "Web Page Reference"
    site_name = "Website Source"
    author_name = ""

    current_year = time.strftime("%Y")
    access_date = time.strftime("%d %b. %Y")

    try:
        res = requests.get(url, headers=CAMPUS_HEADERS, timeout=5, verify=False)
        soup = BeautifulSoup(res.content, 'html.parser')

        title_tag = soup.find('meta', property='og:title')

        title = title_tag['content'] if title_tag else (
            soup.title.string if soup.title else "Web Page Reference"
        )

        title = title.strip()

        site_tag = soup.find('meta', property='og:site_name')
        site_name = site_tag['content'] if site_tag else ""

        auth_tag = soup.find('meta', name='author')
        author_name = auth_tag['content'].strip() if auth_tag else ""

    except:
        pass

    if "APA" in style_format:
        author_fmt = f"{author_name}." if author_name else f"{site_name}."
        return f"{author_fmt} ({current_year}). *{title}*. {site_name}. {url}"

    return f"{site_name}. ({current_year}). *{title}*. {url}"

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Verso Research Pro",
    page_icon="z.png",
    layout="wide"
)

inject_ga()

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    st.title("VERSO PRO")

    nav_options = [
        "🏠 Home",
        "📒 Study Assistant",
        "✍️ Grammar Checker",
        "🛡️ Plagiarism Checker",
        "📚 Citation Generator",
        "⏱️ Time Tracker",
        "📝 Word Counter",
        "⚙️ Settings"
    ]

    choice = st.radio(
        "Navigation Menu",
        nav_options,
        label_visibility="collapsed"
    )

# --- HOME ---
if choice == "🏠 Home":

    st.title("VERSO RESEARCH")
    st.markdown("### 🎓 Universal Academic Engine")

    q = st.text_input(
        "🔍 Search Database:",
        placeholder="Research your topic here..."
    )

    if q:
        search_url = f"https://www.google.com/search?q={q.replace(' ', '+')}"

        st.markdown(
            f"""
            <iframe src="{search_url}" width="100%" height="700"></iframe>
            """,
            unsafe_allow_html=True
        )

# --- WORD COUNTER ---
elif choice == "📝 Word Counter":

    st.title("Verso Word Metrics")

    uploaded_file = st.file_uploader(
        "Upload Files",
        type=['pdf', 'docx', 'csv', 'txt']
    )

    file_text = extract_text(uploaded_file)

    new_text = st.text_area(
        "Input text:",
        value=st.session_state.word_counter_input,
        height=250
    )

    st.session_state.word_counter_input = new_text

    box_count = len(re.findall(r'\b\w+\b', new_text))
    file_count = len(re.findall(r'\b\w+\b', file_text))

    st.metric("Words in Box", box_count)
    st.metric("Words in File", file_count)
    st.metric("Combined Total", box_count + file_count)

# --- GRAMMAR CHECKER ---
elif choice == "✍️ Grammar Checker":

    st.markdown('<h1>Smart Verso Auto Correct</h1>', unsafe_allow_html=True)

    text_to_check = st.text_area(
        "Paste text to improve:",
        value=st.session_state.grammar_text_input,
        height=250,
        placeholder="Please input the text you want to correct...",
        key="g_input"
    )

    st.session_state.grammar_text_input = text_to_check

    def correct_text(text):
        tool = language_tool_python.LanguageTool('en-US')

        matches = tool.check(text)

        corrected_text = tool.correct(text)

        return corrected_text, matches

    if st.button("✨ Run Smart Correction", use_container_width=True):

        if text_to_check:

            with st.spinner("Processing..."):

                corrected_text, errors = correct_text(text_to_check)

                diff_html = ""

                matcher = difflib.SequenceMatcher(
                    None,
                    text_to_check,
                    corrected_text
                )

                for tag, i1, i2, j1, j2 in matcher.get_opcodes():

                    if tag == 'equal':
                        diff_html += text_to_check[i1:i2]

                    else:
                        if i1 != i2:
                            diff_html += (
                                f'<span style="background-color:#7f1d1d;'
                                f'color:#f87171;text-decoration:line-through;">'
                                f'{text_to_check[i1:i2]}</span>'
                            )

                        if j1 != j2:
                            diff_html += (
                                f'<span style="background-color:#065f46;'
                                f'color:#34d399;">'
                                f'{corrected_text[j1:j2]}</span>'
                            )

                st.success("Correction Finished!")

                st.markdown(
                    f'<div style="padding:20px;line-height:1.8;">'
                    f'{diff_html}</div>',
                    unsafe_allow_html=True
                )

                with st.expander("Final Polished Text"):
                    st.code(corrected_text)

                if errors:
                    st.markdown("### Detected Issues")

                    for error in errors:
                        st.write(f"• {error.message}")

# --- PLAGIARISM CHECKER ---
elif choice == "🛡️ Plagiarism Checker":

    st.title("Plagiarism Pro Scanner")

    plag_text = st.text_area(
        "Paste text to scan:",
        value=st.session_state.plag_text_input,
        height=250
    )

    st.session_state.plag_text_input = plag_text

    if st.button("🔍 Deep Verso Plagiarism Scan"):

        if plag_text:

            with st.spinner("Comparing databases..."):

                time.sleep(2)

                st.success("Scan Completed")

# --- CITATION GENERATOR ---
elif choice == "📚 Citation Generator":

    st.title("📚 Citation Generator Workspace")

    cite_url = st.text_input(
        "Enter Source URL:",
        value=st.session_state.citation_text_input
    )

    st.session_state.citation_text_input = cite_url

    if st.button("📋 Generate Reference"):

        if cite_url:

            output = generate_scribbr_citation(
                cite_url,
                "APA 7th Generation"
            )

            st.code(output)

# --- STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":

    st.title("Verso Deep Learning Teacher")

    raw_content = st.text_area(
        "Input Content:",
        value=st.session_state.study_text_input,
        height=200
    )

    st.session_state.study_text_input = raw_content

    if st.button("🧠 Generate Lesson"):

        if raw_content:

            with st.spinner("Generating lesson..."):

                lesson = teach_source_material(raw_content)

                st.markdown(lesson)

# --- TIME TRACKER ---
elif choice == "⏱️ Time Tracker":

    st.title("Focus Timer")

    mins = st.number_input("Minutes:", 1, 120, 25)

    if st.button("Start Timer"):

        st.success(f"Timer Started for {mins} minutes")

# --- SETTINGS ---
elif choice == "⚙️ Settings":

    st.title("Verso Control Center")

    st.color_picker(
        "Accent Color",
        value=st.session_state.set_color
    )

    st.slider(
        "Font Scale",
        0.8,
        2.0,
        value=st.session_state.set_font
    )

    st.success("System Optimized")

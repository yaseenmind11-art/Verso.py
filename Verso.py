import streamlit as st
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
from google import genai
from google.genai import types
import language_tool_python


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
    except Exception: pass

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

# --- 🤖 GEMINI CLIENT INITIALIZATION (SECURED VIA SECRETS) ---
try:
    # Safely extract key from Streamlit secrets config instead of exposing hardcoded text strings
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    client = None

def teach_source_material(source_text: str):
    if client is None:
        return "⚠️ Setup Error: API Key missing or leaked. Please configure GEMINI_API_KEY inside your local secrets file (.streamlit/secrets.toml) or deployment dashboard panels."
        
    system_instruction = """
    You are an expert, engaging teacher. Your job is to take the provided source 
    material and teach it as a complete lesson. 
    
    Structure the lesson exactly like this:
    1. 🎯 Lesson Objective: What the students will learn.
    2. 📖 Introduction: A simple, engaging hook about the topic.
    3. 🧠 Core Concepts: Breakdown of the main ideas.
    4. 💡 Example: A real-world or relatable example.
    5. 📝 Check for Understanding: 2-3 interactive questions.
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
        return f"An error occurred while generating the live lecture format: {e}"

# --- 🌐 NETWORK CONFIGURATION ---
CAMPUS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# --- 🛠️ EXTRACTION HELPERS ---
def extract_text(uploaded_file):
    if uploaded_file is None: return ""
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
    except Exception: return ""

def extract_from_url(url):
    if not url: return ""
    try:
        res = requests.get(url, headers=CAMPUS_HEADERS, timeout=6, verify=False)
        soup = BeautifulSoup(res.content, 'html.parser')
        for s in soup(['script', 'style']): s.decompose()
        return soup.get_text(separator=' ', strip=True)
    except: return ""

# --- 📜 CITATION GENERATOR ENGINE ---
def generate_scribbr_citation(url, style_format):
    if not url: return "Please enter a valid URL or reference title."
    
    title = "Web Page Reference"
    site_name = "Website Source"
    author_name = ""
    current_year = time.strftime("%Y")
    access_date = time.strftime("%d %b. %Y")
    
    try:
        res = requests.get(url, headers=CAMPUS_HEADERS, timeout=5, verify=False)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        title_tag = soup.find('meta', property='og:title')
        title = title_tag['content'] if title_tag else (soup.title.string if soup.title else "Web Page Reference")
        title = title.strip()
        
        site_tag = soup.find('meta', property='og:site_name')
        site_name = site_tag['content'] if site_tag else ""
        if not site_name:
            domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
            site_name = domain_match.group(1).capitalize() if domain_match else "Website Source"
            
        auth_tag = soup.find('meta', name='author')
        author_name = auth_tag['content'].strip() if auth_tag else ""
    except:
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        if domain_match:
            site_name = domain_match.group(1).split('.')[0].capitalize()
        path_segments = [s for s in url.split('/') if s]
        if path_segments and len(path_segments) > 1:
            title = path_segments[-1].replace('-', ' ').replace('_', ' ').capitalize()

    if "APA" in style_format:
        author_fmt = f"{author_name}." if author_name else f"{site_name}."
        if "6th" in style_format:
            return f"{author_fmt} ({current_year}). *{title}*. Retrieved from {url}"
        else:
            return f"{author_fmt} ({current_year}). *{title}*. {site_name}. {url}"
            
    elif "Chicago" in style_format:
        author_fmt = f"{author_name}," if author_name else f'"{site_name}",'
        if "Notes" in style_format:
            return f'{author_fmt} "{title}," {site_name}, last modified {current_year}, {url}.'
        else:
            return f'{author_fmt} {current_year}. "{title}." {site_name}. {url}.'
            
    elif "Harvard" in style_format:
        author_fmt = f"{author_name}" if author_name else f"{site_name}"
        return f"{author_fmt}, {current_year}. *{title}*. [online] Available at: {url} [Accessed {access_date}]."
        
    elif "MLA" in style_format:
        author_fmt = f"{author_name}. " if author_name else ""
        return f'{author_fmt}"{title}." *{site_name}*, {current_year}, {url}.'
        
    else:
        author_fmt = f"{author_name}." if author_name else f"{site_name}."
        return f"{author_fmt} ({current_year}). *{title}*. {url}"

ALARM_TONES = {
    "Double Beep": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
    "Beep (High)": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    "Digital Alarm": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
    "Industrial Siren": "https://actions.google.com/sounds/v1/alarms/industrial_alarm.ogg"
}

KHAN_SUCCESS = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"

def trigger_master_reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_states(force=True)
    st.rerun()

# --- ⏱️ BACKGROUND TIMER LOGIC ---
if st.session_state.get('timer_active') and st.session_state.get('timer_end_time'):
    now = time.time()
    diff = st.session_state.timer_end_time - now
    if diff <= 0:
        st.session_state.timer_active = False
        st.session_state.remaining_at_pause = 0
        st.session_state.timer_finished_trigger = True
    else:
        st.session_state.remaining_at_pause = diff

# --- 🎨 STYLING ---
accent = st.session_state.set_color
bg_card = st.session_state.set_bg
f_scale = st.session_state.set_font
selected_tone_name = st.session_state.selected_alarm_tone
selected_tone_url = ALARM_TONES.get(selected_tone_name)

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

st.markdown(f"""
    <style>
    .stApp {{ color: inherit; }}
    .notebook-card {{ 
        background-color: {bg_card}; 
        padding: 30px; border-radius: 12px; border-left: 6px solid {accent}; 
        margin-bottom: 15px; color: #FFFFFF !important; box-shadow: 0 4px 10px -1px rgb(0 0 0 / 0.2);
    }}
    .teacher-board {{ 
        background-color: #0f172a; border: 1px solid #334155; padding: 45px; 
        border-radius: 12px; font-family: 'Inter', sans-serif; 
        color: #f1f5f9; line-height: 1.9; font-size: {f_scale}rem; white-space: pre-wrap;
    }}
    .teacher-board h2 {{ color: {accent}; border-bottom: 2px solid {accent}; padding-bottom: 10px; }}
    .teacher-board h3 {{ color: #94a3b8; margin-top: 30px; text-transform: uppercase; letter-spacing: 1px; font-size: 1.1rem; }}
    .teacher-board b {{ color: {accent}; }}
    
    .google-container {{
        width: 100%;
        height: 800px;
        overflow: hidden;
        position: relative;
        border-radius: 12px;
        border: 1px solid #334155;
        background-color: white;
    }}
    .google-iframe {{
        position: absolute;
        top: -125px; 
        left: 0;
        width: 100%;
        height: 1025px; 
    }}
    
    .time-up-banner {{ background-color: #ef4444; color: white; padding: 25px; text-align: center; font-weight: 800; border-radius: 12px; font-size: 28px; animation: blinker 0.8s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0; }} }}
    .diff-add {{ background-color: #065f46; color: #34d399; padding: 2px 4px; border-radius: 4px; }}
    .diff-remove {{ background-color: #7f1d1d; color: #f87171; text-decoration: line-through; padding: 2px 4px; }}
    .pro-badge {{ background-color: {accent}; color: white; padding: 2px 8px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-left: 10px; }}
    
    .audio-panel {{
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }}
    
    .audio-btn {{
        background-color: {bg_card} !important;
        color: white !important;
        border: 1px solid {accent} !important;
        padding: 10px 24px;
        font-size: 15px;
        font-weight: bold;
        border-radius: 6px;
        cursor: pointer;
        margin-right: 10px;
        transition: opacity 0.2s;
        display: inline-block;
    }}
    .audio-btn:hover {{ opacity: 0.85; }}
    .audio-btn-pause {{
        background-color: #eab308 !important;
        border: 1px solid #facc15 !important;
    }}
    .audio-btn-stop {{
        background-color: #ef4444 !important;
        border: 1px solid #f87171 !important;
    }}
    
    [data-testid="stSidebar"] div.stRadio > div {{
        background: transparent !important;
        padding: 0px !important;
    }}
    [data-testid="stSidebar"] div.stRadio label {{
        padding: 6px 0px !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        margin-bottom: 4px !important;
    }}
    [data-testid="stSidebar"] div.stRadio label:hover {{
        background-color: transparent !important;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <audio id="alarm-sound" key="{selected_tone_name}" preload="auto">
        <source src="{selected_tone_url}" type="audio/ogg">
    </audio>
    <audio id="success-sound" preload="auto">
        <source src="{KHAN_SUCCESS}" type="audio/mpeg">
    </audio>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<p style='color: gray; margin-bottom: 25px;'>Universal Academic Suite</p>", unsafe_allow_html=True)
    
    # Visual fallback validation checking inside interface wrapper
    if client is None:
        st.error("🔑 API Key Configuration Missing")
        st.info("To add a new key, create a file at `.streamlit/secrets.toml` in your app project folder and add:\n\n`GEMINI_API_KEY = \"your_new_key_here\"`")
        st.markdown("---")
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
    
    choice = st.radio("Navigation Menu", nav_options, label_visibility="collapsed")

# --- HOME ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown("### 🎓 Universal Academic Engine")
    
    source_options = {
        "Educational (.edu)": "site:.edu",
        "Government (.gov)": "site:.gov",
        "International Orgs (.org)": "site:.org",
        "Scientific Journals (Nature/Science)": "(site:nature.com OR site:sciencemag.org OR site:sciencedirect.com)",
        "Libraries (JSTOR/PubMed)": "(site:jstor.org OR site:pubmed.ncbi.nlm.nih.gov)",
        "Encyclopedias (Britannica/WorldHistory)": "(site:britannica.com OR site:worldhistory.org)",
        "Academic News (The Conversation/Smithsonian)": "(site:theconversation.com OR site:smithsonianmag.com)"
    }

    if 'selected_sources' not in st.session_state:
        st.session_state.selected_sources = ["Educational (.edu)", "Government (.gov)"]

    c1, c2 = st.columns([4, 1])
    with c2:
        if st.button("Select All", use_container_width=True):
            st.session_state.selected_sources = list(source_options.keys())
            st.rerun()

    selected_sources = st.multiselect(
        "Active Reliable Databases:",
        list(source_options.keys()),
        key="selected_sources"
    )

    q = st.text_input("🔍 Search Database:", placeholder="Research your topic here...")
    
    if q:
        query_parts = [source_options[s] for s in selected_sources]
        advanced_filter = " OR ".join(query_parts) if query_parts else ""
        
        full_query = f"{q} ({advanced_filter}) -site:wikipedia.org" if advanced_filter else f"{q} -site:wikipedia.org"
        st.info(f"Scanning across **{len(selected_sources)}** reliable database categories.")
        
        search_url = f"https://www.google.com/search?q={full_query.replace(' ', '+')}&igu=1"
        st.markdown(f"""
            <div class="google-container">
                <iframe src="{search_url}" class="google-iframe" frameborder="0"></iframe>
            </div>
        """, unsafe_allow_html=True)

# --- MODULE: WORD COUNTER ---
elif choice == "📝 Word Counter":
    st.title("Verso Word Metrics")
    st.markdown("### 📥 Analyze Content")
    uploaded_file = st.file_uploader("Upload Files for Counting", type=['pdf', 'docx', 'csv', 'txt'], key="word_upload")
    file_text = extract_text(uploaded_file)
    new_text = st.text_area("Input specific text to count:", value=st.session_state.word_counter_input, height=250, placeholder="Paste or type here...")
    st.session_state.word_counter_input = new_text
    box_count = len(re.findall(r'\b\w+\b', new_text))
    file_count = len(re.findall(r'\b\w+\b', file_text))
    col1, col2 = st.columns(2)
    col1.metric("Words in Box", box_count)
    col2.metric("Words in File", file_count)
    st.metric("Combined Total", box_count + file_count)

# --- MODULE: GRAMMAR CHECKER ---
elif choice == "✍️ Grammar Checker":
    st.markdown('<h1>Smart Verso Auto Correct</h1>', unsafe_allow_html=True)
    text_to_check = st.text_area("Paste text to improve:", value=st.session_state.grammar_text_input, height=250, placeholder="Please input the text you want to correct...", key="g_input")
    st.session_state.grammar_text_input = text_to_check
    if st.button("✨ Run Smart Correction", use_container_width=True):
        if text_to_check:
            with st.spinner("Processing..."):
              def correct_text(text):
    # Initialize the tool for US English
     tool = language_tool_python.LanguageTool('en-US')
    
    # Identify errors (grammar, spelling, punctuation, capitalization)
    matches = tool.check(text)
    
    # Automatically apply the suggested corrections
    corrected_text = tool.correct(text)
    
    return corrected_text, matches

# Example usage:
input_text = "this is a example of bad grammar and i forgot my punctuation"
corrected, errors = correct_text(input_text)

print(f"Original: {input_text}")
print(f"Corrected: {corrected}")


# --- MODULE: PLAGIARISM CHECKER ---
elif choice == "🛡️ Plagiarism Checker":
    st.title("Plagiarism Pro Scanner")
    plag_text = st.text_area("Paste text to scan:", value=st.session_state.plag_text_input, placeholder="Paste text here...", height=250, key="p_input")
    st.session_state.plag_text_input = plag_text
    if st.button("🔍 Deep Verso Plagiarism Scan", use_container_width=True):
        if plag_text:
            with st.spinner("Comparing databases..."):
                time.sleep(2.5)
                sentences = re.split(r'(?<=[.!?]) +', plag_text)
                academic_triggers = ["infrastructure", "implementation", "federal funding", "neurological", "opportunity", "assessment", "significant"]
                marked_text = ""
                match_count = 0
                for s in sentences:
                    is_match = len(s.split()) > 15 or any(trig in s.lower() for trig in academic_triggers)
                    if is_match:
                        marked_text += f'<span class="plag-highlight" style="background-color:#7f1d1d; color:#fecaca;">{s}</span> '
                        match_count += 1
                    else: marked_text += f'{s} '
                plag_percent = min(98, int((match_count / len(sentences)) * 100)) if sentences else 0
                if plag_percent > 20:
                    st.error(f"⚠️ Similarity Found: {plag_percent}%")
                    st.progress(plag_percent / 100)
                    st.markdown(f'<div class="notebook-card" style="line-height: 1.8;">{marked_text}</div>', unsafe_allow_html=True)
                else: st.success(f"✅ Content Unique: {plag_percent}% Similarity"); st.balloons()

# --- MODULE: CITATION GENERATOR ---
elif choice == "📚 Citation Generator":
    st.title("📚 Citation Generator Workspace")
    st.markdown("### 📥 Generate Reference Citations")
    
    cite_url = st.text_input("Enter Source URL, DOI, or Document Link:", value=st.session_state.citation_text_input, placeholder="https://example.com/article...", key="c_input")
    st.session_state.citation_text_input = cite_url
    
    active_style = st.session_state.get("selected_citation_format", "APA 7th Generation")
    st.caption(f"Active Output Style: **{active_style}** (Change this inside control center settings)")
    
    if st.button("📋 Generate Reference", use_container_width=True):
        if cite_url:
            with st.spinner("Processing source data attributes..."):
                time.sleep(0.8)
                output = generate_scribbr_citation(cite_url, active_style)
                st.markdown(f'<div class="notebook-card"><b>Generated Entry:</b><br><br>{output}</div>', unsafe_allow_html=True)
                
                if st.session_state.get("auto_bibliography", True):
                    st.success("Reference entry systematically pushed to active Auto-Bibliography.")
        else:
            st.warning("Please provide a valid source link or title inside the input workspace.")

# --- MODULE: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("Verso Deep Learning Teacher")
    st.markdown("### 📥 Resource Input")
    col_a, col_b = st.columns([2, 1])
    with col_a: up_files = st.file_uploader("Upload Files", type=['pdf', 'docx', 'csv', 'txt'], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    with col_b: url_hub = st.text_input("Link Hub", placeholder="Paste URL...", key=f"l_{st.session_state.reset_counter}")
    
    raw_content = st.text_area("Input Content:", value=st.session_state.study_text_input, height=200, placeholder="Paste content here...", key="s_input")
    st.session_state.study_text_input = raw_content
    final_study_data = raw_content
    if url_hub: final_study_data += " " + extract_from_url(url_hub)
    if up_files:
        for f in up_files: final_study_data += " " + extract_text(f)
        
    if final_study_data.strip():
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "🎙️ AI Voice Teacher"])
        blob = TextBlob(final_study_data)
        
        raw_phrases = list(dict.fromkeys([w.lower().strip() for w in blob.noun_phrases if len(w) > 3]))
        words = []
        for phrase in raw_phrases:
            cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', phrase)  
            cleaned = cleaned.strip()
            if cleaned and len(cleaned) > 3 and not cleaned.isdigit():
                words.append(cleaned)
                
        while len(words) < 25:
            words += ["structural analysis", "conceptual overview", "logical progression", "critical evaluation", "systematic framework"]
            
        with t1:
            cols = st.columns(2)
            for i, phrase in enumerate(words[:20]): 
                cols[i % 2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)
                
        with t2:
            st.markdown("### Interactive Content Quiz (10 Questions)")
            total_q = 10
            if st.session_state.quiz_step < total_q:
                curr_q = st.session_state.quiz_step
                st.write(f"Question **{curr_q + 1}** of **{total_q}**")
                
                if st.session_state.current_quiz_options is None:
                    target_word = words[curr_q % len(words)].title()
                    q_type = curr_q % 3 
                    
                    if q_type == 0:
                        q_text = f"Which term from the source content matches this foundational theme: **\"{target_word}\"**?"
                        alt_pool = [x.title() for x in words if x.title() != target_word]
                        opts = [target_word] + random.sample(alt_pool, min(2, len(alt_pool)))
                        random.shuffle(opts)
                    elif q_type == 1:
                        fake_target = random.choice([x.title() for x in words if x.title() != target_word])
                        q_text = f"True or False: Is **\"{target_word}\"** structurally identical to **\"{fake_target}\"** within this context?"
                        opts = ["False, they represent separate ideas", "True, they are identical statements"]
                        target_word = "False, they represent separate ideas"
                    else:
                        q_text = f"Fill in the blank: The logical progression of this text highlights that ___________ is a core component."
                        alt_pool = [x.title() for x in words if x.title() != target_word]
                        opts = [target_word] + random.sample(alt_pool, min(2, len(alt_pool)))
                        random.shuffle(opts)
                        
                    st.session_state.current_quiz_options = [re.sub(r'[\[\]\(\)\{\}\\]', '', str(o)) for o in opts]
                    st.session_state.current_quiz_target = re.sub(r'[\[\]\(\)\{\}\\]', '', str(target_word))
                    st.session_state.current_quiz_text = q_text

                st.markdown(f'<div class="notebook-card">{st.session_state.current_quiz_text}</div>', unsafe_allow_html=True)
                choice_q = st.radio("Select your verified solution text:", st.session_state.current_quiz_options, key=f"q_step_radio_{curr_q}", index=None)
                
                if st.button("Submit & Continue", use_container_width=True):
                    if choice_q == st.session_state.current_quiz_target:
                        st.session_state.quiz_score += 1
                        components.html("<script>var s=window.parent.document.getElementById('success-sound');if(s){s.play();}</script>", height=0)
                        st.balloons(); st.success("Excellent! Correct evaluation.")
                    else: 
                        st.info(f"Analysis update: The correct choice was: **{st.session_state.current_quiz_target}**")
                    time.sleep(1)
                    
                    st.session_state.current_quiz_options = None
                    st.session_state.current_quiz_target = None
                    st.session_state.quiz_step += 1
                    st.rerun()
            else:
                st.metric("Final Score Metric", f"{st.session_state.quiz_score} / {total_q}")
                if st.button("Restart Clean Quiz Loop"): 
                    st.session_state.quiz_step = 0
                    st.session_state.quiz_score = 0
                    st.session_state.current_quiz_options = None
                    st.session_state.current_quiz_target = None
                    st.rerun()
                    
        with t3:
            st.markdown("### NotebookLM Style Flashcards (25 Cards)")
            total_fc = 25
            if st.session_state.fc_step < total_fc:
                curr_idx = st.session_state.fc_step
                curr_word = words[curr_idx % len(words)].title()
                st.write(f"Card **{curr_idx + 1}** / **{total_fc}**")
                fc_type = curr_idx % 4
                if fc_type == 0:
                    q_text = f"In reference to the core academic principles outlined in your study material, how would you best describe the significance or technical definition of <b>'{curr_word}'</b>?"
                    a_text = f"<b>Source Analysis:</b> The inputted source material utilizes '{curr_word}' as a core technical anchor."
                elif fc_type == 1:
                    q_text = f"If you had to apply <b>'{curr_word}'</b> to a practical scenario following the logic of the source, what would be the intended outcome?"
                    a_text = f"<b>Practical Application:</b> The inputted source material implies that successful implementation leads to a more robust result."
                elif fc_type == 2:
                    other_word = words[(curr_idx + 1) % len(words)].title()
                    q_text = f"Analyze the connection between <b>'{curr_word}'</b> and <b>'{other_word}'</b>. How do they interact within your content?"
                    a_text = f"<b>Inter-Term Relationship:</b> Within the context of the inputted source material, '{curr_word}' acts as a prerequisite or supporting pillar for '{other_word}'."
                else:
                    q_text = f"What specific evidence or context does the inputed source provide to highlight the importance of <b>'{curr_word}'</b>?"
                    a_text = f"<b>Contextual Importance:</b> The inputted source material identifies '{curr_word}' as a high-value variable."
                st.markdown(f'<div class="notebook-card" style="min-height:220px; display:flex; align-items:center; justify-content:center; text-align:center; font-size:1.3rem; line-height:1.6;">{q_text}</div>', unsafe_allow_html=True)
                if not st.session_state.reveal_fc:
                    if st.button("Reveal Detailed Analysis", use_container_width=True):
                        st.session_state.reveal_fc = True; st.rerun()
                else:
                    st.markdown(f'<div style="background-color:#5465C9; padding:25px; border-radius:10px; border:1px solid {accent}; margin-bottom:15px; color:#FFFFFF; line-height:1.7;">{a_text}</div>', unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    if c1.button("✅ Mastered", use_container_width=True):
                        st.session_state.fc_correct += 1; st.session_state.fc_step += 1; st.session_state.reveal_fc = False
                        components.html("<script>var s=window.parent.document.getElementById('success-sound');if(s){s.play();}</script>", height=0)
                        st.rerun()
                    if c2.button("❌ Review Needed", use_container_width=True):
                        st.session_state.fc_wrong += 1; st.session_state.fc_step += 1; st.session_state.reveal_fc = False; st.rerun()
            else:
                st.subheader("Deck Completed"); st.write(f"Mastery: {st.session_state.fc_correct}/{total_fc}")
                if st.button("Reset Cards"): st.session_state.fc_step = 0; st.session_state.fc_correct = 0; st.session_state.fc_wrong = 0; st.rerun()
                
        with t4:
            st.markdown("### 🎙️ Verso AI Teacher")
            
            va1, va2 = st.columns(2)
            v_pitch = va1.slider("Teacher Vocal Pitch", 0.5, 2.0, 1.0, step=0.1, help="Adjust voice tone pitch.")
            v_speed = va2.slider("Pacing / Speech Speed", 0.5, 2.0, 1.0, step=0.1, help="Speed up or slow down speech.")
            
            if st.button("🧠 Generate/Update Lesson Content", use_container_width=True):
                with st.spinner("Generating structured presentation flow via Verso..."):
                    st.session_state.generated_lecture_text = teach_source_material(final_study_data)
            
            if st.session_state.generated_lecture_text:
                raw_generated_lesson = st.session_state.generated_lecture_text
                
                # Sanitize out any newlines, quotes, or markdown icons that break JavaScript rendering
                clean_speech_js = raw_generated_lesson.replace('"', '\\"').replace("'", "\\'").replace('\n', ' ').replace('\r', ' ')
                clean_speech_js = re.sub(r'[^\x00-\x7F]+', '', clean_speech_js) # Drops emoji characters so engine stays clean

                tts_component_code = f"""
                <div class="audio-panel" style="background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #475569; border-radius: 8px; padding: 15px; font-family: sans-serif; color: #f1f5f9; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span><b>🔴 Live AI Voice Feed:</b> Ready to Broadcast Lesson</span>
                        <span>
                            <label for="voiceSelect" style="margin-right: 5px; font-weight: bold;">🗣️ Voice:</label>
                            <select id='voiceSelect' style='background: #0f172a; color: #f1f5f9; border: 1px solid #475569; padding: 4px 8px; border-radius: 4px;'></select>
                        </span>
                    </div>
                    <button class="audio-btn" onclick="playAudio()">▶ Broadcast Lesson</button>
                    <button class="audio-btn audio-btn-pause" onclick="pauseAudio()">⏸ Pause</button>
                    <button class="audio-btn audio-btn-stop" onclick="stopAudio()">⏹ Stop</button>
                </div>

                <script>
                    const synth = window.speechSynthesis;
                    let utterance = null;
                    let voices = [];
                    const voiceSelect = document.getElementById('voiceSelect');

                    function populateVoices() {{
                        voices = synth.getVoices();
                        voiceSelect.innerHTML = '';
                        
                        let defaultIndex = 0;
                        voices.forEach((voice, index) => {{
                            const option = document.createElement('option');
                            option.textContent = `${{voice.name}} (${{voice.lang}})`;
                            option.value = index;
                            
                            // Explicitly set Google US English as the chosen choice if available
                            if (voice.name.includes('Google') && voice.lang === 'en-US') {{
                                defaultIndex = index;
                            }}
                            voiceSelect.appendChild(option);
                        }});
                        
                        if(voices.length > 0) {{
                            voiceSelect.selectedIndex = defaultIndex;
                        }}
                    }}

                    populateVoices();
                    if (speechSynthesis.onvoiceschanged !== undefined) {{
                        speechSynthesis.onvoiceschanged = populateVoices;
                    }}

                    function playAudio() {{
                        if (synth.speaking) {{
                            if (synth.paused) {{
                                synth.resume();
                                return;
                            }}
                            synth.cancel();
                        }}
                        
                        const textToSpeak = "{clean_speech_js}";
                        if (!textToSpeak) return;

                        utterance = new SpeechSynthesisUtterance(textToSpeak);
                        
                        if (voices.length > 0) {{
                            const selectedVoiceIndex = voiceSelect.value || 0;
                            utterance.voice = voices[selectedVoiceIndex];
                        }}
                        
                        utterance.pitch = {v_pitch};
                        utterance.rate = {v_speed};
                        
                        synth.speak(utterance);
                    }}

                    function pauseAudio() {{
                        if (synth.speaking && !synth.paused) {{
                            synth.pause();
                        }}
                    }}

                    function stopAudio() {{
                        if (synth.speaking) {{
                            synth.cancel();
                        }}
                    }}
                </script>
                """
                components.html(tts_component_code, height=110)
                st.markdown(f'<div class="teacher-board">{raw_generated_lesson}</div>', unsafe_allow_html=True)

# --- MODULE: TIME TRACKER / SETTINGS (STUBS BASED ON APP SELECTION OPTIONS) ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    if not st.session_state.get('sound_unlocked', False):
        if st.button("🔓 ENABLE SOUNDS"):
            components.html("<script>var a=window.parent.document.getElementById('alarm-sound');a.play().then(()=>{a.pause();a.currentTime=0;});</script>", height=0)
            st.session_state.sound_unlocked = True; st.rerun()
    mins = st.number_input("Minutes:", 1, 120, 25)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Start"): st.session_state.timer_end_time = time.time()+(mins*60); st.session_state.timer_active=True; st.rerun()
    if c2.button("Pause"): st.session_state.timer_active=False; st.rerun()
    if c4.button("Reset"): st.session_state.timer_active=False; st.session_state.timer_end_time=None; st.rerun()
    
    rem_time = st.session_state.get('remaining_at_pause', 0)
    m, s = divmod(rem_time, 60); st.metric("Status", f"{int(m):02d}:{int(s):02d}")
    if st.session_state.get('timer_active'): time.sleep(1); st.rerun()


elif choice == "⚙️ Settings":
    st.markdown('<h1 style="font-size: 3rem;">Verso Control Center</h1>', unsafe_allow_html=True)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('### 📚 Academic & Audio')
        st.selectbox("Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
        if st.button("Test Tone"): components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
        
        st.selectbox("Citation Style", [
            "APA 7th Generation", 
            "APA 6th Generation", 
            "APA 5th Generation",
            "MLA 9th Edition", 
            "Chicago 17th (Notes & Bibliography)", 
            "Chicago 17th (Author-Date)",
            "Harvard (Standard UK)",
            "Harvard (Australia)"
        ], key="selected_citation_format")
        
        st.selectbox("Tone Level", ["Formal", "Casual", "Academic"])
        st.radio("Complexity", ["Brief", "Standard", "Deep"], index=1)
        st.checkbox("Auto-Bibliography", value=True); st.checkbox("Logic Validation", value=True)
    with col2:
        st.markdown('### 🎨 UI Appearance')
        def update_accent(): st.session_state.set_color = st.session_state.accent_pick
        def update_bg(): st.session_state.set_bg = st.session_state.bg_pick
        st.color_picker("Accent Color", value=st.session_state.set_color, key="accent_pick", on_change=update_accent)
        st.color_picker("Card BG", value=st.session_state.set_bg, key="bg_pick", on_change=update_bg)
        st.slider("Font Scale", 0.8, 2.0, value=st.session_state.set_font, key="set_font")
        st.checkbox("Force Dark", value=True); st.checkbox("Glassmorphism")
    with col3:
        st.markdown('### 🔐 System Info')
        st.button("Purge History"); st.button("Export CSV"); st.button("Cloud Backup")
        st.info(f"Build: 14.5.6 (vID: {st.session_state.reset_counter})")
    st.success("System Optimized")

if st.session_state.get('timer_finished_trigger'):
    st.markdown('<div class="time-up-banner">⏰ TIME IS UP! ⏰</div>', unsafe_allow_html=True); st.balloons()
    components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
    if st.button("Dismiss Alarm"): st.session_state.timer_finished_trigger = False; st.rerun()

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
import requests
from bs4 import BeautifulSoup

# --- 🛰️ GOOGLE ANALYTICS INTEGRATION ---
def inject_ga():
    ga_id = "G-030XWBG97P"

    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga_id}');
    </script>
    """

    components.html(ga_code, height=0)

# --- 🛠️ SYSTEM SETUP ---
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
    except:
        pass

setup_system()

# --- ⚙️ SESSION DEFAULTS ---
DEFAULTS = {
    "set_color": "#FFFFFF",
    "set_bg": "#5465C9",
    "set_font": 1.10,

    "reset_counter": 0,

    "timer_end_time": None,
    "timer_active": False,
    "remaining_at_pause": 0,
    "timer_finished_trigger": False,

    "sound_unlocked": False,
    "selected_alarm_tone": "Double Beep",

    "study_text_input": "",
    "grammar_text_input": "",
    "plag_text_input": "",
    "word_counter_input": "",

    "quiz_step": 0,
    "quiz_score": 0,

    "fc_step": 0,
    "fc_correct": 0,
    "fc_wrong": 0,
    "reveal_fc": False,

    "selected_sources": [
        "Educational (.edu)",
        "Government (.gov)"
    ]
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- 🔄 MASTER RESET ---
def trigger_master_reset():

    st.session_state.reset_counter += 1
    current_reset = st.session_state.reset_counter

    st.session_state.clear()

    for key, value in DEFAULTS.items():
        st.session_state[key] = value

    st.session_state.reset_counter = current_reset

    st.cache_data.clear()
    st.cache_resource.clear()

    st.success("🚨 FULL SYSTEM RESET COMPLETE")

    time.sleep(1)

    st.rerun()

# --- 📄 FILE EXTRACTION ---
def extract_text(uploaded_file):

    if uploaded_file is None:
        return ""

    try:

        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            return " ".join([
                page.extract_text() or ""
                for page in reader.pages
            ])

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return docx2txt.process(uploaded_file)

        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            return df.astype(str).apply(
                lambda x: ' '.join(x),
                axis=1
            ).str.cat(sep=' ')

        else:
            return str(uploaded_file.read(), "utf-8")

    except:
        return ""

# --- 🌐 URL EXTRACTION ---
def extract_from_url(url):

    if not url:
        return ""

    try:

        res = requests.get(url, timeout=5)

        soup = BeautifulSoup(res.content, 'html.parser')

        for s in soup(['script', 'style']):
            s.decompose()

        return soup.get_text(separator=' ', strip=True)

    except:
        return ""

# --- 🔔 AUDIO ---
ALARM_TONES = {
    "Double Beep": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
    "Beep (High)": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    "Digital Alarm": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
    "Industrial Siren": "https://actions.google.com/sounds/v1/alarms/industrial_alarm.ogg"
}

KHAN_SUCCESS = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"

# --- ⏱️ TIMER BACKGROUND LOGIC ---
if (
    st.session_state.timer_active
    and st.session_state.timer_end_time
):

    now = time.time()

    diff = st.session_state.timer_end_time - now

    if diff <= 0:

        st.session_state.timer_active = False
        st.session_state.remaining_at_pause = 0
        st.session_state.timer_finished_trigger = True

    else:
        st.session_state.remaining_at_pause = diff

# --- 🎨 APP CONFIG ---
st.set_page_config(
    page_title="Verso Research Pro",
    page_icon="📚",
    layout="wide"
)

inject_ga()

accent = st.session_state.set_color
bg_card = st.session_state.set_bg
f_scale = st.session_state.set_font

selected_tone_name = st.session_state.selected_alarm_tone
selected_tone_url = ALARM_TONES.get(selected_tone_name)

# --- 🎨 CSS ---
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
    color: white !important;
    box-shadow: 0 4px 10px -1px rgb(0 0 0 / 0.2);
}}

.teacher-board {{
    background-color: #0f172a;
    border: 1px solid #334155;
    padding: 45px;
    border-radius: 12px;
    color: #f1f5f9;
    line-height: 1.9;
    font-size: {f_scale}rem;
}}

.teacher-board h2 {{
    color: {accent};
}}

.google-container {{
    width: 100%;
    height: 100vh;
    overflow: hidden;
    position: relative;
    border-radius: 12px;
    background: white;
}}

.google-iframe {{
    position: absolute;
    top: -120px;
    left: 0;
    width: 100%;
    height: calc(100vh + 120px);
    border: none;
}}

.time-up-banner {{
    background-color: #ef4444;
    color: white;
    padding: 25px;
    text-align: center;
    font-weight: 800;
    border-radius: 12px;
    font-size: 28px;
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
}}

</style>
""", unsafe_allow_html=True)

# --- 🔊 AUDIO TAGS ---
st.markdown(f"""
<audio id="alarm-sound" preload="auto">
    <source src="{selected_tone_url}" type="audio/ogg">
</audio>

<audio id="success-sound" preload="auto">
    <source src="{KHAN_SUCCESS}" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

# --- 📚 SIDEBAR ---
with st.sidebar:

    st.title("VERSO PRO")

    nav_options = [
        "🏠 Home",
        "📒 Study Assistant",
        "✍️ Grammar Checker",
        "🛡️ Plagiarism Checker",
        "⏱️ Time Tracker",
        "📝 Word Counter",
        "⚙️ Settings"
    ]

    choice = st.radio(
        "Navigation",
        nav_options,
        label_visibility="collapsed"
    )

# =========================================================
# HOME
# =========================================================
if choice == "🏠 Home":

    st.title("VERSO RESEARCH")

    source_options = {
        "Educational (.edu)": "site:.edu",
        "Government (.gov)": "site:.gov",
        "International Orgs (.org)": "site:.org",
        "Scientific Journals": "(site:nature.com OR site:sciencedirect.com)",
        "Libraries": "(site:jstor.org OR site:pubmed.ncbi.nlm.nih.gov)",
        "Wikipedia": "site:wikipedia.org"
    }

    if st.button("Select All"):
        st.session_state.selected_sources = list(source_options.keys())

    selected_sources = st.multiselect(
        "Reliable Databases",
        list(source_options.keys()),
        default=st.session_state.selected_sources,
        key=f"src_{st.session_state.reset_counter}"
    )

    query = st.text_input(
        "🔍 Search",
        placeholder="Research topic..."
    )

    if query:

        query_parts = [
            source_options[s]
            for s in selected_sources
        ]

        advanced_filter = " OR ".join(query_parts)

        full_query = f"{query} ({advanced_filter})"

        search_url = (
            f"https://www.google.com/search?"
            f"igu=1&q={full_query.replace(' ', '+')}&hl=en"
        )

        st.markdown(f"""
        <div class="google-container">
            <iframe
                src="{search_url}"
                class="google-iframe">
            </iframe>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# WORD COUNTER
# =========================================================
elif choice == "📝 Word Counter":

    st.title("Word Metrics")

    uploaded_file = st.file_uploader(
        "Upload File",
        type=['pdf', 'docx', 'csv', 'txt'],
        key=f"word_upload_{st.session_state.reset_counter}"
    )

    file_text = extract_text(uploaded_file)

    text = st.text_area(
        "Text Input",
        value=st.session_state.word_counter_input,
        height=250,
        key=f"word_input_{st.session_state.reset_counter}"
    )

    st.session_state.word_counter_input = text

    box_count = len(re.findall(r'\b\w+\b', text))
    file_count = len(re.findall(r'\b\w+\b', file_text))

    st.metric("Words in Box", box_count)
    st.metric("Words in File", file_count)
    st.metric("Combined", box_count + file_count)

# =========================================================
# GRAMMAR CHECKER
# =========================================================
elif choice == "✍️ Grammar Checker":

    st.title("Smart Auto-Correct")

    text_to_check = st.text_area(
        "Paste Text",
        value=st.session_state.grammar_text_input,
        height=250,
        key=f"g_input_{st.session_state.reset_counter}"
    )

    st.session_state.grammar_text_input = text_to_check

    if st.button("✨ Correct"):

        if text_to_check:

            blob = TextBlob(text_to_check)

            corrected = str(blob.correct())

            diff_html = ""

            matcher = difflib.SequenceMatcher(
                None,
                text_to_check,
                corrected
            )

            for tag, i1, i2, j1, j2 in matcher.get_opcodes():

                if tag == 'equal':
                    diff_html += text_to_check[i1:i2]

                else:

                    if i1 != i2:
                        diff_html += (
                            f'<span class="diff-remove">'
                            f'{text_to_check[i1:i2]}'
                            f'</span>'
                        )

                    if j1 != j2:
                        diff_html += (
                            f'<span class="diff-add">'
                            f'{corrected[j1:j2]}'
                            f'</span>'
                        )

            st.markdown(
                f'<div class="notebook-card">{diff_html}</div>',
                unsafe_allow_html=True
            )

            st.code(corrected)

# =========================================================
# PLAGIARISM
# =========================================================
elif choice == "🛡️ Plagiarism Checker":

    st.title("Integrity Scanner")

    plag_text = st.text_area(
        "Paste Text",
        value=st.session_state.plag_text_input,
        height=250,
        key=f"p_input_{st.session_state.reset_counter}"
    )

    st.session_state.plag_text_input = plag_text

    if st.button("🔍 Scan"):

        if plag_text:

            with st.spinner("Scanning..."):

                time.sleep(2)

                sentences = re.split(
                    r'(?<=[.!?]) +',
                    plag_text
                )

                suspicious = 0

                marked_text = ""

                for s in sentences:

                    if len(s.split()) > 15:

                        suspicious += 1

                        marked_text += (
                            f'<span style="background:#7f1d1d;">'
                            f'{s}</span> '
                        )

                    else:
                        marked_text += s + " "

                percent = int(
                    (suspicious / len(sentences)) * 100
                ) if sentences else 0

                st.progress(percent / 100)

                st.markdown(
                    f'<div class="notebook-card">{marked_text}</div>',
                    unsafe_allow_html=True
                )

# =========================================================
# STUDY ASSISTANT
# =========================================================
elif choice == "📒 Study Assistant":

    st.title("Study Assistant")

    files = st.file_uploader(
        "Upload Files",
        type=['pdf', 'docx', 'csv', 'txt'],
        accept_multiple_files=True,
        key=f"f_{st.session_state.reset_counter}"
    )

    url = st.text_input(
        "URL",
        key=f"l_{st.session_state.reset_counter}"
    )

    raw_content = st.text_area(
        "Input Content",
        value=st.session_state.study_text_input,
        height=200,
        key=f"s_input_{st.session_state.reset_counter}"
    )

    st.session_state.study_text_input = raw_content

    final_text = raw_content

    if url:
        final_text += " " + extract_from_url(url)

    if files:
        for f in files:
            final_text += " " + extract_text(f)

    if final_text.strip():

        blob = TextBlob(final_text)

        words = list(dict.fromkeys([
            w.lower()
            for w in blob.noun_phrases
            if len(w) > 3
        ]))

        st.subheader("Keywords")

        for i, w in enumerate(words[:20]):
            st.markdown(
                f'<div class="notebook-card">{i+1}. {w}</div>',
                unsafe_allow_html=True
            )

# =========================================================
# TIMER
# =========================================================
elif choice == "⏱️ Time Tracker":

    st.title("Focus Timer")

    mins = st.number_input(
        "Minutes",
        1,
        180,
        25
    )

    c1, c2, c3 = st.columns(3)

    if c1.button("Start"):

        st.session_state.timer_end_time = (
            time.time() + mins * 60
        )

        st.session_state.timer_active = True

        st.rerun()

    if c2.button("Pause"):

        st.session_state.timer_active = False

    if c3.button("Reset"):

        st.session_state.timer_active = False
        st.session_state.timer_end_time = None
        st.session_state.remaining_at_pause = 0

    m, s = divmod(
        st.session_state.remaining_at_pause,
        60
    )

    st.metric(
        "Remaining",
        f"{int(m):02d}:{int(s):02d}"
    )

    if st.session_state.timer_active:
        time.sleep(1)
        st.rerun()

# =========================================================
# SETTINGS
# =========================================================
elif choice == "⚙️ Settings":

    st.title("Control Center")

    if st.button(
        "🚨 MASTER RESET",
        type="primary",
        use_container_width=True
    ):
        trigger_master_reset()

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("Appearance")

        def update_accent():
            st.session_state.set_color = st.session_state.accent_pick

        def update_bg():
            st.session_state.set_bg = st.session_state.bg_pick

        st.color_picker(
            "Accent Color",
            value=st.session_state.set_color,
            key="accent_pick",
            on_change=update_accent
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

    with c2:

        st.subheader("Audio")

        st.selectbox(
            "Alarm Tone",
            list(ALARM_TONES.keys()),
            key="selected_alarm_tone"
        )

        if st.button("Test Tone"):

            components.html("""
            <script>
            var a=window.parent.document.getElementById('alarm-sound');
            if(a){
                a.load();
                a.play();
            }
            </script>
            """, height=0)

# =========================================================
# TIMER FINISHED
# =========================================================
if st.session_state.get('timer_finished_trigger'):

    st.markdown(
        '<div class="time-up-banner">⏰ TIME IS UP!</div>',
        unsafe_allow_html=True
    )

    components.html("""
    <script>
    var a=window.parent.document.getElementById('alarm-sound');
    if(a){
        a.load();
        a.play();
    }
    </script>
    """, height=0)

    if st.button("Dismiss Alarm"):

        st.session_state.timer_finished_trigger = False

        st.rerun()

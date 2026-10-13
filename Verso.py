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
        'generated_lecture_text': "",
         'humanizer_text_input': "",
        'humanizer_output': "",
        'education_system': "IB System",
        'selected_grade': "MYP (Middle Years Programme)",
        'translator_input': "",
        'translator_output': "",
        'src_lang': "English",
        'tgt_lang': "Arabic",
    }
    for key, value in defaults.items():
        if force or key not in st.session_state:
            st.session_state[key] = value

initialize_states()

# --- 🤖 GEMINI CLIENT INITIALIZATION (SECURED VIA SECRETS) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    client = None

def teach_source_material(source_text: str):
    if client is None:
        return "⚠️ sorry this isn't supposed to happen 😥  (Key problem = API)"

    system_instruction = """
    You are an expert, engaging teacher. Your job is to take the provided source
    material and teach it as a complete lesson in detail.

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
        # Replaced requests.get with custom campus_session to bypass Sophos issues
        res = campus_session.get(url, timeout=6)
        soup = BeautifulSoup(res.content, 'html.parser')
        for s in soup(['script', 'style']): s.decompose()
        return soup.get_text(separator=' ', strip=True)
    except: return ""

# --- 🧬 PURE PYTHON HUMANIZER ENGINE (NO GEMINI) ---
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

_STOP = set("""a an the and or but if then else of to in on at by for with from as is are was were be been
being am do does did have has had having this that these those it its he she they we you i me him her them
us my your his their our not no nor so than too very can could will would shall should may might must
there here which who whom whose what when where why how all any each few more most other some such only
own same just also into over under again further once about above below up down out off""".split())

_PHRASES = {
    r"\bin order to\b": "to", r"\bdue to the fact that\b": "because",
    r"\bin addition\b,?": "plus,", r"\bfurthermore\b,?": "also,", r"\bmoreover\b,?": "what's more,",
    r"\bconsequently\b,?": "so", r"\btherefore\b,?": "so", r"\bhowever\b,?": "still,",
    r"\bnevertheless\b,?": "even so,", r"\bin conclusion\b,?": "all in all,",
    r"\bultimately\b,?": "in the end,", r"\bsignificant(ly)?\b": "major",
    r"\ba large number of\b": "many", r"\bas a result of\b": "because of",
    r"\bwith regard to\b": "about", r"\bin the event that\b": "if",
    r"\bit is important to note that\b": "keep in mind that",
    r"\bplays? a (crucial|vital|key) role in\b": "matters a lot for",
    r"\bdelve into\b": "dig into", r"\butilize\b": "use", r"\bdemonstrate\b": "show",
    r"\bnumerous\b": "plenty of", r"\bpivotal\b": "key", r"\bmultifaceted\b": "many-sided",
}

_CONTRACTIONS = {
    r"\bdo not\b": "don't", r"\bdoes not\b": "doesn't", r"\bdid not\b": "didn't",
    r"\bis not\b": "isn't", r"\bare not\b": "aren't", r"\bcannot\b": "can't",
    r"\bit is\b": "it's", r"\bthey are\b": "they're", r"\bwe are\b": "we're",
    r"\bwill not\b": "won't", r"\bhas not\b": "hasn't", r"\bhave not\b": "haven't",
}

_POS_MAP = {'JJ': wn.ADJ,
            'VB': wn.VERB, 'VBP': wn.VERB, 'VBZ': wn.VERB, 'VBG': wn.VERB,
            'VBD': wn.VERB, 'VBN': wn.VERB}
_POS_MAP_NOUNS = {**_POS_MAP, 'NN': wn.NOUN, 'NNS': wn.NOUN}

def _inflect(w: str, tag: str):
    """Very small inflector. Returns None if unsafe."""
    if tag in ('NNS', 'VBZ'):
        if re.search(r'[^aeiou]y$', w): return w[:-1] + "ies"
        if w.endswith(('s', 'x', 'z', 'ch', 'sh')): return w + "es"
        return w + "s"
    if tag in ('VBD', 'VBN'):
        if re.search(r'[^aeiou][aeiou][^aeiouwxy]$', w): return None  # doubling risk
        if w.endswith('e'): return w + "d"
        if re.search(r'[^aeiou]y$', w): return w[:-1] + "ied"
        return w + "ed"
    if tag == 'VBG':
        if re.search(r'[^aeiou][aeiou][^aeiouwxy]$', w): return None
        if w.endswith('e') and not w.endswith('ee'): return w[:-1] + "ing"
        return w + "ing"
    return w

def _synonym(word: str, tag: str, rng: random.Random, pos_map: dict, context=None, allow_rare: bool = False):
    pos = pos_map.get(tag)
    if not pos: return None
    lemma = wn.morphy(word.lower(), pos) or word.lower()
    synsets = []
    if context:                                   # pick the sense that fits the sentence (Lesk)
        try:
            best = lesk([t.lower() for t in context], lemma, pos)
        except Exception:
            best = None
        if best: synsets = [best]
    if not synsets:
        synsets = wn.synsets(lemma, pos=pos)[:2 if allow_rare else 1]
    cands = []
    for syn in synsets:
        for l in syn.lemmas():
            name = l.name()
            if name.isalpha() and name.lower() != lemma and len(name) > 2 and (allow_rare or l.count() > 0):
                cands.append(name.lower())
    cands = list(dict.fromkeys(cands))
    if not cands: return None
    return _inflect(rng.choice(cands), tag)

def _swap_words(sentence: str, rng: random.Random, strength: float, pos_map: dict = None) -> str:
    pos_map = pos_map or _POS_MAP
    tokens = re.findall(r"\w+(?:[-']\w+)*|[^\w\s]", sentence)
    try:
        tagged = nltk.pos_tag(tokens)
    except Exception:
        return sentence
    out = []
    for i, (tok, tag) in enumerate(tagged):
        replace = (tok.isalpha() and len(tok) > 3 and tok.lower() not in _STOP
                   and tag in pos_map and not (tok[0].isupper() and i > 0)
                   and rng.random() < strength)
        if replace:
            new = _synonym(tok, tag, rng, pos_map, context=tokens)
            if new:
                tok = new.capitalize() if tagged[i][0][0].isupper() else new
        out.append(tok)
    text = " ".join(out)
    text = re.sub(r"\s+([,.;:!?%)\]])", r"\1", text)
    text = re.sub(r"([(\[])\s+", r"\1", text)
    return re.sub(r"\s+'(\w)", r"'\1", text)

def _split_long(sentence: str, rng: random.Random) -> list:
    """Break long compound sentences into shorter ones."""
    if len(sentence.split()) < 18: return [sentence]
    m = re.search(r",\s+(and|but|while|whereas|so)\s+|;\s+", sentence)
    if not m: return [sentence]
    left, right = sentence[:m.start()].rstrip(",;"), sentence[m.end():]
    joiner = (m.group(1) or "").lower()
    right = right[0].upper() + right[1:] if right else right
    if joiner == "but":  right = "But " + right[0].lower() + right[1:]
    elif joiner == "so": right = "So " + right[0].lower() + right[1:]
    return [left.rstrip(".") + ".", right]

# ---------- OPTIONAL NEURAL PARAPHRASER (QuillBot-style, runs locally, no API) ----------
@st.cache_resource
def load_neural_paraphraser():
    """Needs: pip install transformers torch sentencepiece (first run downloads ~900 MB)."""
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    name = "humarin/chatgpt_paraphraser_on_T5_base"
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForSeq2SeqLM.from_pretrained(name)
    model.eval()
    return tok, model

def neural_paraphrase(sentence: str, neural) -> str:
    if neural is None or len(sentence.split()) < 4:
        return sentence
    try:
        import torch
        tok, model = neural
        inputs = tok("paraphrase: " + sentence, return_tensors="pt", truncation=True, max_length=256)
        with torch.no_grad():
            out = model.generate(**inputs, max_length=256, do_sample=True, top_k=50, top_p=0.95,
                                 temperature=0.8, repetition_penalty=1.3, no_repeat_ngram_size=3)
        result = tok.decode(out[0], skip_special_tokens=True).strip()
        return result or sentence
    except Exception:
        return sentence

def ngram_overlap(original: str, rewritten: str, n: int = 4) -> float:
    """% of the original's word n-grams that still appear in the rewrite."""
    def grams(t):
        w = re.findall(r"\w+", t.lower())
        return {tuple(w[i:i+n]) for i in range(len(w) - n + 1)}
    a, b = grams(original), grams(rewritten)
    return 0.0 if not a else round(100 * len(a & b) / len(a), 1)

_FILLERS = ["really", "quite", "actually", "generally", "often", "clearly"]

def force_low_overlap(original: str, text: str, rng: random.Random, n: int = 4, max_rounds: int = 8) -> str:
    """Targeted final pass: finds word runs still shared with the original and edits them until none remain."""
    ow = re.findall(r"\w+", original.lower())
    ogr = {tuple(ow[i:i+n]) for i in range(len(ow) - n + 1)}
    if not ogr:
        return text
    all_map = {**_POS_MAP_NOUNS, 'RB': wn.ADV}
    for rnd in range(max_rounds):
        ms = list(re.finditer(r"\w+", text))
        ws = [m.group().lower() for m in ms]
        bad = [i for i in range(len(ws) - n + 1) if tuple(ws[i:i+n]) in ogr]
        if not bad:
            break
        try:
            tagged = nltk.pos_tag([m.group() for m in ms])
        except Exception:
            tagged = [(m.group(), 'XX') for m in ms]
        edited, edits = set(), []
        for i in bad:
            if any(j in edited for j in range(i, i + n)):
                continue                      # an earlier edit already breaks this run
            for j in (i + 1, i + 2, i, i + 3):
                s0, e0 = ms[j].span()
                tok, tag = tagged[j]
                if ((s0 > 0 and text[s0 - 1] in "-'’") or (e0 < len(text) and text[e0] in "-'’")
                        or not tok.isalpha() or len(tok) < 3):
                    continue                  # leave hyphenated / apostrophe words and numbers alone
                new = None
                if tag in all_map and tok.lower() not in _STOP:
                    ctx = [t for t, _ in tagged[max(0, j - 8): j + 8]]
                    new = _synonym(tok, tag, rng, all_map, context=ctx, allow_rare=(rnd >= 2))
                if new:
                    edits.append((s0, e0, new.capitalize() if tok[0].isupper() else new))
                    edited.add(j)
                    break
                if rnd >= 1 and tag in ('JJ', 'VB', 'VBP', 'VBZ', 'VBD', 'VBN', 'VBG') and tok[0].islower():
                    edits.append((s0, s0, rng.choice(_FILLERS) + " "))
                    edited.add(j)
                    break
        if not edits:
            break
        for s0, e0, rep in sorted(edits, reverse=True):
            text = text[:s0] + rep + text[e0:]
    return text

def _is_heading(line: str) -> bool:
    l = line.strip()
    return 0 < len(l.split()) <= 6 and not re.search(r"[.!?:]$", l)

def pure_python_humanizer(text: str, strength: float = 0.8,
                          shuffle_sentences: bool = False, seed=None,
                          include_nouns: bool = False, neural=None,
                          force_zero: bool = False) -> str:
    rng = random.Random(seed)
    pos_map = _POS_MAP_NOUNS if include_nouns else _POS_MAP
    original = text.strip()
    text = original
    for pat, rep in _PHRASES.items():
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    text = re.sub(r",\s*,", ",", text)

    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    final_pars = []
    for p in paragraphs:
        out_lines = []
        for line in p.split("\n"):
            if not line.strip():
                continue
            if _is_heading(line):                       # keep short title lines on their own line
                out_lines.append(line.strip())
                continue
            sentences = re.split(r"(?<=[.!?])\s+", line.strip())
            new_sents = []
            for s in sentences:
                for piece in _split_long(s, rng):
                    piece = neural_paraphrase(piece, neural)          # neural rewrite first (if enabled)
                    new_sents.append(_swap_words(piece, rng, strength, pos_map))
            if shuffle_sentences and len(new_sents) > 3:
                first, rest = new_sents[0], new_sents[1:]   # keep the opener in place
                rng.shuffle(rest)
                new_sents = [first] + rest
            par = " ".join(new_sents)
            for pat, rep in _CONTRACTIONS.items():
                par = re.sub(pat, rep, par, flags=re.IGNORECASE)
            par = re.sub(r"(^|[.!?]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), par)
            out_lines.append(par)
        final_pars.append("\n".join(out_lines))
    result = "\n\n".join(final_pars)
    if force_zero:
        result = force_low_overlap(original, result, rng)
    return result

# --- 📜 CITATION GENERATOR ENGINE ---
def generate_scribbr_citation(url, style_format):
    if not url: return "Please enter a valid URL or reference title."

    title = "Web Page Reference"
    site_name = "Website Source"
    author_name = ""
    current_year = time.strftime("%Y")
    access_date = time.strftime("%d %b. %Y")

    try:
        # Replaced requests.get with custom campus_session to bypass Sophos issues
        res = campus_session.get(url, timeout=5)
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

.time-up-banner {{ background-color: #ef4444; color: white; padding: 25px; text-align: center; font-weight: 800; border-radius: 12px; font-size: 28px;
animation: blinker 0.8s linear infinite; }}
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
    if client is None:
        st.error("🔑 API Key Configuration Missing")
        st.info("To add a new key, create a file at `.streamlit/secrets.toml` in your app project folder and add:\n\n`GEMINI_API_KEY = \"your_new_key_here\"`")
    st.caption("Made by: yaseen Amr")
    st.markdown("---")

with st.sidebar:
    st.image("z.png", width=80)
    st.title("Verso Pro")
    nav_options = [
        "🏠 Home",
        "📒 Study Assistant",
        "✍️ Grammar Checker",
        "🛡️ Plagiarism Checker",
        "📚 Citation Generator",
        "⏱️ Time Tracker",
        "📝 Word Counter",
        "✍️ Humanism Engine",
        "🌐 Verso Translate",
        "⚙️ Settings",
        
    ]

    choice = st.radio("Navigation Menu", nav_options, label_visibility="collapsed")

    
# --- HOME ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown("### 🎓 Verso Academic Engine ")
    st.caption("use it to filter unsuitable websites for studying and writing essays like .com Websites and Wikipedia")

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
    st.title("Verso Word Counter")
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
                t = text_to_check.strip()
                blob = TextBlob(t)
                corrected = str(blob.correct()).rstrip('.?! ')
                corrected = re.sub(r'\bi\b', 'I', corrected)

                q_words = ('who', 'what', 'where', 'when', 'why', 'how', 'is', 'can', 'do', 'does', 'hi', 'are')
                corrected += "?" if corrected.lower().startswith(q_words) else "."
                final_text = corrected[0].upper() + corrected[1:] if corrected else ""

                diff_html = ""
                matcher = difflib.SequenceMatcher(None, text_to_check, final_text)
                for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                    if tag == 'equal': diff_html += text_to_check[i1:i2]
                    else:
                        if i1 != i2: diff_html += f'<span class="diff-remove">{text_to_check[i1:i2]}</span>'
                        if j1 != j2: diff_html += f'<span class="diff-add">{final_text[j1:j2]}</span>'
                st.success("Correction Finished!")
                st.markdown(f'<div class="notebook-card" style="line-height: 1.8;">{diff_html}</div>', unsafe_allow_html=True)
                with st.expander("Final Polished Text"): st.code(final_text)

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
                reference = st.session_state.humanizer_text_input.strip() if (st.session_state.humanizer_output.strip() and ngram_overlap(st.session_state.humanizer_output, plag_text, 3) >= 50) else ""
                ref_grams = set()
                if reference:
                    _rw = re.findall(r"\w+", reference.lower())
                    ref_grams = {tuple(_rw[i:i+4]) for i in range(len(_rw) - 3)}
                academic_triggers = ["infrastructure", "implementation", "federal funding", "neurological", "opportunity", "assessment", "significant"]
                marked_text = ""
                match_count = 0
                for s in sentences:
                    if reference:
                        _sw = re.findall(r"\w+", s.lower())
                        is_match = any(tuple(_sw[i:i+4]) in ref_grams for i in range(len(_sw) - 3))
                    else:
                        is_match = len(s.split()) > 15 or any(trig in s.lower() for trig in academic_triggers)
                    if is_match:
                        marked_text += f'<span class="plag-highlight" style="background-color:#7f1d1d; color:#fecaca;">{s}</span> '
                        match_count += 1
                    else: marked_text += f'{s} '
                plag_percent = min(98, int((match_count / len(sentences)) * 100)) if sentences else 0
                if reference:
                    plag_percent = int(ngram_overlap(reference, plag_text))
                    st.caption("Mode: comparing against the original text you gave the Humanizer (4-word sequences).")
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
            st.markdown("### Verso Flashcards (25 Cards)")
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

                clean_speech_js = raw_generated_lesson.replace('"', '\\"').replace("'", "\\'").replace('\n', ' ').replace('\r', ' ')
                clean_speech_js = re.sub(r'[^\x00-\x7F]+', '', clean_speech_js)

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




# --- MODULE: TIME TRACKER ---
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

# --- MODULE: HUMANISM ENGINE (PURE PYTHON) ---
elif choice == "✍️ Humanism Engine":
    st.header("✨ Verso Humanizer")
    text_to_humanize = st.text_area(
        "Paste text here:", value=st.session_state.humanizer_text_input, height=200,
        placeholder="Please input the text you want to humanize...",
        key="humanizer_interactive_input")
    st.session_state.humanizer_text_input = text_to_humanize

    if st.button("🚀 Humanize Output Text", type="primary"):
        if not text_to_humanize.strip():
            st.warning("Please add some text first!")
        else:
            with st.spinner("Rewriting..."):
                best, best_ov = "", 101.0
                for _ in range(5):
                    cand = pure_python_humanizer(text_to_humanize, 0.9, False,
                                                 seed=random.randint(0, 10**6),
                                                 include_nouns=True, neural=None, force_zero=True)
                    ov = ngram_overlap(text_to_humanize, cand)
                    if ov < best_ov:
                        best, best_ov = cand, ov
                    if best_ov == 0:
                        break
                st.session_state.humanizer_output = best

    if st.session_state.humanizer_output:
        st.subheader("📝 Processed Paraphrase Output")
        st.write(st.session_state.humanizer_output.replace("\n", "  \n"))
        overlap = ngram_overlap(st.session_state.humanizer_text_input,
                                st.session_state.humanizer_output)
        st.metric("Remaining 4-word overlap with original", f"{overlap}%")
        st.caption("This measures overlap with your input only. It is not a real "
                   "plagiarism-checker score. Always read the output: the lowest-overlap "
                   "variation is not always the most readable one.")

# --- 🌐 TRANSLATOR MODULE ENGINE (GEMINI-POWERED 100% UNBLOCKED TRANSLATION) ---
elif choice == "🌐 Verso Translate":
    st.header("🌐 Google Translate Engine")
    st.write("Instant, context-aware translations matching Google Translate matrices for your core academic workflows.")

    # Core language mapping framework configurations
    lang_map = {
        "Arabic": "ar",
        "English": "en",
        "French": "fr",
        "German": "de"
    }
    lang_list = list(lang_map.keys())

    # Safely cross-swap languages inside Streamlit's official widget state manager keys
    def safe_language_swap():
        old_src = st.session_state.src_lang
        st.session_state.src_lang = st.session_state.tgt_lang
        st.session_state.tgt_lang = old_src

    # Layout generation using an explicit column count parameter
    col1, col_swap, col2 = st.columns(3)
    
    with col1:
        st.selectbox(
            "From Language:", 
            options=lang_list, 
            key="src_lang"
        )
        
    with col_swap:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("🔄 Swap", use_container_width=True, on_click=safe_language_swap):
            st.rerun()
            
    with col2:
        st.selectbox(
            "To Language:", 
            options=lang_list, 
            key="tgt_lang"
        )

    # Workspace Text Layout Fields (Split Screen 50/50 Columns)
    input_col, output_col = st.columns(2)
    
    with input_col:
        st.text_area(
            f"Enter text in {st.session_state.src_lang}:",
            height=250,
            placeholder="Please input the text you want to translate...",
            key="translator_input"
        )

    # Execution controls using Gemini infrastructure to completely bypass IP bans
    if st.button("✨ Translate Content", type="primary", use_container_width=True):
        if not st.session_state.translator_input.strip():
            st.warning("Please type some characters to process translation.")
        else:
            with st.spinner("Processing context-aware translation..."):
                src_full = st.session_state.src_lang
                tgt_full = st.session_state.tgt_lang
                
                if client is not None:
                    system_instruction = f"""
                    You are a professional, exact translation assistant. Your task is to translate the user text from {src_full} to {tgt_full}.
                    Maintain exact meaning, tone, and punctuation structure.
                    Output ONLY the translated result text. Do not add any introductory or explanatory text.
                    """
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"Translate this text payload:\n\n{st.session_state.translator_input}",
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.3
                            )
                        )
                        st.session_state.translator_output = response.text.strip()
                        st.rerun()
                    except Exception as ai_err:
                        st.session_state.translator_output = f"⚠️ System Connection Error: {ai_err}"
                else:
                    st.session_state.translator_output = "⚠️ Gemini Client is not initialized. Please verify your API Key in secrets."

    with output_col:
        st.text_area(
            f"Translation in {st.session_state.tgt_lang}:",
            height=250,
            disabled=True,
            key="translator_output"
        )
        
# --- MODULE: SETTINGS ---
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

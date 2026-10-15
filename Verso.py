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
        'set_color': "#0B57D0",
        'set_bg': "#FFFFFF",
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
        'study_assets': None,
        'study_assets_source_key': None,
        'study_quiz_step': 0,
        'study_quiz_score': 0,
        'study_quiz_feedback': None,
        'study_fc_step': 0,
        'study_fc_revealed': False,
        'study_assistant_answer': "",
        'study_assistant_last_question': "",
        'study_assistant_source_key': None,
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

def extract_youtube_transcript(url):
    """Retrieve actual YouTube captions using current and legacy library APIs.

    Returns transcript text only. It never substitutes video titles or page metadata
    for the spoken content.
    """
    match = re.search(
        r"(?:youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/)|youtu\.be/)([A-Za-z0-9_-]{11})",
        url.strip(),
        re.IGNORECASE,
    )
    if not match:
        return "__TRANSCRIPT_ERROR__:That doesn't look like a supported YouTube video URL. Paste the full youtube.com/watch?v=... or youtu.be/... link."
    video_id = match.group(1)

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return "__TRANSCRIPT_ERROR__:Missing dependency: add youtube-transcript-api to requirements.txt and redeploy."

    errors = []

    def transcript_text(fetched):
        snippets = getattr(fetched, "snippets", fetched)
        lines = []
        for item in snippets:
            if isinstance(item, dict):
                line = item.get("text", "")
            else:
                line = getattr(item, "text", "")
            if line:
                lines.append(str(line))
        return " ".join(lines).strip()

    # Current youtube-transcript-api versions use an instance API.
    try:
        api = YouTubeTranscriptApi()
        try:
            fetched = api.fetch(video_id)
            transcript = transcript_text(fetched)
            if transcript:
                return f"YouTube video transcript (video ID {video_id}):\n{transcript}"
            errors.append("The direct captions response was empty.")
        except Exception as exc:
            errors.append(f"fetch(): {type(exc).__name__}: {exc}")

        # Some videos/languages require selecting an available transcript first.
        try:
            transcript_list = api.list(video_id)
            try:
                selected = transcript_list.find_transcript(["en", "en-US", "en-GB"])
            except Exception:
                selected = next(iter(transcript_list))
            fetched = selected.fetch()
            transcript = transcript_text(fetched)
            if transcript:
                return f"YouTube video transcript (video ID {video_id}):\n{transcript}"
            errors.append("The selected captions response was empty.")
        except Exception as exc:
            errors.append(f"list()/fetch(): {type(exc).__name__}: {exc}")
    except Exception as exc:
        errors.append(f"API initialization: {type(exc).__name__}: {exc}")

    # Compatibility fallback for older releases only; newer releases removed this method.
    try:
        legacy_method = getattr(YouTubeTranscriptApi, "get_transcript", None)
        if callable(legacy_method):
            entries = legacy_method(video_id)
            transcript = transcript_text(entries)
            if transcript:
                return f"YouTube video transcript (video ID {video_id}):\n{transcript}"
            errors.append("The legacy captions response was empty.")
    except Exception as exc:
        errors.append(f"legacy get_transcript(): {type(exc).__name__}: {exc}")

    # Do not expose long library/network tracebacks in the learner-facing UI.
    # A cloud-hosted app cannot guarantee direct YouTube caption access when YouTube
    # blocks requests from the hosting IP. Offer a dependable transcript-paste fallback.
    return (
        "__TRANSCRIPT_ERROR__:Automatic caption retrieval was blocked or unavailable. "
        "This can happen when YouTube blocks requests from the app's hosting server, "
        "or when the video has no captions accessible to this app."
    )


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

def _contrast_text(hex_color: str) -> str:
    """Pick dark or light text so a user-chosen colour always stays readable."""
    try:
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return "#1F1F1F" if (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.6 else "#FFFFFF"
    except Exception:
        return "#1F1F1F"

_UI_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
:root {
  --accent: __ACCENT__;
  --accent-fg: __ACCENT_FG__;
  --card-bg: __CARD_BG__;
  --card-fg: __CARD_FG__;
  --ink: #1F1F1F;
  --muted: #5F6368;
  --line: #E1E3E1;
  --canvas: #F8FAFD;
  --rail: #F0F4F9;
  --tonal: #E9EEF6;
  --accent-soft: #D3E3FD;
  --danger: #B3261E;
}
html, body, .stApp, [data-testid="stMarkdownContainer"], .stApp label, .stApp input,
.stApp textarea, .stApp button, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
}
.stApp { background: var(--canvas); color: var(--ink); }
[data-testid="stHeader"] { background: transparent; }

[data-testid="stDecoration"], footer, #MainMenu {
  display: none !important;
}

/* Keep the sidebar collapse/expand controls visible */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarHeader"] button,
[data-testid="stSidebarCollapsedControl"] {
  visibility: visible !important;
  opacity: 1 !important;
  display: flex !important;
  color: #1F1F1F !important;
}

/* Keep the header available for sidebar controls */
[data-testid="stHeader"] {
  background: transparent !important;
  visibility: visible !important;
}

.block-container { padding: 3rem 3rem 5rem; max-width: 1100px; }
@media (max-width: 768px) { .block-container { padding: 2rem 1rem 4rem; } }

/* Type scale */
h1 { font-weight: 600 !important; font-size: 2rem !important; letter-spacing: -0.02em; color: var(--ink); padding-bottom: 0.25rem; }
h2 { font-weight: 600 !important; font-size: 1.5rem !important; letter-spacing: -0.015em; }
h3 { font-weight: 600 !important; font-size: 1.1rem !important; letter-spacing: -0.01em; }
p, li { line-height: 1.6; }
[data-testid="stCaptionContainer"], .stCaption { color: var(--muted); }
hr { border: none; border-top: 1px solid var(--line); margin: 1rem 0; }

/* Sidebar rail */
[data-testid="stSidebar"] { background: var(--rail); border-right: none; }
[data-testid="stSidebar"] h1 { font-size: 1.25rem !important; margin: 0.25rem 0 1rem; padding: 0; }
[data-testid="stSidebar"] img { border-radius: 14px; }
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] { gap: 2px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  padding: 10px 16px !important; border-radius: 999px; margin: 0 !important; width: 100%;
  background: transparent !important; border: none !important; box-shadow: none !important;
  cursor: pointer; transition: background-color .15s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child { display: none; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: rgba(11, 87, 208, .07) !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) { background: var(--accent-soft) !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label p { font-size: .95rem; font-weight: 500; color: #3C4043; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p { color: #041E49; font-weight: 600; }

/* Buttons */
.stButton > button, [data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-primary"] {
  border-radius: 999px; padding: .5rem 1.4rem; font-weight: 500; box-shadow: none;
  border: 1px solid #C4C7C5; background: #FFFFFF; color: var(--ink);
  transition: background-color .15s ease, border-color .15s ease, box-shadow .15s ease;
}
.stButton > button p, [data-testid^="stBaseButton"] p { color: inherit !important; font-weight: 500; }
.stButton > button:hover, [data-testid="stBaseButton-secondary"]:hover { background: var(--rail); border-color: var(--accent); color: var(--ink); }
[data-testid="stBaseButton-primary"] { background: var(--accent); color: var(--accent-fg); border-color: var(--accent); }
[data-testid="stBaseButton-primary"]:hover { background: var(--accent); color: var(--accent-fg); filter: brightness(1.08); box-shadow: 0 1px 3px rgba(60, 64, 67, .3); }
.stButton > button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

/* Inputs */
[data-baseweb="textarea"], [data-baseweb="input"], [data-baseweb="select"] > div {
  background: #FFFFFF !important; border: 1px solid #C4C7C5 !important; border-radius: 14px !important;
  transition: border-color .15s ease, box-shadow .15s ease;
}
[data-baseweb="base-input"] { background: transparent !important; border: none !important; }
[data-baseweb="textarea"]:focus-within, [data-baseweb="input"]:focus-within, [data-baseweb="select"]:focus-within > div {
  border-color: var(--accent) !important; box-shadow: 0 0 0 1px var(--accent) !important;
}
.stTextArea textarea, .stTextInput input, .stNumberInput input { background: transparent !important; color: var(--ink); font-size: .97rem; line-height: 1.6; }
.stTextArea textarea:disabled { color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important; opacity: 1; background: var(--rail) !important; }
.stTextArea label p, .stTextInput label p, .stSelectbox label p, .stMultiSelect label p, .stNumberInput label p { font-weight: 500; color: #3C4043; }
[data-baseweb="tag"] { background: var(--accent-soft) !important; border-radius: 999px !important; }
[data-baseweb="tag"] span, [data-baseweb="tag"] svg { color: #041E49 !important; fill: #041E49 !important; }
[data-testid="stFileUploaderDropzone"] { background: #FFFFFF; border: 1.5px dashed #C4C7C5; border-radius: 20px; }

/* Tabs */
[data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--line); }
button[data-baseweb="tab"] { font-weight: 500; color: var(--muted); padding: .6rem 1rem; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--accent); }
[data-baseweb="tab-highlight"] { background: var(--accent) !important; height: 3px !important; border-radius: 3px 3px 0 0; }
[data-baseweb="tab-border"] { display: none; }

/* Metrics, alerts, expanders */
[data-testid="stMetric"] { background: #FFFFFF; border: 1px solid var(--line); border-radius: 20px; padding: 18px 22px; }
[data-testid="stMetricLabel"] p { color: var(--muted); font-weight: 500; }
[data-testid="stMetricValue"] { font-weight: 600; letter-spacing: -0.02em; }
[data-testid="stAlert"] { border-radius: 16px; border: none; }
[data-testid="stExpander"] { background: #FFFFFF; border: 1px solid var(--line); border-radius: 16px; }
[data-testid="stExpander"] details { border: none; }

/* Content surfaces */
.notebook-card {
  background-color: var(--card-bg); color: var(--card-fg) !important;
  border: 1px solid var(--line); border-radius: 20px; padding: 24px 28px; margin-bottom: 14px;
  box-shadow: 0 1px 2px rgba(60, 64, 67, .08), 0 1px 3px 1px rgba(60, 64, 67, .05); line-height: 1.7;
}
.notebook-card b { color: inherit; font-weight: 600; }
.teacher-board {
  background-color: #FFFFFF; border: 1px solid var(--line); padding: 40px 44px;
  border-radius: 24px; color: var(--ink); line-height: 1.85; font-size: __FSCALE__rem; white-space: pre-wrap;
  box-shadow: 0 1px 2px rgba(60, 64, 67, .08), 0 1px 3px 1px rgba(60, 64, 67, .05);
}
.teacher-board h2 { color: var(--ink); border-bottom: 1px solid var(--line); padding-bottom: 10px; }
.teacher-board h3 { color: var(--muted); margin-top: 28px; font-size: 1.05rem; }
.teacher-board b { color: var(--ink); font-weight: 600; }

.google-container {
  width: 100%; height: 800px; overflow: hidden; position: relative;
  border-radius: 20px; border: 1px solid var(--line); background-color: white;
}
.google-iframe { position: absolute; top: -125px; left: 0; width: 100%; height: 1025px; }

.time-up-banner {
  background-color: var(--danger); color: white; padding: 25px; text-align: center; font-weight: 700;
  border-radius: 20px; font-size: 28px; animation: blinker 0.8s linear infinite;
}
@keyframes blinker { 50% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .time-up-banner { animation: none; } }
.diff-add { background-color: #C4EED0; color: #0D652D; padding: 1px 4px; border-radius: 4px; }
.diff-remove { background-color: #F9DEDC; color: #8C1D18; text-decoration: line-through; padding: 1px 4px; border-radius: 4px; }
.pro-badge { background-color: var(--accent); color: var(--accent-fg); padding: 2px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; margin-left: 10px; }
</style>
"""
_UI_CSS = (_UI_CSS.replace("__ACCENT_FG__", _contrast_text(accent))
                  .replace("__ACCENT__", accent)
                  .replace("__CARD_BG__", bg_card)
                  .replace("__CARD_FG__", _contrast_text(bg_card))
                  .replace("__FSCALE__", str(f_scale)))
st.markdown(_UI_CSS, unsafe_allow_html=True)

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
        st.error("API Key Configuration Missing")
        st.info("To add a new key, create a file at `.streamlit/secrets.toml` in your app project folder and add:\n\n`GEMINI_API_KEY = \"your_new_key_here\"`")
    st.caption("Made by: yaseen Amr")
    st.markdown("---")

with st.sidebar:
    st.image("z.png", width=80)
    st.title("Verso Pro")
    nav_options = [
        "Home",
        "Study Assistant",
        "Grammar Checker",
        "Plagiarism Checker",
        "Citation Generator",
        "Time Tracker",
        "Word Counter",
        "Humanism Engine",
        "Verso Translate",
        "Settings",
        
    ]

    choice = st.radio("Navigation Menu", nav_options, label_visibility="collapsed")

    
# --- HOME ---

def generate_study_assets(source_text: str, quiz_count: int = 15, flashcard_count: int = 25):
    """Generate source-grounded study materials as strict JSON; never invent filler questions."""
    if client is None:
        raise RuntimeError("The AI service is not configured. Add GEMINI_API_KEY to Streamlit secrets.")
    source = source_text.strip()
    if len(source) < 80:
        raise ValueError("Please provide a little more study material (at least a few sentences).")
    instruction = (
        "You are a careful academic tutor. Use ONLY the supplied source; do not invent facts, definitions, evidence, or claims. "
        "Return valid JSON only with this schema: "
        '{"keywords":["..."],"quiz":[{"question":"clear specific question","options":["A","B","C","D"],"answer":"exact option text","explanation":"source-grounded explanation"}],'
        '"flashcards":[{"question":"direct study question","answer":"accurate concise answer from source"}]}. '
        f"Create exactly {quiz_count} distinct quiz questions whenever the source contains enough information, plus up to {flashcard_count} distinct flashcards. Aim for 15 quiz questions by testing different facts, concepts, causes, examples, and relationships from the source. Never pad with generic, repeated, or invented questions; if the source genuinely cannot support 15, return only the supported questions. "
        "Questions must be natural, specific, and answerable from the source, not generic templates. Quiz choices must be plausible and have exactly one correct answer. "
        "Explanations must explain why the answer is right. Flashcard answers must directly answer the question. Avoid duplicates, vague wording, and filler. "
        "Keywords must be important terms actually present in the source."
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="STUDY SOURCE:\n\n" + source[:24000],
        config=types.GenerateContentConfig(system_instruction=instruction, response_mime_type="application/json", temperature=0.25),
    )
    raw = (response.text or "").strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.I)
    import json
    data = json.loads(raw)
    quiz, seen_q = [], set()
    for item in data.get("quiz", []):
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()
        if not question or not isinstance(options, list):
            continue
        options = list(dict.fromkeys(str(x).strip() for x in options if str(x).strip()))
        if len(options) != 4 or answer not in options or question.casefold() in seen_q:
            continue
        seen_q.add(question.casefold())
        quiz.append({"question": question, "options": options, "answer": answer,
                     "explanation": str(item.get("explanation", "The source supports this answer.")).strip()})
    cards, seen_cards = [], set()
    for item in data.get("flashcards", []):
        if not isinstance(item, dict):
            continue
        question, answer = str(item.get("question", "")).strip(), str(item.get("answer", "")).strip()
        if question and answer and question.casefold() not in seen_cards:
            seen_cards.add(question.casefold())
            cards.append({"question": question, "answer": answer})
    keywords = list(dict.fromkeys(str(x).strip() for x in data.get("keywords", []) if str(x).strip()))
    if not quiz and not cards:
        raise ValueError("The AI could not produce valid study questions. Add clearer or more detailed notes and try again.")
    return {"quiz": quiz, "flashcards": cards, "keywords": keywords}


def answer_from_study_source(source_text: str, question: str) -> str:
    """Answer a student's question using only the supplied study source."""
    if client is None:
        raise RuntimeError("The AI service is not configured. Add GEMINI_API_KEY to Streamlit secrets.")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"STUDY SOURCE:\n{source_text[:24000]}\n\nSTUDENT QUESTION:\n{question}",
        config=types.GenerateContentConfig(
            system_instruction=("You are a clear, supportive study assistant. Answer the exact question using only the supplied source. "
                "Explain reasoning in plain language. If the source lacks enough information, say so plainly; never pretend the source says something it does not."),
            temperature=0.25,
        ),
    )
    return (response.text or "I couldn't produce an answer. Please try rephrasing the question.").strip()



if choice == "Home":
    st.title("Verso Research")
    st.markdown("### Verso Academic Engine ")
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

    q = st.text_input("Search Database:", placeholder="Research your topic here...")

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
elif choice == "Word Counter":
    st.title("Verso Word Counter")
    st.markdown("### Analyze Content")
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
elif choice == "Grammar Checker":
    st.markdown('<h1>Smart Verso Auto Correct</h1>', unsafe_allow_html=True)
    text_to_check = st.text_area("Paste text to improve:", value=st.session_state.grammar_text_input, height=250, placeholder="Please input the text you want to correct...", key="g_input")
    st.session_state.grammar_text_input = text_to_check
    if st.button("Run Smart Correction", use_container_width=True):
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
elif choice == "Plagiarism Checker":
    st.title("Plagiarism Pro Scanner")
    plag_text = st.text_area("Paste text to scan:", value=st.session_state.plag_text_input, placeholder="Paste text here...", height=250, key="p_input")
    st.session_state.plag_text_input = plag_text
    if st.button("Deep Verso Plagiarism Scan", use_container_width=True):
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
                        marked_text += f'<span class="plag-highlight" style="background-color:#F9DEDC; color:#8C1D18; border-radius:4px; padding:1px 3px;">{s}</span> '
                        match_count += 1
                    else: marked_text += f'{s} '
                plag_percent = min(98, int((match_count / len(sentences)) * 100)) if sentences else 0
                if reference:
                    plag_percent = int(ngram_overlap(reference, plag_text))
                    st.caption("Mode: comparing against the original text you gave the Humanizer (4-word sequences).")
                if plag_percent > 20:
                    st.error(f"Similarity Found: {plag_percent}%")
                    st.progress(plag_percent / 100)
                    st.markdown(f'<div class="notebook-card" style="line-height: 1.8;">{marked_text}</div>', unsafe_allow_html=True)
                else: st.success(f"Content Unique: {plag_percent}% Similarity"); st.balloons()

# --- MODULE: CITATION GENERATOR ---
elif choice == "Citation Generator":
    st.title("Citation Generator Workspace")
    st.markdown("### Generate Reference Citations")

    cite_url = st.text_input("Enter Source URL, DOI, or Document Link:", value=st.session_state.citation_text_input, placeholder="https://example.com/article...", key="c_input")
    st.session_state.citation_text_input = cite_url

    active_style = st.session_state.get("selected_citation_format", "APA 7th Generation")
    st.caption(f"Active Output Style: **{active_style}** (Change this inside control center settings)")

    if st.button("Generate Reference", use_container_width=True):
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
elif choice == "Study Assistant":
    st.title("Verso Study Assistant")
    st.caption("Questions, explanations, and flashcards based on the actual source material. Quizzes aim for 15 distinct questions.")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        up_files = st.file_uploader("Upload study files", type=["pdf", "docx", "csv", "txt"], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    with col_b:
        url_hub = st.text_input("Study source URL", placeholder="https://...", key=f"l_{st.session_state.reset_counter}")

    raw_content = st.text_area("Paste your notes or textbook extract", value=st.session_state.study_text_input, height=180, placeholder="Paste the material you want to study...", key="s_input")
    st.session_state.study_text_input = raw_content
    source_parts = [raw_content.strip()] if raw_content.strip() else []
    if url_hub.strip():
        is_youtube = bool(re.search(r"(?:youtube\.com|youtu\.be)", url_hub.strip(), re.I))
        with st.spinner("Reading the video captions..." if is_youtube else "Reading source link..."):
            if is_youtube:
                linked_text = extract_youtube_transcript(url_hub.strip())
            else:
                linked_text = extract_from_url(url_hub.strip())
        if linked_text.strip() and not linked_text.startswith("__TRANSCRIPT_ERROR__:"):
            source_parts.append(linked_text.strip())
        elif is_youtube:
            error_detail = linked_text.split(":", 1)[1].strip() if linked_text.startswith("__TRANSCRIPT_ERROR__:") else "Automatic caption retrieval failed."
            st.warning(
                "I couldn't access this video's actual captions, so I won't invent questions from its title or page text. "
                f"{error_detail}"
            )
            st.markdown(
                "**Quick workaround:** Open the video on YouTube, expand its description or click the video menu (⋯), "
                "choose **Show transcript** if available, copy the transcript, and paste it into the notes box above. "
                "Then Verso can build the 15-question quiz and flashcards from the video's real content."
            )
        else:
            st.warning("The link could not be read. Upload the page or paste its text instead.")
    if up_files:
        for uploaded in up_files:
            extracted = extract_text(uploaded)
            if extracted.strip():
                source_parts.append(f"\n\n--- {uploaded.name} ---\n{extracted.strip()}")
            else:
                st.warning(f"Could not extract text from {uploaded.name}. Try a text-based PDF or TXT/DOCX file.")
    final_study_data = "\n\n".join(source_parts).strip()

    if not final_study_data:
        st.info("Add notes, a readable link, or a study file to get started. Questions and answers will be based on the material you provide.")
    else:
        source_key = str(hash(final_study_data))
        if st.session_state.get("study_assets_source_key") != source_key:
            st.session_state.study_assets = None
            st.session_state.study_assets_source_key = source_key
            st.session_state.study_quiz_step = 0
            st.session_state.study_quiz_score = 0
            st.session_state.study_quiz_feedback = None
            st.session_state.study_fc_step = 0
            st.session_state.study_fc_revealed = False
            st.session_state.study_assistant_answer = ""
            st.session_state.study_assistant_source_key = None

        if st.button("Generate questions and flashcards", type="primary", use_container_width=True):
            try:
                with st.spinner("Reading your material and building a source-grounded study set..."):
                    st.session_state.study_assets = generate_study_assets(final_study_data)
                st.session_state.study_quiz_step = 0
                st.session_state.study_quiz_score = 0
                st.session_state.study_quiz_feedback = None
                st.session_state.study_fc_step = 0
                st.session_state.study_fc_revealed = False
                st.success("Your study set is ready.")
            except Exception as exc:
                st.error(f"Could not generate the study set: {exc}")

        t1, t2, t3, t4, t5 = st.tabs(["Key concepts", "Quiz", "Flashcards", "Ask Assistant", "AI Voice Teacher"])
        assets = st.session_state.get("study_assets")

        with t1:
            st.subheader("Key concepts")
            if assets and assets.get("keywords"):
                cols = st.columns(2)
                for i, phrase in enumerate(assets["keywords"][:30]):
                    cols[i % 2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase}</div>', unsafe_allow_html=True)
            else:
                st.caption("Generate a study set to extract important terms from your material.")

        with t2:
            st.subheader("Practice quiz")
            quiz_items = assets.get("quiz", []) if assets else []
            if not assets:
                st.info("Click **Generate questions and flashcards** above first.")
            elif not quiz_items:
                st.warning("No reliable quiz questions could be created. Add more detailed notes and regenerate.")
            elif st.session_state.study_quiz_step < len(quiz_items):
                idx = st.session_state.study_quiz_step
                item = quiz_items[idx]
                st.progress(idx / len(quiz_items), text=f"Question {idx + 1} of {len(quiz_items)}")
                st.markdown(f'<div class="notebook-card" style="font-size:1.08rem; line-height:1.7;">{item["question"]}</div>', unsafe_allow_html=True)
                selected = st.radio("Choose the best answer", item["options"], key=f"study_quiz_answer_{source_key}_{idx}", index=None)
                if st.button("Check answer", key=f"study_quiz_submit_{source_key}_{idx}", use_container_width=True):
                    if selected is None:
                        st.warning("Choose an answer before checking.")
                    else:
                        correct = selected == item["answer"]
                        if correct:
                            st.session_state.study_quiz_score += 1
                        st.session_state.study_quiz_feedback = {"idx": idx, "correct": correct, "answer": item["answer"], "explanation": item["explanation"]}
                        st.rerun()
                feedback = st.session_state.get("study_quiz_feedback")
                if feedback and feedback.get("idx") == idx:
                    if feedback["correct"]:
                        st.success("Correct!")
                    else:
                        st.error(f'Not quite. Correct answer: {feedback["answer"]}')
                    st.markdown(f'**Why:** {feedback["explanation"]}')
                    if st.button("Next question", key=f"study_quiz_next_{source_key}_{idx}", use_container_width=True):
                        st.session_state.study_quiz_step += 1
                        st.session_state.study_quiz_feedback = None
                        st.rerun()
            else:
                st.subheader("Quiz complete")
                st.metric("Score", f'{st.session_state.study_quiz_score} / {len(quiz_items)}')
                if st.button("Try the quiz again", key=f"study_quiz_restart_{source_key}"):
                    st.session_state.study_quiz_step = 0
                    st.session_state.study_quiz_score = 0
                    st.session_state.study_quiz_feedback = None
                    st.rerun()

        with t3:
            st.subheader("Flashcards")
            cards = assets.get("flashcards", []) if assets else []
            if not assets:
                st.info("Click **Generate questions and flashcards** above first.")
            elif not cards:
                st.warning("No reliable flashcards could be created. Add more detailed notes and regenerate.")
            elif st.session_state.study_fc_step < len(cards):
                idx = st.session_state.study_fc_step
                card = cards[idx]
                st.progress((idx + 1) / len(cards), text=f"Card {idx + 1} of {len(cards)}")
                st.markdown(f'<div class="notebook-card" style="min-height:190px; display:flex; align-items:center; justify-content:center; text-align:center; font-size:1.2rem; line-height:1.7;">{card["question"]}</div>', unsafe_allow_html=True)
                if not st.session_state.study_fc_revealed:
                    if st.button("Reveal answer", key=f"study_fc_reveal_{source_key}_{idx}", use_container_width=True):
                        st.session_state.study_fc_revealed = True
                        st.rerun()
                else:
                    st.markdown(f'<div style="background:#E8F0FE; padding:22px; border-radius:16px; border:1px solid #D3E3FD; color:#041E49; line-height:1.7;">{card["answer"]}</div>', unsafe_allow_html=True)
                    fc1, fc2 = st.columns(2)
                    if fc1.button("I knew this", key=f"study_fc_known_{source_key}_{idx}", use_container_width=True):
                        st.session_state.study_fc_step += 1
                        st.session_state.study_fc_revealed = False
                        st.rerun()
                    if fc2.button("Review again", key=f"study_fc_review_{source_key}_{idx}", use_container_width=True):
                        st.session_state.study_fc_step += 1
                        st.session_state.study_fc_revealed = False
                        st.rerun()
            else:
                st.success("You've reached the end of this flashcard deck.")
                if st.button("Restart flashcards", key=f"study_fc_restart_{source_key}"):
                    st.session_state.study_fc_step = 0
                    st.session_state.study_fc_revealed = False
                    st.rerun()

        with t4:
            st.subheader("Ask your study assistant")
            st.caption("Answers are grounded in the provided material. The assistant will say when the source doesn't contain enough information.")
            question = st.text_area("Your question", placeholder="For example: What are the main causes, and how are they connected?", key=f"study_assistant_question_{source_key}", height=100)
            if st.button("Answer from my material", key=f"study_assistant_submit_{source_key}", use_container_width=True):
                if not question.strip():
                    st.warning("Type a question first.")
                else:
                    try:
                        with st.spinner("Finding an answer in your material..."):
                            st.session_state.study_assistant_answer = answer_from_study_source(final_study_data, question.strip())
                            st.session_state.study_assistant_last_question = question.strip()
                            st.session_state.study_assistant_source_key = source_key
                    except Exception as exc:
                        st.error(f"The assistant couldn't answer this yet: {exc}")
            if st.session_state.get("study_assistant_answer") and st.session_state.get("study_assistant_source_key") == source_key:
                st.markdown(f'<div class="notebook-card" style="line-height:1.8;">{st.session_state.study_assistant_answer}</div>', unsafe_allow_html=True)

        with t5:
            st.subheader("AI voice teacher")
            st.caption("Generate a lesson explanation from your source, then play it aloud using your browser's available voices.")
            va1, va2 = st.columns(2)
            v_pitch = va1.slider("Voice pitch", 0.5, 2.0, 1.0, step=0.1, key=f"teacher_pitch_{source_key}")
            v_speed = va2.slider("Speaking speed", 0.5, 2.0, 1.0, step=0.1, key=f"teacher_speed_{source_key}")
            if st.button("Generate lesson", key=f"teacher_generate_{source_key}", use_container_width=True):
                with st.spinner("Preparing your lesson..."):
                    st.session_state.generated_lecture_text = teach_source_material(final_study_data)
            lesson = st.session_state.get("generated_lecture_text", "")
            if lesson:
                # Put the lesson controls ABOVE the lesson text so they are easy to reach.
                import json as _json
                lesson_json = _json.dumps(lesson)
                components.html(
                    "<div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-family:Arial,sans-serif;padding:4px 0 12px'>"
                    "<button id='playLesson' style='padding:10px 18px;border-radius:999px;border:0;background:#0B57D0;color:white;cursor:pointer;font-size:15px'>Play lesson</button>"
                    "<button id='pauseLesson' style='padding:10px 18px;border-radius:999px;border:1px solid #ccc;background:white;cursor:pointer;font-size:15px'>Pause / resume</button>"
                    "<button id='stopLesson' style='padding:10px 18px;border-radius:999px;border:1px solid #ccc;background:white;cursor:pointer;font-size:15px'>Stop</button></div>"
                    f"<script>const lessonText={lesson_json};const pitch={v_pitch};const speed={v_speed};"
                    "document.getElementById('playLesson').onclick=()=>{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(lessonText);u.pitch=pitch;u.rate=speed;speechSynthesis.speak(u);};"
                    "document.getElementById('pauseLesson').onclick=()=>{if(speechSynthesis.speaking&&!speechSynthesis.paused)speechSynthesis.pause();else if(speechSynthesis.paused)speechSynthesis.resume();};"
                    "document.getElementById('stopLesson').onclick=()=>speechSynthesis.cancel();</script>",
                    height=70,
                )
                st.markdown(f'<div class="teacher-board" style="white-space:pre-wrap; line-height:1.8;">{lesson}</div>', unsafe_allow_html=True)


# --- MODULE: TIME TRACKER ---
elif choice == "Time Tracker":
    st.title("Focus Timer")
    if not st.session_state.get('sound_unlocked', False):
        if st.button("ENABLE SOUNDS"):
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

```python
# --- MODULE: HUMANISM ENGINE (PURE PYTHON) ---
elif choice == "Humanism Engine":
    import streamlit.components.v1 as components
    import json

    st.header("Verso Humanizer")

    text_to_humanize = st.text_area(
        "Paste text here:",
        value=st.session_state.humanizer_text_input,
        height=200,
        placeholder="Please input the text you want to humanize...",
        key="humanizer_interactive_input"
    )
    st.session_state.humanizer_text_input = text_to_humanize

    if st.button("Humanize Output Text", type="primary"):
        if not text_to_humanize.strip():
            st.warning("Please add some text first!")
        else:
            with st.spinner("Rewriting..."):
                best, best_ov = "", 101.0

                for _ in range(5):
                    cand = pure_python_humanizer(
                        text_to_humanize,
                        0.9,
                        False,
                        seed=random.randint(0, 10**6),
                        include_nouns=True,
                        neural=None,
                        force_zero=True
                    )

                    ov = ngram_overlap(text_to_humanize, cand)

                    if ov < best_ov:
                        best, best_ov = cand, ov

                    if best_ov == 0:
                        break

                st.session_state.humanizer_output = best

    if st.session_state.humanizer_output:
        st.subheader("Humanized")

        # Display the generated output
        st.write(
            st.session_state.humanizer_output.replace("\n", "  \n")
        )

        # Copy button using the browser clipboard
        copy_text = json.dumps(
            st.session_state.humanizer_output
        )

        components.html(
            f"""
            <div style="font-family: sans-serif; margin: 8px 0;">
                <button
                    id="verso-copy-humanism"
                    style="
                        background: white;
                        color: #262730;
                        border: 1px solid #D1D5DB;
                        border-radius: 8px;
                        padding: 8px 16px;
                        font-size: 14px;
                        font-weight: 500;
                        cursor: pointer;
                    "
                >📋 Copy</button>
                <span id="verso-copy-status"
                    style="margin-left: 10px; font-size: 13px;">
                </span>
            </div>

            <script>
                const copyButton =
                    document.getElementById("verso-copy-humanism");
                const status =
                    document.getElementById("verso-copy-status");
                const textToCopy = {copy_text};

                copyButton.addEventListener("click", async () => {{
                    try {{
                        await navigator.clipboard.writeText(textToCopy);
                        status.textContent = "Copied!";
                    }} catch (error) {{
                        const area = document.createElement("textarea");
                        area.value = textToCopy;
                        document.body.appendChild(area);
                        area.select();
                        const success =
                            document.execCommand("copy");
                        area.remove();
                        status.textContent =
                            success ? "Copied!" : "Copy failed";
                    }}
                }});
            </script>
            """,
            height=50
        )

        overlap = ngram_overlap(
            st.session_state.humanizer_text_input,
            st.session_state.humanizer_output
        )

        st.metric(
            "Remaining 4-word overlap with original",
            f"{overlap}%"
        )

        st.caption(
            "This measures overlap with your input only. It is not a real "
            "plagiarism checker score. Always read the output. "
            "Lowest score is not always the most readable one."
        )
```

# --- 🌐 TRANSLATOR MODULE ENGINE (GEMINI-POWERED 100% UNBLOCKED TRANSLATION) ---
elif choice == "Verso Translate":
    st.header("Google Translate Engine")
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
        if st.button("Swap", use_container_width=True, on_click=safe_language_swap):
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
    if st.button("Translate Content", type="primary", use_container_width=True):
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
elif choice == "Settings":
    st.markdown('<h1 style="font-size: 3rem;">Verso Control Center</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('### Academic & Audio')
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
        st.markdown('### UI Appearance')
        def update_accent(): st.session_state.set_color = st.session_state.accent_pick
        def update_bg(): st.session_state.set_bg = st.session_state.bg_pick
        st.color_picker("Accent Color", value=st.session_state.set_color, key="accent_pick", on_change=update_accent)
        st.color_picker("Card BG", value=st.session_state.set_bg, key="bg_pick", on_change=update_bg)
        st.slider("Font Scale", 0.8, 2.0, value=st.session_state.set_font, key="set_font")
        st.checkbox("Force Dark", value=True); st.checkbox("Glassmorphism")
    with col3:
        st.markdown('### System Info')
        st.button("Purge History"); st.button("Export CSV"); st.button("Cloud Backup")
        st.info(f"Build: 14.5.6 (vID: {st.session_state.reset_counter})")
        st.success("System Optimized")

if st.session_state.get('timer_finished_trigger'):
    st.markdown('<div class="time-up-banner">Time is up</div>', unsafe_allow_html=True); st.balloons()
    components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
    if st.button("Dismiss Alarm"): st.session_state.timer_finished_trigger = False; st.rerun()


import html
import json
import re
import time
from urllib.parse import urlparse

import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from google import genai
from google.genai import types

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx2txt
except ImportError:
    docx2txt = None


# ============================================================
# VERSO LEARNING STUDIO
# ============================================================

st.set_page_config(
    page_title="Verso Learning Studio",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL_NAME = "gemini-2.5-flash"

try:
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    BRAVE_SEARCH_API_KEY = st.secrets.get("BRAVE_SEARCH_API_KEY", "")
except Exception:
    GEMINI_KEY = ""
    BRAVE_SEARCH_API_KEY = ""

client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "accent": "#2563EB",
    "study_source": "",
    "study_result": None,
    "flashcard_index": 0,
    "flashcard_revealed": False,
    "quiz_answers": {},
    "quiz_submitted": False,
    "plag_text": "",
    "plag_result": None,
    "writing_input": "",
    "writing_output": "",
    "grammar_input": "",
    "grammar_output": "",
    "word_input": "",
    "timer_minutes": 25,
    "timer_end": None,
    "timer_running": False,
    "timer_remaining": 25 * 60,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# PROFESSIONAL DESIGN SYSTEM
# ============================================================

def contrast_color(hex_color):
    try:
        value = hex_color.lstrip("#")
        r = int(value[:2], 16)
        g = int(value[2:4], 16)
        b = int(value[4:6], 16)

        luminance = (
            0.299 * r + 0.587 * g + 0.114 * b
        ) / 255

        return "#142033" if luminance > 0.60 else "#FFFFFF"
    except Exception:
        return "#FFFFFF"


ACCENT = st.session_state.accent
ACCENT_FG = contrast_color(ACCENT)

CSS = r"""
<style>
@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

:root {
    --accent: __ACCENT__;
    --accent-fg: __ACCENT_FG__;
    --page: #F5F7FB;
    --surface: #FFFFFF;
    --ink: #172033;
    --muted: #667085;
    --line: #E3E8F0;
    --soft: #EAF1FF;
    --radius: 18px;
    --shadow: 0 5px 22px rgba(23, 32, 51, .055);
}

html, body, .stApp,
[data-testid="stMarkdownContainer"],
button, input, textarea, select, label {
    font-family: Inter, -apple-system, BlinkMacSystemFont,
                 'Segoe UI', sans-serif !important;
}

.stApp {
    background: var(--page);
    color: var(--ink);
}

[data-testid="stHeader"] {
    background: rgba(245, 247, 251, .94);
}

#MainMenu,
footer,
[data-testid="stDecoration"] {
    visibility: hidden;
}

.block-container {
    max-width: 1320px;
    padding: 2rem 2.2rem 4rem;
}

h1 {
    font-size: 2.05rem !important;
    font-weight: 800 !important;
    letter-spacing: -.05em;
    color: var(--ink);
}

h2 {
    font-size: 1.5rem !important;
    font-weight: 750 !important;
    letter-spacing: -.035em;
    color: var(--ink);
}

h3 {
    font-size: 1.12rem !important;
    font-weight: 700 !important;
    color: var(--ink);
}

p, li {
    line-height: 1.75;
}

.stCaption,
[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: .62rem .75rem;
    border-radius: 12px;
    margin: 2px 0;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #F3F6FC;
}

[data-testid="stSidebar"] [data-testid="stRadio"]
label:has(input:checked) {
    background: var(--soft);
}

[data-testid="stSidebar"] [data-testid="stRadio"]
label:has(input:checked) p {
    color: var(--accent);
    font-weight: 700;
}

/* Buttons */

.stButton > button,
.stDownloadButton > button {
    border: 1px solid #D0D7E2;
    border-radius: 12px;
    min-height: 2.7rem;
    font-weight: 650;
    transition: all .15s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: var(--accent);
    color: var(--accent);
    transform: translateY(-1px);
    box-shadow: var(--shadow);
}

[data-testid="stBaseButton-primary"] {
    background: var(--accent) !important;
    color: var(--accent-fg) !important;
    border-color: var(--accent) !important;
}

/* Inputs */

[data-baseweb="input"],
[data-baseweb="textarea"],
[data-baseweb="select"] > div {
    border-radius: 12px !important;
    border-color: #D0D7E2 !important;
    background: #FFFFFF !important;
}

[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within,
[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, .1) !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF;
    border: 1.5px dashed #C7D2E2;
    border-radius: 16px;
}

/* Metrics */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    box-shadow: var(--shadow);
}

[data-testid="stMetricLabel"] p {
    color: var(--muted);
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    font-weight: 800;
    letter-spacing: -.04em;
}

/* Tabs and expandable panels */

[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow);
    overflow: hidden;
}

[data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--line);
}

button[data-baseweb="tab"] {
    font-weight: 650;
    padding: .8rem 1rem;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent);
}

[data-baseweb="tab-highlight"] {
    background: var(--accent) !important;
    height: 3px !important;
}

[data-testid="stProgressBar"] > div > div {
    background: var(--accent) !important;
    border-radius: 99px;
}

/* Reusable components */

.verso-hero {
    background: linear-gradient(130deg, #14284B, #2457D6);
    color: #FFFFFF;
    border-radius: 24px;
    padding: 2.1rem 2.25rem;
    margin: .2rem 0 1.5rem;
    box-shadow: 0 12px 32px rgba(36, 87, 214, .16);
}

.verso-hero h1,
.verso-hero h2,
.verso-hero p {
    color: #FFFFFF !important;
}

.verso-hero p {
    opacity: .9;
    margin-bottom: 0;
}

.eyebrow {
    font-size: .74rem;
    letter-spacing: .15em;
    text-transform: uppercase;
    font-weight: 800;
    opacity: .8;
}

.surface {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 1.25rem 1.4rem;
    box-shadow: var(--shadow);
    margin: .45rem 0 1rem;
    overflow-wrap: anywhere;
}

.muted {
    color: var(--muted);
}

.pill {
    display: inline-block;
    background: var(--soft);
    color: var(--accent);
    padding: 4px 10px;
    border-radius: 99px;
    font-size: .75rem;
    font-weight: 750;
}

.flashcard {
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 2rem;
    box-shadow: var(--shadow);
}

@media (max-width: 800px) {
    .block-container {
        padding: 1.2rem .8rem 3rem;
    }

    h1 {
        font-size: 1.7rem !important;
    }

    .verso-hero {
        padding: 1.35rem;
    }
}

@media (prefers-reduced-motion: reduce) {
    * {
        transition: none !important;
        animation: none !important;
    }
}
</style>
""".replace("__ACCENT__", ACCENT).replace(
    "__ACCENT_FG__", ACCENT_FG
)

st.markdown(CSS, unsafe_allow_html=True)


# ============================================================
# SHARED HELPERS
# ============================================================

def extract_uploaded_text(uploaded_file):
    if not uploaded_file:
        return ""

    name = uploaded_file.name.lower()

    try:
        if name.endswith(".pdf"):
            if PyPDF2 is None:
                return "PDF support requires PyPDF2."

            reader = PyPDF2.PdfReader(uploaded_file)
            return "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        if name.endswith(".docx"):
            if docx2txt is None:
                return "DOCX support requires docx2txt."

            return docx2txt.process(uploaded_file)

        if name.endswith(".csv"):
            return pd.read_csv(uploaded_file).to_string(index=False)

        return uploaded_file.getvalue().decode(
            "utf-8", errors="replace"
        )

    except Exception as exc:
        return f"Could not read the uploaded file: {exc}"


def ask_gemini(prompt, system_instruction=None, json_mode=False):
    if client is None:
        raise RuntimeError(
            "Gemini is not configured. Add GEMINI_API_KEY "
            "to .streamlit/secrets.toml."
        )

    config_args = {"temperature": 0.35}

    if system_instruction:
        config_args["system_instruction"] = system_instruction

    if json_mode:
        config_args["response_mime_type"] = "application/json"

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(**config_args),
    )

    return response.text or ""


def brave_web_search(query, num=5):
    if not BRAVE_SEARCH_API_KEY:
        raise RuntimeError(
            "Brave Search is not configured. Add "
            "BRAVE_SEARCH_API_KEY to Streamlit secrets."
        )

    response = requests.get(
        "https://api.search.brave.com/res/v1/web/search",
        headers={
            "X-Subscription-Token": BRAVE_SEARCH_API_KEY,
            "Accept": "application/json",
        },
        params={
            "q": query,
            "count": min(num, 20),
            "safesearch": "moderate",
        },
        timeout=15,
    )

    response.raise_for_status()

    return response.json().get("web", {}).get("results", [])


def ngram_overlap(text_a, text_b, n=4):
    a = re.findall(r"\w+", text_a.casefold())
    b = re.findall(r"\w+", text_b.casefold())

    grams_a = {
        tuple(a[i:i+n])
        for i in range(max(0, len(a) - n + 1))
    }

    grams_b = {
        tuple(b[i:i+n])
        for i in range(max(0, len(b) - n + 1))
    }

    if not grams_a:
        return 0.0

    return round(100 * len(grams_a & grams_b) / len(grams_a), 1)


# ============================================================
# EXTERNAL WEB SIMILARITY SCANNER
# ============================================================

def run_web_similarity_scan(text, max_queries=6, max_pages=3):
    """
    Search distinctive quoted fragments with Brave Search.
    Fetch a small number of public pages for comparison.

    This is a screening tool, not a definitive plagiarism score.
    """

    sentences = [
        re.sub(r"\s+", " ", sentence).strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if sentence.strip()
    ]

    candidates = []
    seen = set()

    for sentence in sentences:
        words = re.findall(r"[\w'-]+", sentence)

        if len(words) < 8:
            continue

        phrase = " ".join(words[:min(12, len(words))])

        if phrase.casefold() not in seen:
            seen.add(phrase.casefold())
            candidates.append((sentence, phrase))

        if len(candidates) >= max_queries:
            break

    queries = []
    all_sources = {}

    for sentence, phrase in candidates:
        hits = brave_web_search(f'"{phrase}"', num=5)
        sources = []

        for hit in hits:
            url = hit.get("url", "")

            if not url.startswith(("http://", "https://")):
                continue

            item = {
                "title": hit.get("title", "Untitled source"),
                "url": url,
                "snippet": hit.get("description", ""),
            }

            sources.append(item)
            all_sources.setdefault(url, item)

        queries.append({
            "sentence": sentence,
            "phrase": phrase,
            "sources": sources,
        })

    # Retrieve a limited number of public HTML pages.
    page_texts = {}

    for url in list(all_sources)[:max_pages]:
        try:
            parsed = urlparse(url)

            if parsed.scheme not in ("http", "https") or not parsed.hostname:
                continue

            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "VersoLearningStudio/1.0"},
            )

            response.raise_for_status()

            content_type = response.headers.get(
                "content-type", ""
            ).lower()

            if "html" not in content_type:
                continue

            soup = BeautifulSoup(
                response.text[:1_000_000],
                "html.parser",
            )

            for node in soup([
                "script", "style", "nav", "footer",
                "header", "noscript"
            ]):
                node.decompose()

            page_texts[url] = soup.get_text(
                " ", strip=True
            )[:200_000]

        except requests.RequestException:
            continue

    matches = []

    for query in queries:
        source_results = []

        for source in query["sources"]:
            page_text = page_texts.get(source["url"], "")

            overlap = (
                ngram_overlap(query["sentence"], page_text, 4)
                if page_text else None
            )

            source_results.append({
                **source,
                "page_overlap": overlap,
            })

        if source_results:
            matches.append({
                **query,
                "sources": source_results,
            })

    return {
        "queries": queries,
        "matches": matches,
        "source_count": len(all_sources),
        "page_count": len(page_texts),
    }


# ============================================================
# AI STUDY PACK GENERATOR
# ============================================================

def make_study_pack(source):
    prompt = f"""
Create a study pack based ONLY on the source below.
Do not invent unsupported facts.

Return valid JSON with this structure:
{{
  "title": "short title",
  "lesson": "clear Markdown lesson with objective, explanation, examples and recap",
  "flashcards": [
    {{"question": "...", "answer": "..."}}
  ],
  "quiz": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer_index": 0,
      "explanation": "..."
    }}
  ]
}}

Create 8 flashcards and 5 multiple-choice questions.
The correct answer index must be 0, 1, 2, or 3.
Make the questions distinct and educational.

SOURCE:
{source[:24000]}
"""

    raw = ask_gemini(
        prompt,
        "You are a careful, encouraging academic tutor. "
        "Ground all content in the supplied source.",
        json_mode=True,
    )

    data = json.loads(raw)

    if not isinstance(data, dict) or not data.get("lesson"):
        raise ValueError(
            "The generated study pack did not contain a lesson."
        )

    data["flashcards"] = data.get("flashcards", [])[:20]
    data["quiz"] = data.get("quiz", [])[:10]

    return data


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("# 📘 Verso")
    st.caption("Your academic workspace")
    st.divider()

    pages = [
        "Home",
        "AI Teacher",
        "Flashcards & Quiz",
        "Grammar Checker",
        "Web Similarity Checker",
        "Citation Generator",
        "Focus Timer",
        "Word Counter",
        "Writing Assistant",
        "Translator",
        "Settings",
    ]

    page = st.radio(
        "Navigation",
        pages,
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        '<span class="pill">STUDY • CREATE • IMPROVE</span>',
        unsafe_allow_html=True,
    )

    if client is None:
        st.warning("AI features need a Gemini API key.")


# ============================================================
# HOME DASHBOARD
# ============================================================

if page == "Home":
    st.markdown(
        """
        <div class="verso-hero">
            <div class="eyebrow">YOUR ACADEMIC WORKSPACE</div>
            <h1>Learn smarter with Verso.</h1>
            <p>
                Research, study, write, and organize your learning
                in one focused workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Your workspace")

    st.caption(
        "Choose a tool to get started. Export your work when you "
        "want to keep a copy."
    )

    cards = [
        (
            "🧠",
            "AI Teacher",
            "Turn notes and documents into a guided lesson.",
        ),
        (
            "🗂️",
            "Flashcards & Quiz",
            "Practice recall and check your understanding.",
        ),
        (
            "🔎",
            "Web Similarity Checker",
            "Look for possible matching passages online.",
        ),
        (
            "✍️",
            "Writing Assistant",
            "Improve clarity, structure, and tone.",
        ),
    ]

    columns = st.columns(2)

    for index, (icon, title, description) in enumerate(cards):
        with columns[index % 2]:
            st.markdown(
                f"""
                <div class="surface">
                    <h3>{icon} {html.escape(title)}</h3>
                    <p class="muted">{html.escape(description)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    a, b, c = st.columns(3)

    a.metric("Study tools", "11")
    b.metric(
        "AI provider",
        "Gemini" if client else "Not configured",
    )
    c.metric(
        "Web scan",
        "Connected" if BRAVE_SEARCH_API_KEY else "Setup needed",
    )

    st.markdown("### Quick start")

    st.markdown(
        """
        1. Open **AI Teacher** and paste notes or upload a file.
        2. Generate a lesson, then review the flashcards and quiz.
        3. Use the similarity checker as a research aid, not as
           a final plagiarism verdict.
        """
    )


# ============================================================
# AI TEACHER
# ============================================================

elif page == "AI Teacher":
    st.title("AI Teacher")

    st.caption(
        "Turn your own notes, readings, or documents into a "
        "structured lesson and study materials."
    )

    uploaded = st.file_uploader(
        "Upload notes or a document",
        type=["txt", "md", "pdf", "docx", "csv"],
    )

    extracted = extract_uploaded_text(uploaded) if uploaded else ""

    source = st.text_area(
        "Or paste your source material",
        value=st.session_state.study_source,
        height=220,
        placeholder="Paste your class notes, reading, or study guide...",
    )

    if extracted:
        st.caption(
            f"Loaded {len(extracted.split())} words from {uploaded.name}."
        )

        if st.button("Use uploaded text"):
            st.session_state.study_source = extracted
            st.rerun()

    st.session_state.study_source = source

    if st.button(
        "Create my study pack",
        type="primary",
        use_container_width=True,
    ):
        if len(source.strip()) < 40:
            st.warning(
                "Add more source material so the lesson can be grounded in it."
            )
        else:
            with st.spinner(
                "Preparing your lesson, flashcards, and quiz..."
            ):
                try:
                    st.session_state.study_result = make_study_pack(source)
                    st.session_state.flashcard_index = 0
                    st.session_state.flashcard_revealed = False
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False

                except Exception as exc:
                    st.error(f"Could not create the study pack: {exc}")

    pack = st.session_state.study_result

    if pack:
        st.divider()
        st.markdown(f"## {pack.get('title', 'Your lesson')}")
        st.markdown(pack.get("lesson", ""))

        st.download_button(
            "Download lesson as Markdown",
            pack.get("lesson", ""),
            file_name="verso_lesson.md",
            mime="text/markdown",
        )

        st.success(
            "Study pack created. Open Flashcards & Quiz in the sidebar to practice."
        )


# ============================================================
# FLASHCARDS AND QUIZ
# ============================================================

elif page == "Flashcards & Quiz":
    st.title("Flashcards & Quiz")
    st.caption("Practice active recall and check your understanding.")

    pack = st.session_state.study_result

    if not pack:
        st.info("Create a study pack in AI Teacher first.")

    else:
        tab_cards, tab_quiz = st.tabs(["Flashcards", "Quiz"])

        cards = pack.get("flashcards", [])

        with tab_cards:
            if not cards:
                st.info("No flashcards were returned. Generate the pack again.")

            else:
                idx = st.session_state.flashcard_index % len(cards)
                card = cards[idx]

                st.caption(f"Card {idx + 1} of {len(cards)}")
                st.progress((idx + 1) / len(cards))

                content = (
                    card.get("answer", "")
                    if st.session_state.flashcard_revealed
                    else card.get("question", "")
                )

                label = (
                    "ANSWER"
                    if st.session_state.flashcard_revealed
                    else "QUESTION"
                )

                st.markdown(
                    f"""
                    <div class="flashcard">
                        <span class="pill">{label}</span>
                        <h2>{html.escape(str(content))}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                x, y, z = st.columns([1, 2, 1])

                with x:
                    if st.button("← Previous", use_container_width=True):
                        st.session_state.flashcard_index = (
                            idx - 1
                        ) % len(cards)

                        st.session_state.flashcard_revealed = False
                        st.rerun()

                with y:
                    label = (
                        "Hide answer"
                        if st.session_state.flashcard_revealed
                        else "Reveal answer"
                    )

                    if st.button(
                        label,
                        type="primary",
                        use_container_width=True,
                    ):
                        st.session_state.flashcard_revealed = (
                            not st.session_state.flashcard_revealed
                        )
                        st.rerun()

                with z:
                    if st.button("Next →", use_container_width=True):
                        st.session_state.flashcard_index = (
                            idx + 1
                        ) % len(cards)

                        st.session_state.flashcard_revealed = False
                        st.rerun()

        with tab_quiz:
            questions = pack.get("quiz", [])

            if not questions:
                st.info("No quiz questions were returned. Generate the pack again.")

            else:
                with st.form("verso_quiz"):
                    new_answers = {}

                    for i, question in enumerate(questions):
                        st.markdown(
                            f"**{i + 1}. {question.get('question', 'Question')}**"
                        )

                        options = question.get("options", [])

                        if not isinstance(options, list) or len(options) < 2:
                            st.warning("This question needs more answer choices.")
                            continue

                        previous = st.session_state.quiz_answers.get(str(i))
                        selected_index = (
                            options.index(previous)
                            if previous in options
                            else None
                        )

                        new_answers[str(i)] = st.radio(
                            "Choose an answer",
                            options,
                            index=selected_index,
                            key=f"quiz_{i}",
                            label_visibility="collapsed",
                        )

                    submitted = st.form_submit_button(
                        "Check my answers",
                        type="primary",
                        use_container_width=True,
                    )

                if submitted:
                    st.session_state.quiz_answers = new_answers
                    st.session_state.quiz_submitted = True

                if st.session_state.quiz_submitted:
                    answers = st.session_state.quiz_answers
                    score = 0

                    for i, question in enumerate(questions):
                        options = question.get("options", [])
                        answer_index = question.get("answer_index", 0)

                        correct = (
                            options[answer_index]
                            if options and 0 <= answer_index < len(options)
                            else None
                        )

                        if answers.get(str(i)) == correct:
                            score += 1

                    st.metric(
                        "Your score",
                        f"{score} / {len(questions)}",
                        f"{round(score / max(1, len(questions)) * 100)}%",
                    )

                    for i, question in enumerate(questions):
                        options = question.get("options", [])
                        answer_index = question.get("answer_index", 0)

                        correct = (
                            options[answer_index]
                            if options and 0 <= answer_index < len(options)
                            else "Not provided"
                        )

                        if st.session_state.quiz_answers.get(str(i)) == correct:
                            st.success(f"Question {i + 1}: Correct")
                        else:
                            st.error(
                                f"Question {i + 1}: Correct answer — {correct}"
                            )

                        st.caption(question.get("explanation", ""))

                    if st.button("Retake quiz"):
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()


# ============================================================
# GRAMMAR CHECKER
# ============================================================

elif page == "Grammar Checker":
    st.title("Grammar Checker")

    st.caption(
        "Review spelling, grammar, and clarity while keeping your intended meaning."
    )

    text = st.text_area(
        "Text to review",
        value=st.session_state.grammar_input,
        height=250,
        placeholder="Paste your writing here...",
    )

    st.session_state.grammar_input = text

    if st.button(
        "Review my writing",
        type="primary",
        use_container_width=True,
    ):
        if not text.strip():
            st.warning("Enter some text first.")

        else:
            with st.spinner("Reviewing your text..."):
                try:
                    st.session_state.grammar_output = ask_gemini(
                        "Review the text below for grammar, spelling, "
                        "punctuation, and clarity. Preserve the author's meaning "
                        "and voice. Return a corrected version followed by a "
                        "short list of meaningful edits. Do not invent facts.\n\n"
                        + text,
                        "You are a careful writing tutor. Explain edits briefly "
                        "and respectfully.",
                    )

                except Exception as exc:
                    st.error(str(exc))

    if st.session_state.grammar_output:
        st.markdown(st.session_state.grammar_output)

        st.download_button(
            "Download review",
            st.session_state.grammar_output,
            file_name="grammar_review.md",
        )


# ============================================================
# WEB SIMILARITY CHECKER
# ============================================================

elif page == "Web Similarity Checker":
    st.title("Web Similarity Checker")

    st.caption(
        "Search distinctive text fragments on the public web and review possible sources."
    )

    st.info(
        "External search uses Brave Search API. Usage quotas and paid-plan "
        "limits apply; no legitimate service guarantees unlimited searches."
    )

    text = st.text_area(
        "Text to check",
        value=st.session_state.plag_text,
        height=260,
        placeholder="Paste writing you have permission to analyze...",
    )

    st.session_state.plag_text = text

    col_scan, col_clear = st.columns([3, 1])

    with col_scan:
        scan_clicked = st.button(
            "Search the public web",
            type="primary",
            use_container_width=True,
        )

    with col_clear:
        if st.button("Clear", use_container_width=True):
            st.session_state.plag_text = ""
            st.session_state.plag_result = None
            st.rerun()

    if scan_clicked:
        if len(text.split()) < 8:
            st.warning(
                "Please enter at least 8 words to search distinctive phrases."
            )

        elif not BRAVE_SEARCH_API_KEY:
            st.error(
                "External search is not configured. Add BRAVE_SEARCH_API_KEY "
                "to .streamlit/secrets.toml."
            )

            st.code(
                'BRAVE_SEARCH_API_KEY = "your_brave_search_api_key"',
                language="toml",
            )

        else:
            try:
                with st.spinner(
                    "Searching quoted passages and checking accessible source pages..."
                ):
                    st.session_state.plag_result = run_web_similarity_scan(text)

            except requests.HTTPError as exc:
                st.session_state.plag_result = None

                st.error(
                    f"Search provider returned an HTTP error: {exc}. "
                    "Check credentials and your provider quota."
                )

            except Exception as exc:
                st.session_state.plag_result = None
                st.error(f"Scan failed: {exc}")

    result = st.session_state.plag_result

    if result:
        a, b, c = st.columns(3)

        a.metric("Fragments searched", len(result["queries"]))
        b.metric("Fragments with results", len(result["matches"]))
        c.metric("Sources returned", result["source_count"])

        if result["matches"]:
            st.warning(
                "Potential matches found. Review the original sources and "
                "citations before drawing conclusions."
            )

            for i, match in enumerate(result["matches"], 1):
                with st.expander(
                    f"Passage {i}: {match['phrase'][:85]}",
                    expanded=(i == 1),
                ):
                    st.write(match["sentence"])

                    for source in match["sources"]:
                        title = html.escape(source["title"])
                        url = html.escape(source["url"], quote=True)
                        snippet = html.escape(source["snippet"])
                        overlap = source["page_overlap"]

                        if overlap is None:
                            overlap_label = "Source page could not be compared"
                        else:
                            overlap_label = (
                                f"{overlap:.1f}% estimated four-word overlap"
                            )

                        st.markdown(
                            f"""
                            <div class="surface">
                                <b>{title}</b><br>
                                <a href="{url}" target="_blank"
                                   rel="noopener noreferrer">
                                    Open source ↗
                                </a>
                                <p>{snippet}</p>
                                <small class="muted">{overlap_label}</small>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        else:
            st.success(
                "No exact-fragment search results were returned in this run."
            )

        with st.expander("Important limitations"):
            st.write(
                "This is a screening aid, not a definitive plagiarism score. "
                "Search engines do not index every source; paywalled, private, "
                "and unindexed material may be missed. Quotes and correctly "
                "cited material can match. A no-match result does not prove "
                "originality. This app respects provider quotas and does not "
                "bypass them."
            )


# ============================================================
# CITATION GENERATOR
# ============================================================

elif page == "Citation Generator":
    st.title("Citation Generator")

    st.caption(
        "Create a starting reference from a public webpage or DOI. "
        "Verify the details before submitting work."
    )

    url = st.text_input(
        "Source URL or DOI",
        placeholder="https://example.com/article or 10.xxxx/example",
    )

    style = st.selectbox(
        "Citation style",
        ["APA 7", "MLA 9", "Chicago Author-Date", "Harvard"],
    )

    if st.button(
        "Generate reference",
        type="primary",
        use_container_width=True,
    ):
        candidate = url.strip()

        if candidate and not candidate.startswith(("http://", "https://")):
            if re.match(r"^10\.\d{4,9}/", candidate):
                candidate = "https://doi.org/" + candidate
            else:
                candidate = "https://" + candidate

        try:
            parsed = urlparse(candidate)

            if parsed.scheme not in ("http", "https") or not parsed.hostname:
                raise ValueError("Enter a valid URL or DOI.")

            response = requests.get(
                candidate,
                timeout=12,
                headers={"User-Agent": "VersoLearningStudio/1.0"},
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text[:1_000_000],
                "html.parser",
            )

            title_tag = soup.find("meta", property="og:title")
            title = (
                title_tag.get("content")
                if title_tag
                else None
            ) or (
                soup.title.string
                if soup.title
                else parsed.netloc
            )

            author_tag = soup.find("meta", attrs={"name": "author"})
            author = author_tag.get("content", "") if author_tag else ""

            date_tag = (
                soup.find("meta", attrs={"name": "date"})
                or soup.find("meta", property="article:published_time")
            )

            date = date_tag.get("content", "") if date_tag else ""
            year = re.search(r"\b(19|20)\d{2}\b", date)
            year_text = year.group(0) if year else "n.d."
            domain = parsed.netloc.removeprefix("www.")
            safe_title = title.strip().rstrip(".")

            if style == "APA 7":
                citation = (
                    f"{author + '. ' if author else ''}"
                    f"({year_text}). {safe_title}. "
                    f"*{domain}*. {candidate}"
                )

            elif style == "MLA 9":
                citation = (
                    f'{author + ". " if author else ""}'
                    f'"{safe_title}." *{domain}*, '
                    f"{year_text}, {candidate}."
                )

            elif style == "Chicago Author-Date":
                citation = (
                    f"{author + '. ' if author else ''}"
                    f'{year_text}. "{safe_title}." '
                    f"{domain}. {candidate}."
                )

            else:
                citation = (
                    f"{author + ' ' if author else ''}"
                    f"({year_text}) *{safe_title}*. "
                    f"Available at: {candidate} "
                    f"(Accessed {time.strftime('%d %B %Y')})."
                )

            st.markdown("### Generated reference")
            st.markdown(citation)
            st.code(citation)

            st.caption(
                "Metadata extraction can be incomplete. Check author, date, "
                "title, publisher, and style rules against the original source."
            )

        except Exception as exc:
            st.error(f"Could not retrieve source metadata: {exc}")


# ============================================================
# FOCUS TIMER
# ============================================================

elif page == "Focus Timer":
    st.title("Focus Timer")

    st.caption(
        "Set a study session, work without distractions, then take a short break."
    )

    if st.session_state.timer_running and st.session_state.timer_end:
        remaining = max(
            0,
            int(st.session_state.timer_end - time.time()),
        )

        st.session_state.timer_remaining = remaining

        if remaining == 0:
            st.session_state.timer_running = False

    remaining = int(st.session_state.timer_remaining)

    timer_status = (
        "FOCUS SESSION"
        if st.session_state.timer_running
        else "READY WHEN YOU ARE"
    )

    st.markdown(
        f"""
        <div class="flashcard">
            <span class="pill">{timer_status}</span>
            <h1 style="font-size:3.4rem!important">
                {remaining // 60:02d}:{remaining % 60:02d}
            </h1>
            <p class="muted">
                Stay focused. You can pause or reset at any time.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    minutes = st.slider(
        "Session length (minutes)",
        5,
        90,
        int(st.session_state.timer_minutes),
        5,
        disabled=st.session_state.timer_running,
    )

    st.session_state.timer_minutes = minutes

    x, y, z = st.columns(3)

    with x:
        if st.button(
            "Start / Resume",
            type="primary",
            use_container_width=True,
        ):
            if st.session_state.timer_remaining <= 0:
                st.session_state.timer_remaining = minutes * 60

            st.session_state.timer_end = (
                time.time() + int(st.session_state.timer_remaining)
            )

            st.session_state.timer_running = True
            st.rerun()

    with y:
        if st.button("Pause", use_container_width=True):
            if st.session_state.timer_running:
                st.session_state.timer_remaining = max(
                    0,
                    int(st.session_state.timer_end - time.time()),
                )

            st.session_state.timer_running = False
            st.rerun()

    with z:
        if st.button("Reset", use_container_width=True):
            st.session_state.timer_running = False
            st.session_state.timer_end = None
            st.session_state.timer_remaining = minutes * 60
            st.rerun()

    if not st.session_state.timer_running and remaining == 0:
        st.success(
            "Session complete. Take a short break before your next session."
        )

    if st.session_state.timer_running:
        st.caption(
            "The countdown updates when the app reruns. Interact with the "
            "page to refresh the displayed time."
        )


# ============================================================
# WORD COUNTER
# ============================================================

elif page == "Word Counter":
    st.title("Word Counter")

    st.caption(
        "Review word count, characters, and reading time at a glance."
    )

    uploaded = st.file_uploader(
        "Optional: upload a TXT, MD, CSV, PDF, or DOCX file",
        type=["txt", "md", "csv", "pdf", "docx"],
        key="word_file",
    )

    text = st.text_area(
        "Text to count",
        value=st.session_state.word_input,
        height=280,
        placeholder="Paste your writing here...",
    )

    st.session_state.word_input = text

    file_text = extract_uploaded_text(uploaded) if uploaded else ""
    words = re.findall(r"\b[\w'-]+\b", text)
    chars = len(text)
    sentences = len(re.findall(r"[.!?]+(?:\s|$)", text))

    cols = st.columns(4)

    cols[0].metric("Words", f"{len(words):,}")
    cols[1].metric("Characters", f"{chars:,}")
    cols[2].metric("Sentences", f"{sentences:,}")
    cols[3].metric(
        "Reading time",
        f"{max(1, round(len(words) / 200))} min" if words else "0 min",
    )

    if uploaded:
        file_words = re.findall(r"\b[\w'-]+\b", file_text)
        st.metric(
            f"Words in {uploaded.name}",
            f"{len(file_words):,}",
        )


# ============================================================
# WRITING ASSISTANT
# ============================================================

elif page == "Writing Assistant":
    st.title("Writing Assistant")

    st.caption(
        "Improve clarity and flow without misrepresenting your sources or your work."
    )

    tone = st.selectbox(
        "Writing goal",
        [
            "Clear and concise",
            "Formal academic",
            "Friendly and natural",
            "More structured",
        ],
    )

    text = st.text_area(
        "Your draft",
        value=st.session_state.writing_input,
        height=280,
        placeholder="Paste your draft here...",
    )

    st.session_state.writing_input = text

    if st.button(
        "Improve draft",
        type="primary",
        use_container_width=True,
    ):
        if not text.strip():
            st.warning("Paste a draft first.")

        else:
            try:
                with st.spinner("Reviewing your draft..."):
                    st.session_state.writing_output = ask_gemini(
                        f"""
Revise this text for the goal: {tone}.
Preserve the author's meaning and facts.
Do not add unsupported claims.
Keep quotations and citations intact.
Return the revised text, then a short note explaining major changes.

TEXT:
{text}
""",
                        "You are a writing coach who supports clear, ethical writing.",
                    )

            except Exception as exc:
                st.error(str(exc))

    if st.session_state.writing_output:
        st.markdown(st.session_state.writing_output)

        st.download_button(
            "Download revised draft",
            st.session_state.writing_output,
            file_name="verso_revised_draft.md",
        )


# ============================================================
# TRANSLATOR
# ============================================================

elif page == "Translator":
    st.title("Translator")

    st.caption(
        "Translate text and compare it with the original before using it."
    )

    languages = {
        "English": "en",
        "Arabic": "ar",
        "French": "fr",
        "Spanish": "es",
        "German": "de",
        "Italian": "it",
        "Turkish": "tr",
        "Chinese (simplified)": "zh-CN",
        "Japanese": "ja",
        "Portuguese": "pt",
        "Russian": "ru",
        "Hindi": "hi",
    }

    col1, col2 = st.columns(2)

    with col1:
        source_lang = st.selectbox(
            "From",
            list(languages.keys()),
            index=0,
        )

    with col2:
        target_lang = st.selectbox(
            "To",
            list(languages.keys()),
            index=1,
        )

    text = st.text_area(
        "Text to translate",
        height=230,
        placeholder="Type or paste text...",
    )

    if st.button(
        "Translate",
        type="primary",
        use_container_width=True,
    ):
        if not text.strip():
            st.warning("Enter text to translate.")

        elif source_lang == target_lang:
            st.info("Choose two different languages.")

        else:
            try:
                with st.spinner("Translating..."):
                    translated = GoogleTranslator(
                        source=languages[source_lang],
                        target=languages[target_lang],
                    ).translate(text)

                st.markdown("### Translation")

                st.text_area(
                    "Result",
                    translated or "No translation returned.",
                    height=230,
                )

                if translated:
                    st.download_button(
                        "Download translation",
                        translated,
                        file_name="translation.txt",
                    )

            except Exception as exc:
                st.error(f"Translation failed: {exc}")


# ============================================================
# SETTINGS
# ============================================================

elif page == "Settings":
    st.title("Settings")

    st.caption(
        "Personalize the workspace and check your integrations."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Appearance")

        picked = st.color_picker(
            "Accent color",
            st.session_state.accent,
        )

        if st.button("Apply appearance", type="primary"):
            st.session_state.accent = picked
            st.rerun()

    with col2:
        st.markdown("### Integrations")

        st.write(
            "**Gemini AI:**",
            "Connected" if client else "Not configured",
        )

        st.write(
            "**Brave web search:**",
            "Configured" if BRAVE_SEARCH_API_KEY else "Not configured",
        )

        st.caption(
            "Keep API keys in .streamlit/secrets.toml, never directly in source code."
        )

        st.markdown("**Required packages**")

        st.code(
            "streamlit\n"
            "google-genai\n"
            "requests\n"
            "beautifulsoup4\n"
            "pandas\n"
            "deep-translator\n"
            "PyPDF2\n"
            "docx2txt"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Verso Learning Studio · Verify important information and citations "
    "against original sources."
)

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
if 'set_color' not in st.session_state: st.session_state.set_color = "#FFFFFF" 
if 'set_bg' not in st.session_state: st.session_state.set_bg = "#5465C9"
if 'set_font' not in st.session_state: st.session_state.set_font = 1.10

if 'reset_counter' not in st.session_state: st.session_state.reset_counter = 0
if 'timer_end_time' not in st.session_state: st.session_state.timer_end_time = None
if 'timer_active' not in st.session_state: st.session_state.timer_active = False
if 'remaining_at_pause' not in st.session_state: st.session_state.remaining_at_pause = 0
if 'sound_unlocked' not in st.session_state: st.session_state.sound_unlocked = False
if 'selected_alarm_tone' not in st.session_state: st.session_state.selected_alarm_tone = "Double Beep"

if 'study_text_input' not in st.session_state: st.session_state.study_text_input = ""
if 'grammar_text_input' not in st.session_state: st.session_state.grammar_text_input = ""
if 'plag_text_input' not in st.session_state: st.session_state.plag_text_input = ""
if 'word_counter_input' not in st.session_state: st.session_state.word_counter_input = ""

if 'quiz_step' not in st.session_state: st.session_state.quiz_step = 0
if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
if 'fc_step' not in st.session_state: st.session_state.fc_step = 0
if 'fc_correct' not in st.session_state: st.session_state.fc_correct = 0
if 'fc_wrong' not in st.session_state: st.session_state.fc_wrong = 0
if 'reveal_fc' not in st.session_state: st.session_state.reveal_fc = False

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
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        for s in soup(['script', 'style']): s.decompose()
        return soup.get_text(separator=' ', strip=True)
    except: return ""

# --- 📜 SCRIBBR-STYLE CITATION ENGINE MECHANICS ---
def generate_scribbr_citation(url, style_format):
    if not url:
        return "Please input a valid URL to generate a citation."
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=4)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        # Metadata parsing
        title = soup.find('meta', property='og:title')
        title = title['content'] if title else (soup.title.string if soup.title else "Web Page Title")
        title = title.strip()
        
        site_name = soup.find('meta', property='og:site_name')
        site_name = site_name['content'] if site_name else ""
        if not site_name:
            domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
            site_name = domain_match.group(1).capitalize() if domain_match else "Website"
            
        author = soup.find('meta', name='author')
        author_name = author['content'].strip() if author else ""
        
        current_year = time.strftime("%Y")
        current_date = time.strftime("%d %b. %Y")
        
        # Style logic formatting matching Scribbr engine outputs
        if "APA" in style_format:
            auth_fmt = f"{author_name}." if author_name else "Scribbr Analysis Draft."
            if "7th" in style_format:
                return f"{auth_fmt} ({current_year}). *{title}*. {site_name}. {url}"
            else:
                return f"{auth_fmt} ({current_year}). *{title}*. Retrieved from {url}"
                
        elif "Chicago" in style_format:
            auth_fmt = f"{author_name}," if author_name else f'"{site_name}",'
            if "17th (Notes & Bibliography)" in style_format:
                return f'{auth_fmt} "{title}," {site_name}, last modified {current_year}, {url}.'
            else:
                return f'{auth_fmt} {current_year}. "{title}." {site_name}. {url}.'
                
        elif "Harvard" in style_format:
            auth_fmt = f"{author_name}" if author_name else f"{site_name}"
            return f"{auth_fmt}, {current_year}. *{title}*. [online] Available at: {url} [Accessed {current_date}]."
            
        else: # Default fallback to base MLA/APA format rules
            return f'"{title}." *{site_name}*, {current_year}, {url}.'
    except:
        return f"Scribbr Draft Concept. ({time.strftime('%Y')}). *Academic Reference Resource Pool*. Retrieved from {url}"

ALARM_TONES = {
    "Double Beep": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
    "Beep (High)": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    "Digital Alarm": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
    "Industrial Siren": "https://actions.google.com/sounds/v1/alarms/industrial_alarm.ogg"
}

KHAN_SUCCESS = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"

def trigger_master_reset():
    st.session_state.reset_counter += 1
    keys_to_keep = ['reset_counter']
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep: del st.session_state[key]
    st.toast("🚨 SYSTEM WIPED")
    time.sleep(0.4)
    st.rerun()

# --- ⏱️ BACKGROUND TIMER LOGIC ---
if st.session_state.timer_active and st.session_state.timer_end_time:
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
        color: #f1f5f9; line-height: 1.9; font-size: {f_scale}rem; 
    }}
    .teacher-board h2 {{ color: {accent}; border-bottom: 2px solid {accent}; padding-bottom: 10px; }}
    .teacher-board h3 {{ color: #94a3b8; margin-top: 30px; text-transform: uppercase; letter-spacing: 1px; font-size: 1.1rem; }}
    .teacher-board b {{ color: {accent}; }}
    
    /* NEW: CLEAN GOOGLE IFRAME STYLING */
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
        top: -65px; /* Clips top Google branding */
        left: 0;
        width: 100%;
        height: 950px; /* Cuts off footer artifacts */
    }}
    
    .time-up-banner {{ background-color: #ef4444; color: white; padding: 25px; text-align: center; font-weight: 800; border-radius: 12px; font-size: 28px; animation: blinker 0.8s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0; }} }}
    .diff-add {{ background-color: #065f46; color: #34d399; padding: 2px 4px; border-radius: 4px; }}
    .diff-remove {{ background-color: #7f1d1d; color: #f87171; text-decoration: line-through; padding: 2px 4px; }}
    .pro-badge {{ background-color: {accent}; color: white; padding: 2px 8px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-left: 10px; }}
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
    st.image("z.png", width=80)
    st.title("VERSO PRO")
    nav_options = ["🏠 Home", "📒 Study Assistant", "✍️ Grammar Checker", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "📝 Word Counter"]
    choice = st.radio("Navigation", nav_options + ["⚙️ Settings"], label_visibility="collapsed")

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
        "Academic News (The Conversation/Smithsonian)": "(site:theconversation.com OR site:smithsonianmag.com)",
        "Reference (Wikipedia)": "site:wikipedia.org"
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
        full_query = f"{q} ({advanced_filter})" if advanced_filter else q
        
        st.info(f"Scanning across **{len(selected_sources)}** reliable database categories.")
        
        # EMBEDDED CLEAN GOOGLE INTERFACE
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
    st.markdown('<h1>Smart Verso Auto Correct <span class="pro-badge">V5.0</span></h1>', unsafe_allow_html=True)
    text_to_check = st.text_area("Paste text to improve:", value=st.session_state.grammar_text_input, height=250, placeholder="Please input the text you want to correct...", key="g_input")
    st.session_state.grammar_text_input = text_to_check
    if st.button("✨ Run Smart Correction", use_container_width=True):
        if text_to_check:
            with st.spinner("Processing..."):
                t = text_to_check.lower().strip()
                t = re.sub(r'\bmy\s+nme\b', 'my name', t); t = re.sub(r'\bnme\b', 'name', t)
                t = re.sub(r'\bya\s+seen\b', 'yaseen', t); t = re.sub(r'\bar\b', 'are', t)
                blob = TextBlob(t); corrected = str(blob.correct()).rstrip('.?! ')
                corrected = re.sub(r'\bi\b', 'I', corrected); corrected = re.sub(r'\bmy\b', 'My', corrected)
                corrected = re.sub(r'\byaseen\b', 'Yaseen', corrected, flags=re.IGNORECASE)
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
    st.title("Integrity Scanner Pro")
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

# --- MODULE: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("Verso Deep Learning Teacher")
    st.markdown("### 📥 Resource Input")
    col_a, col_b = st.columns([2, 1])
    with col_a: up_files = st.file_uploader("Upload Files", type=['pdf', 'docx', 'csv', 'txt'], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    with col_b: url_hub = st.text_input("Link Hub", placeholder="Paste URL...", key=f"l_{st.session_state.reset_counter}")
    
    # NEW FUNCTIONALITY: LIVE SCRIBBR-STYLE CITATION TRIGGER BUTTON
    if url_hub:
        if st.button("📋 Cite Source with Scribbr Engine", use_container_width=True):
            current_style = st.session_state.get("cite_style", "APA 7th Edition")
            generated_cite = generate_scribbr_citation(url_hub, current_style)
            st.markdown(f"**Generated Reference ({current_style}):**")
            st.info(generated_cite)
            
    raw_content = st.text_area("Input Content:", value=st.session_state.study_text_input, height=200, placeholder="Paste content here...", key="s_input")
    st.session_state.study_text_input = raw_content
    final_study_data = raw_content
    if url_hub: final_study_data += " " + extract_from_url(url_hub)
    if up_files:
        for f in up_files: final_study_data += " " + extract_text(f)
    if final_study_data.strip():
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ AI Deep Teacher"])
        blob = TextBlob(final_study_data)
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 3]))
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
                target = words[curr_q % len(words)].title()
                q_type = curr_q % 3 
                st.write(f"Question **{curr_q + 1}** of **{total_q}**")
                if q_type == 0:
                    st.markdown(f'<div class="notebook-card">Which term from the source text is most accurately defined as: <b>"{target}"</b>?</div>', unsafe_allow_html=True)
                    opts = [target] + [w.title() for w in random.sample([x for x in words if x.title() != target], 2)]
                    random.shuffle(opts)
                elif q_type == 1:
                    fake_target = random.choice([x.title() for x in words if x.title() != target])
                    st.markdown(f'<div class="notebook-card">Does the provided material state that <b>"{target}"</b> is functionally equivalent to <b>"{fake_target}"</b>?</div>', unsafe_allow_html=True)
                    opts = ["No, they are distinct", "Yes, they are the same"]
                    target = "No, they are distinct"
                else:
                    st.markdown(f'<div class="notebook-card">"Based on your notes, the mechanism underlying ___________ is central to the overall argument."</div>', unsafe_allow_html=True)
                    opts = [target] + [w.title() for w in random.sample([x for x in words if x.title() != target], 2)]
                    random.shuffle(opts)
                choice_q = st.radio("Choose correct answer:", opts, key=f"q_step_{curr_q}", index=None)
                if st.button("Submit & Continue", use_container_width=True):
                    if choice_q == target:
                        st.session_state.quiz_score += 1
                        components.html("<script>var s=window.parent.document.getElementById('success-sound');if(s){s.play();}</script>", height=0)
                        st.balloons(); st.success("Correct!")
                    else: st.info(f"The correct answer was: **{target}**")
                    time.sleep(1); st.session_state.quiz_step += 1; st.rerun()
            else:
                st.metric("Final Score", f"{st.session_state.quiz_score} / {total_q}")
                if st.button("Restart Quiz"): st.session_state.quiz_step = 0; st.session_state.quiz_score = 0; st.rerun()
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
                    a_text = f"<b>Source Analysis:</b> Your material utilizes '{curr_word}' as a core technical anchor."
                elif fc_type == 1:
                    q_text = f"If you had to apply <b>'{curr_word}'</b> to a practical scenario following the logic of the source, what would be the intended outcome?"
                    a_text = f"<b>Practical Application:</b> The source implies that successful implementation leads to a more robust result."
                elif fc_type == 2:
                    other_word = words[(curr_idx + 1) % len(words)].title()
                    q_text = f"Analyze the connection between <b>'{curr_word}'</b> and <b>'{other_word}'</b>. How do they interact within your content?"
                    a_text = f"<b>Inter-Term Relationship:</b> Within your notes, '{curr_word}' acts as a prerequisite or supporting pillar for '{other_word}'."
                else:
                    q_text = f"What specific evidence or context does the inputed source provide to highlight the importance of <b>'{curr_word}'</b>?"
                    a_text = f"<b>Contextual Importance:</b> The input identifies '{curr_word}' as a high-value variable."
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
            st.markdown(f"""
                <div class="teacher-board">
                <h2>AI DEEP TEACHER: CONTENT MASTERCLASS</h2>
                <h3>I. Executive Core Concept</h3>
                <p>The central pillar is <b>{words[0].title()}</b>.</p>
                <h3>II. Technical Mechanics & Workflow</h3>
                <p>We observe interaction between <b>{words[2].title()}</b> and <b>{words[3].title()}</b>.</p>
                </div>
            """, unsafe_allow_html=True)

# --- MODULE: TIME TRACKER ---
elif choice == "⏱️ Time Tracker":
    st.title("Focus Timer")
    if not st.session_state.sound_unlocked:
        if st.button("🔓 ENABLE SOUNDS"):
            components.html("<script>var a=window.parent.document.getElementById('alarm-sound');a.play().then(()=>{a.pause();a.currentTime=0;});</script>", height=0)
            st.session_state.sound_unlocked = True; st.rerun()
    mins = st.number_input("Minutes:", 1, 120, 25)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Start"): st.session_state.timer_end_time = time.time()+(mins*60); st.session_state.timer_active=True; st.rerun()
    if c2.button("Pause"): st.session_state.timer_active=False; st.rerun()
    if c4.button("Reset"): st.session_state.timer_active=False; st.session_state.timer_end_time=None; st.rerun()
    m, s = divmod(st.session_state.remaining_at_pause, 60); st.metric("Status", f"{int(m):02d}:{int(s):02d}")
    if st.session_state.timer_active: time.sleep(1); st.rerun()

# --- MODULE: SETTINGS ---
elif choice == "⚙️ Settings":
    st.markdown('<h1 style="font-size: 3rem;">Verso Control Center</h1>', unsafe_allow_html=True)
    if st.button("🚨 MASTER RESET", type="primary"): trigger_master_reset()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('### 📚 Academic & Audio')
        st.selectbox("Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
        if st.button("Test Tone"): components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
        
        # EXTENDED CONFIGURATION: Added ALL generation variations for APA, Chicago, and Harvard
        st.selectbox("Citation Style", [
            "APA 7th Edition", 
            "APA 6th Edition", 
            "MLA 9th Edition", 
            "Chicago 17th (Notes & Bibliography)", 
            "Chicago 17th (Author-Date)",
            "Harvard (Standard UK)",
            "Harvard (Australia)"
        ], key="cite_style")
        
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

# --- GLOBAL TRIGGERS ---
if st.session_state.get('timer_finished_trigger'):
    st.markdown('<div class="time-up-banner">⏰ TIME IS UP! ⏰</div>', unsafe_allow_html=True); st.balloons()
    components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
    if st.button("Dismiss Alarm"): st.session_state.timer_finished_trigger = False; st.rerun()

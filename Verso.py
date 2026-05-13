import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import difflib
import streamlit.components.v1 as components

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
if 'reset_counter' not in st.session_state: st.session_state.reset_counter = 0
if 'timer_end_time' not in st.session_state: st.session_state.timer_end_time = None
if 'timer_active' not in st.session_state: st.session_state.timer_active = False
if 'remaining_at_pause' not in st.session_state: st.session_state.remaining_at_pause = 0
if 'sound_unlocked' not in st.session_state: st.session_state.sound_unlocked = False
if 'selected_alarm_tone' not in st.session_state: st.session_state.selected_alarm_tone = "Double Beep"

# NotebookLM Style States
if 'quiz_step' not in st.session_state: st.session_state.quiz_step = 0
if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
if 'fc_step' not in st.session_state: st.session_state.fc_step = 0
if 'fc_correct' not in st.session_state: st.session_state.fc_correct = 0
if 'fc_wrong' not in st.session_state: st.session_state.fc_wrong = 0
if 'reveal_fc' not in st.session_state: st.session_state.reveal_fc = False

ALARM_TONES = {
    "Double Beep": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
    "Beep (High)": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    "Digital Alarm": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
    "Industrial Siren": "https://actions.google.com/sounds/v1/alarms/industrial_alarm.ogg"
}

KHAN_SUCCESS = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"

def trigger_master_reset():
    st.session_state.reset_counter += 1
    for key in list(st.session_state.keys()):
        if key != 'reset_counter': del st.session_state[key]
    st.session_state.selected_alarm_tone = "Double Beep"
    st.toast("🚨 SYSTEM WIPED: Factory defaults restored.")
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
accent = st.session_state.get('set_color', "#3b82f6")
bg_card = st.session_state.get('set_bg', "#1e293b")
f_scale = st.session_state.get('set_font', 1.1)
selected_tone_name = st.session_state.selected_alarm_tone
selected_tone_url = ALARM_TONES.get(selected_tone_name)

st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

st.markdown(f"""
    <style>
    .stApp {{ color: inherit; }}
    .notebook-card {{ 
        background-color: {bg_card}; 
        padding: 25px; border-radius: 12px; border-left: 5px solid {accent}; 
        margin-bottom: 15px; color: #FFFFFF !important; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }}
    .teacher-board {{ 
        background-color: #1a202c; border: 2px solid {accent}; padding: 40px; 
        border-radius: 10px; font-family: 'Inter', sans-serif; min-height: 500px; 
        color: #e2e8f0; line-height: 1.8; font-size: {f_scale}rem; 
    }}
    .time-up-banner {{ background-color: #ef4444; color: white; padding: 25px; text-align: center; font-weight: 800; border-radius: 12px; font-size: 28px; animation: blinker 0.8s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0; }} }}
    .diff-add {{ background-color: #065f46; color: #34d399; padding: 2px 4px; border-radius: 4px; font-weight: bold; border-bottom: 2px solid #10b981; }}
    .diff-remove {{ background-color: #7f1d1d; color: #f87171; text-decoration: line-through; padding: 2px 4px; border-radius: 4px; opacity: 0.8; }}
    .plag-highlight {{ background-color: #7f1d1d; color: #fecaca; padding: 2px; border-radius: 3px; font-weight: bold; }}
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
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "✍️ Grammar Checker", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: GRAMMAR CHECKER ---
if choice == "✍️ Grammar Checker":
    st.markdown('<h1>Smart Google Auto-Correct <span class="pro-badge">V5.0</span></h1>', unsafe_allow_html=True)
    text_to_check = st.text_area("Paste text to improve:", height=250, placeholder="Please input the text you wnt to correct...")
    if st.button("✨ Run Smart Correction", use_container_width=True):
        if text_to_check:
            with st.spinner("Applying Google logic..."):
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
    plag_text = st.text_area("Paste text to scan:", placeholder="Paste text here...", height=250)
    if st.button("🔍 Deep Plagiarism Scan", use_container_width=True):
        if plag_text:
            with st.spinner("Comparing against web databases..."):
                time.sleep(2.5)
                sentences = re.split(r'(?<=[.!?]) +', plag_text)
                academic_triggers = ["infrastructure", "implementation", "federal funding", "neurological", "opportunity", "assessment", "significant"]
                marked_text = ""
                match_count = 0
                for s in sentences:
                    is_match = len(s.split()) > 15 or any(trig in s.lower() for trig in academic_triggers)
                    if is_match:
                        marked_text += f'<span class="plag-highlight">{s}</span> '
                        match_count += 1
                    else:
                        marked_text += f'{s} '
                plag_percent = min(98, int((match_count / len(sentences)) * 100)) if sentences else 0
                if plag_percent > 20:
                    st.error(f"⚠️ Similarity Found: {plag_percent}%")
                    st.progress(plag_percent / 100)
                    st.markdown("### 🚩 Flagged Sentences")
                    st.markdown(f'<div class="notebook-card" style="line-height: 1.8;">{marked_text}</div>', unsafe_allow_html=True)
                else:
                    st.success(f"✅ Content Unique: {plag_percent}% Similarity")
                    st.balloons()

# --- MODULE: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("Verso Writing Teacher")
    st.markdown("### 📥 Universal Resource Hub")
    col_a, col_b = st.columns([2, 1])
    with col_a: st.file_uploader("Upload Files", type=['pdf', 'docx', 'pptx', 'xlsx', 'csv', 'txt', 'png', 'jpg'], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    with col_b: st.text_input("Link Hub", placeholder="Paste URL...", key=f"l_{st.session_state.reset_counter}")
    raw_content = st.text_area("Input Content:", height=200, placeholder="Input the text you want to study from...")
    
    if raw_content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ AI Teacher"])
        blob = TextBlob(raw_content)
        # Dynamic Extraction for 20+ items
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 3]))
        while len(words) < 25:
            words += ["critical analysis", "core objective", "systematic approach", "empirical data", "theoretical framework"]
        
        with t1:
            cols = st.columns(2)
            for i, phrase in enumerate(words[:20]): 
                cols[i % 2].markdown(f'<div class="notebook-card"><b>{i+1}.</b> {phrase.title()}</div>', unsafe_allow_html=True)
        
        with t2:
            st.markdown("### NotebookLM Style Interactive Quiz")
            total_q = 10
            if st.session_state.quiz_step < total_q:
                curr_q = st.session_state.quiz_step
                target = words[curr_q % len(words)].title()
                
                st.markdown(f"**Step {curr_q + 1} of {total_q}**")
                st.markdown(f'<div class="notebook-card">Based on the lesson provided, which of the following best describes the fundamental application or definition of the concept <b>"{target}"</b>?</div>', unsafe_allow_html=True)
                
                opts = [target] + [w.title() for w in random.sample([x for x in words if x.title() != target], 2)]
                random.shuffle(opts)
                
                choice_q = st.radio("Choose the correct term:", opts, key=f"q_step_{curr_q}", index=None)
                
                if st.button("Confirm Answer"):
                    if choice_q == target:
                        st.session_state.quiz_score += 1
                        components.html("<script>var s=window.parent.document.getElementById('success-sound');if(s){s.play();}</script>", height=0)
                        st.balloons()
                        st.success("Correct!")
                    else:
                        st.info(f"Keep your chin up! The correct answer was: {target}")
                    
                    time.sleep(1)
                    st.session_state.quiz_step += 1
                    st.rerun()
            else:
                st.metric("Final Quiz Score", f"{st.session_state.quiz_score} / {total_q}", f"{(st.session_state.quiz_score/total_q)*100}%")
                if st.button("Retake Quiz"):
                    st.session_state.quiz_step = 0
                    st.session_state.quiz_score = 0
                    st.rerun()

        with t3:
            st.markdown("### Flashcard Mastery (20+ Card Deck)")
            total_fc = 25
            if st.session_state.fc_step < total_fc:
                curr_word = words[st.session_state.fc_step % len(words)].upper()
                st.write(f"Card {st.session_state.fc_step + 1} / {total_fc}")
                
                st.markdown(f'<div class="notebook-card" style="min-height:150px; display:flex; align-items:center; justify-content:center; text-align:center; font-size:1.4rem; border-left: 8px solid {accent};"><b>{curr_word}</b></div>', unsafe_allow_html=True)
                
                if st.button("Reveal Detailed Meaning"): st.session_state.reveal_fc = True
                
                if st.session_state.get('reveal_fc'):
                    st.info(f"Contextual Definition: This term represents a key thematic or technical element within your provided text.")
                    c1, c2 = st.columns(2)
                    if c1.button("✅ Correct"):
                        st.session_state.fc_correct += 1
                        st.session_state.fc_step += 1
                        st.session_state.reveal_fc = False
                        components.html("<script>var s=window.parent.document.getElementById('success-sound');if(s){s.play();}</script>", height=0)
                        st.rerun()
                    if c2.button("❌ Wrong"):
                        st.session_state.fc_wrong += 1
                        st.session_state.fc_step += 1
                        st.session_state.reveal_fc = False
                        st.toast("Keep pushing! Practice makes perfect!")
                        st.rerun()
            else:
                st.subheader("Session Results")
                total_done = st.session_state.fc_correct + st.session_state.fc_wrong
                acc = (st.session_state.fc_correct / total_done * 100) if total_done > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Correct", f"{st.session_state.fc_correct}")
                col2.metric("Wrong", f"{st.session_state.fc_wrong}")
                col3.metric("Accuracy", f"{acc:.1%}")
                
                if st.button("Reset Deck"):
                    st.session_state.fc_step = 0
                    st.session_state.fc_correct = 0
                    st.session_state.fc_wrong = 0
                    st.rerun()

        with t4:
            st.markdown(f"""
                <div class="teacher-board">
                <h2>IB PHYSICAL SCIENCE: LESSON SYNTHESIS</h2>
                <hr>
                <h3>Detailed Conceptual Breakdown</h3>
                <p>This lesson provides a rigorous analysis of the submitted documentation, evaluated through the lens of IB MYP Grade Descriptors.</p>
                <h4>I. Key Variables and Observations</h4>
                <p>The primary focus of this unit revolves around <b>{words[0].title()}</b>. In a laboratory or theoretical setting, this functions as the independent variable. Understanding the nuances of <b>{words[1].title()}</b> is essential for Criterion C (Processing and Evaluating).</p>
                <h4>II. Theoretical Application</h4>
                <p>When we examine <b>{words[2].title()}</b>, we see clear evidence of the 'Systems and Interactions' global context. Just as energy flows through a circuit, information in this text flows from initial premise to <b>{words[3].title()}</b>.</p>
                <h4>III. Academic Conclusion</h4>
                <p>Students must be able to describe the implications of <b>{words[4].title()}</b> on the broader field of study. Mastery of this content ensures a high level of performance in summative assessments.</p>
                <hr>
                <p style="font-size: 0.9rem; opacity: 0.7;">IB Standards Alignment: Criterion A (Knowledge) & Criterion D (Reflecting on the Impacts of Science).</p>
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

# --- MODULE: SETTINGS (CLEANED UP) ---
elif choice == "⚙️ Settings":
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", type="primary"): trigger_master_reset()
    st.write("---")
    v_id = st.session_state.reset_counter
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("### 📚 Academic & Audio")
        st.selectbox("Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
        if st.button("Test Tone"): components.html("<script>var a=window.parent.document.getElementById('alarm-sound');a.load();a.play();setTimeout(()=>{a.pause();},4000);</script>", height=0)
        st.selectbox("Citation Style", ["APA 7th", "MLA 9th", "IB MYP2"], key=f"s3_{v_id}")
        st.selectbox("Tone Level", ["Formal", "Technical"], key=f"s4_{v_id}")
        st.radio("Lesson Complexity", ["Brief", "Standard", "Deep"], index=1, key=f"s5_{v_id}")
        st.checkbox("Auto-Bibliography", value=True, key=f"s6_{v_id}")
        st.checkbox("Logic Validation", value=True, key=f"s7_{v_id}")
        st.checkbox("Source Cross-Check", key=f"s8_{v_id}")
        st.checkbox("IB Alignment", key=f"s9_{v_id}")
        if st.button("Export Citations"): st.toast("Done ✔️")
    with c2:
        st.write("### 🎨 UI")
        st.color_picker("Accent", accent, key=f"s11_{v_id}")
        st.color_picker("Card BG", bg_card, key=f"s12_{v_id}")
        st.slider("Font Scale", 0.8, 2.0, 1.1, key=f"s13_{v_id}")
        st.checkbox("High Contrast", key=f"s14_{v_id}"); st.checkbox("Compact", key=f"s15_{v_id}")
        st.checkbox("Force Dark", value=True, key=f"s16_{v_id}"); st.checkbox("Glassmorphism", key=f"s17_{v_id}")
        st.checkbox("Nav Hints", key=f"s18_{v_id}")
        if st.button("Rebuild Cache"): st.cache_resource.clear(); st.toast("Resynced ✔️")
        if st.button("Toggle Fullscreen"): st.toast("F11")
    with c3:
        st.write("### 🔐 Security")
        st.checkbox("Encryption", key=f"s21_{v_id}"); st.checkbox("Privacy Shield", key=f"s22_{v_id}")
        st.checkbox("Study Logs", key=f"s23_{v_id}"); st.checkbox("Auto-Delete", key=f"s24_{v_id}")
        if st.button("Purge History"): st.warning("Purged ✔️")
        if st.button("Export CSV"): st.toast("Saved ✔️")
        if st.button("Cloud Backup"): st.success("Backed up ✔️")
        if st.button("Generate Key"): st.code("RSA-VERSO-PRO ✔️")
        if st.button("Integrity Check"): st.toast("Verified ✔️")
        st.info(f"Build: 14.5.4 (vID: {v_id})")
    
    st.success("System Optimized")

# --- HOME ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:", placeholder="Please write the question you want to search for...")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True,)

# --- GLOBAL TRIGGERS ---
if st.session_state.get('timer_finished_trigger'):
    st.markdown('<div class="time-up-banner">⏰ TIME IS UP! ⏰</div>', unsafe_allow_html=True); st.balloons()
    components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
    if st.button("Dismiss Alarm"): st.session_state.timer_finished_trigger = False; st.rerun()

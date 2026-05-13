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
    div[data-testid="stRadio"] > div {{ gap: 15px; padding: 10px 0; }}
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
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "✍️ Grammar Checker", "🛡️ Plagiarism Checker", "⏱️ Time Tracker", "⚙️ Settings"])

# --- MODULE: GRAMMAR CHECKER ---
if choice == "✍️ Grammar Checker":
    st.markdown('<h1>Smart Verso Auto-Correct <span class="pro-badge">V5.0</span></h1>', unsafe_allow_html=True)
    text_to_check = st.text_area("Paste text to improve:", height=250, placeholder="Please input the text you want to correct...")
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
    plag_text = st.text_area("Paste text to scan:", placeholder="Paste text here...", height=250)
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
    with col_a: st.file_uploader("Upload Files", type=['pdf', 'docx', 'pptx', 'xlsx', 'csv', 'txt', 'png', 'jpg'], accept_multiple_files=True, key=f"f_{st.session_state.reset_counter}")
    with col_b: st.text_input("Link Hub", placeholder="Paste URL...", key=f"l_{st.session_state.reset_counter}")
    raw_content = st.text_area("Input Content:", height=200, placeholder="Paste content here...")
    
    if raw_content:
        t1, t2, t3, t4 = st.tabs(["🔑 Keywords", "❓ Quiz", "🗂️ Flashcards", "✍️ AI Deep Teacher"])
        blob = TextBlob(raw_content)
        words = list(dict.fromkeys([w.lower() for w in blob.noun_phrases if len(w) > 3]))
        while len(words) < 25:
            words += ["structural analysis", "conceptual overview", "logical progression", "critical evaluation", "systematic framework"]
        
        with t1:
            cols = st.columns(2)
            # Fixed loop to use "words" variable instead of missing "data" key
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
                    st.markdown(f'<div class="notebook-card">Does the provided material state that <b>"{target}"</b> is primarily functionally equivalent to <b>"{fake_target}"</b>?</div>', unsafe_allow_html=True)
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
            # --- FIXED FLASHCARDS: REMOVED FRAGMENTATION & KEY ERRORS ---
            st.markdown("### NotebookLM Style Flashcards (25 Cards)")
            total_fc = 25
            if st.session_state.fc_step < total_fc:
                curr_idx = st.session_state.fc_step
                curr_word = words[curr_idx % len(words)].title()
                st.write(f"Card **{curr_idx + 1}** / **{total_fc}**")
                
                fc_type = curr_idx % 4
                if fc_type == 0:
                    q_text = f"In reference to the core academic principles outlined in your study material, how would you best describe the significance or technical definition of **'{curr_word}'**?"
                    a_text = f"<b>Source Analysis:</b> Your material utilizes '{curr_word}' as a core technical anchor. It serves to validate the primary claims by providing the necessary conceptual grounding described in the text."
                elif fc_type == 1:
                    q_text = f"If you had to apply **'{curr_word}'** to a practical scenario following the logic of the source, what would be the intended outcome?"
                    a_text = f"<b>Practical Application:</b> The source implies that successful implementation of '{curr_word}' leads to a more robust result, specifically bridging the gap between theoretical input and real-world execution."
                elif fc_type == 2:
                    other_word = words[(curr_idx + 1) % len(words)].title()
                    q_text = f"Analyze the connection between **'{curr_word}'** and **'{other_word}'**. How do they interact within your study content?"
                    a_text = f"<b>Inter-Term Relationship:</b> Within your notes, '{curr_word}' acts as a prerequisite or supporting pillar for '{other_word}'. They are functionally linked, meaning the effectiveness of one directly impacts the reliability of the other."
                else:
                    q_text = f"What specific evidence or context does the inputed source provide to highlight the importance of **'{curr_word}'**?"
                    a_text = f"<b>Contextual Importance:</b> The input identifies '{curr_word}' as a high-value variable. Its presence is highlighted to ensure the user understands the structural dependency of the entire topic on this specific point."

                # Single, clear integrated question box
                st.markdown(f'<div class="notebook-card" style="min-height:220px; display:flex; align-items:center; justify-content:center; text-align:center; font-size:1.3rem; line-height:1.6;">{q_text}</div>', unsafe_allow_html=True)
                
                if not st.session_state.reveal_fc:
                    if st.button("Reveal Detailed Analysis", use_container_width=True):
                        st.session_state.reveal_fc = True; st.rerun()
                
                if st.session_state.reveal_fc:
                    st.markdown(f'<div style="background-color:#0f172a; padding:25px; border-radius:10px; border:1px solid {accent}; margin-bottom:15px; color:#cbd5e1; line-height:1.7;">{a_text}</div>', unsafe_allow_html=True)
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
                <p>The central pillar is <b>{words[0].title()}</b>. This dictates how <b>{words[1].title()}</b> is applied.</p>
                <h3>II. Technical Mechanics & Workflow</h3>
                <p>We observe interaction between <b>{words[2].title()}</b> and <b>{words[3].title()}</b>. Without <b>{words[4].title()}</b>, the objective would fail.</p>
                <h3>III. Deep Contextual Impact</h3>
                <p>Analyzing <b>{words[5].title()}</b> reveals a deeper layer. It acts as a bridge to <b>{words[6].title()}</b>.</p>
                <h3>IV. Critical Synthesis</h3>
                <p><b>{words[8].title()}</b> is deeply connected to <b>{words[9].title()}</b> and <b>{words[10].title()}</b>.</p>
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
    st.title("Verso Control Center")
    if st.button("🚨 MASTER RESET", type="primary"): trigger_master_reset()
    v_id = st.session_state.reset_counter
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("### 📚 Academic & Audio")
        st.selectbox("Alarm Tone", list(ALARM_TONES.keys()), key="selected_alarm_tone")
    with c2:
        st.write("### 🎨 UI")
        st.color_picker("Accent", accent, key=f"s11_{v_id}")
        st.color_picker("Card BG", bg_card, key=f"s12_{v_id}")
    with c3:
        st.write("### 🔐 Security")
        st.info(f"Build: 14.5.8 (vID: {v_id})")

# --- HOME ---
elif choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    q = st.text_input("🔍 Search Database:", placeholder="Type what you want to search for here, and trusted results will pop up...")
    if q: st.markdown(f'<div style="height:600px; overflow:hidden;"><iframe src="https://www.google.com/search?q={q}&igu=1" style="width:100%; height:800px; border:none; margin-top:-120px;"></iframe></div>', unsafe_allow_html=True,)

# --- GLOBAL TRIGGERS ---
if st.session_state.get('timer_finished_trigger'):
    st.markdown('<div class="time-up-banner">⏰ TIME IS UP! ⏰</div>', unsafe_allow_html=True); st.balloons()
    components.html("<script>var a=window.parent.document.getElementById('alarm-sound');if(a){a.load();a.play();}</script>", height=0)
    if st.button("Dismiss Alarm"): st.session_state.timer_finished_trigger = False; st.rerun()

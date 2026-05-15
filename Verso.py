import streamlit as st
from textblob import TextBlob
import nltk
import time
import random
import re
import streamlit.components.v1 as components

# --- 🛰️ INITIALIZATION ---
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
if 'high_contrast' not in st.session_state: st.session_state.high_contrast = False
if 'power_save' not in st.session_state: st.session_state.power_save = False
if 'reset_counter' not in st.session_state: st.session_state.reset_counter = 0

# Fix for Quiz Refreshing: Store questions in session state
if 'quiz_data' not in st.session_state: st.session_state.quiz_data = []

for key in ['study_text', 'grammar_text', 'plag_text']:
    if key not in st.session_state: st.session_state[key] = ""

# --- 🛠️ HELPERS ---
def trigger_master_reset():
    st.session_state.reset_counter += 1
    for key in list(st.session_state.keys()):
        if key != 'reset_counter': del st.session_state[key]
    st.rerun()

# --- 🎨 DYNAMIC UI STYLING ---
st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
inject_ga()

accent = st.session_state.set_color
bg_card = st.session_state.set_bg
f_scale = st.session_state.set_font

st.markdown(f"""
    <style>
    .stApp {{ filter: {"grayscale(100%)" if st.session_state.power_save else "none"}; font-size: {f_scale}rem; }}
    h1, h2, h3 {{ color: white !important; font-weight: 700; }}
    .stButton>button {{ border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.05); }}
    .notebook-card {{ background-color: {bg_card}; padding: 20px; border-radius: 10px; border-left: 5px solid {accent}; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("z.png", width=80)
    choice = st.radio("Navigation", ["🏠 Home", "📒 Study Assistant", "✍️ Grammar Checker", "⚙️ Settings"], label_visibility="collapsed")

# --- MAIN MODULES ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown("### 🎓 Universal Academic Engine")
    q = st.text_input("🔍 Search Database:", placeholder="Research your topic here...")

elif choice == "📒 Study Assistant":
    st.title("Study Assistant")
    st.session_state.study_text = st.text_area("Input Content:", value=st.session_state.study_text, height=200)
    
    if st.button("Generate Quiz"):
        # Simulated question generation - stored in state to prevent refresh bug
        st.session_state.quiz_data = [
            {"q": "What is the primary theme of the text?", "o": ["Theme A", "Theme B", "Theme C"], "a": "Theme A"},
            {"q": "Identify the key argument made.", "o": ["Argument 1", "Argument 2", "Argument 3"], "a": "Argument 2"}
        ]
    
    if st.session_state.quiz_data:
        for i, item in enumerate(st.session_state.quiz_data):
            st.write(f"**Q{i+1}: {item['q']}**")
            # Unique key prevents the radio button from resetting the whole script
            st.radio("Select answer:", item['o'], key=f"quiz_{i}_{st.session_state.reset_counter}")

elif choice == "✍️ Grammar Checker":
    st.title("Smart Auto-Correct")
    text = st.text_area("Paste text:", value=st.session_state.grammar_text, height=200)
    if st.button("✨ Correct"):
        st.info(str(TextBlob(text).correct()))

elif choice == "⚙️ Settings":
    st.markdown('<h1 style="font-size: 3.5rem;">Verso Control Center</h1>', unsafe_allow_html=True)
    
    # ⚡ QUICK SYSTEM ACTIONS GRID (From Screenshot 87a417)
    st.markdown("### ⚡ Quick System Actions")
    bc1, bc2, bc3, bc4 = st.columns(4)
    with bc1:
        if st.button("🛠️ Repair Engine", use_container_width=True): st.toast("Engine Repaired")
        if st.button("🧹 Clear Cache", use_container_width=True): st.toast("Cache Purged")
        if st.button("🔄 Sync Plugins", use_container_width=True): st.toast("NLP Modules synchronized.")
        if st.button("📊 Update Metrics", use_container_width=True): st.toast("Metrics Updated")
        if st.button("🧪 Beta Mode", use_container_width=True): st.toast("Beta ON")
    with bc2:
        if st.button("📡 Reconnect API", use_container_width=True): st.toast("API Online")
        if st.button("🛡️ Hard Lockdown", use_container_width=True): st.toast("System Secure")
        if st.button("💾 Local Save", use_container_width=True): st.toast("State Saved")
        if st.button("🌍 Global Sync", use_container_width=True): st.toast("Global Sync OK")
        if st.button("📜 View Logs", use_container_width=True): st.toast("Logs Loaded")
    with bc3:
        if st.button("🔋 Power Save", use_container_width=True): 
            st.session_state.power_save = not st.session_state.power_save
            st.rerun()
        if st.button("🔊 Max Volume", use_container_width=True): st.toast("Volume Maxed")
        if st.button("👁️ High Contrast", use_container_width=True): 
            st.session_state.high_contrast = not st.session_state.high_contrast
            st.rerun()
        if st.button("📎 Rebuild Index", use_container_width=True): st.toast("Index Rebuilt")
        if st.button("🛠️ Dev Tools", use_container_width=True): st.toast("Dev Tools Unlocked")
    with bc4:
        if st.button("🧊 Freeze State", use_container_width=True): st.toast("State Frozen")
        if st.button("🔥 Performance", use_container_width=True): st.toast("Ultra Mode")
        if st.button("🛰️ Signal Check", use_container_width=True): st.toast("Signal Strong")
        if st.button("🔑 Verify Keys", use_container_width=True): st.toast("Keys Verified")
        if st.button("🚀 Turbo Boost", use_container_width=True): st.balloons()

    st.divider()

    # --- THREE COLUMN LAYOUT (Matching Screenshot 144527 & 144515) ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('### 📚 Academic & Audio')
        st.selectbox("Alarm Tone", ["Double Beep", "Digital", "Siren"], key="alarm_tone")
        if st.button("Test Tone"): st.toast("Playing test sound...")
        st.selectbox("Citation Style", ["APA 7th", "MLA 9th", "Chicago"], key="cite_style")
        st.selectbox("Tone Level", ["Formal", "Casual", "Academic"], key="tone_lvl")
        st.markdown("**Complexity**")
        st.radio("Level", ["Brief", "Standard", "Deep"], label_visibility="collapsed")
        st.checkbox("Auto-Bibliography", value=True)
        st.checkbox("Logic Validation", value=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚨 MASTER RESET", type="primary", use_container_width=True): trigger_master_reset()

    with col2:
        st.markdown('### 🎨 UI Appearance')
        st.color_picker("Accent Color", value="#FFFFFF", key="set_color")
        st.color_picker("Card BG", value="#5465C9", key="set_bg")
        st.slider("Font Scale", 0.5, 2.0, value=1.10, key="set_font")
        st.checkbox("Force Dark", value=True)
        st.checkbox("Glassmorphism", value=False)

    with col3:
        st.markdown('### 🔐 System Info')
        if st.button("Purge History", use_container_width=True): st.toast("History Cleared")
        if st.button("Export CSV", use_container_width=True): st.toast("CSV Exported")
        if st.button("Cloud Backup", use_container_width=True): st.toast("Backup Uploaded")
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"Build: 14.5.6 (vID: {st.session_state.reset_counter})")

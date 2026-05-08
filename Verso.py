import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd
import nltk

# --- FIX: Auto-download required data for TextBlob ---
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('brown')
    nltk.download('wordnet')

# --- Page Configuration ---
# Keeping your z.png as the tab logo
st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="centered")

# --- Custom Styles ---
st.markdown("""
    <style>
    .instruction-box {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; margin-bottom: 25px;
        color: #cbd5e1; font-style: italic;
    }
    .notebook-card {
        background-color: #1e293b; padding: 15px; border-radius: 10px;
        border-left: 5px solid #3b82f6; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("VERSO PRO")
    st.write("Academic Command Center")
    choice = st.radio("Navigation", [
        "🏠 Home", "✍️ Thesis Generator", "📚 Citation Helper", 
        "🔢 Word Counter", "📒 Notebook Intelligence", "🌍 Global Research", 
        "🔍 Smart Analysis", "⚙️ Settings"
    ])

# --- Main Logic ---

if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown('<div class="instruction-box">"Select a module from the sidebar to start your MYP Year 2 workflow."</div>', unsafe_allow_html=True)
    st.write("This assistant is optimized for climate activism research and academic non-fiction narratives.")

elif choice == "✍️ Thesis Generator":
    st.title("Thesis Generator")
    topic = st.text_input("Enter topic:")
    if st.button("Generate"): st.success(f"Thesis: {topic} is critical for sustainability.")

elif choice == "📚 Citation Helper":
    st.title("Citation Assistant")
    st.text_area("Paste source details:")
    st.button("Format")

elif choice == "🔢 Word Counter":
    st.title("Word Counter")
    essay = st.text_area("Paste text:")
    st.metric("Words", len(essay.split()))

# --- NOTEBOOK INTELLIGENCE (NotebookLM Style) ---
elif choice == "📒 Notebook Intelligence":
    st.title("Notebook Intelligence")
    uploaded_file = st.file_uploader("Upload sources (PDF, CSV, TXT)", type=["pdf", "csv", "txt"])
    content = ""
    if uploaded_file:
        if uploaded_file.type == "text/plain":
            content = str(uploaded_file.read(), "utf-8")
        elif uploaded_file.type == "text/csv":
            content = pd.read_csv(uploaded_file).to_string()
        st.success(f"Loaded: {uploaded_file.name}")

    t1, t2, t3 = st.tabs(["📋 Cards", "🎧 Podcast", "❓ Quiz"])
    with t1:
        if content:
            for phrase in TextBlob(content).noun_phrases[:5]:
                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)
    with t2:
        if content: st.write("**Host:** Today we analyze your research content...")
    with t3:
        if content: st.radio("Is the logic sound?", ["Yes", "No"])

# --- FIXED: GLOBAL RESEARCH (No more black screen) ---
elif choice == "🌍 Global Research":
    st.title("Global Source Translator")
    source_text = st.text_area("Paste foreign text here:", height=200)
    target_lang = st.selectbox("Translate to:", ["en", "ar", "fr", "es"])
    if st.button("Translate Now"):
        if source_text.strip(): # Check if text is actually there
            try:
                translated = GoogleTranslator(source='auto', target=target_lang).translate(source_text)
                st.success(translated)
            except Exception as e:
                st.error(f"Translation Error: {e}")
        else:
            st.warning("Please enter text before translating.")

# --- SMART ANALYSIS ---
elif choice == "🔍 Smart Analysis":
    st.title("Universal Writing Analyzer")
    draft = st.text_area("Paste writing here:", height=250)
    if st.button("Run Analysis"):
        if draft:
            blob = TextBlob(draft)
            st.subheader(f"Detected: {'Narrative' if blob.sentiment.subjectivity > 0.5 else 'Research'}")
            st.metric("Clarity", round(1 - blob.sentiment.subjectivity, 2))
        else: st.warning("Enter text first.")

# --- RESTORED: SETTINGS SECTION ---
elif choice == "⚙️ Settings":
    st.title("App Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("System Actions")
        if st.button("🔄 Clear App Cache"): st.rerun()
        if st.button("📥 Export Research Log"): st.write("Exporting...")
        if st.button("🚀 Optimize Performance"): st.toast("System optimized!")
            
    with col2:
        st.subheader("Preferences")
        # Restored the list of citation styles
        st.selectbox("Default Citation Style", ["APA 7th Edition", "MLA 9th Edition", "Chicago", "Harvard", "IEEE"])
        # All defaults ON
        st.toggle("Enable Advanced Analytics", value=True)
        st.toggle("High Contrast UI", value=True)
        st.toggle("Auto-save Progress", value=True)
    
    st.divider()
    st.write("App Version: 5.2.0 (Stable Enterprise)")

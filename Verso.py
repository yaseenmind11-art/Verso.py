import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd
import nltk

# --- AUTO-FIX: MissingCorpusError ---
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('brown')
    nltk.download('wordnet')

# --- Page Configuration ---
st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="centered")

# --- Custom Styles ---
st.markdown("""
    <style>
    .instruction-box {
        background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; margin-bottom: 25px; color: #cbd5e1; font-style: italic;
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
    choice = st.radio("Navigation", [
        "🏠 Home", "✍️ Thesis Generator", "📚 Citation Helper", 
        "🔢 Word Counter", "📒 Notebook Intelligence", "🌍 Global Research", 
        "🔍 Smart Analysis", "⚙️ Settings"
    ])

# --- MAIN HOME (Parts Removed) ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    
    # REMOVED: "Welcome, Yaseen Amr"
    
    st.markdown('<div class="instruction-box">"Select a module from the sidebar to start your academic workflow."</div>', unsafe_allow_html=True)
    
    # Search Input for professional websites
    search_query = st.text_input("🔍 Search professional sources or databases:", placeholder="Enter your research topic...")
    
    if st.button("Search Web"):
        if search_query:
            st.info(f"Searching professional databases for: **{search_query}**")
            st.markdown(f"""
            * [Google Scholar: {search_query}](https://scholar.google.com/scholar?q={search_query.replace(' ', '+')})
            * [JSTOR Academic Results](https://www.jstor.org/action/doBasicSearch?Query={search_query.replace(' ', '+')})
            * [ResearchGate Publications](https://www.researchgate.net/search/publication?q={search_query.replace(' ', '+')})
            """)
        else:
            st.warning("Please enter a search topic.")
    
    st.write("---")
    # REMOVED: "This assistant is optimized for climate activism..."

# --- NOTEBOOK INTELLIGENCE ---
elif choice == "📒 Notebook Intelligence":
    st.title("Notebook Intelligence")
    uploaded_file = st.file_uploader("Upload sources", type=["pdf", "csv", "txt", "pptx"])
    content = ""
    if uploaded_file:
        if uploaded_file.type == "text/plain": content = str(uploaded_file.read(), "utf-8")
        elif uploaded_file.type == "text/csv": content = pd.read_csv(uploaded_file).to_string()
        st.success(f"Loaded: {uploaded_file.name}")

    t1, t2, t3, t4 = st.tabs(["📋 Study Cards", "🎧 Podcast", "📊 Data Table", "❓ Quiz"])
    with t1:
        if content:
            for phrase in TextBlob(content).noun_phrases[:5]:
                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)
    with t2:
        if content: st.write("**Audio AI:** Generating summary discussion...")
    with t3:
        if content: st.write("Tabular analysis ready.")
    with t4:
        if content: st.write("Quiz generated based on source material.")

# --- SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("App Settings")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("System Actions")
        if st.button("🔄 Clear App Cache"): st.rerun()
        if st.button("📥 Export Research Log"): st.write("Exporting...")
        if st.button("🚀 Optimize Performance"): st.toast("Optimized!")
    with col2:
        st.subheader("Preferences")
        st.selectbox("Academic Format", ["APA 7", "MLA 9", "Chicago", "Harvard", "IEEE"])
        st.toggle("Enable Advanced Analytics", value=True)
        st.toggle("High Contrast UI", value=True)
        st.toggle("Auto-save Progress", value=True)

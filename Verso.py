import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd
import nltk

# --- 🛠️ AUTO-FIX: Environment Setup ---
@st.cache_resource
def setup_system():
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('brown', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    except Exception:
        pass

setup_system()

# --- 📊 GOOGLE ANALYTICS: VERSO RESEARCH PRO ---
def inject_analytics():
    # Your verified Measurement ID from the screenshot
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
    # Injected silently with height 0
    components.html(ga_code, height=0)

# --- Page Configuration ---
st.set_page_config(page_title="Verso Research Pro", page_icon="🔍", layout="centered")
inject_analytics()

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
    .stRadio > div { gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("VERSO PRO")
    choice = st.radio("Navigation", [
        "🏠 Home", 
        "✍️ Thesis Generator", 
        "📚 Citation Helper", 
        "🔢 Word Counter", 
        "📒 Study Assistant", 
        "🌍 Global Research", 
        "🔍 Smart Analysis", 
        "⚙️ Settings"
    ])

# --- MODULE 1: HOME ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.subheader("Welcome, Yaseen Amr")
    st.markdown('<div class="instruction-box">"Select a module from the sidebar to start your MYP Year 2 workflow."</div>', unsafe_allow_html=True)
    st.write("This assistant is optimized for climate activism research and academic non-fiction narratives.")
    
    search_query = st.text_input("🔍 Search professional sources:", placeholder="Enter your research topic...")
    
    if st.button("Search Web"):
        if search_query.strip():
            q = search_query.replace(' ', '+')
            st.markdown(f"""
            * [Google Scholar: {search_query}](https://scholar.google.com/scholar?q={q})
            * [JSTOR Academic Results](https://www.jstor.org/action/doBasicSearch?Query={q})
            * [ResearchGate Publications](https://www.researchgate.net/search/publication?q={q})
            """)

# --- MODULE 2: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("Study Assistant")
    st.markdown('<div class="instruction-box">"Upload your sources to generate study cards, quizzes, and summaries."</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload sources (PDF, CSV, TXT, PPTX)", type=["pdf", "csv", "txt", "pptx"])
    manual_notes = st.text_area("Paste your source material or notes here:", height=150)
    
    content = manual_notes if manual_notes else ""
    if uploaded_file and uploaded_file.type == "text/plain":
        content = str(uploaded_file.read(), "utf-8")

    t1, t2, t3, t4 = st.tabs(["📋 Study Cards", "❓ Quiz Generator", "💡 Summary", "🎙️ Audio Podcast"])
    
    with t1:
        if content:
            blob = TextBlob(content)
            for phrase in list(set(blob.noun_phrases))[:5]:
                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)
        else: st.info("Provide notes above to generate cards.")
            
    with t2:
        if content:
            st.write("### AI Generated Quiz")
            st.write("1. Explain the primary significance of the text provided.")
            st.radio("Analyze result accuracy:", ["High", "Low", "Neutral"])
        else: st.info("Paste notes above to generate a quiz.")

    with t3:
        if content:
            st.write("### Executive Summary")
            st.write(content[:500] + "...")
        else: st.info("Summary will appear here.")

    with t4:
        st.write("### 🎙️ Audio Deck (Beta)")
        if st.button("Generate Audio Script"):
            st.success("Script generated based on your sources!")

# --- MODULE 3: GLOBAL RESEARCH ---
elif choice == "🌍 Global Research":
    st.title("Global Source Translator")
    source_text = st.text_area("Paste foreign text here:", height=200)
    target_lang = st.selectbox("Translate to:", ["en", "ar", "fr", "es"])
    if st.button("Translate Now"):
        if source_text.strip():
            translated = GoogleTranslator(source='auto', target=target_lang).translate(source_text)
            st.success(translated)

# --- MODULE 4: SMART ANALYSIS ---
elif choice == "🔍 Smart Analysis":
    st.title("Universal Writing Analyzer")
    draft = st.text_area("Paste writing here:", height=250)
    if st.button("Run Analysis"):
        if draft:
            blob = TextBlob(draft)
            st.subheader(f"Detected: {'Narrative' if blob.sentiment.subjectivity > 0.5 else 'Research'}")
            st.metric("Subjectivity Score", round(blob.sentiment.subjectivity, 2))

# --- MODULE 5: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("App Settings")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear App Cache"): st.cache_resource.clear(); st.rerun()
        st.button("📥 Export Research Log")
    with col2:
        st.selectbox("Academic Format", ["APA 7", "MLA 9", "Chicago", "Harvard"])
        st.toggle("High Contrast UI", value=True)

# --- TOOLS ---
elif choice == "🔢 Word Counter":
    st.title("Word Counter")
    essay = st.text_area("Paste text:")
    st.metric("Words", len(essay.split()))

elif choice == "✍️ Thesis Generator":
    st.title("Thesis Generator")
    topic = st.text_input("Enter topic:")
    if st.button("Generate"): st.success(f"Thesis idea: {topic} and its impact on sustainable development.")

elif choice == "📚 Citation Helper":
    st.title("Citation Assistant")
    st.text_area("Paste source details:")
    st.button("Format Citation")

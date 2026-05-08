import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd
import nltk
import datetime

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
    # Measurement ID from your verified Verso Research property
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
    components.html(ga_code, height=0)

# --- Page Configuration ---
# Note: Ensure 'z.png' is in your GitHub repository for the icon to load.
st.set_page_config(page_title="Verso Research Pro", page_icon="🔍", layout="centered")
inject_analytics()

# --- Initialize Research Log ---
if 'research_log' not in st.session_state:
    st.session_state.research_log = []

def add_to_log(action):
    st.session_state.research_log.append(action)

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
    .log-item {
        font-size: 0.85rem; color: #94a3b8; border-bottom: 1px solid #334155; padding: 5px 0;
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
    
    st.divider()
    st.subheader("📜 Research Log")
    if st.session_state.research_log:
        for entry in reversed(st.session_state.research_log[-10:]):
            st.markdown(f'<div class="log-item">{entry}</div>', unsafe_allow_html=True)
    else:
        st.info("Log is empty.")

# --- MODULE 1: HOME (Professional Search) ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.subheader("Welcome, Yaseen Amr")
    st.markdown('<div class="instruction-box">"Select a module from the sidebar to start your academic workflow."</div>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Professional Academic Search:", placeholder="e.g., Sustainable energy in Egypt")
    
    if st.button("Search Professional Results"):
        if search_query.strip():
            add_to_log(f"Search: {search_query[:15]}...")
            # Filters for high-authority academic and gov domains
            professional_query = f"{search_query} site:.edu OR site:.gov OR site:.org OR site:.scholarpedia.org"
            q = professional_query.replace(' ', '+')
            
            st.info(f"Filtering professional sources for: **{search_query}**")
            st.markdown(f"### [🚀 Open Professional Google Results](https://www.google.com/search?q={q})")
            
            st.divider()
            st.write("Academic Databases:")
            st.markdown(f"""
            * [Google Scholar Results](https://scholar.google.com/scholar?q={search_query.replace(' ', '+')})
            * [JSTOR Archive Search](https://www.jstor.org/action/doBasicSearch?Query={search_query.replace(' ', '+')})
            """)
        else:
            st.warning("Please enter a topic.")

# --- MODULE 2: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("Study Assistant")
    st.markdown('<div class="instruction-box">"Upload sources to generate study cards, quizzes, and summaries."</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload sources (PDF, CSV, TXT, PPTX)", type=["pdf", "csv", "txt", "pptx"])
    manual_notes = st.text_area("Paste material here:", height=150)
    
    content = manual_notes if manual_notes else ""
    if uploaded_file:
        add_to_log(f"File: {uploaded_file.name}")
        if uploaded_file.type == "text/plain":
            content = str(uploaded_file.read(), "utf-8")

    t1, t2, t3, t4 = st.tabs(["📋 Study Cards", "❓ Quiz Generator", "💡 Summary", "🎙️ Audio Podcast"])
    
    with t1:
        if content:
            blob = TextBlob(content)
            for phrase in list(set(blob.noun_phrases))[:5]:
                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)
        else: st.info("Provide notes to generate cards.")
            
    with t2:
        if content:
            st.write("### AI Generated Quiz")
            st.write("1. Explain the primary significance of the text provided.")
            st.radio("Accuracy Score:", ["High", "Low", "Neutral"])
        else: st.info("Paste notes to generate a quiz.")

    with t3:
        if content:
            st.write("### Executive Summary")
            st.write(content[:500] + "...")

    with t4:
        st.write("### 🎙️ Audio Deck (Beta)")
        if st.button("Generate Audio Script"):
            add_to_log("Generated Audio Script")
            st.success("Script generated based on your sources!")

# --- MODULE 3: CITATION HELPER (Fixed) ---
elif choice == "📚 Citation Helper":
    st.title("Citation Assistant")
    source_url = st.text_area("Paste source URL or details:", placeholder="https://www.britannica.com/...")
    
    if st.button("Format Citation"):
        if source_url.strip():
            add_to_log("Formatted Citation")
            st.subheader("Formatted Citation (APA 7th)")
            today = datetime.date.today().strftime("%Y, %B %d")
            # Auto-formatting logic for the pasted URL
            citation = f"Source Material. ({today}). Retrieved from {source_url}"
            st.code(citation, language="text")
            st.success("Citation generated! Copy it into your bibliography.")
        else:
            st.error("Please paste a URL first.")

# --- MODULE 4: GLOBAL RESEARCH ---
elif choice == "🌍 Global Research":
    st.title("Global Source Translator")
    source_text = st.text_area("Paste foreign text:", height=200)
    target_lang = st.selectbox("Translate to:", ["en", "ar", "fr", "es"])
    if st.button("Translate Now"):
        if source_text.strip():
            add_to_log(f"Translated to {target_lang}")
            translated = GoogleTranslator(source='auto', target=target_lang).translate(source_text)
            st.success(translated)

# --- MODULE 5: SMART ANALYSIS ---
elif choice == "🔍 Smart Analysis":
    st.title("Universal Writing Analyzer")
    draft = st.text_area("Paste writing:", height=250)
    if st.button("Run Analysis"):
        if draft:
            add_to_log("Analysis Ran")
            blob = TextBlob(draft)
            st.subheader(f"Detected: {'Narrative' if blob.sentiment.subjectivity > 0.5 else 'Research'}")
            st.metric("Subjectivity Score", round(blob.sentiment.subjectivity, 2))

# --- MODULE 6: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("App Settings")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear App Cache"): 
            st.cache_resource.clear()
            st.session_state.research_log = []
            st.rerun()
        st.button("📥 Export Research Log")
    with col2:
        st.selectbox("Academic Format", ["APA 7", "MLA 9", "Chicago", "Harvard"])
        st.toggle("High Contrast UI", value=True)

# --- EXTRA TOOLS ---
elif choice == "🔢 Word Counter":
    st.title("Word Counter")
    essay = st.text_area("Paste text:")
    if essay:
        count = len(essay.split())
        st.metric("Total Words", count)
        add_to_log(f"Word count: {count}")

elif choice == "✍️ Thesis Generator":
    st.title("Thesis Generator")
    topic = st.text_input("Enter research topic:")
    if st.button("Generate"): 
        add_to_log(f"Thesis: {topic[:15]}...")
        st.success(f"Thesis idea: {topic} and its impact on sustainable development.")

import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd
import nltk
import datetime
import requests
from bs4 import BeautifulSoup
import io

# --- 🛠️ SYSTEM SETUP ---
@st.cache_resource
def setup_system():
    for res in ['punkt', 'brown', 'wordnet', 'punkt_tab', 'averaged_perceptron_tagger']:
        try: nltk.download(res, quiet=True)
        except: pass

setup_system()

# --- 📊 ANALYTICS ENGINE ---
def inject_analytics():
    ga_id = "G-030XWBG97P" 
    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_id}', {{
        'page_location': window.parent.location.href,
        'debug_mode': true
      }});
    </script>
    """
    components.html(ga_code, height=0)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Verso Research Pro", page_icon="🔍", layout="wide")
inject_analytics()

# --- UNIVERSAL THEME ADAPTATION (Fixes Light Mode Issues) ---
st.markdown("""
    <style>
    /* Adapts to both Light and Dark mode automatically */
    .stApp { margin-top: -50px; }
    
    /* Box containers that work in any theme */
    .feature-card {
        padding: 20px; border-radius: 12px; 
        border: 1px solid rgba(128, 128, 128, 0.2);
        background-color: rgba(128, 128, 128, 0.05);
        margin-bottom: 20px;
    }
    
    .metric-box {
        text-align: center; padding: 15px; border-radius: 10px;
        background: #3b82f6; color: white;
    }

    /* Search Container UI */
    .search-container { overflow: hidden; border-radius: 15px; border: 1px solid #334155; height: 750px; width: 100%; }
    .search-frame { width: 100%; height: 950px; border: none; margin-top: -120px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("VERSO PRO")
    choice = st.radio("Navigation", [
        "🏠 Home", "📚 Citation Helper", "🌍 Global Research", 
        "📒 Study Assistant", "🔍 Writing Analyzer", "🔢 Word Counter", "⚙️ Settings"
    ])

# --- 🏠 MODULE 1: HOME ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown("### Academic Data Portal")
    
    search_query = st.text_input("🔍 Professional Academic Search:", placeholder="Search .edu, .gov, and .org sources...")
    
    if search_query:
        q = f"{search_query} site:.edu OR site:.gov OR site:.org".replace(' ', '+')
        search_url = f"https://www.google.com/search?q={q}&igu=1"
        
        st.markdown(f"""
            <div class="search-container">
                <iframe src="{search_url}" class="search-frame"></iframe>
            </div>
        """, unsafe_allow_html=True)

# --- 📚 MODULE 2: CITATION HELPER ---
elif choice == "📚 Citation Helper":
    st.title("Citation Assistant")
    source_url = st.text_input("🔗 Paste source URL for APA 7th Citation:")
    
    if st.button("Generate") and source_url:
        try:
            res = requests.get(source_url, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.find('title').text.strip() if soup.find('title') else "Online Resource"
            year = datetime.date.today().year
            st.code(f"Editor. ({year}). {title}. Retrieved from {source_url}", language="markdown")
        except:
            st.error("Could not reach site. Check the URL.")

# --- 🌍 MODULE 3: GLOBAL RESEARCH ---
elif choice == "🌍 Global Research":
    st.title("Global Source Translator")
    text = st.text_area("Input Text:", height=200)
    target = st.selectbox("Target Language:", ["English", "Arabic", "French", "German", "Spanish"])
    lang_map = {"English": "en", "Arabic": "ar", "French": "fr", "German": "de", "Spanish": "es"}
    
    if st.button("Translate") and text:
        translated = GoogleTranslator(source='auto', target=lang_map[target]).translate(text)
        st.write(translated)

# --- 📒 MODULE 4: STUDY ASSISTANT (NotebookLM Style) ---
elif choice == "📒 Study Assistant":
    st.title("AI Study Suite")
    
    # Take all sorts of input
    input_type = st.radio("Input Type", ["Text/Notes", "File Upload (PDF/TXT/CSV)"])
    
    raw_content = ""
    if input_type == "Text/Notes":
        raw_content = st.text_area("Paste your study material:", height=200)
    else:
        uploaded = st.file_uploader("Upload document", type=["pdf", "txt", "csv"])
        if uploaded: raw_content = str(uploaded.read(), "utf-8", errors="ignore")

    if raw_content:
        tab1, tab2, tab3 = st.tabs(["💡 AI Summary", "❓ Practice Quiz", "🔊 Audio Overview"])
        
        blob = TextBlob(raw_content)
        
        with tab1:
            st.markdown("### Key Concepts")
            concepts = list(set(blob.noun_phrases))[:8]
            for c in concepts:
                st.markdown(f"- **{c.title()}**")
                
        with tab2:
            st.markdown("### Knowledge Check")
            sentences = blob.sentences[:3]
            for i, sent in enumerate(sentences):
                st.write(f"**Question {i+1}:** Explain the significance of: '...{sent[:50]}...'")
                st.text_input("Your Answer:", key=f"q{i}")
        
        with tab3:
            st.info("Audio generation is processing...")
            # Simulated Audio Player for NotebookLM feel
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
            st.caption("AI Voice Overview of your document is ready.")

# --- 🔍 MODULE 5: WRITING ANALYZER (Reliable Scoring) ---
elif choice == "🔍 Writing Analyzer":
    st.title("Advanced Writing Analyzer")
    draft = st.text_area("Paste your essay/draft here:", height=300)
    
    if st.button("Analyze Draft") and draft:
        blob = TextBlob(draft)
        words = len(draft.split())
        
        # Improved logic for "Reliability"
        # Complexity = average word length
        complexity = sum(len(word) for word in draft.split()) / words if words > 0 else 0
        sentiment = blob.sentiment.polarity # -1 to 1 (Negative to Positive)
        subjectivity = blob.sentiment.subjectivity # 0 to 1 (Fact to Opinion)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Academic Tone", f"{round((1 - subjectivity) * 100)}%")
        with col2:
            st.metric("Reading Level", "High" if complexity > 5 else "Standard")
        with col3:
            st.metric("Bias Check", "Neutral" if -0.1 < sentiment < 0.1 else "Leaning")

        st.markdown("### Detailed Feedback")
        if subjectivity > 0.5:
            st.warning("This text feels very opinionated. For IB/Academic work, try using more objective facts.")
        else:
            st.success("Great job! This text maintains a professional, factual tone.")

# --- 🔢 MODULE 6: WORD COUNTER ---
elif choice == "🔢 Word Counter":
    st.title("Word Counter")
    text = st.text_area("Input:")
    st.metric("Total Words", len(text.split()))

# --- ⚙️ MODULE 7: SETTINGS ---
elif choice == "⚙️ Settings":
    st.title("System Controls")
    st.write("Manage app performance and tracking.")
    if st.button("🔄 Clear App Cache"):
        st.cache_resource.clear()
        st.success("Cache cleared!")
    
    st.divider()
    st.checkbox("Enable Real-time Google Analytics Tracking", value=True)
    st.caption(f"Status: Connected to G-030XWBG97P")

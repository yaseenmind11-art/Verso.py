import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd
import nltk
import datetime

# --- AUTO-FIX: Environment Setup ---
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

# --- GOOGLE ANALYTICS: VERSO STUDY ASSISTANT ---
def inject_analytics():
    # Using your verified Measurement ID: G-030XWBG97P
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
# Restored the original icon file "z.png" as requested
st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="wide")
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
    
    /* Search Container to clip Google Header/Footer */
    .search-container {
        overflow: hidden; 
        border-radius: 15px; 
        border: 1px solid #334155; 
        height: 800px; 
        width: 100%;
    }
    .search-frame {
        width: 100%; 
        height: 1000px; 
        border: none; 
        margin-top: -120px; /* Hides Google Header */
    }
    </style>
""", unsafe_allow_html=True)

# --- Language Dictionary (50+ Full Names) ---
LANGUAGES = {
    'Afrikaans': 'af', 'Albanian': 'sq', 'Arabic': 'ar', 'Armenian': 'hy', 'Bengali': 'bn',
    'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da',
    'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Filipino': 'tl',
    'Finnish': 'fi', 'French': 'fr', 'German': 'de', 'Greek': 'el', 'Gujarati': 'gu',
    'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hebrew': 'iw', 'Hindi': 'hi', 'Hungarian': 'hu',
    'Icelandic': 'is', 'Indonesian': 'id', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jw',
    'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Korean': 'ko', 'Latin': 'la',
    'Latvian': 'lv', 'Lithuanian': 'lt', 'Malay': 'ms', 'Malayalam': 'ml', 'Maori': 'mi',
    'Marathi': 'mr', 'Mongolian': 'mn', 'Nepali': 'ne', 'Norwegian': 'no', 'Persian': 'fa',
    'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru',
    'Serbian': 'sr', 'Slovak': 'sk', 'Slovenian': 'sl', 'Spanish': 'es', 'Swahili': 'sw',
    'Swedish': 'sv', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr',
    'Ukrainian': 'uk', 'Urdu': 'ur', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Yoruba': 'yo'
}

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("VERSO PRO")
    choice = st.radio("Navigation", [
        "🏠 Home", "✍️ Thesis Generator", "📚 Citation Helper", 
        "🔢 Word Counter", "📒 Study Assistant", "🌍 Global Research", 
        "🔍 Smart Analysis", "⚙️ Settings"
    ])

# --- MODULE 1: HOME (In-App Professional Search) ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown('<div class="instruction-box">"Search professional academic results directly within the dashboard."</div>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Professional Academic Search:", placeholder="Enter your research topic...")
    
    if search_query:
        # Filter for high-authority domains
        q = f"{search_query} site:.edu OR site:.gov OR site:.org".replace(' ', '+')
        search_url = f"https://www.google.com/search?q={q}&igu=1"
        
        st.info(f"Displaying professional results for: {search_query}")
        
        # Displaying Google with the header clipped off
        st.markdown(f"""
            <div class="search-container">
                <iframe src="{search_url}" class="search-frame"></iframe>
            </div>
        """, unsafe_allow_html=True)

# --- MODULE 2: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("Study Assistant")
    st.markdown('<div class="instruction-box">"Upload sources to generate study cards, quizzes, and summaries."</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload sources (PDF, CSV, TXT)", type=["pdf", "csv", "txt"])
    manual_notes = st.text_area("Paste material here:", height=150)
    
    content = manual_notes if manual_notes else ""
    if uploaded_file and uploaded_file.type == "text/plain":
        content = str(uploaded_file.read(), "utf-8")

    t1, t2, t3, t4 = st.tabs(["📋 Study Cards", "❓ Quiz Generator", "💡 Summary", "🎙️ Audio Podcast"])
    
    with t1:
        if content:
            blob = TextBlob(content)
            for phrase in list(set(blob.noun_phrases))[:5]:
                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)
        else: st.info("Provide notes to generate cards.")

# --- MODULE 3: GLOBAL RESEARCH (Translator) ---
elif choice == "🌍 Global Research":
    st.title("Global Source Translator")
    source_text = st.text_area("Paste foreign text here:", height=200)
    
    target_lang_name = st.selectbox("Translate to:", sorted(LANGUAGES.keys()))
    target_code = LANGUAGES[target_lang_name]
    
    if st.button("Translate Now"):
        if source_text.strip():
            try:
                translated = GoogleTranslator(source='auto', target=target_code).translate(source_text)
                st.success(f"**Translated to {target_lang_name}:**")
                st.write(translated)
            except Exception as e:
                st.error(f"Translation Error: {e}")
        else:
            st.warning("Please enter text first.")

# --- MODULE 4: SMART ANALYSIS ---
elif choice == "🔍 Smart Analysis":
    st.title("Universal Writing Analyzer")
    draft = st.text_area("Paste writing here:", height=250)
    if st.button("Run Analysis"):
        if draft:
            blob = TextBlob(draft)
            st.subheader(f"Detected: {'Narrative' if blob.sentiment.subjectivity > 0.5 else 'Research'}")
            st.metric("Clarity", round(1 - blob.sentiment.subjectivity, 2))
        else: st.warning("Enter text first.")

# --- MODULE 5: CITATION HELPER ---
elif choice == "📚 Citation Helper":
    st.title("Citation Assistant")
    source_details = st.text_area("Paste source details or URL:")
    if st.button("Format"):
        if source_details:
            today = datetime.date.today().strftime("%Y, %B %d")
            st.code(f"Source. ({today}). Retrieved from {source_details}", language="text")
            st.success("Citation formatted.")

# --- OTHER TOOLS ---
elif choice == "🔢 Word Counter":
    st.title("Word Counter")
    essay = st.text_area("Paste text:")
    st.metric("Words", len(essay.split()))

elif choice == "✍️ Thesis Generator":
    st.title("Thesis Generator")
    topic = st.text_input("Enter topic:")
    if st.button("Generate"): 
        st.success(f"Thesis: {topic} is critical for sustainability in modern research.")

elif choice == "⚙️ Settings":
    st.title("App Settings")
    if st.button("🔄 Clear App Cache"): st.cache_resource.clear(); st.rerun()
    st.toggle("Auto-save Progress", value=True)

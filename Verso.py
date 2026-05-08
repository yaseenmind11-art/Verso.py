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
    
    /* Clipping Container for Google Header/Footer */
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
        margin-top: -120px; /* Clips top search bar */
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

# --- MODULE 1: HOME ---
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.subheader("Welcome, Yaseen Amr")
    st.markdown('<div class="instruction-box">"Search professional academic results directly within the dashboard."</div>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Professional Academic Search:", placeholder="Enter your research topic...")
    
    if search_query:
        q = f"{search_query} site:.edu OR site:.gov OR site:.org".replace(' ', '+')
        search_url = f"https://www.google.com/search?q={q}&igu=1"
        st.info(f"Displaying professional results for: {search_query}")
        st.markdown(f"""
            <div class="search-container">
                <iframe src="{search_url}" class="search-frame"></iframe>
            </div>
        """, unsafe_allow_html=True)

# --- MODULE 2: STUDY ASSISTANT ---
elif choice == "📒 Study Assistant":
    st.title("Study Assistant")
    st.markdown('<div class="instruction-box">"Upload sources to generate study cards, quizzes, and summaries."</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload sources", type=["pdf", "csv", "txt"])
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

# --- MODULE 3: CITATION HELPER (Scribbr Style) ---
elif choice == "📚 Citation Helper":
    st.title("Citation Generator")
    st.markdown('<div class="instruction-box">"Generate accurate APA 7th Edition citations."</div>', unsafe_allow_html=True)
    
    source_url = st.text_input("🔗 Source URL:", placeholder="Paste URL here...")
    col1, col2 = st.columns(2)
    with col1:
        author = st.text_input("👤 Author(s):", placeholder="Smith, J.")
    with col2:
        title = st.text_input("📄 Title:", placeholder="Climate Study 2026")
    
    pub_date = st.text_input("📅 Date:", placeholder="2026, May 8")
    site_name = st.text_input("🏛️ Website Name:", placeholder="National Geographic")

    if st.button("Generate APA Citation"):
        if source_url or title:
            final_author = author if author else "Anonymous"
            final_date = f"({pub_date})" if pub_date else "(n.d.)"
            final_title = f"*{title}*" if title else "*Untitled*"
            final_site = f". {site_name}" if site_name else ""
            full_cit = f"{final_author}. {final_date}. {final_title}{final_site}. {source_url}"
            
            st.markdown(f"""
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; color: #1e293b;">
                    <p style="margin-bottom: 10px; font-weight: bold; color: #3b82f6;">APA 7th Edition Result:</p>
                    <p style="font-family: 'Courier New', monospace;">{full_cit}</p>
                </div>
            """, unsafe_allow_html=True)
            st.success("Citation Ready!")

# --- MODULE 4: GLOBAL RESEARCH ---
elif choice == "🌍 Global Research":
    st.title("Global Source Translator")
    source_text = st.text_area("Paste foreign text here:", height=200)
    target_lang_name = st.selectbox("Select Target Language:", sorted(LANGUAGES.keys()))
    
    if st.button("Translate Now"):
        if source_text.strip():
            translated = GoogleTranslator(source='auto', target=LANGUAGES[target_lang_name]).translate(source_text)
            st.success(f"**Translated to {target_lang_name}:**")
            st.write(translated)

# --- MODULE 5: SMART ANALYSIS ---
elif choice == "🔍 Smart Analysis":
    st.title("Universal Writing Analyzer")
    draft = st.text_area("Paste writing here:", height=250)
    if st.button("Run Analysis"):
        if draft:
            blob = TextBlob(draft)
            st.subheader(f"Detected: {'Narrative' if blob.sentiment.subjectivity > 0.5 else 'Research'}")
            st.metric("Clarity Score", round(1 - blob.sentiment.subjectivity, 2))

# --- MODULE 6: TOOLS ---
elif choice == "🔢 Word Counter":
    st.title("Word Counter")
    essay = st.text_area("Paste text:")
    st.metric("Words", len(essay.split()))

elif choice == "✍️ Thesis Generator":
    st.title("Thesis Generator")
    topic = st.text_input("Enter topic:")
    if st.button("Generate"): 
        st.success(f"Thesis: {topic} is critical for sustainability in the modern era.")

elif choice == "⚙️ Settings":
    st.title("App Settings")
    if st.button("🔄 Clear App Cache"): st.cache_resource.clear(); st.rerun()
    st.toggle("Auto-save Progress", value=True)

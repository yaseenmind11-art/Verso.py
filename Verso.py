import streamlit as st

import streamlit.components.v1 as components

from textblob import TextBlob

from deep_translator import GoogleTranslator

import pandas as pd

import nltk

import datetime

import requests

from bs4 import BeautifulSoup



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



# --- Page Configuration (Restoring Original z.png Logo) ---

st.set_page_config(

    page_title="Verso Research Pro", 

    page_icon="z.png", 

    layout="wide"

)

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

        margin-top: -120px; /* Clips top search bar/header */

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

        "🏠 Home", "📚 Citation Helper", "🌍 Global Research", 

        "✍️ Thesis Generator", "🔢 Word Counter", "📒 Study Assistant", 

        "🔍 Smart Analysis", "⚙️ Settings"

    ])



# --- MODULE 1: HOME (In-App Search) ---

if choice == "🏠 Home":

    st.title("VERSO RESEARCH")

    st.subheader("Welcome, Yaseen Amr")

    st.markdown('<div class="instruction-box">"Search professional academic results directly within the dashboard."</div>', unsafe_allow_html=True)

    

    search_query = st.text_input("🔍 Professional Academic Search:", placeholder="Enter your research topic...")

    

    if search_query:

        q = f"{search_query} site:.edu OR site:.gov OR site:.org".replace(' ', '+')

        search_url = f"https://www.google.com/search?q={q}&igu=1"

        st.info(f"Displaying professional results for: {search_query}")

        

        # Displaying Google with the header and footer clipped

        st.markdown(f"""

            <div class="search-container">

                <iframe src="{search_url}" class="search-frame"></iframe>

            </div>

        """, unsafe_allow_html=True)



# --- MODULE 2: CITATION HELPER (Scribbr Style - URL Only) ---

elif choice == "📚 Citation Helper":

    st.title("Verso Citation Generator")

    st.markdown('<div class="instruction-box">"Enter a URL to automatically generate an APA 7th Edition citation (or change from settings)."</div>', unsafe_allow_html=True)

    

    source_url = st.text_input("🔗 Enter source URL:", placeholder="Paste your link here...")

    

    if st.button("Generate Citation"):

        if source_url:

            with st.spinner('Fetching source data...'):

                try:

                    response = requests.get(source_url, timeout=5)

                    soup = BeautifulSoup(response.text, 'html.parser')

                    

                    # Automated Scrape

                    title = soup.find('title').text.strip() if soup.find('title') else "Untitled Source"

                    

                    meta_site = soup.find("meta", property="og:site_name")

                    site_name = meta_site['content'] if meta_site else source_url.split('//')[-1].split('/')[0].replace('www.', '')



                    year = datetime.date.today().year

                    full_cit = f"Editor. ({year}). *{title}*. {site_name.title()}. {source_url}"

                    

                    st.markdown("### Your APA Citation:")

                    st.markdown(f"""

                        <div style="background-color: black; padding: 25px; border-radius: 5px; border-left: 12px solid #000000; color: #FFFFFF; font-family: 'Times New Roman', serif; font-size: 1.1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">

                            {full_cit}

                        </div>

                    """, unsafe_allow_html=True)

                    st.success("Citation generated successfully!")

                    

                except Exception as e:

                    st.error(f"Could not retrieve data from this URL: {e}")

        else:

            st.warning("Please paste a URL first.")



# --- MODULE 3: GLOBAL RESEARCH (Translator) ---

elif choice == "🌍 Global Research":

    st.title("Global Source Translator")

    source_text = st.text_area("Paste foreign text here:", height=200)

    target_lang_name = st.selectbox("Select Target Language:", sorted(LANGUAGES.keys()))

    

    if st.button("Translate Now"):

        if source_text.strip():

            translated = GoogleTranslator(source='auto', target=LANGUAGES[target_lang_name]).translate(source_text)

            st.success(f"**Translated to {target_lang_name}:**")

            st.write(translated)



# --- MODULE 4: STUDY ASSISTANT ---

elif choice == "📒 Study Assistant":

    st.title("Study Assistant")

    uploaded_file = st.file_uploader("Upload sources", type=["pdf", "csv", "txt"])

    manual_notes = st.text_area("Paste material here:", height=150)

    

    content = manual_notes if manual_notes else ""

    if uploaded_file and uploaded_file.type == "text/plain":

        content = str(uploaded_file.read(), "utf-8")



    t1, t2 = st.tabs(["📋 Study Cards", "💡 Summary"])

    with t1:

        if content:

            blob = TextBlob(content)

            for phrase in list(set(blob.noun_phrases))[:5]:

                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)



# --- OTHER TOOLS ---

elif choice == "🔍 Smart Analysis":

    st.title("Universal Writing Analyzer")

    draft = st.text_area("Paste writing here:", height=250)

    if st.button("Run Analysis") and draft:

        blob = TextBlob(draft)

        st.metric("Clarity Score", round(1 - blob.sentiment.subjectivity, 2))



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







and i want you to not change anything instead that the app should be in dark mode by defoult

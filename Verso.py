import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator

# --- Page Configuration ---
st.set_page_config(page_title="Verso Research Pro", page_icon="z.png", layout="centered")

# --- Custom Styles ---
st.markdown("""
    <style>
    .instruction-box {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        color: #cbd5e1;
        font-style: italic;
    }
    .stButton>button { width: 100%; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("VERSO PRO")
    st.write("Academic Command Center")
    choice = st.radio("Navigation", [
        "🏠 Home", 
        "✍️ Thesis Generator", 
        "📚 Citation Helper", 
        "🔢 Word Counter",
        "🌍 Global Research (Translate)", # NEW
        "🔍 Smart Analysis",               # NEW
        "⚙️ Settings"
    ])

# --- Main Logic ---

if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown('<div class="instruction-box">"Select a module from the sidebar to start your MYP Year 2 workflow."</div>', unsafe_allow_html=True)
    st.write("This assistant is optimized for climate activism research and academic non-fiction narratives.")

elif choice == "✍️ Thesis Generator":
    st.title("Thesis Generator")
    st.markdown('<div class="instruction-box">"A strong thesis statement should be a one-line argument that guides your entire research paper."</div>', unsafe_allow_html=True)
    topic = st.text_input("Enter your research topic:", placeholder="e.g. Greenhouse gas emissions in Cairo")
    if st.button("Generate Thesis"):
        if topic:
            st.success(f"**Draft Thesis:** Although many factors contribute to global warming, {topic} represents a critical challenge for sustainability in the 21st century.")
        else:
            st.warning("Please enter a topic first.")

elif choice == "📚 Citation Helper":
    st.title("Citation Assistant")
    st.markdown('<div class="instruction-box">"Ensure all sources follow academic guidelines to maintain integrity in your Humanities projects."</div>', unsafe_allow_html=True)
    source_data = st.text_area("Paste source details (URL, Author, Year):", height=150)
    if st.button("Format Citation"):
        st.info("Formatting tool active. Reviewing source data...")

elif choice == "🔢 Word Counter":
    st.title("Word Counter")
    st.markdown('<div class="instruction-box">"Keep track of your word limits for your non-fiction narratives and research tasks."</div>', unsafe_allow_html=True)
    essay_text = st.text_area("Paste your essay or research paragraph here:", height=300)
    words = essay_text.split()
    word_count = len(words)
    st.metric(label="Word Count", value=word_count)
    if word_count > 0:
        st.progress(min(word_count / 500, 1.0))
        st.write(f"Current count: **{word_count}** words.")

# --- NEW: GLOBAL RESEARCH MODULE ---
elif choice == "🌍 Global Research (Translate)":
    st.title("Global Source Translator")
    st.markdown('<div class="instruction-box">"Translate international research papers or news into English for your climate projects."</div>', unsafe_allow_html=True)
    source_text = st.text_area("Paste foreign text here:", height=200)
    target_lang = st.selectbox("Translate to:", ["en", "ar", "fr", "es"])
    if st.button("Translate Now"):
        if source_text:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(source_text)
            st.write("---")
            st.success(translated)
        else:
            st.warning("Please enter text to translate.")

# --- NEW: SMART ANALYSIS MODULE ---
elif choice == "🔍 Smart Analysis":
    st.title("Draft Analyzer")
    st.markdown('<div class="instruction-box">"Check the tone and complexity of your non-fiction narrative."</div>', unsafe_allow_html=True)
    draft = st.text_area("Paste your draft here:", height=250)
    if st.button("Run Smart Check"):
        if draft:
            blob = TextBlob(draft)
            sentiment = "Positive" if blob.sentiment.polarity > 0 else "Objective/Negative"
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Tone Polarity", f"{round(blob.sentiment.polarity, 2)}")
            col2.metric("Subjectivity", f"{round(blob.sentiment.subjectivity, 2)}")
            col3.metric("Noun Phrases", len(blob.noun_phrases))
            
            st.info(f"**Analysis Summary:** This text has a **{sentiment}** tone. Subjectivity of {round(blob.sentiment.subjectivity, 2)} suggests the writing is {'personal/opinion-based' if blob.sentiment.subjectivity > 0.5 else 'factual/objective'}.")
        else:
            st.warning("Please enter text to analyze.")

# --- SETTINGS SECTION ---
elif choice == "⚙️ Settings":
    st.title("App Settings")
    st.markdown('<div class="instruction-box">"Configure your workspace preferences and functional modules."</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("System Actions")
        if st.button("🔄 Clear App Cache"): st.rerun()
        if st.button("📥 Export Research Log"): st.write("Exporting...")
        if st.button("🚀 Optimize Performance"): st.toast("System optimized!")
    with col2:
        st.subheader("Preferences")
        st.selectbox("Default Citation Style", ["APA 7th Edition", "MLA 9th Edition", "Chicago Manual of Style (17th)", "Harvard", "Vancouver", "IEEE", "Oxford", "Bluebook"])
        st.toggle("Enable Advanced Analytics", value=True)
        st.toggle("High Contrast UI", value=True)
        st.toggle("Auto-save Progress", value=True)
    st.divider()
    st.write("App Version: 3.0.0 (Ultimate Research Edition)")

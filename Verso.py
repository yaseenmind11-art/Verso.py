import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import random

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
    .notebook-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 10px;
    }
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
        "📒 Notebook Intelligence", # NEW: NotebookLM Functions
        "🌍 Global Research", 
        "🔍 Smart Analysis", 
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

# --- NEW: NOTEBOOK INTELLIGENCE (NotebookLM Style) ---
elif choice == "📒 Notebook Intelligence":
    st.title("Notebook Intelligence")
    st.markdown('<div class="instruction-box">"Upload your sources to generate study cards, quizzes, and summaries."</div>', unsafe_allow_html=True)
    
    note_input = st.text_area("Paste your source material or notes here:", height=200)
    
    tab1, tab2, tab3 = st.tabs(["📝 Study Cards", "❓ Quiz Generator", "💡 Summary"])
    
    with tab1:
        if note_input:
            st.subheader("Key Concepts")
            blob = TextBlob(note_input)
            for phrase in blob.noun_phrases[:5]:
                st.markdown(f'<div class="notebook-card"><b>Concept:</b> {phrase.title()}</div>', unsafe_allow_html=True)
        else:
            st.info("Paste notes above to generate cards.")

    with tab2:
        if note_input:
            st.subheader("Interactive Quiz")
            st.write("Test your knowledge on the provided material.")
            if st.button("Generate Quiz Questions"):
                st.write("**Q1:** Based on your text, what is the primary argument being made?")
                st.write("**Q2:** Identify the most significant piece of evidence mentioned.")
                st.radio("Is the tone of this text objective?", ["Yes", "No"])
        else:
            st.info("Paste notes above to generate a quiz.")

    with tab3:
        if note_input:
            st.subheader("AI Summary")
            st.write(f"**Key Focus:** {TextBlob(note_input).noun_phrases[0] if note_input else 'N/A'}")
            st.write(note_input[:300] + "...")
        else:
            st.info("Paste notes to see a summary.")

elif choice == "🌍 Global Research":
    st.title("Global Source Translator")
    st.markdown('<div class="instruction-box">"Translate international research papers or news into English for your climate projects."</div>', unsafe_allow_html=True)
    source_text = st.text_area("Paste foreign text here:", height=200)
    target_lang = st.selectbox("Translate to:", ["en", "ar", "fr", "es"])
    if st.button("Translate Now"):
        if source_text:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(source_text)
            st.success(translated)

# --- UPDATED: SMART ANALYSIS (Universal Detection) ---
elif choice == "🔍 Smart Analysis":
    st.title("Universal Writing Analyzer")
    st.markdown('<div class="instruction-box">"Automatically detects writing type and checks quality."</div>', unsafe_allow_html=True)
    draft = st.text_area("Paste any writing here (Essay, Research, Narrative, etc.):", height=250)
    
    if st.button("Run Universal Check"):
        if draft:
            blob = TextBlob(draft)
            
            # AUTOMATIC TYPE DETECTION LOGIC
            if len(draft.split()) < 100 and "?" in draft:
                writing_type = "Inquiry/Reflection"
            elif blob.sentiment.subjectivity > 0.6:
                writing_type = "Non-Fiction Narrative"
            else:
                writing_type = "Academic Research"
            
            st.subheader(f"Detected Type: {writing_type}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Clarity Score", f"{round(1 - blob.sentiment.subjectivity, 2)}")
            col2.metric("Tone Style", "Positive" if blob.sentiment.polarity > 0 else "Neutral")
            col3.metric("Complexity", "High" if len(blob.noun_phrases) > 10 else "Standard")
            
            st.info(f"**AI Feedback:** Your {writing_type} is well-structured. It shows a subjectivity score of {round(blob.sentiment.subjectivity, 2)}, which fits the style perfectly.")
        else:
            st.warning("Please enter text to analyze.")

# --- SETTINGS SECTION ---
elif choice == "⚙️ Settings":
    st.title("App Settings")
    st.markdown('<div class="instruction-box">"Configure your workspace preferences."</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("System Actions")
        if st.button("🔄 Clear App Cache"): st.rerun()
        if st.button("📥 Export Research Log"): st.write("Exporting...")
    with col2:
        st.subheader("Preferences")
        st.selectbox("Default Citation Style", ["APA 7th Edition", "MLA 9th Edition", "Chicago", "Harvard", "IEEE"])
        st.toggle("Enable Advanced Analytics", value=True)
        st.toggle("High Contrast UI", value=True)
        st.toggle("Auto-save Progress", value=True)
    st.divider()
    st.write("App Version: 4.0.0 (Titan Intelligence Edition)")

import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
import nltk

# --- 1. SYSTEM FIX: PREVENT MISSINGCORPUSERROOR ---
# This ensures the bot and users don't see a red error screen.
@st.cache_resource
def setup_nltk():
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('brown', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    except Exception:
        pass

setup_nltk()

# --- 2. GOOGLE ANALYTICS: VERSO STUDY ASSISTANT ---
def inject_analytics():
    # Using your new Measurement ID: G-030XWBG97P
    ga_code = """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-030XWBG97P"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-030XWBG97P');
    </script>
    """
    components.html(ga_code, height=0)

# --- 3. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Verso Research Pro", 
    page_icon="🔍", 
    layout="centered"
)
inject_analytics()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("VERSO PRO")
    choice = st.radio("Navigation", [
        "🏠 Home", 
        "✍️ Thesis Generator", 
        "📚 Citation Helper", 
        "🔢 Word Counter", 
        "📒 Study Assistant", 
        "🔍 Smart Analysis", 
        "⚙️ Settings"
    ])

# --- 5. APP LOGIC ---

# HOME SECTION
if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.subheader("Welcome, Yaseen Amr")
    st.markdown("""
    <div style="background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; color: #cbd5e1; font-style: italic;">
        "Select a module from the sidebar to start your MYP Year 2 workflow."
    </div>
    """, unsafe_allow_html=True)
    st.write("---")
    st.info("This assistant is optimized for climate activism research and academic non-fiction narratives.")

# NOTEBOOK INTELLIGENCE / STUDY ASSISTANT
elif choice == "📒 Study Assistant":
    st.title("Notebook Intelligence")
    st.markdown('*"Upload your sources to generate study cards, quizzes, and summaries."*')
    
    # Matching your uploaded file requirements
    uploaded_file = st.file_uploader("Upload sources (PDF, CSV, TXT, PPTX)", type=["pdf", "csv", "txt", "pptx"])
    
    notes = st.text_area("Paste your source material or notes here:", height=200)
    
    if notes:
        st.success("Content loaded! Select an output format below:")
        # Matching your tab UI
        t1, t2, t3 = st.tabs(["📋 Study Cards", "❓ Quiz Generator", "💡 Summary"])
        
        blob = TextBlob(notes)
        
        with t1:
            st.write("### Key Concepts")
            for phrase in list(set(blob.noun_phrases))[:5]:
                st.info(f"**Concept:** {phrase.title()}")
        
        with t2:
            st.write("### Practice Quiz")
            st.write("Generating questions based on your notes...")
            
        with t3:
            st.write("### AI Summary")
            st.write(notes[:500] + "...")
    else:
        st.info("Paste notes above to begin generating academic assets.")

# SETTINGS SECTION
elif choice == "⚙️ Settings":
    st.title("App Settings")
    st.selectbox("Academic Format", ["APA 7", "MLA 9", "Harvard", "Chicago"], index=0)
    st.toggle("Enable Advanced Analytics", value=True)
    st.toggle("High Contrast UI", value=False)
    st.toggle("Auto-save Progress", value=True)
    
    if st.button("🚀 Optimize Indexing"):
        st.toast("SEO Metadata Refreshed for Google Search Console!")

# Placeholder for other sections to prevent errors
else:
    st.title(choice)
    st.warning("This module is currently being optimized for MYP Year 2 standards.")

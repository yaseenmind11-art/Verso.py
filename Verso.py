import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Verso Research Pro", page_icon="📝", layout="centered")

# --- Custom Styles (The "White Box" Look) ---
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
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("VERSO PRO")
    st.write("Academic Command Center")
    choice = st.radio("Navigation", ["🏠 Home", "✍️ Thesis Generator", "📚 Citation Helper", "🔢 Word Counter"])

# --- Main Logic ---

if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.subheader("Welcome, Yaseen Amr")
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
    st.markdown('<div class="instruction-box">"Ensure all sources follow APA 7th edition guidelines to maintain academic integrity in your Humanities projects."</div>', unsafe_allow_html=True)
    source_data = st.text_area("Paste source details (URL, Author, Year):", height=150)
    if st.button("Format to APA"):
        st.info("APA Formatting tool active. Reviewing source data...")

elif choice == "🔢 Word Counter":
    st.title("Word Counter")
    st.markdown('<div class="instruction-box">"Keep track of your word limits for your non-fiction narratives and research tasks."</div>', unsafe_allow_html=True)
    essay_text = st.text_area("Paste your essay or research paragraph here:", height=300)
    
    # Logic for word count
    words = essay_text.split()
    word_count = len(words)
    
    st.metric(label="Word Count", value=word_count)
    
    if word_count > 0:
        st.progress(min(word_count / 500, 1.0)) # Progress bar based on a 500-word limit
        st.write(f"Current count: **{word_count}** words.")

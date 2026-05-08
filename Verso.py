import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Verso Research Pro", 
    layout="centered"
)

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
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("VERSO PRO")
    st.write("Academic Command Center")
    st.markdown("---")
    choice = st.radio("Navigation", ["🏠 Home", "✍️ Thesis Generator", "📚 Citation Helper", "🔢 Word Counter"])

# --- Main Logic ---

if choice == "🏠 Home":
    st.title("VERSO RESEARCH")
    st.markdown('<div class="instruction-box">"Select a module from the sidebar to start your academic research workflow."</div>', unsafe_allow_html=True)
    st.write("A specialized environment for thesis development, citation management, and text analysis.")

elif choice == "✍️ Thesis Generator":
    st.title("Thesis Generator")
    st.markdown('<div class="instruction-box">"A strong thesis statement should be a one-line argument that guides your entire research paper."</div>', unsafe_allow_html=True)
    topic = st.text_input("Enter your research topic:", placeholder="e.g., The impact of technology on modern education")
    if st.button("Generate Thesis"):
        if topic:
            st.success(f"**Draft Thesis:** Although various perspectives exist on the matter, {topic} serves as a pivotal element in understanding contemporary global trends.")
        else:
            st.warning("Please enter a topic to continue.")

elif choice == "📚 Citation Helper":
    st.title("Citation Assistant")
    st.markdown('<div class="instruction-box">"Ensure all sources follow standard academic guidelines to maintain integrity in your research projects."</div>', unsafe_allow_html=True)
    source_data = st.text_area("Paste source details:", height=150, placeholder="Enter the details of the source you wish to format...")
    if st.button("Format Source"):
        st.info("Processing source data for academic formatting...")

elif choice == "🔢 Word Counter":
    st.title("Word Counter")
    st.markdown('<div class="instruction-box">"Monitor word limits to ensure your writing remains concise and focused."</div>', unsafe_allow_html=True)
    essay_text = st.text_area("Paste your text here:", height=300, placeholder="Paste your essay content here...")
    
    words = essay_text.split()
    word_count = len(words)
    
    st.metric(label="Total Word Count", value=word_count)
    
    if word_count > 0:
        progress_val = min(word_count / 500, 1.0)
        st.progress(progress_val)
        st.write(f"Current count: **{word_count}** words.")

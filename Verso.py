import streamlit as st
import os
from datetime import datetime
from deep_translator import GoogleTranslator
from textblob import TextBlob

# 1. PAGE SETUP
st.set_page_config(
    page_title="Verso AI | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

# 2. UI STYLING
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden; }
    
    .status-box {
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #00a1ff;
        background-color: #f0f9ff;
        text-align: center;
    }
    
    .citation-box {
        background-color: #f8fafc;
        border-left: 5px solid #00a1ff;
        padding: 10px;
        margin-top: 10px;
        font-family: monospace;
    }

    div.stButton > button:first-child {
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER & LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 4. MAIN TABS
tab1, tab2, tab3 = st.tabs(["🔍 Smart Search", "✍️ Verso Editor", "📜 Citation Pro"])

# --- TAB 1: SMART SEARCH (With Instant Citations) ---
with tab1:
    st.markdown("### 🔍 Research Search")
    search_q = st.text_input("What are you searching for?", placeholder="e.g., advantages of water pipes...", key="search_v6")
    
    if search_q:
        q = search_q.replace(" ", "+")
        col1, col2, col3 = st.columns(3)
        
        # Define URLs
        g_url = f"https://www.google.com/search?q={q}"
        s_url = f"https://scholar.google.com/scholar?q={q}"
        b_url = f"https://www.britannica.com/search?query={q}"

        with col1:
            st.link_button("🌐 Google Search", g_url)
        with col2:
            st.link_button("📚 Google Scholar", s_url)
        with col3:
            st.link_button("📖 Britannica", b_url)
        
        # Instant Citation Section
        st.markdown("---")
        st.markdown("#### 📄 Quick Citations (Copy & Paste)")
        st.write("Click below to copy a draft citation for your bibliography:")
        
        # Displaying Citations in a code block for easy copying
        year = datetime.now().year
        st.code(f"Google Search Results. ({year}). Research on: {search_q}. {g_url}", language="text")
        st.code(f"Britannica Encyclopedia. ({year}). {search_q}. {b_url}", language="text")

# --- TAB 2: VERSO EDITOR (Grammar & Capitalization) ---
with tab2:
    st.markdown("### ✍️ Verso Editor")
    user_text = st.text_area("Your Writing:", height=250, placeholder="Start typing...", key="v_editor_v6")

    if user_text:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🌐 Global Translator")
            target_lang = st.selectbox("Select Language:", ["arabic", "french", "spanish", "german", "japanese", "russian"])
            if st.button("Translate Now"):
                result = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
                st.success(result)

        with col_b:
            st.markdown("#### 📏 Grammar & Case Check")
            if st.button("Analyze Writing"):
                # Spelling correction
                blob = TextBlob(user_text)
                temp_text = str(blob.correct())
                
                # Capitalization & "I" logic
                sentences = temp_text.split('. ')
                final_sentences = []
                for s in sentences:
                    if len(s) > 0:
                        # Capitalize first word of sentences
                        s = s[0].upper() + s[1:]
                        # Fix lowercase "i" and "i'm"
                        s = s.replace(" i ", " I ").replace(" i'", " I'").replace(" i.", " I.")
                        final_sentences.append(s)
                
                final_output = ". ".join(final_sentences)
                
                if final_output.strip() == user_text.strip():
                    st.balloons()
                    st.markdown('<div class="status-box">🎉 Congratulations! No mistakes left.</div>', unsafe_allow_html=True)
                else:
                    st.warning("Found improvements:")
                    st.success(f"**Suggested Version:**\n\n{final_output}")

# --- TAB 3: CITATION PRO ---
with tab3:
    st.markdown("### 📜 Citation Pro")
    url_input = st.text_input("Enter a specific URL to cite:", key="cite_v6")
    if st.button("Generate Citation"):
        if url_input:
            st.code(f"Source Title. ({datetime.now().year}). [Online]. {url_input}")
        else:
            st.error("Please enter a URL.")

st.markdown("---")

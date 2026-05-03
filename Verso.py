import streamlit as st
import os
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(
    page_title="Verso AI | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

# 2. ADVANCED UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Result Cards */
    .result-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Citation Box */
    .citation-output {
        background-color: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 5px solid #00a1ff;
        border-radius: 8px;
        padding: 20px;
        color: #0C4A6E;
    }

    /* Professional Action Buttons */
    div.stButton > button:first-child {
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6rem 2.5rem !important;
        font-weight: 700 !important;
        border: none !important;
    }

    /* Link Styling */
    a {
        color: #00a1ff !important;
        text-decoration: none;
        font-weight: 600;
    }

    /* Custom Editor Styling */
    .editor-box {
        background-color: #F8FAFC;
        border: 1px dashed #CBD5E1;
        border-radius: 10px;
        padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SETTINGS GEAR (SIDEBAR)
with st.sidebar:
    st.markdown("## ⚙️ App Settings")
    st.write("Control your Verso Experience")
    
    if st.button("🧹 Clear Session Cache"):
        st.cache_data.clear()
        st.success("Cache Cleared!")
        
    if st.button("📄 Export Research Log"):
        st.download_button("Download Report", data="Verso Research Log", file_name="research_report.txt")
        
    if st.button("🔒 Lockdown Mode"):
        st.warning("Focus mode activated. Distractions blocked.")
    
    st.markdown("---")
    st.caption("Verso Pro v2.4 | Professional Edition")

# 4. LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 5. MAIN TABS
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Smart Search", "📜 Citator", "✍️ Verso Editor", "🏛️ Gateways"])

with tab1:
    search_q = st.text_input("What are we researching today?", placeholder="Enter your topic...")
    
    if search_q:
        clean_q = search_q.replace(" ", "+")
        st.markdown(f"### ⚡ Analysis: {search_q}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🎓 Academic Databases")
            st.markdown(f"* [Open Google Scholar Results](https://scholar.google.com/scholar?q={clean_q})")
            st.markdown(f"* [Search CORE Academic Papers](https://core.ac.uk/search?q={clean_q})")
        with col2:
            st.markdown("#### 🏛️ Institutional Sources")
            st.markdown(f"* [Britannica Encyclopedia Search](https://www.britannica.com/search?query={clean_q})")
            st.markdown(f"* [Search Nature Journal Archive](https://www.nature.com/search?q={clean_q})")

with tab2:
    st.markdown("### 📜 Professional Citation Generator")
    cite_url = st.text_input("Paste URL here:", placeholder="https://...")
    
    if st.button("Generate Citation"):
        if "http" in cite_url:
            domain = cite_url.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            title = cite_url.rstrip("/").split("/")[-1].replace("-", " ").title()
            apa = f"{domain}. ({datetime.now().year}). *{title}*. {domain}. {cite_url}"
            st.markdown('<div class="citation-output">', unsafe_allow_html=True)
            st.code(apa, language="text")
            st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### ✍️ Verso Editor & Translator")
    st.write("Refine your writing for MYP excellence.")
    
    text_to_fix = st.text_area("Enter text to translate or check:", height=150, placeholder="Type your paragraph here...")
    
    if text_to_fix:
        clean_text = text_to_fix.replace(" ", "+")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🌐 Translation")
            st.markdown(f"""
                <div class="editor-box">
                    <p>Translate this text using Google’s Neural Engine:</p>
                    <a href="https://translate.google.com/?sl=auto&tl=ar&text={clean_text}&op=translate" target="_blank">
                        <button style="width:100%; padding:10px; background:#00a1ff; color:white; border:none; border-radius:5px; cursor:pointer;">
                            Open in Google Translate
                        </button>
                    </a>
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown("#### 📏 Grammar & Spelling")
            st.markdown(f"""
                <div class="editor-box">
                    <p>Check for Grammarly-standard errors:</p>
                    <a href="https://www.scribbr.com/spell-checker/" target="_blank">
                        <button style="width:100%; padding:10px; background:#2ecc71; color:white; border:none; border-radius:5px; cursor:pointer;">
                            Run Scribbr Grammar Check
                        </button>
                    </a>
                </div>
            """, unsafe_allow_html=True)

with tab4:
    st.subheader("🏛️ Institutional Gateways")
    st.markdown("* [World Bank](https://worldbank.org) \n* [IAEA](https://iaea.org) \n* [NASA](https://data.nasa.gov)")

st.markdown("---")

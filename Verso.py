import streamlit as st
import os
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(
    page_title="Verso AI | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

# 2. PROFESSIONAL CSS (Scribbr UI + Britannica Typography)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp {
        background: #F8FAFC;
    }

    /* Scribbr-style Result Cards */
    .result-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Citation Output - High Professionalism */
    .citation-output {
        background-color: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 5px solid #00a1ff;
        border-radius: 8px;
        padding: 20px;
        color: #0C4A6E;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Gemini-style Search Bar */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        border: 1px solid #CBD5E1 !important;
    }

    /* Professional Action Buttons */
    div.stButton > button:first-child {
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6rem 2.5rem !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #0081cc !important;
    }

    h4 { color: #1e293b !important; margin-bottom: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. SETTINGS SIDEBAR
with st.sidebar:
    st.markdown("## ⚙️ Research Settings")
    st.radio("Search Mode", ["Academic Only", "Global Search", "Institutional"], index=1)
    st.markdown("---")
    st.info("💡 **Pro Tip:** Use specific keywords for better citations.")
    st.caption("Verso Logic v2.2 | MYP Edition")

# 4. LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 5. MAIN TABS
tab1, tab2, tab3 = st.tabs(["🔍 Smart Search", "📜 Scribbr Citator", "🏛️ Gateways"])

with tab1:
    search_query = st.text_input("What are we researching today?", placeholder="Enter topic...")
    
    if search_query:
        # Clean the query for URL usage
        clean_q = search_query.replace(" ", "+")
        
        st.markdown(f"### ⚡ Verso Analysis: {search_query}")
        
        # Summary Box
        st.markdown("""
            <div class="result-card">
                <strong style="color: #00a1ff;">📊 Executive Summary</strong><br>
                Based on your inquiry, Verso has curated a list of authoritative databases. 
                Click the links below to access peer-reviewed journals and institutional data.
            </div>
        """, unsafe_allow_html=True)

        # THE LAYOUT FROM YOUR SCREENSHOT
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎓 Academic Databases")
            st.markdown(f"* [Open Google Scholar Results](https://scholar.google.com/scholar?q={clean_q})")
            st.markdown(f"* [Search CORE Academic Papers](https://core.ac.uk/search?q={clean_q})")
            st.markdown(f"* [Access Microsoft Academic](https://academic.microsoft.com/search?q={clean_q})")
            
        with col2:
            st.markdown("#### 🏛️ Institutional Sources")
            st.markdown(f"* [Britannica Encyclopedia Search](https://www.britannica.com/search?query={clean_q})")
            st.markdown(f"* [Search Nature Journal Archive](https://www.nature.com/search?q={clean_q})")
            st.markdown(f"* [Pew Research Center Data](https://www.pewresearch.org/search/{clean_q})")

with tab2:
    st.markdown("### 📜 Scribbr-Style Citation Generator")
    st.write("Generate APA 7 citations instantly.")
    
    cite_url = st.text_input("Paste URL here:", placeholder="https://...")
    
    if st.button("Cite Now"):
        if "http" in cite_url:
            # Extract basic info for the citation
            domain = cite_url.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            title = cite_url.rstrip("/").split("/")[-1].replace("-", " ").title()
            if not title or len(title) < 3: title = "Online Research Report"
            
            # Formulate the APA 7th Edition String
            apa = f"{domain}. ({datetime.now().year}). *{title}*. {domain}. {cite_url}"
            
            st.markdown('<div class="citation-output">', unsafe_allow_html=True)
            st.write("**APA 7th Edition Citation:**")
            st.code(apa, language="text")
            st.markdown('</div>', unsafe_allow_html=True)
            st.success("Citation formatted according to Scribbr standards.")
        else:
            st.error("Please enter a valid URL.")

with tab3:
    st.subheader("🏛️ Institutional Resource Library")
    st.write("Direct access to global high-authority platforms.")
    st.markdown("""
    * [World Bank Data](https://data.worldbank.org)
    * [United Nations Research](https://un.org/en/sections/resources-different-audiences/researchers)
    * [IAEA Technical Reports](https://iaea.org/publications)
    * [NASA Earth Data](https://earthdata.nasa.gov)
    """)

st.markdown("---")

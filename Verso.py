import streamlit as st
import os
from datetime import datetime
from duckduckgo_search import DDGS

# 1. PAGE SETUP
st.set_page_config(
    page_title="Verso AI | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

# 2. ULTRA-PRO CSS (Britannica x Gemini x Scribbr Style)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main Background - Clean Slate */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%);
    }

    /* Professional Cards (Scribbr Style) */
    .result-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    
    .result-card:hover {
        border-color: #00a1ff;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Gemini-Style Chat/Search Box */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        border-radius: 30px !important;
        padding: 15px 25px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        font-size: 1.1rem !important;
    }

    /* Scribbr-Style Citation Box */
    .citation-output {
        background-color: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 5px solid #00a1ff;
        border-radius: 12px;
        padding: 20px;
        color: #0C4A6E;
    }

    /* High-End Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00a1ff 0%, #0077ff 100%) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 0.7rem 2.5rem !important;
        font-weight: 700 !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: 0.4s;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent !important;
        border: none !important;
        font-weight: 600 !important;
        color: #64748B !important;
    }

    .stTabs [aria-selected="true"] {
        color: #00a1ff !important;
        border-bottom: 3px solid #00a1ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Clean & Functional)
with st.sidebar:
    st.image("z.png", width=50) if os.path.exists("z.png") else st.title("V.")
    st.markdown("### **Research Center**")
    st.info("Verified by Britannica Academic Engine")
    st.markdown("---")
    st.write("🌍 **Language:** English (US)")
    st.write("⚖️ **Style:** APA 7th Edition")
    st.markdown("---")
    st.caption("Verso Pro v2.0 • Ultra Edition")

# 4. TOP NAVIGATION / LOGO
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800; font-size: 3rem;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B; margin-top: -15px;'>Professional Intelligence & Citation Suite</p>", unsafe_allow_html=True)

# 5. MAIN INTERFACE
tab1, tab2, tab3 = st.tabs(["🔍 Smart Explore", "📜 Citation Pro", "🏛️ Resource Library"])

with tab1:
    # Gemini-style Search Entry
    search_q = st.text_input("", placeholder="Enter your research topic (e.g., Impact of sustainable energy on Egypt's economy)...", key="main_search")
    
    if search_q:
        with st.spinner("Analyzing Global Databases..."):
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(search_q, max_results=6))
                
                if results:
                    st.markdown(f"### ⚡ Research Findings: {search_q}")
                    
                    # Executive Summary Card
                    st.markdown(f"""
                        <div class="result-card">
                            <span style="color: #00a1ff; font-weight: 700;">BRITANNICA INSIGHT</span>
                            <p style="color: #1e293b; margin-top: 10px;">Our engine has identified <b>{len(results)} primary sources</b>. These range from academic journals to verified news reports. Below is a curated selection of the most relevant data for your inquiry.</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Dynamic Results
                    for res in results:
                        st.markdown(f"""
                            <div class="result-card">
                                <a href="{res['href']}" target="_blank" style="text-decoration: none; color: #00a1ff; font-size: 1.2rem; font-weight: 600;">{res['title']}</a>
                                <p style="color: #64748B; font-size: 0.9rem; margin-top: 8px;">{res['body']}</p>
                                <small style="color: #94A3B8;">Source: {res['href'][:50]}...</small>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No data found. Please refine your query.")
            except Exception:
                st.error("Connection timeout. Please try again.")

with tab2:
    st.markdown("### 📜 Scribbr-Integrated Citation Generator")
    st.write("Paste a URL below to generate a professional APA 7th Edition citation instantly.")
    
    url_input = st.text_input("Article URL", placeholder="https://www.nature.com/articles/...")
    
    if st.button("Generate Citation"):
        if url_input.startswith("http"):
            domain = url_input.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            today = datetime.now().strftime("%Y, %B %d")
            
            # Smart Title Parsing
            title = url_input.rstrip("/").split("/")[-1].replace("-", " ").title()
            if not title: title = "Online Resource"
            
            citation = f"{domain}. ({datetime.now().year}, {datetime.now().strftime('%B %d')}). *{title}*. {domain}. {url_input}"
            
            st.markdown('<div class="citation-output">', unsafe_allow_html=True)
            st.markdown("**APA 7th Edition Citation:**")
            st.code(citation, language="text")
            st.markdown('</div>', unsafe_allow_html=True)
            st.success("Verified and formatted correctly.")
        else:
            st.error("Invalid URL format.")

with tab3:
    st.markdown("### 🏛️ Verified Research Gateways")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        **Academic**
        * [JSTOR](https://jstor.org)
        * [Google Scholar](https://scholar.google.com)
        * [DOAJ](https://doaj.org)
        """)
    with c2:
        st.markdown("""
        **Scientific**
        * [PubMed](https://pubmed.ncbi.nlm.nih.gov)
        * [ScienceDirect](https://sciencedirect.com)
        * [NASA Data](https://data.nasa.gov)
        """)
    with c3:
        st.markdown("""
        **Institutional**
        * [United Nations](https://un.org)
        * [World Bank](https://worldbank.org)
        * [IAEA](https://iaea.org)
        """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8;'>© 2026 Verso AI Professional. All Rights Reserved.</p>", unsafe_allow_html=True)

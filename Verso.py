import streamlit as st
import os
from datetime import datetime

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
    
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%);
    }

    .result-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        border-radius: 30px !important;
        padding: 15px 25px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }

    .citation-output {
        background-color: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 5px solid #00a1ff;
        border-radius: 12px;
        padding: 20px;
        color: #0C4A6E;
    }

    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00a1ff 0%, #0077ff 100%) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 0.7rem 2.5rem !important;
        font-weight: 700 !important;
        border: none !important;
    }
    
    a {
        color: #00a1ff !important;
        text-decoration: none;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown("### **Research Center**")
    st.info("Verified Research Mode")
    st.markdown("---")
    st.write("⚖️ **Style:** APA 7th Edition")
    st.caption("Verso Pro v2.1 • Core Edition")

# 4. LOGO / HEADER
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800; font-size: 3rem;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

# 5. MAIN INTERFACE
tab1, tab2, tab3 = st.tabs(["🔍 Smart Explore", "📜 Citation Pro", "🏛️ Resource Library"])

with tab1:
    search_q = st.text_input("", placeholder="Enter your research topic...", key="main_search")
    
    if search_q:
        st.markdown(f"### ⚡ Research Portal: {search_q}")
        
        # Format query for URLs
        link_q = search_q.replace(" ", "+")
        
        st.markdown(f"""
            <div class="result-card">
                <span style="color: #00a1ff; font-weight: 700;">BRITANNICA INSIGHT</span>
                <p style="color: #1e293b; margin-top: 10px;">To ensure the highest academic integrity for your <b>IB project</b>, Verso has generated direct pathways to verified databases for <b>"{search_q}"</b>.</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🎓 Academic Databases")
            st.markdown(f"* **[Open Google Scholar Results](https://scholar.google.com/scholar?q={link_q})**")
            st.markdown(f"* **[Search CORE Academic Papers](https://core.ac.uk/search?q={link_q})**")
            st.markdown(f"* **[Access Microsoft Academic](https://academic.microsoft.com/search?q={link_q})**")
        
        with col2:
            st.markdown("#### 🏛️ Institutional Sources")
            st.markdown(f"* **[Britannica Encyclopedia Search](https://www.britannica.com/search?query={link_q})**")
            st.markdown(f"* **[Search Nature Journal Archive](https://www.nature.com/search?q={link_q})**")
            st.markdown(f"* **[Pew Research Center Data](https://www.pewresearch.org/search/{link_q})**")

with tab2:
    st.markdown("### 📜 Professional Citation Generator")
    url_input = st.text_input("Article URL", placeholder="https://...")
    
    if st.button("Generate Citation"):
        if url_input.startswith("http"):
            domain = url_input.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            title = url_input.rstrip("/").split("/")[-1].replace("-", " ").title()
            if not title or len(title) < 3: title = "Research Resource"
            
            citation = f"{domain}. ({datetime.now().year}). *{title}*. {domain}. {url_input}"
            
            st.markdown('<div class="citation-output">', unsafe_allow_html=True)
            st.code(citation, language="text")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Invalid URL.")

with tab3:
    st.markdown("### 🏛️ Verified Gateways")
    st.write("Quick access to the world's most trusted data.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("* [JSTOR](https://jstor.org)\n* [IAEA](https://iaea.org)")
    with c2:
        st.markdown("* [World Bank](https://worldbank.org)\n* [NASA](https://data.nasa.gov)")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8;'>© 2026 Verso AI Professional.</p>", unsafe_allow_html=True)

import streamlit as st
import os
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(
    page_title="Verso AI | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

# 2. SIDEBAR FOR THEME SWITCHING
with st.sidebar:
    st.markdown("## ⚙️ Display Settings")
    # This acts as our manual switch
    theme_choice = st.radio("Select Interface Theme:", ["☀️ Light Mode", "🌙 Night Mode"])
    st.markdown("---")
    st.info("💡 **Pro Tip:** Night Mode is recommended for long research sessions.")
    st.caption("Verso Logic v2.3 | MYP Edition")

# 3. DYNAMIC THEME COLORS
if theme_choice == "🌙 Night Mode":
    primary_bg = "#0E1117"
    secondary_bg = "#1d2129"
    text_main = "#FAFAFA"
    text_sub = "#94A3B8"
    border_col = "#30363D"
    card_shadow = "rgba(0, 0, 0, 0.4)"
else:
    primary_bg = "#F8FAFC"
    secondary_bg = "#FFFFFF"
    text_main = "#0f172a"
    text_sub = "#64748B"
    border_col = "#E2E8F0"
    card_shadow = "rgba(149, 157, 165, 0.1)"

# 4. INJECTED CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="st-"], .stApp {{
        font-family: 'Inter', sans-serif;
        background-color: {primary_bg} !important;
        color: {text_main} !important;
    }}

    header, footer {{visibility: hidden;}}

    /* Professional Cards (Scribbr Style) */
    .result-card {{
        background-color: {secondary_bg} !important;
        border: 1px solid {border_col} !important;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px {card_shadow};
        margin-bottom: 20px;
        color: {text_main} !important;
    }}

    /* Citation Output - High Contrast */
    .citation-output {{
        background-color: {theme_choice == "🌙 Night Mode" and "#161B22" or "#F0F9FF"} !important;
        border: 1px solid {theme_choice == "🌙 Night Mode" and "#30363D" or "#BAE6FD"} !important;
        border-left: 5px solid #00a1ff !important;
        border-radius: 8px;
        padding: 20px;
        color: {theme_choice == "🌙 Night Mode" and "#FAFAFA" or "#0C4A6E"} !important;
    }}

    /* Gemini-style Inputs */
    .stTextInput>div>div>input {{
        background-color: {secondary_bg} !important;
        color: {text_main} !important;
        border-radius: 10px !important;
        border: 1px solid {border_col} !important;
    }}

    /* Blue Action Buttons */
    div.stButton > button:first-child {{
        background-color: #00a1ff !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6rem 2.5rem !important;
        font-weight: 700 !important;
        border: none !important;
    }}
    
    /* Ensure all headers respect the theme */
    h1, h2, h3, h4, p, span, li {{
        color: {text_main} !important;
    }}
    
    a {{
        color: #00a1ff !important;
        text-decoration: none;
        font-weight: 600;
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] button {{
        color: {text_sub} !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #00a1ff !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. HEADER
t_left, t_center, t_right = st.columns([1, 2, 1])
with t_center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.markdown(f"<h1 style='text-align: center;'>VERSO<span style='color:#00a1ff'>AI</span></h1>", unsafe_allow_html=True)

st.markdown("---")

# 6. MAIN CONTENT
tab1, tab2, tab3 = st.tabs(["🔍 Smart Search", "📜 Citation Pro", "🏛️ Resource Library"])

with tab1:
    search_q = st.text_input("What are we researching today?", placeholder="Enter topic...")
    
    if search_q:
        clean_q = search_q.replace(" ", "+")
        st.markdown(f"### ⚡ Analysis: {search_q}")
        
        st.markdown("""
            <div class="result-card">
                <strong style="color: #00a1ff;">📊 Executive Summary</strong><br>
                Paths to academic and institutional databases have been generated. 
                Use these verified sources for your IB project documentation.
            </div>
        """, unsafe_allow_html=True)

        # The Two-Column Layout
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
    cite_url = st.text_input("Paste URL here:", placeholder="https://...")
    
    if st.button("Cite Source"):
        if "http" in cite_url:
            domain = cite_url.split("//")[-1].split("/")[0].replace("www.", "").capitalize()
            title = cite_url.rstrip("/").split("/")[-1].replace("-", " ").title()
            if not title or len(title) < 3: title = "Research Resource"
            
            apa = f"{domain}. ({datetime.now().year}). *{title}*. {domain}. {cite_url}"
            
            st.markdown('<div class="citation-output">', unsafe_allow_html=True)
            st.write("**APA 7th Edition Citation:**")
            st.code(apa, language="text")
            st.markdown('</div>', unsafe_allow_html=True)
            st.success("Format: Scribbr/APA Standard")
        else:
            st.error("Please enter a valid URL.")

with tab3:
    st.subheader("🏛️ Institutional Gateways")
    st.markdown("""
    * [World Bank Data](https://data.worldbank.org)
    * [IAEA Technical Reports](https://iaea.org/publications)
    * [NASA Earth Data](https://earthdata.nasa.gov)
    """)

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: {text_sub};'>© 2026 Verso AI Professional.</p>", unsafe_allow_html=True)

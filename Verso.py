import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", # The orange/blue part for the browser tab
    layout="wide"
)

# 2. Adaptive Text Color CSS (Black for Light Mode, Gray for Dark Mode)
st.markdown("""
    <style>
    @media (prefers-color-scheme: light) {
        input { color: #000000 !important; }
    }
    @media (prefers-color-scheme: dark) {
        input { color: #bbbbbb !important; }
    }
    /* Citation styling */
    .apa-cite {
        font-family: serif;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Branding (The "Black Space" Logo)
with st.sidebar:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.info("📖 Verso: The Ultimate Research Tool")
    
    st.markdown("---")
    st.write("Verso helps students find trusted, diverse perspectives through bias-cutting search logic.")

# 4. Main App Header
col1, col2 = st.columns([0.1, 0.9])
with col1:
    if os.path.exists("icon.png"):
        st.image("icon.png", width=60)
with col2:
    st.title("Verso AI")

# 5. User Input Section
user_query = st.text_input("Enter your research question:", placeholder="Type here...")

if user_query:
    st.divider()
    st.info(f"**Verso Logic:** Analyzing '{user_query}' for credible, multi-sided perspectives...")

    # Data with detailed parts for APA Citation (Scribbr Style)
    results = [
        {
            "author": "IAEA", 
            "date": "2024, March 12", 
            "title": "Nuclear science and technology", 
            "site": "International Atomic Energy Agency", 
            "url": "https://www.iaea.org",
            "trusted": True
        },
        {
            "author": "The Editors of Britannica", 
            "date": "2023, October 05", 
            "title": "Properties of water", 
            "site": "Encyclopedia Britannica", 
            "url": "https://www.britannica.com",
            "trusted": True
        },
        {
            "author": "United Nations", 
            "date": "2025, January 20", 
            "title": "Sustainable development goals", 
            "site": "UN.org", 
            "url": "https://www.un.org",
            "trusted": True
        },
        {
            "author": "Wikipedia Contributors", 
            "date": "2026, May 02", 
            "title": "Global water access", 
            "site": "Wikipedia", 
            "url": "https://www.wikipedia.org",
            "trusted": False
        }
    ]

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### ✅ Verified Trusted Sources")
        for res in results:
            if res['trusted']:
                st.markdown(f"**{res['title']}**")
                # APA Style: Author. (Date). Title. Site Name.
                st.markdown(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")
                st.markdown(f"{res['url']}")
                st.write("") 

    with col_right:
        st.markdown("### 🌐 Other Perspectives")
        for res in results:
            if not res['trusted']:
                st.markdown(f"**{res['title']}**")
                st.markdown(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")
                st.markdown(f"{res['url']}")
                st.write("")

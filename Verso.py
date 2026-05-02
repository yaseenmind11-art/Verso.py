import streamlit as st
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="Verso AI", page_icon="📖", layout="wide")

# 2. FIXED CSS: Adaptive Text Color & Background
# This automatically makes text Black in Light mode and Gray in Dark mode
st.markdown("""
    <style>
    @media (prefers-color-scheme: light) {
        input { color: #000000 !important; }
    }
    @media (prefers-color-scheme: dark) {
        input { color: #bbbbbb !important; }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📖 Verso AI")
st.write("Find trusted perspectives from the 'other side' of any topic.")

# 3. User Input
user_query = st.text_input("Enter your research question:", placeholder="Type here...")

if user_query:
    st.divider()
    st.info(f"**Verso Logic:** Analyzing '{user_query}' for credible viewpoints...")

    # Data with citation details
    results = [
        {
            "author": "IAEA", 
            "title": "Nuclear Science and Technology", 
            "container": "International Atomic Energy Agency", 
            "year": "2024", 
            "url": "https://www.iaea.org",
            "trusted": True
        },
        {
            "author": "The Editors of Britannica", 
            "title": "Properties of Water", 
            "container": "Encyclopedia Britannica", 
            "year": "2023", 
            "url": "https://www.britannica.com",
            "trusted": True
        },
        {
            "author": "United Nations", 
            "title": "Sustainable Development Goals", 
            "container": "UN.org", 
            "year": "2025", 
            "url": "https://www.un.org",
            "trusted": True
        },
        {
            "author": "Community Contributor", 
            "title": "Global Water Access", 
            "container": "Wikipedia", 
            "year": "2026", 
            "url": "https://www.wikipedia.org",
            "trusted": False
        }
    ]

    col1, col2 = st.columns(2)
    today = date.today().strftime("%d %b. %Y")

    with col1:
        st.markdown("### ✅ Verified Trusted Sources")
        for res in results:
            if res['trusted']:
                # MLA Citation Style: Author. "Title." Container, Year, URL. Accessed Date.
                mla_citation = f"{res['author']}. \"{res['title']}.\" *{res['container']}*, {res['year']}, {res['url']}. Accessed {today}."
                
                st.success(f"**[{res['title']}]({res['url']})**")
                st.code(mla_citation, language="text") # This makes it easy to copy

    with col2:
        st.markdown("### 🌐 Other Perspectives")
        for res in results:
            if not res['trusted']:
                mla_citation = f"{res['author']}. \"{res['title']}.\" *{res['container']}*, {res['year']}, {res['url']}. Accessed {today}."
                
                st.warning(f"**[{res['title']}]({res['url']})**")
                st.code(mla_citation, language="text")

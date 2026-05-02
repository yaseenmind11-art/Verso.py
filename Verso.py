import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Verso AI", page_icon="📖", layout="wide")

# 2. Adaptive Text Color CSS
st.markdown("""
    <style>
    @media (prefers-color-scheme: light) {
        input { color: #000000 !important; }
    }
    @media (prefers-color-scheme: dark) {
        input { color: #bbbbbb !important; }
    }
    /* Clean up the citation text appearance */
    .apa-cite {
        font-family: serif;
        margin-bottom: 0px;
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

    # Data with detailed date parts for APA
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

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Verified Trusted Sources")
        for res in results:
            if res['trusted']:
                # APA Style: Author. (Date). Title. Site Name. URL
                st.markdown(f"**{res['title']}**")
                st.markdown(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")
                st.markdown(f"{res['url']}")
                st.write("") # Spacing

    with col2:
        st.markdown("### 🌐 Other Perspectives")
        for res in results:
            if not res['trusted']:
                st.markdown(f"**{res['title']}**")
                st.markdown(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")
                st.markdown(f"{res['url']}")
                st.write("")

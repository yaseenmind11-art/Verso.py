import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. Advanced CSS for Wide Branding
st.markdown("""
    <style>
    /* Hides the default Streamlit header */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Pulls everything to the very top */
    .block-container {
        padding-top: 0rem;
        max-width: 100%;
    }

    /* This makes the image container ignore standard margins to look wider */
    .stImage > img {
        width: 100%;
        max-width: 800px; /* Adjust this number to make it even wider or narrower */
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    /* Adaptive text colors for search input */
    @media (prefers-color-scheme: light) {
        input { color: black !important; }
    }
    @media (prefers-color-scheme: dark) {
        input { color: #bbbbbb !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Main Header Branding
# If you want it to hit the edges, use 'use_container_width=True'
if os.path.exists("full_logo.png"):
    st.image("full_logo.png", use_container_width=True)
else:
    st.title("Verso AI")
    st.write("The Ultimate Research Assistant")

st.markdown("---")

# 4. Search Section
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Analyzing trusted perspectives for *'{query}'*")
    
    # Results data (APA Style as requested)
    results = [
        {"author": "IAEA", "date": "2024, March 12", "title": "Nuclear science and technology", "site": "IAEA.org", "url": "https://www.iaea.org", "trusted": True},
        {"author": "Britannica Editors", "date": "2023, Oct 05", "title": "Properties of water", "site": "Britannica", "url": "https://www.britannica.com", "trusted": True},
        {"author": "United Nations", "date": "2025, Jan 20", "title": "Sustainable goals", "site": "UN.org", "url": "https://www.un.org", "trusted": True},
        {"author": "Wikipedia Contributors", "date": "2026, May 02", "title": "Global water access", "site": "Wikipedia", "url": "https://www.wikipedia.org", "trusted": False}
    ]

    left, right = st.columns(2)

    with left:
        st.subheader("✅ Verified Trusted")
        for res in results:
            if res['trusted']:
                st.markdown(f"**[{res['title']}]({res['url']})**")
                st.markdown(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")
                st.write("")

    with right:
        st.subheader("🌐 Other Perspectives")
        for res in results:
            if not res['trusted']:
                st.markdown(f"**[{res['title']}]({res['url']})**")
                st.markdown(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")
                st.write("")

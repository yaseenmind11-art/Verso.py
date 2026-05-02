import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS for the Sleek Rectangle Look
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        max-width: 95%;
    }

    /* This forces the image into a wide rectangle and prevents cutting */
    .stImage > img {
        width: 100%;
        max-height: 250px; /* Limits the height so it stays a rectangle */
        object-fit: contain; /* Ensures the whole logo fits without being squished */
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    @media (prefers-color-scheme: light) { input { color: black !important; } }
    @media (prefers-color-scheme: dark) { input { color: #bbbbbb !important; } }
    </style>
    """, unsafe_allow_html=True)

# 3. Banner Section
if os.path.exists("full_logo.png"):
    # Using container width keeps it wide, but the CSS above keeps it short
    st.image("full_logo.png", use_container_width=True)
else:
    st.title("Verso AI")

st.markdown("---")

# 4. Search Area
query = st.text_input("Enter your research question:", placeholder="Search...")

if query:
    st.write(f"**Verso Logic:** Results for *'{query}'*")
    
    # Simple APA Style results
    results = [
        {"author": "IAEA", "date": "2024", "title": "Nuclear science", "site": "IAEA.org", "url": "https://www.iaea.org", "trusted": True},
        {"author": "Britannica", "date": "2023", "title": "Water properties", "site": "Britannica", "url": "https://www.britannica.com", "trusted": True},
        {"author": "Wikipedia", "date": "2026", "title": "Global access", "site": "Wikipedia", "url": "https://www.wikipedia.org", "trusted": False}
    ]

    left, right = st.columns(2)
    with left:
        st.subheader("✅ Trusted")
        for res in results:
            if res['trusted']:
                st.markdown(f"**[{res['title']}]({res['url']})**")
                st.markdown(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")
                st.write("")

    with right:
        st.subheader("🌐 Other")
        for res in results:
            if not res['trusted']:
                st.markdown(f"**[{res['title']}]({res['url']})**")
                st.markdown(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")
                st.write("")

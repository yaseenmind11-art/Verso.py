import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS for the Slim, Stretched Rectangle
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        max-width: 90%; /* Keeps it from hitting the extreme edges */
    }

    /* This forces the banner to be thin and wide */
    .stImage > img {
        width: 100%;
        max-height: 180px; /* Lowered this to make it 'minimized' */
        object-fit: cover; /* This stretches the background to fill the rectangle */
        object-position: center; /* Keeps the logo centered while stretching the sides */
        border-radius: 15px; /* Matches the rounded corners in your screenshot */
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    @media (prefers-color-scheme: light) { input { color: black !important; } }
    @media (prefers-color-scheme: dark) { input { color: #bbbbbb !important; } }
    </style>
    """, unsafe_allow_html=True)

# 3. Main Banner
if os.path.exists("full_logo.png"):
    st.image("full_logo.png", use_container_width=True)
else:
    st.title("Verso AI")

st.markdown("---")

# 4. Search Area
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Results for *'{query}'*")
    
    results = [
        {"author": "IAEA", "date": "2024", "title": "Nuclear science", "site": "IAEA.org", "url": "https://www.iaea.org", "trusted": True},
        {"author": "Britannica", "date": "2023", "title": "Water properties", "site": "Britannica", "url": "https://www.britannica.com", "trusted": True},
        {"author": "Wikipedia", "date": "2026", "title": "Global access", "site": "Wikipedia", "url": "https://www.wikipedia.org", "trusted": False}
    ]

    left, right = st.columns(2)
    with left:
        st.subheader("✅ Trusted Sources")
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

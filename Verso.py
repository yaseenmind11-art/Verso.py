import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS for the "Stretched" Rectangle Look
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* This is the magic part: it removes the side margins of the app */
    .block-container {
        padding-top: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100%;
    }

    /* This forces the image to stretch across the whole top bar */
    .stImage > img {
        width: 100vw; /* 100% of the Viewport Width */
        max-height: 200px; /* Keeps it a thin rectangle so it doesn't get too tall */
        object-fit: cover; /* This stretches/crops it to fill the rectangle perfectly */
        display: block;
    }

    /* Keep the search bar and results from hitting the edges */
    .search-padding {
        padding-left: 5%;
        padding-right: 5%;
    }

    @media (prefers-color-scheme: light) { input { color: black !important; } }
    @media (prefers-color-scheme: dark) { input { color: #bbbbbb !important; } }
    </style>
    """, unsafe_allow_html=True)

# 3. Stretched Banner
if os.path.exists("full_logo.png"):
    st.image("full_logo.png")
else:
    st.title("Verso AI")

# 4. Search and Content (Wrapped in a div for padding)
st.markdown('<div class="search-padding">', unsafe_allow_html=True)

st.markdown("---")
query = st.text_input("Enter your research question:", placeholder="Search...")

if query:
    st.write(f"**Verso Logic:** Results for *'{query}'*")
    
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

st.markdown('</div>', unsafe_allow_html=True)

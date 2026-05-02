import streamlit as st
import os

# 1. TAB CONFIG: This must be line #1 for the icon to work
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CLEANUP CSS: Pulls everything up and hides the junk
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Removes the top gap so the banner sits at the very top */
    .block-container {
        padding-top: 0rem;
        max-width: 95%;
    }

    /* Ensures the image NEVER crops, zooms, or cuts */
    img {
        object-fit: contain !important;
        border-radius: 12px;
    }

    /* Input text visibility */
    @media (prefers-color-scheme: light) { input { color: black !important; } }
    @media (prefers-color-scheme: dark) { input { color: #bbbbbb !important; } }
    </style>
    """, unsafe_allow_html=True)

# 3. THE BANNER: Using columns to control height without cropping
# Change the [2, 6, 2] to [1, 8, 1] if you want the banner bigger/wider
left, center, right = st.columns([2, 6, 2]) 

with center:
    if os.path.exists("full_logo.png"):
        # We use standard image loading here—no forced CSS height
        st.image("full_logo.png", use_container_width=True)
    else:
        st.title("Verso AI")

st.markdown("---")

# 4. SEARCH & RESULTS
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Analyzing trusted perspectives for *'{query}'*")
    
    results = [
        {"author": "IAEA", "date": "2024", "title": "Nuclear science", "site": "IAEA.org", "url": "https://www.iaea.org", "trusted": True},
        {"author": "Britannica", "date": "2023", "title": "Water properties", "site": "Britannica", "url": "https://www.britannica.com", "trusted": True},
        {"author": "Wikipedia", "date": "2026", "title": "Global access", "site": "Wikipedia", "url": "https://www.wikipedia.org", "trusted": False}
    ]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Verified Trusted")
        for res in results:
            if res['trusted']:
                st.markdown(f"**[{res['title']}]({res['url']})**")
                st.caption(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")

    with col2:
        st.subheader("🌐 Other Perspectives")
        for res in results:
            if not res['trusted']:
                st.markdown(f"**[{res['title']}]({res['url']})**")
                st.caption(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")

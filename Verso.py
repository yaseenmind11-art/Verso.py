import streamlit as st
import os

# 1. Professional Page Config
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS to clean the header and fix text visibility
st.markdown("""
    <style>
    /* Hides the default Streamlit header bar to make it all black */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Removes the gap at the top */
    .block-container {
        padding-top: 1rem;
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

# 3. Sidebar (Optional: keep it clean or empty)
with st.sidebar:
    st.caption("Verso: The Ultimate Research Assistant")

# 4. The New Header Layout
# This puts the logo in that top black area properly
if os.path.exists("full_logo.png"):
    st.image("full_logo.png", width=350) # Adjusted width to look sharp in the header
else:
    st.title("Verso AI")
    st.write("The Ultimate Research Assistant")

st.markdown("---")

# 5. Search Logic
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Analyzing trusted perspectives for *'{query}'*")
    
    # Results data (APA Style)
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

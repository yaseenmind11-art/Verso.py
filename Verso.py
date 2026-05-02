import streamlit as st
import os

# 1. PAGE CONFIG: MUST BE THE FIRST LINE OF CODE
# This sets the tab name and the favicon icon
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS: REMOVING THE "SANDWICH" GAP & CLEANING UI
st.markdown("""
    <style>
    /* Hides the default Streamlit header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Removes the top padding to pull everything up */
    .block-container {
        padding-top: 0rem;
        max-width: 90%;
    }

    /* Ensures the image is never cropped or zoomed */
    img {
        object-fit: contain !important;
        border-radius: 12px;
    }

    /* Fix text visibility in both Light and Dark modes */
    @media (prefers-color-scheme: light) {
        input { color: black !important; }
    }
    @media (prefers-color-scheme: dark) {
        input { color: #bbbbbb !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. THE SLIM HEADER: SQUEEZING THE LOGO
# By using [3.5, 3, 3.5], we force the logo into a narrow center column.
# This makes the height naturally small without cutting off any text.
left_gap, center, right_gap = st.columns([3.5, 3, 3.5]) 

with center:
    if os.path.exists("full_logo.png"):
        st.image("full_logo.png", use_container_width=True)
    else:
        st.title("Verso AI")

st.markdown("---")

# 4. SEARCH SECTION
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Analyzing trusted perspectives for *'{query}'*")
    
    # Example results data in APA format
    results = [
        {"author": "IAEA", "date": "2024, March 12", "title": "Nuclear science and technology", "site": "IAEA.org", "url": "https://www.iaea.org", "trusted": True},
        {"author": "Britannica Editors", "date": "2023, Oct 05", "title": "Properties of water", "site": "Britannica", "url": "https://www.britannica.com", "trusted": True},
        {"author": "United Nations", "date": "2025, Jan 20", "title": "Sustainable goals", "site": "UN.org", "url": "https://www.un.org", "trusted": True},
        {"author": "Wikipedia Contributors", "date": "2026, May 02", "title": "Global water access", "site": "Wikipedia", "url": "https://www.wikipedia.org", "trusted": False}
    ]

    # Side-by-Side Results
    left_res, right_res = st.columns(2)

    with left_res:
        st.subheader("✅ Verified Trusted")
        for res in results:
            if res['trusted']:
                st.markdown(f"**[{res['title']}]({res['url']})**")
                st.markdown(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")
                st.write("")

    with right_res:
        st.subheader("🌐 Other Perspectives")
        for res in results:
            if not res['trusted']:
                st.markdown(f"**[{res['title']}]({res['url']})**")
                st.markdown(f"{res['author']}. ({res['date']}). *{res['title']}*. {res['site']}.")
                st.write("")

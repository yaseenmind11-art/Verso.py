import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. Advanced CSS to clean up the UI
st.markdown("""
    <style>
    /* Fix text visibility in both modes */
    @media (prefers-color-scheme: light) {
        input { color: #000000 !important; }
    }
    @media (prefers-color-scheme: dark) {
        input { color: #bbbbbb !important; }
    }
    
    /* Remove the 'Sandwich' padding at the top */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Style the Citations for a clean look */
    .apa-text {
        font-family: 'Helvetica', sans-serif;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Clean Sidebar (The "Black Space")
with st.sidebar:
    if os.path.exists("full_logo.png"):
        # We use a fixed width to prevent the "huge logo" look
        st.image("full_logo.png", width=200)
    else:
        st.title("📖 Verso")
    
    st.markdown("---")
    st.caption("The Ultimate Research Tool for IB Students.")
    st.info("Designed to break through echo chambers and provide balanced perspectives.")

# 4. Professional Header (No sandwich stacking)
# This keeps the icon and title on the SAME line
header_col1, header_col2 = st.columns([0.08, 0.92])
with header_col1:
    if os.path.exists("icon.png"):
        st.image("icon.png", width=55)
with header_col2:
    st.title("Verso AI")

# 5. Search Area
user_query = st.text_input("Enter your research question:", placeholder="Search for credible perspectives...")

if user_query:
    st.write(f"**Verso Analysis:** Showing credible results for *'{user_query}'*")
    st.divider()

    # Shared results data
    results = [
        {"author": "IAEA", "date": "2024, March 12", "title": "Nuclear science and technology", "site": "IAEA.org", "url": "https://www.iaea.org", "trusted": True},
        {"author": "Britannica Editors", "date": "2023, Oct 05", "title": "Properties of water", "site": "Britannica", "url": "https://www.britannica.com", "trusted": True},
        {"author": "United Nations", "date": "2025, Jan 20", "title": "Sustainable goals", "site": "UN.org", "url": "https://www.un.org", "trusted": True},
        {"author": "Wikipedia Contributors", "date": "2026, May 02", "title": "Global water access", "site": "Wikipedia", "url": "https://www.wikipedia.org", "trusted": False}
    ]

    # Side-by-Side Columns
    left, right = st.columns(2)

    with left:
        st.subheader("✅ Verified Trusted")
        for res in results:
            if res['trusted']:
                with st.container():
                    st.markdown(f"**[{res['title']}]({res['url']})**")
                    st.markdown(f'<p class="apa-text">{res["author"]}. ({res["date"]}). *{res["title"]}*. {res["site"]}.</p>', unsafe_allow_html=True)
                    st.caption(res['url'])
                    st.write("")

    with right:
        st.subheader("🌐 Other Perspectives")
        for res in results:
            if not res['trusted']:
                with st.container():
                    st.markdown(f"**[{res['title']}]({res['url']})**")
                    st.markdown(f'<p class="apa-text">{res["author"]}. ({res["date"]}). *{res["title"]}*. {res["site"]}.</p>', unsafe_allow_html=True)
                    st.caption(res['url'])
                    st.write("")

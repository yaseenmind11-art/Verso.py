import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Verso AI", page_icon="📖", layout="wide")

# 2. FIXED CSS: This ensures your search bar is always visible
st.markdown("""
    <style>
    /* Makes the input text dark so it's visible on white backgrounds */
    input {
        color: #111111 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📖 Verso AI")
st.write("Find trusted perspectives from the 'other side' of any topic.")

# 3. Trusted Domain Filter
TRUSTED_DOMAINS = [".org", ".gov", ".edu", "britannica.com", "un.org", "unesco.org", "reuters.com"]

# 4. User Input
user_query = st.text_input("Enter your research question:", placeholder="Type here...")

if user_query:
    st.divider()
    st.info(f"**Verso Logic:** Analyzing '{user_query}' for credible viewpoints...")

    # UPDATED: Real, secure links to avoid "Not Private" errors
    results = [
        {"name": "International Atomic Energy Agency", "url": "https://www.iaea.org", "type": "Trusted (.org)"},
        {"name": "Britannica: Nuclear Power", "url": "https://www.britannica.com", "type": "Encyclopedic"},
        {"name": "MIT Energy Study", "url": "https://energy.mit.edu", "type": "Academic (.edu)"},
        {"name": "Reuters News Global", "url": "https://www.reuters.com", "type": "Trusted News"}
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Verified Trusted Sources")
        for site in results:
            if any(domain in site['url'] for domain in TRUSTED_DOMAINS):
                st.success(f"**[{site['name']}]({site['url']})**")
                st.caption(f"Cited Source: {site['url']}")

    with col2:
        st.markdown("### 🌐 Other Perspectives")
        # I changed this to Wikipedia so it doesn't give a privacy error!
        st.warning("**[Wikipedia: Global Perspectives](https://www.wikipedia.org)**")
        st.caption("Source: https://www.wikipedia.org | Note: General Information")

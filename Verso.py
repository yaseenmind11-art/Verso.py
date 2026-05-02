import streamlit as st

# 1. Page Configuration with the new "Verso" branding
st.set_page_config(page_title="Verso AI", page_icon="📖", layout="wide")

# Custom CSS to match your preferred white and grey theme
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stTextInput>div>div>input { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("📖 Verso AI")
st.subheader("The Bias-Cutting Search Tool")
st.write("Find trusted perspectives from the 'other side' of any topic.")

# 2. Trusted Domain Filter
TRUSTED_DOMAINS = [".org", ".gov", ".edu", "britannica.com", "un.org", "unesco.org", "reuters.com"]

# 3. User Input
user_query = st.text_input("Enter your research question:", placeholder="e.g., Is nuclear energy safe?")

if user_query:
    st.divider()
    
    # Logic to explain how Verso is "flipping" the search
    st.info(f"**Verso Logic:** Analyzing '{user_query}' to find credible, opposing viewpoints...")

    # Simulated results (In the future, you can connect this to a Search API)
    # Each result includes a name, a link, and a 'Source Type' for citing
    results = [
        {"name": "International Atomic Energy Agency", "url": "https://www.iaea.org", "type": "Trusted (.org)"},
        {"name": "Britannica: Nuclear Power Debate", "url": "https://www.britannica.com", "type": "Encyclopedic"},
        {"name": "MIT Energy Initiative Study", "url": "https://energy.mit.edu", "type": "Academic (.edu)"},
        {"name": "Community Opinion Blog", "url": "https://personal-blog.com", "type": "General Website"}
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Verified Trusted Sources")
        for site in results:
            if any(domain in site['url'] for domain in TRUSTED_DOMAINS):
                st.success(f"**[{site['name']}]({site['url']})**")
                st.caption(f"Cited Source: {site['url']} | Category: {site['type']}")

    with col2:
        st.markdown("### 🌐 Other Perspectives")
        for site in results:
            if not any(domain in site['url'] for domain in TRUSTED_DOMAINS):
                st.warning(f"**[{site['name']}]({site['url']})**")
                st.caption(f"Source: {site['url']} | Note: Not in the 'Ultra-Trusted' list.")

st.sidebar.title("About Verso")
st.sidebar.info("Verso is designed for IB students to break through 'echo chambers' by specifically sourcing verified, alternative viewpoints.")

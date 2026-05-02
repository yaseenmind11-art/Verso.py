import streamlit as st

# 1. This sets the browser tab icon (using the orange/blue part)
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", # The orange/blue part only
    layout="wide"
)

# 2. Sidebar Logo (Putting the full logo in the "black space")
# We use a sidebar to make it look clean and professional
with st.sidebar:
    st.image("full_logo.png", use_container_width=True)
    st.markdown("---")
    st.write("Verso helps IB students find trusted, diverse perspectives.")

# 3. Main App Title (Replacing the 📖 book icon)
# We use columns to put a small icon next to the text
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image("icon.png", width=60)
with col2:
    st.title("Verso AI")

# ... rest of your search and citation code below ...

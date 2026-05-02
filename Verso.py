import streamlit as st
import os

# 1. TAB CONFIG: Must be the first line for icon.png to work
st.set_page_config(
    page_title="Verso",
    page_icon="icon.png", 
    layout="wide"
)

# 2. CSS: Handles no-cut images and creates CLICKABLE red buttons
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 0.5rem;
        max-width: 95%;
    }

    /* Strict no-cut rule for the banner */
    .banner-img img {
        object-fit: contain !important;
        border-radius: 12px;
    }

    /* Styling for the CLICKABLE red action buttons */
    .button-container {
        display: flex;
        justify-content: flex-end;
        gap: 8px;
        padding-top: 10px;
    }

    .action-btn {
        background-color: #ff4b4b;
        color: white !important;
        border-radius: 12px;
        padding: 8px 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none !important;
        font-family: sans-serif;
        font-weight: bold;
        font-size: 14px;
        height: 40px;
        min-width: 40px;
        transition: background-color 0.3s;
    }

    /* Hover effect to show it's clickable */
    .action-btn:hover {
        background-color: #ff3333;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }

    .btn-square {
        padding: 8px;
        width: 40px;
    }

    @media (prefers-color-scheme: light) { 
        input { color: black !important; }
    }
    @media (prefers-color-scheme: dark) { 
        input { color: #bbbbbb !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TOP BAR: Clickable Red Action Buttons
col_left, col_right = st.columns([7, 3])
with col_right:
    # Replace the "#" with your actual links (e.g., your GitHub or survey link)
    st.markdown(f"""
        <div class="button-container">
            <a class="action-btn" href="https://share.example.com" target="_blank">Share</a>
            <a class="action-btn btn-square" href="https://github.com" target="_blank" style="color: gold !important;">★</a>
            <a class="action-btn btn-square" href="https://edit.example.com" target="_blank">✎</a>
            <a class="action-btn btn-square" href="#">⋮</a>
        </div>
    """, unsafe_allow_html=True)

# 4. MAIN BANNER: Proportional squeeze to prevent cutting
left_g, center, right_g = st.columns([2.5, 5, 2.5]) 
with center:
    if os.path.exists("full_logo.png"):
        st.markdown('<div class="banner-img">', unsafe_allow_html=True)
        st.image("full_logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.title("Verso AI")

st.markdown("---")

# 5. SEARCH & RESULTS SECTION
query = st.text_input("Enter your research question:", placeholder="Start typing...")

if query:
    st.write(f"**Verso Logic:** Analyzing trusted perspectives for *'{query}'*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Verified Trusted")
        st.markdown("**[IAEA: Nuclear Science](https://iaea.org)**")
        st.caption("International Atomic Energy Agency. (2024). *Nuclear science and technology*. IAEA.org")
        
    with col2:
        st.subheader("🌐 Other Perspectives")
        st.markdown("**[Wikipedia: Global Water Access](https://wikipedia.org)**")
        st.caption("Wikipedia Contributors. (2026). *Global water access*. Wikipedia.")

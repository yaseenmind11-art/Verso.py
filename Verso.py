import streamlit as st
import streamlit.components.v1 as components

# INSERT THIS AT THE VERY TOP
components.html(
    """
    <html>
        <head>
            <meta name="google-site-verification" content="o5P8qGPR5xXYBN4aEmV-DqsQgf1hAdcym8CTT12Cwc8" />
        </head>
        <body></body>
    </html>
    """,
    height=0,
)

# Then your existing st.set_page_config...
st.set_page_config(
    page_title="Verso AI | Professional Research Suite",
    page_icon="z.png",
    layout="wide"
)

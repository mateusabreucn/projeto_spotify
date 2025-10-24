"""CSS customizado para estilização Spotify no Streamlit."""

import streamlit as st

CUSTOM_CSS = """
<style>
    :root {
        --green: #1DB954;
        --green-dark: #1aa34a;
        --bg-primary: #0F1419;
        --bg-secondary: #1A1F26;
        --text-primary: #FFFFFF;
        --text-secondary: #E0E0E0;
        --orange: #FFA500;
        --red: #FF6B6B;
    }

    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    body {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }

    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--green);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--green-dark);
    }

    .stButton > button {
        background-color: var(--green);
        color: white;
        border: none;
        border-radius: 24px;
        font-weight: 600;
        padding: 8px 32px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(29, 185, 84, 0.2);
    }

    .stButton > button:hover {
        background-color: var(--green-dark);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.3);
        transform: translateY(-2px);
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid rgba(29, 185, 84, 0.2) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--green) !important;
        box-shadow: 0 0 0 3px rgba(29, 185, 84, 0.1) !important;
    }

    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, var(--green) 0%, var(--green-dark) 100%);
        box-shadow: 0 0 8px rgba(29, 185, 84, 0.4);
    }

    .streamlit-expanderHeader {
        background-color: transparent;
        border: 1px solid rgba(29, 185, 84, 0.2);
        border-radius: 8px;
        padding: 12px 16px;
    }

    .streamlit-expanderHeader:hover {
        background-color: rgba(29, 185, 84, 0.05);
        border-color: var(--green);
    }

    a {
        color: var(--green);
        text-decoration: none;
    }

    a:hover {
        color: var(--green-dark);
        text-decoration: underline;
    }

    pre {
        background-color: var(--bg-secondary) !important;
        border-left: 3px solid var(--green);
        border-radius: 4px;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: var(--green);
        border-color: var(--green);
    }

    hr {
        border-color: rgba(29, 185, 84, 0.2);
    }
</style>
"""


def inject_custom_css():
    """Injeta CSS customizado na página."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

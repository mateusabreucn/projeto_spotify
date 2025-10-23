"""CSS customizado para estilização avançada do Streamlit."""

CUSTOM_CSS = """
<style>
    /* === VARIÁVEIS DE COR === */
    :root {
        --spotify-green: #1DB954;
        --spotify-green-dark: #1aa34a;
        --black-primary: #0F1419;
        --black-secondary: #1A1F26;
        --text-primary: #FFFFFF;
        --text-secondary: #E0E0E0;
        --warning-color: #FFA500;
        --error-color: #FF6B6B;
    }

    /* === GLOBAL === */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    body {
        background-color: var(--black-primary);
        color: var(--text-primary);
    }

    /* === SCROLLBAR === */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--black-secondary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--spotify-green);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--spotify-green-dark);
    }

    /* === BOTÕES === */
    .stButton > button {
        background-color: var(--spotify-green);
        color: white;
        border: none;
        border-radius: 24px;
        font-weight: 600;
        padding: 8px 32px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(29, 185, 84, 0.2);
    }

    .stButton > button:hover {
        background-color: var(--spotify-green-dark);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.3);
        transform: translateY(-2px);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* === INPUTS === */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: var(--black-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid rgba(29, 185, 84, 0.2) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--spotify-green) !important;
        box-shadow: 0 0 0 3px rgba(29, 185, 84, 0.1) !important;
    }

    /* === SLIDERS === */
    .stSlider > div > div > div {
        background-color: var(--black-secondary);
    }

    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, var(--spotify-green) 0%, var(--spotify-green-dark) 100%);
        box-shadow: 0 0 8px rgba(29, 185, 84, 0.4);
    }

    /* === EXPANDER === */
    .streamlit-expanderHeader {
        background-color: transparent;
        border: 1px solid rgba(29, 185, 84, 0.2);
        border-radius: 8px;
        padding: 12px 16px;
        transition: all 0.2s ease;
    }

    .streamlit-expanderHeader:hover {
        background-color: rgba(29, 185, 84, 0.05);
        border-color: var(--spotify-green);
    }

    /* === DATAFRAME === */
    .streamlit-dataframe {
        border: 1px solid rgba(29, 185, 84, 0.1);
        border-radius: 8px;
        overflow: hidden;
    }

    .streamlit-dataframe tr:nth-child(even) {
        background-color: rgba(29, 185, 84, 0.02);
    }

    .streamlit-dataframe tr:hover {
        background-color: rgba(29, 185, 84, 0.08);
    }

    .streamlit-dataframe th {
        background-color: var(--spotify-green) !important;
        color: white !important;
        font-weight: 600;
    }

    /* === DIVIDERS === */
    hr {
        border-color: rgba(29, 185, 84, 0.2);
    }

    /* === LINKS === */
    a {
        color: var(--spotify-green);
        text-decoration: none;
        transition: color 0.2s ease;
    }

    a:hover {
        color: var(--spotify-green-dark);
        text-decoration: underline;
    }

    /* === CODE BLOCKS === */
    pre {
        background-color: var(--black-secondary) !important;
        border-left: 3px solid var(--spotify-green);
        border-radius: 4px;
        padding: 12px;
    }

    code {
        background-color: rgba(29, 185, 84, 0.1);
        color: var(--spotify-green);
        padding: 2px 6px;
        border-radius: 3px;
    }

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
    }

    .stTabs [data-baseweb="tab"] {
        border-bottom: 2px solid transparent;
        color: var(--text-secondary);
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: var(--spotify-green);
        border-color: var(--spotify-green);
    }

    /* === MODAIS/POPUPS === */
    .streamlit-modal {
        background-color: var(--black-secondary);
        border: 1px solid rgba(29, 185, 84, 0.2);
        border-radius: 12px;
    }

    /* === SIDEBAR === */
    .streamlit-sidebar {
        background-color: var(--black-secondary);
        border-right: 1px solid rgba(29, 185, 84, 0.1);
    }

    .streamlit-sidebar .element-container {
        color: var(--text-primary);
    }

    /* === METRIC === */
    [data-testid="metric-container"] {
        background-color: var(--black-secondary);
        border: 1px solid rgba(29, 185, 84, 0.15);
        border-radius: 8px;
        padding: 16px;
    }

    /* === RESPONSIVO === */
    @media (max-width: 640px) {
        .stButton > button {
            width: 100%;
        }

        .streamlit-dataframe {
            font-size: 12px;
        }
    }

    /* === ANIMAÇÕES === */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .streamlit-container {
        animation: fadeIn 0.3s ease-out;
    }

    /* === CLASSE PARA ALERTS CUSTOMIZADOS === */
    .spotify-alert {
        border-left: 4px solid var(--spotify-green);
        background-color: rgba(29, 185, 84, 0.1);
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
    }

    .spotify-alert.success {
        border-left-color: var(--spotify-green);
        background-color: rgba(29, 185, 84, 0.1);
    }

    .spotify-alert.error {
        border-left-color: var(--error-color);
        background-color: rgba(255, 107, 107, 0.1);
    }

    .spotify-alert.warning {
        border-left-color: var(--warning-color);
        background-color: rgba(255, 165, 0, 0.1);
    }
</style>
"""


def inject_custom_css():
    """Injeta CSS customizado na página Streamlit."""
    import streamlit as st

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# Exemplo de uso no app.py:
# from src.custom_css import inject_custom_css
#
# def main():
#     st.set_page_config(...)
#     inject_custom_css()
#     # ... resto do código

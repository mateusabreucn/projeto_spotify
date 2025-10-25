"""Configurações centralizadas do projeto."""

import os
import streamlit as st
from dotenv import load_dotenv

# Tenta carregar do .env primeiro (para desenvolvimento local)
load_dotenv()

# Função para obter credenciais com fallback entre secrets e .env
def _get_spotify_credentials():
    """Obtém credenciais do Spotify com fallback: st.secrets → .env → variáveis de ambiente."""
    try:
        # Tenta st.secrets primeiro (Streamlit Cloud)
        client_id = st.secrets.get("SPOTIFY_CLIENT_ID", "").strip()
        client_secret = st.secrets.get("SPOTIFY_CLIENT_SECRET", "").strip()
        if client_id and client_secret:
            return client_id, client_secret
    except (AttributeError, FileNotFoundError, KeyError):
        # st.secrets não está disponível ou não encontrado
        pass
    
    # Fallback para .env ou variáveis de ambiente
    client_id = os.getenv("SPOTIFY_CLIENT_ID", "").strip()
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "").strip()
    return client_id, client_secret

# Carrega credenciais
SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET = _get_spotify_credentials()

TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE = "https://api.spotify.com/v1"

FEATURE_COLS = [
    "danceability",
    "energy",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "speechiness",
    "loudness",
]

VIBE_LABELS_BASE = [
    "Party / Upbeat",
    "Chill / Acoustic",
    "Happy / Feel-good",
]

VIBE_LABELS_EXTENDED = [
    "Party / Upbeat",
    "Chill / Acoustic",
    "Happy / Feel-good",
    "Dark / Intense",
    "Instrumental / Dreamy",
    "Romantic / Smooth",
    "Energetic / Aggressive",
    "Melancholic / Sad",
]

DEFAULT_CLUSTERS = 4
PAGE_TITLE = "Spotify Vibes - Classificação"
LAYOUT = "wide"


def get_vibe_labels(n_clusters: int) -> list[str]:
    """Retorna labels de vibes para o número de clusters."""
    n = max(3, min(8, n_clusters))
    return VIBE_LABELS_EXTENDED[:n]


def validate_config() -> tuple[bool, list[str]]:
    """Valida se as configurações necessárias estão definidas."""
    errors = []
    if not SPOTIFY_CLIENT_ID:
        errors.append("SPOTIFY_CLIENT_ID não definido")
    if not SPOTIFY_CLIENT_SECRET:
        errors.append("SPOTIFY_CLIENT_SECRET não definido")
    return len(errors) == 0, errors

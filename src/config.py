"""Configurações centralizadas do projeto Spotify Playlist Analyzer."""

import os

from dotenv import load_dotenv

load_dotenv()

# =========================
# Configurações da API Spotify (Client Credentials)
# =========================
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "").strip()
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "").strip()

# URLs da API Spotify
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE = "https://api.spotify.com/v1"

# =========================
# Configurações do Dataset
# =========================
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

# =========================
# Configurações das Vibes
# =========================
# Vibes base (3-4)
VIBE_LABELS_BASE = [
    "Party / Upbeat",
    "Chill / Acoustic",
    "Happy / Feel-good",
]

# Vibes adicionais (5+)
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


def get_vibe_labels(n_clusters: int) -> list[str]:
    """Retorna labels de vibes baseado no número de clusters.

    Args:
        n_clusters: Número de clusters (3-8)

    Returns:
        list: Labels de vibes apropriados
    """
    n_clusters = max(3, min(8, n_clusters))  # Limita entre 3 e 8
    return VIBE_LABELS_EXTENDED[:n_clusters]

# =========================
# Configurações da Interface
# =========================
PAGE_TITLE = "Spotify + Dataset local (Vibes Clustering)"
LAYOUT = "wide"


# =========================
# Validação das configurações
# =========================
def validate_config() -> tuple[bool, list[str]]:
    """Valida se as configurações necessárias estão definidas."""
    errors = []

    if not SPOTIFY_CLIENT_ID:
        errors.append("SPOTIFY_CLIENT_ID não está definido no .env")

    if not SPOTIFY_CLIENT_SECRET:
        errors.append("SPOTIFY_CLIENT_SECRET não está definido no .env")

    return len(errors) == 0, errors

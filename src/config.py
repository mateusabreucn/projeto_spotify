"""Configurações centralizadas do projeto."""

import os

from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "").strip()
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "").strip()

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
PAGE_TITLE = "Spotify + Dataset Vibes Clustering"
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

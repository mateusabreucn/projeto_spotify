"""Autenticação e cliente da API Spotify usando Client Credentials Flow."""

import requests
import streamlit as st

from .config import API_BASE, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, TOKEN_URL


def get_spotify_token() -> str:
    """Obtém token de acesso com cache em session state.
    
    Returns:
        Token de acesso válido
        
    Raises:
        RuntimeError: Se autenticação falhar
    """
    if "spotify_token" in st.session_state:
        return st.session_state.spotify_token

    auth = (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    data = {"grant_type": "client_credentials"}

    try:
        response = requests.post(TOKEN_URL, auth=auth, data=data, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Erro ao autenticar: {e}") from e

    token = response.json().get("access_token")
    if not token:
        raise RuntimeError("Token de acesso não obtido")

    st.session_state.spotify_token = token
    return token


def api_get(path: str, params: dict | None = None) -> requests.Response:
    """Requisição GET autenticada para API Spotify.
    
    Args:
        path: Endpoint (ex: "/playlists/{id}/tracks")
        params: Query string parameters
        
    Returns:
        Response HTTP
        
    Raises:
        RuntimeError: Se requisição falhar
    """
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}

    try:
        return requests.get(
            f"{API_BASE}{path}",
            headers=headers,
            params=params,
            timeout=30,
        )
    except requests.RequestException as e:
        raise RuntimeError(f"Erro na requisição: {e}") from e

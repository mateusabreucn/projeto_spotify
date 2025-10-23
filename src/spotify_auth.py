"""Módulo para autenticação com Spotify usando Client Credentials Flow."""

import requests
import streamlit as st

from .config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, TOKEN_URL, API_BASE


def get_spotify_token() -> str:
    """Obtém token de acesso usando Client Credentials Flow.

    Returns:
        str: Token de acesso válido

    Raises:
        RuntimeError: Se não conseguir autenticar
    """
    # Verifica se há token em cache
    if "spotify_token" in st.session_state:
        return st.session_state.spotify_token

    # Credenciais
    auth = (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

    # Dados da requisição
    data = {"grant_type": "client_credentials"}

    # Faz requisição para obter token
    try:
        response = requests.post(TOKEN_URL, auth=auth, data=data, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        msg = f"Erro ao autenticar com Spotify: {e}"
        raise RuntimeError(msg) from e

    token_data = response.json()
    token = token_data.get("access_token")

    if not token:
        msg = "Não foi possível obter token de acesso"
        raise RuntimeError(msg)

    # Armazena em cache
    st.session_state.spotify_token = token
    return token


def api_get(path: str, params: dict | None = None) -> requests.Response:
    """Faz requisição GET autenticada para API do Spotify.

    Args:
        path: Caminho do endpoint (ex: "/playlists/{id}/tracks")
        params: Parâmetros da query string

    Returns:
        Response: Resposta da API

    Raises:
        RuntimeError: Se falhar na autenticação ou requisição
    """
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}

    try:
        return requests.get(
            f"{API_BASE}{path}",
            headers=headers,
            params=params,
            timeout=30
        )
    except requests.RequestException as e:
        msg = f"Erro na requisição da API: {e}"
        raise RuntimeError(msg) from e

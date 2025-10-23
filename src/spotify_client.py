"""Versão melhorada sem login necessário - Client Credentials Flow."""

import requests
from .config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, TOKEN_URL, API_BASE


class SpotifyAPI:
    """Cliente para Spotify API com Client Credentials (sem login necessário)."""

    def __init__(self):
        self.access_token = None
        self.token_type = None

    def authenticate(self) -> bool:
        """Autentica usando Client Credentials (não requer interação do usuário)."""
        if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
            raise ValueError("SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET são obrigatórios")

        data = {
            "grant_type": "client_credentials",
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        }

        try:
            response = requests.post(TOKEN_URL, data=data, timeout=10)
            response.raise_for_status()

            token_data = response.json()
            self.access_token = token_data.get("access_token")
            self.token_type = token_data.get("token_type", "Bearer")

            return bool(self.access_token)
        except requests.RequestException as e:
            print(f"Erro ao autenticar com Spotify: {e}")
            return False

    def get(self, endpoint: str, params: dict | None = None) -> requests.Response:
        """Faz requisição GET autenticada."""
        if not self.access_token:
            if not self.authenticate():
                msg = "Falha na autenticação com Spotify"
                raise RuntimeError(msg)

        headers = {"Authorization": f"{self.token_type} {self.access_token}"}
        url = f"{API_BASE}{endpoint}"

        return requests.get(url, headers=headers, params=params, timeout=30)


# Instância global
spotify_client = SpotifyAPI()
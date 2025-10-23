"""Módulo para interações com a API do Spotify."""

from .spotify_auth import api_get


def extract_playlist_id(s: str) -> str | None:
    """Extrai ID da playlist de URL ou string do Spotify."""
    s = (s or "").strip()
    if s.startswith("spotify:playlist:"):
        s = s.split("spotify:playlist:")[1]
    elif "open.spotify.com/playlist/" in s:
        s = s.split("open.spotify.com/playlist/")[1]

    for sep in ("?", "&", "#", "/"):
        if sep in s:
            s = s.split(sep)[0]

    return s if len(s) == 22 else None


def fetch_playlist_tracks(playlist_id: str) -> tuple[list[dict], list[str], list[str]]:
    """Busca todas as tracks de uma playlist.

    Args:
        playlist_id: ID da playlist no Spotify

    Returns:
        tuple: (tracks_data, track_names, artist_names)
    """
    tracks_raw = []
    params = {"limit": 100, "offset": 0}

    while True:
        r = api_get(f"/playlists/{playlist_id}/tracks", params=params)
        if r.status_code != 200:
            msg = f"Erro ao ler playlist: {r.status_code} {r.text}"
            raise RuntimeError(msg)

        data = r.json()
        items = data.get("items", [])
        tracks_raw.extend(items)

        if data.get("next"):
            params["offset"] += params["limit"]
        else:
            break

    tracks, names, artists = [], [], []
    for it in tracks_raw:
        t = (it or {}).get("track") or {}
        if not t or t.get("is_local") or t.get("type") != "track":
            continue

        tid = t.get("id")
        if not tid:
            continue

        tracks.append(t)
        names.append(t.get("name", ""))

        artist_str = ", ".join(
            [a.get("name", "") for a in (t.get("artists") or []) if a.get("name")]
        )
        artists.append(artist_str)

    # Remove duplicatas por ID
    seen = set()
    uniq_tracks, uniq_names, uniq_artists = [], [], []

    for t, n, a in zip(tracks, names, artists, strict=False):
        tid = t.get("id")
        if tid and tid not in seen:
            seen.add(tid)
            uniq_tracks.append(t)
            uniq_names.append(n)
            uniq_artists.append(a)

    return uniq_tracks, uniq_names, uniq_artists


def get_playlist_info(playlist_id: str) -> dict:
    """Obtém informações básicas de uma playlist.

    Args:
        playlist_id: ID da playlist no Spotify

    Returns:
        dict: Informações da playlist (nome, descrição, etc.)
    """
    r = api_get(f"/playlists/{playlist_id}")
    if r.status_code != 200:
        msg = f"Erro ao buscar playlist: {r.status_code} {r.text}"
        raise RuntimeError(msg)

    return r.json()


def get_user_playlists(limit: int = 20) -> list[dict]:
    """Obtém playlists do usuário autenticado.

    Args:
        limit: Número máximo de playlists a retornar

    Returns:
        list: Lista de playlists do usuário
    """
    r = api_get("/me/playlists", params={"limit": limit})
    if r.status_code != 200:
        msg = f"Erro ao buscar playlists: {r.status_code} {r.text}"
        raise RuntimeError(msg)

    return r.json().get("items", [])


def get_user_profile() -> dict:
    """Obtém perfil do usuário autenticado.

    Returns:
        dict: Dados do perfil do usuário
    """
    r = api_get("/me")
    if r.status_code != 200:
        msg = f"Erro ao buscar perfil: {r.status_code} {r.text}"
        raise RuntimeError(msg)

    return r.json()

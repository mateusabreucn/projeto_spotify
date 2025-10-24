"""Interações com API Spotify."""

from .spotify_auth import api_get


def extract_playlist_id(s: str) -> str | None:
    """Extrai ID da playlist de URL ou string Spotify."""
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
    """Busca todas as tracks de uma playlist."""
    tracks_raw = []
    params = {"limit": 100, "offset": 0}

    while True:
        r = api_get(f"/playlists/{playlist_id}/tracks", params=params)
        if r.status_code != 200:
            raise RuntimeError(f"Erro ao ler playlist: {r.status_code} {r.text}")

        data = r.json()
        items = data.get("items", [])
        tracks_raw.extend(items)

        if not data.get("next"):
            break
        params["offset"] += params["limit"]

    tracks, names, artists = [], [], []
    seen = set()

    for item in tracks_raw:
        t = (item or {}).get("track") or {}
        if not t or t.get("is_local") or t.get("type") != "track":
            continue

        tid = t.get("id")
        if not tid or tid in seen:
            continue

        seen.add(tid)
        tracks.append(t)
        names.append(t.get("name", ""))
        artist_str = ", ".join([a.get("name", "") for a in (t.get("artists") or [])])
        artists.append(artist_str)

    return tracks, names, artists


def get_playlist_info(playlist_id: str) -> dict:
    """Obtém informações básicas de uma playlist."""
    r = api_get(f"/playlists/{playlist_id}")
    if r.status_code != 200:
        raise RuntimeError(f"Erro ao buscar playlist: {r.status_code}")
    return r.json()


def get_user_playlists(limit: int = 20) -> list[dict]:
    """Obtém playlists do usuário."""
    r = api_get("/me/playlists", params={"limit": limit})
    if r.status_code != 200:
        raise RuntimeError(f"Erro ao buscar playlists: {r.status_code}")
    return r.json().get("items", [])


def get_user_profile() -> dict:
    """Obtém perfil do usuário."""
    r = api_get("/me")
    if r.status_code != 200:
        raise RuntimeError(f"Erro ao buscar perfil: {r.status_code}")
    return r.json()

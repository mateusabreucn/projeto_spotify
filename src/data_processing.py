"""Módulo para processamento de dados e merge com dataset local."""

import numpy as np
import pandas as pd

from .config import FEATURE_COLS
from .spotify_api import extract_playlist_id, fetch_playlist_tracks


def normalize_artists_string(s: str) -> str:
    """Normaliza string de artistas para comparação."""
    if pd.isna(s):
        return ""

    txt = str(s)
    for ch in ["[", "]", "'", '"']:
        txt = txt.replace(ch, "")
    txt = txt.replace(";", ",")

    return ", ".join([p.strip().lower() for p in txt.split(",") if p.strip()])


def load_local_dataset(file) -> pd.DataFrame:
    """Carrega e processa dataset local com audio features.

    Args:
        file: Arquivo CSV carregado

    Returns:
        DataFrame processado com colunas normalizadas

    Raises:
        ValueError: Se colunas obrigatórias não existem
    """
    df = pd.read_csv(file)
    must_have = {"id", "name", "artists"}

    if not must_have.issubset(set(df.columns)):
        msg = f"O CSV precisa conter colunas: {must_have}. Encontrado: {list(df.columns)}"
        raise ValueError(msg)

    # Normaliza colunas para merge
    df["sid_norm"] = df["id"].astype(str)
    df["name_norm"] = df["name"].astype(str).str.strip().str.lower()
    df["artist_norm"] = df["artists"].map(normalize_artists_string)

    # Garante que audio features existem (com NaN se ausentes)
    for c in FEATURE_COLS:
        if c not in df.columns:
            df[c] = np.nan

    # Mantém apenas colunas relevantes
    keep = ["sid_norm", "name_norm", "artist_norm", "name", "artists", *FEATURE_COLS]
    return df[keep].copy()


def merge_playlist_with_local(
    tracks: list[dict], names: list[str], artists: list[str], local_df: pd.DataFrame
) -> pd.DataFrame:
    """Faz merge entre tracks da playlist e dataset local.

    Args:
        tracks: Lista de tracks do Spotify
        names: Lista de nomes das tracks
        artists: Lista de artistas
        local_df: DataFrame do dataset local

    Returns:
        DataFrame com tracks que foram encontradas no dataset local
    """
    # Garante que local_df tem as colunas normalizadas
    if "sid_norm" not in local_df.columns:
        local_df = local_df.copy()
        local_df["sid_norm"] = local_df["id"].astype(str)
    if "name_norm" not in local_df.columns:
        local_df["name_norm"] = local_df["name"].astype(str).str.strip().str.lower()
    if "artist_norm" not in local_df.columns:
        local_df["artist_norm"] = local_df["artists"].map(normalize_artists_string)

    # Cria DataFrame da playlist
    pl = pd.DataFrame(
        {
            "sid_norm": [t.get("id") for t in tracks],
            "name_norm": pd.Series(names, dtype=str).str.strip().str.lower(),
            "artist_norm": pd.Series([normalize_artists_string(a) for a in artists], dtype=str),
            "track_name": names,
            "artists_raw": artists,
        }
    )

    # Primeiro merge: por ID do Spotify
    df = pl.merge(local_df, on="sid_norm", how="left", suffixes=("", "_loc"))

    # Segundo merge: fallback por nome + artista para tracks sem match por ID
    miss = df[FEATURE_COLS].isna().any(axis=1)

    if miss.any():
        aux = local_df.drop_duplicates(subset=["name_norm", "artist_norm"]).copy()
        joined = df.loc[miss, ["name_norm", "artist_norm"]].merge(
            aux[["name_norm", "artist_norm", *FEATURE_COLS]],
            on=["name_norm", "artist_norm"],
            how="left",
        )

        # Atualiza features ausentes
        for c in FEATURE_COLS:
            df.loc[miss, c] = joined[c].values

    # Retorna apenas tracks com todas as features
    got = df.dropna(subset=FEATURE_COLS, how="any").copy()
    return got


def analyze_playlist_with_dataset(playlist_url_or_id: str, local_df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline completo de análise de playlist com dataset local.

    Args:
        playlist_url_or_id: URL ou ID da playlist
        local_df: DataFrame do dataset local

    Returns:
        DataFrame com tracks processadas e features

    Raises:
        ValueError: Se playlist inválida ou sem tracks compatíveis
    """
    # Extrai ID da playlist
    pid = extract_playlist_id(playlist_url_or_id)
    if not pid:
        msg = "URL/ID da playlist inválido."
        raise ValueError(msg)

    # Busca tracks da playlist
    tracks, names, artists = fetch_playlist_tracks(pid)
    if not tracks:
        msg = "Playlist sem itens de catálogo acessíveis."
        raise ValueError(msg)

    # Faz merge com dataset local
    merged = merge_playlist_with_local(tracks, names, artists, local_df)
    if merged.empty:
        msg = (
            "Nenhuma faixa da playlist foi encontrada no dataset local "
            "(por ID ou por nome+artista)."
        )
        raise ValueError(msg)

    return merged


def prepare_features_for_ml(df: pd.DataFrame) -> np.ndarray:
    """Prepara features para machine learning.

    Args:
        df: DataFrame com audio features

    Returns:
        Array numpy com features processadas
    """
    x = df[FEATURE_COLS].astype(float).to_numpy()
    return np.nan_to_num(x, nan=0.0)


def get_dataset_stats(df: pd.DataFrame) -> dict:
    """Calcula estatísticas do dataset.

    Args:
        df: DataFrame a ser analisado

    Returns:
        Dicionário com estatísticas básicas
    """
    stats = {
        "total_tracks": len(df),
        "unique_artists": df.get("artist_norm", pd.Series()).nunique(),
        "features_mean": df[FEATURE_COLS].mean().to_dict(),
        "features_std": df[FEATURE_COLS].std().to_dict(),
        "missing_features": df[FEATURE_COLS].isna().sum().to_dict(),
    }

    return stats

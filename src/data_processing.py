"""Processamento de dados e merge com dataset local."""

import numpy as np
import pandas as pd

from .config import FEATURE_COLS
from .spotify_api import extract_playlist_id, fetch_playlist_tracks


def _normalize_artists_string(s: str) -> str:
    """Normaliza string de artistas para comparação."""
    if pd.isna(s):
        return ""

    txt = str(s)
    for ch in ["[", "]", "'", '"', ";"]:
        txt = txt.replace(ch, "")
    return ", ".join([p.strip().lower() for p in txt.split(",") if p.strip()])


def load_local_dataset(file) -> pd.DataFrame:
    """Carrega dataset local com features de áudio."""
    df = pd.read_csv(file)
    required = {"id", "name", "artists"}

    if not required.issubset(df.columns):
        raise ValueError(f"Colunas obrigatórias: {required}")

    df["sid_norm"] = df["id"].astype(str)
    df["name_norm"] = df["name"].astype(str).str.strip().str.lower()
    df["artist_norm"] = df["artists"].map(_normalize_artists_string)

    for col in FEATURE_COLS:
        if col not in df.columns:
            df[col] = np.nan

    keep = ["sid_norm", "name_norm", "artist_norm", "name", "artists", *FEATURE_COLS]
    return df[keep].copy()


def merge_playlist_with_local(
    tracks: list[dict], names: list[str], artists: list[str], local_df: pd.DataFrame
) -> pd.DataFrame:
    """Faz merge entre tracks da playlist e dataset local."""
    if "sid_norm" not in local_df.columns:
        local_df = local_df.copy()
        local_df["sid_norm"] = local_df["id"].astype(str)
    if "name_norm" not in local_df.columns:
        local_df["name_norm"] = local_df["name"].astype(str).str.strip().str.lower()
    if "artist_norm" not in local_df.columns:
        local_df["artist_norm"] = local_df["artists"].map(_normalize_artists_string)

    pl = pd.DataFrame({
        "sid_norm": [t.get("id") for t in tracks],
        "name_norm": pd.Series(names, dtype=str).str.strip().str.lower(),
        "artist_norm": pd.Series([_normalize_artists_string(a) for a in artists], dtype=str),
        "track_name": names,
        "artists_raw": artists,
    })

    df = pl.merge(local_df, on="sid_norm", how="left", suffixes=("", "_loc"))

    miss = df[FEATURE_COLS].isna().any(axis=1)
    if miss.any():
        aux = local_df.drop_duplicates(subset=["name_norm", "artist_norm"]).copy()
        joined = df.loc[miss, ["name_norm", "artist_norm"]].merge(
            aux[["name_norm", "artist_norm", *FEATURE_COLS]],
            on=["name_norm", "artist_norm"],
            how="left",
        )

        for col in FEATURE_COLS:
            df.loc[miss, col] = joined[col].values

    return df.dropna(subset=FEATURE_COLS, how="any").copy()


def analyze_playlist_with_dataset(playlist_url_or_id: str, local_df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline completo de análise de playlist."""
    pid = extract_playlist_id(playlist_url_or_id)
    if not pid:
        raise ValueError("URL/ID da playlist inválido")

    tracks, names, artists = fetch_playlist_tracks(pid)
    if not tracks:
        raise ValueError("Playlist vazia ou sem itens acessíveis")

    merged = merge_playlist_with_local(tracks, names, artists, local_df)
    if merged.empty:
        raise ValueError("Nenhuma faixa encontrada no dataset local")

    return merged


def prepare_features_for_ml(df: pd.DataFrame) -> np.ndarray:
    """Prepara features para machine learning."""
    x = df[FEATURE_COLS].astype(float).to_numpy()
    return np.nan_to_num(x, nan=0.0)


def get_dataset_stats(df: pd.DataFrame) -> dict:
    """Calcula estatísticas do dataset."""
    return {
        "total_tracks": len(df),
        "unique_artists": df.get("artist_norm", pd.Series()).nunique(),
        "features_mean": df[FEATURE_COLS].mean().to_dict(),
        "features_std": df[FEATURE_COLS].std().to_dict(),
    }

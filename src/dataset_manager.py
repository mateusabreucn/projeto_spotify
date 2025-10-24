"""Gerenciamento do dataset Kaggle com cache otimizado."""

from pathlib import Path

import pandas as pd
import streamlit as st

from .config import FEATURE_COLS

KAGGLE_DATASET = "bwandowando/spotify-songs-with-attributes-and-lyrics"
DATASET_CACHE_DIR = Path.home() / ".cache" / "spotify_analyzer"
DATASET_PARQUET = "spotify_songs.parquet"


def ensure_dataset_cached() -> Path:
    """Garante que o dataset está em formato parquet (otimizado)."""
    parquet_file = DATASET_CACHE_DIR / DATASET_PARQUET

    if parquet_file.exists():
        return parquet_file

    DATASET_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    try:
        import kagglehub
    except ImportError:
        raise RuntimeError("kagglehub não instalado. Execute: pip install kagglehub") from None

    try:
        dataset_path = Path(kagglehub.dataset_download(KAGGLE_DATASET))
        csv_files = list(dataset_path.glob("*.csv"))

        if not csv_files:
            raise RuntimeError(f"Nenhum CSV encontrado em {dataset_path}")

        source_csv = next((f for f in csv_files if "attributes" in f.name.lower()), None)
        if source_csv is None:
            csv_files.sort(key=lambda x: x.stat().st_size, reverse=True)
            source_csv = csv_files[0]

        df = pd.read_csv(source_csv, low_memory=False)
        df.to_parquet(parquet_file, compression="snappy", index=False)
        return parquet_file

    except Exception as e:
        raise RuntimeError(f"Erro ao baixar dataset: {e}") from e


def load_kaggle_dataset() -> pd.DataFrame:
    """Carrega dataset Kaggle com cache Streamlit."""
    
    @st.cache_data(ttl=3600, show_spinner=False)
    def _load_and_process():
        parquet_path = ensure_dataset_cached()
        df = pd.read_parquet(parquet_path)

        required = {"id", "name", "artists"}
        if not required.issubset(df.columns):
            raise ValueError(f"Colunas obrigatórias faltando: {required}")

        available_features = [c for c in FEATURE_COLS if c in df.columns]
        keep_cols = ["id", "name", "artists", *available_features]
        df = df[keep_cols].copy()
        df = df.drop_duplicates(subset=["id"]).dropna(subset=["id"])

        return df

    return _load_and_process()

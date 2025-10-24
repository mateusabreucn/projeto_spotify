"""Gerenciamento do dataset Kaggle com cache otimizado."""

from pathlib import Path

import pandas as pd
import streamlit as st

KAGGLE_DATASET = "bwandowando/spotify-songs-with-attributes-and-lyrics"
DATASET_CACHE_DIR = Path.home() / ".cache" / "spotify_analyzer"
DATASET_PARQUET = "spotify_songs.parquet"

# Colunas que queremos manter (remove Lyrics, key, mode e outras colunas pesadas/desnecessárias)
REQUIRED_COLUMNS = [
    "id",
    "name",
    "album_name",
    "artists",
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "duration_ms",
]


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

        # OTIMIZAÇÃO CRÍTICA: Carrega apenas colunas específicas
        # Isso evita carregar Lyrics, key, mode e outras colunas pesadas
        print(f"📥 Carregando dataset de: {source_csv}")
        
        # Lê apenas o header para verificar colunas disponíveis
        df_header = pd.read_csv(source_csv, nrows=0)
        available_cols = df_header.columns.tolist()
        
        # Filtra apenas as colunas que existem E que precisamos
        cols_to_load = [col for col in REQUIRED_COLUMNS if col in available_cols]
        
        print(f"✅ Colunas selecionadas ({len(cols_to_load)}): {', '.join(cols_to_load)}")
        print(f"❌ Colunas ignoradas: Lyrics, key, mode e outras (~{len(available_cols) - len(cols_to_load)} colunas)")
        # Carrega CSV APENAS com as colunas selecionadas
        # usecols é a chave: evita carregar dados desnecessários da memória
        df = pd.read_csv(
            source_csv,
            usecols=cols_to_load,
            low_memory=False,
            dtype={
                'id': 'str',
                'name': 'str',
                'album_name': 'str',
                'artists': 'str',
                'danceability': 'float32',
                'energy': 'float32',
                'loudness': 'float32',
                'speechiness': 'float32',
                'acousticness': 'float32',
                'instrumentalness': 'float32',
                'liveness': 'float32',
                'valence': 'float32',
                'tempo': 'float32',
                'duration_ms': 'int32',
            }
        )
        print(f"💾 Salvando {len(df):,} linhas em formato Parquet...")
        # Salva em formato parquet comprimido (muito mais eficiente que CSV)
        df.to_parquet(parquet_file, compression="snappy", index=False)
        print("✅ Dataset salvo com sucesso!")

        # Mostra economia de espaço
        csv_size = source_csv.stat().st_size / (1024 * 1024)  # MB
        parquet_size = parquet_file.stat().st_size / (1024 * 1024)  # MB
        print(f"📊 CSV original: {csv_size:.1f} MB → Parquet otimizado: {parquet_size:.1f} MB")
        print(f"   Economia: {((csv_size - parquet_size) / csv_size * 100):.1f}%")
        return parquet_file

    except Exception as e:
        raise RuntimeError(f"Erro ao baixar dataset: {e}") from e


def load_kaggle_dataset() -> pd.DataFrame:
    """Carrega dataset Kaggle com cache Streamlit."""

    @st.cache_data(ttl=3600, show_spinner=False)
    def _load_and_process():
        parquet_path = ensure_dataset_cached()
        # Carrega parquet de forma otimizada
        df = pd.read_parquet(parquet_path)

        required = {"id", "name", "artists"}
        if not required.issubset(df.columns):
            raise ValueError(f"Colunas obrigatórias faltando: {required}")

        # Remove duplicatas e valores nulos
        df = df.drop_duplicates(subset=["id"]).dropna(subset=["id"])
        # Garante que todas as colunas necessárias estão presentes
        required = {"id", "name", "artists"}
        if not required.issubset(df.columns):
            raise ValueError(f"Colunas obrigatórias faltando: {required}")

        return df

    return _load_and_process()

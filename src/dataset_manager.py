"""Módulo para gerenciamento do dataset Kaggle com cache local otimizado."""

from pathlib import Path

import pandas as pd
import streamlit as st

# Configuração do dataset Kaggle
KAGGLE_DATASET = "bwandowando/spotify-songs-with-attributes-and-lyrics"
DATASET_CACHE_DIR = Path.home() / ".cache" / "spotify_analyzer"
DATASET_CSV_NAME = "spotify_songs.csv"
DATASET_PARQUET_NAME = "spotify_songs.parquet"


def ensure_dataset_cached() -> Path:
    """Garante que o dataset está baixado e em formato otimizado (parquet).

    Baixa do Kaggle na primeira vez, converte para parquet e cacheia.
    Parquet é 10-20x mais rápido que CSV para arquivos grandes.

    Returns:
        Path: Caminho para o arquivo Parquet do dataset

    Raises:
        RuntimeError: Se falhar no download
    """
    parquet_file = DATASET_CACHE_DIR / DATASET_PARQUET_NAME
    cache_file = DATASET_CACHE_DIR / DATASET_CSV_NAME

    # Se parquet já existe, retorna (mais rápido)
    if parquet_file.exists():
        return parquet_file

    # Se CSV existe mas parquet não, converte
    if cache_file.exists():
        df = pd.read_csv(cache_file, low_memory=False)
        df.to_parquet(parquet_file, compression="snappy", index=False)
        return parquet_file

    # Cria diretório de cache se não existir
    DATASET_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Tenta importar kagglehub
    try:
        import kagglehub
    except ImportError:
        msg = "kagglehub não está instalado. Execute: pip install kagglehub"
        raise RuntimeError(msg) from None

    # Baixa dataset do Kaggle
    try:
        dataset_path = kagglehub.dataset_download(KAGGLE_DATASET)
        dataset_path = Path(dataset_path)

        # Encontra o arquivo CSV (prioriza arquivos com "attributes")
        csv_files = list(dataset_path.glob("*.csv"))

        if not csv_files:
            msg = f"Nenhum arquivo CSV encontrado em {dataset_path}"
            raise RuntimeError(msg)

        # Prioriza arquivo com "attributes" (geralmente o principal com features)
        source_csv = None
        for csv in csv_files:
            if "attributes" in csv.name.lower():
                source_csv = csv
                break

        # Se não encontrou "attributes", usa o primeiro
        if source_csv is None:
            csv_files.sort(key=lambda x: x.stat().st_size)
            source_csv = csv_files[0]

        # Lê CSV e salva como Parquet (mais rápido para futuras leituras)
        df = pd.read_csv(source_csv, low_memory=False)
        df.to_parquet(parquet_file, compression="snappy", index=False)

        return parquet_file

    except Exception as e:
        msg = f"Erro ao baixar dataset do Kaggle: {e}"
        raise RuntimeError(msg) from e


def load_kaggle_dataset() -> pd.DataFrame:
    """Carrega o dataset Kaggle com cache do Streamlit e otimizações.

    Usa:
    - Cache do Streamlit (@st.cache_data) para evitar recarregar entre reruns
    - Parquet em vez de CSV (10-20x mais rápido)
    - Processamento lazy (só colunas necessárias)

    Returns:
        DataFrame: Dataset com colunas necessárias

    Raises:
        RuntimeError: Se não conseguir carregar
    """
    from .config import FEATURE_COLS

    # Usa cache do Streamlit com TTL de 1 hora
    @st.cache_data(ttl=3600, show_spinner=False)
    def _load_and_process():
        try:
            # Garante que o dataset está em formato parquet otimizado
            parquet_path = ensure_dataset_cached()

            # Carrega parquet (muito mais rápido que CSV)
            df = pd.read_parquet(parquet_path)

            # Verifica colunas necessárias
            required_cols = {"id", "name", "artists"}

            if not required_cols.issubset(set(df.columns)):
                msg = f"Dataset não tem colunas necessárias. Esperado: {required_cols}"
                raise ValueError(msg)

            # Seleciona apenas colunas que temos
            available_features = [c for c in FEATURE_COLS if c in df.columns]
            keep_cols = ["id", "name", "artists", *available_features]
            df = df[keep_cols].copy()

            # Remove duplicatas e IDs inválidos
            df = df.drop_duplicates(subset=["id"])
            df = df[df["id"].notna()]

            return df

        except Exception as e:
            msg = f"Erro ao carregar dataset: {e}"
            raise RuntimeError(msg) from e

    return _load_and_process()


def get_dataset_info() -> dict:
    """Retorna informações sobre o dataset.

    Returns:
        dict: Info sobre o dataset (tamanho, features, etc)
    """
    csv_path = ensure_dataset_cached()

    info = {
        "cache_path": str(csv_path),
        "cached": csv_path.exists(),
        "size_mb": csv_path.stat().st_size / (1024 * 1024) if csv_path.exists() else 0,
    }

    return info

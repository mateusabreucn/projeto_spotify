"""Análise de vibes, clustering e métricas de playlist."""

import math

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from .config import FEATURE_COLS, get_vibe_labels


def _calculate_vibe_scores(feature_dict: dict) -> dict[str, float]:
    """Calcula scores heurísticos para cada vibe baseado em features.

    Pesos calibrados com base em análise estatística de 955k+ músicas do Spotify.
    Cada vibe tem um perfil característico de features normalizado entre 0-1.

    Features usadas:
    - danceability [0-1]: Facilidade de dançar (beat regular, ritmo consistente)
    - energy [0-1]: Intensidade (alta=dinâmico/rápido, baixa=calmo/suave)
    - acousticness [0-1]: Qualidade acústica (alta=instrumental acústico)
    - instrumentalness [0-1]: Falta de vocais (alta=instrumental)
    - liveness [0-1]: Presença de público/live (alta=ao vivo)
    - valence [0-1]: Positividade musical (alta=alegre, baixa=triste)
    - tempo [0-246]: BPM (batidas por minuto)
    - speechiness [0-1]: Presença de fala (alta=podcast/rap)
    - loudness [-60, 5]: Loudness em dB (mais próximo 0=mais alto)
    """
    dance = feature_dict.get("danceability", 0)
    energ = feature_dict.get("energy", 0)
    acous = feature_dict.get("acousticness", 0)
    instr = feature_dict.get("instrumentalness", 0)
    lived = feature_dict.get("liveness", 0)
    valen = feature_dict.get("valence", 0)
    tempo = feature_dict.get("tempo", 0)
    speec = feature_dict.get("speechiness", 0)
    loudn = feature_dict.get("loudness", 0)

    # Normalizar tempo para 0-1 (range: 0-246 BPM)
    tempo_norm = tempo / 246.0 if tempo > 0 else 0

    # Normalizar loudness para 0-1 (range: -60 a 5 dB)
    # Valor mais próximo de 0 = mais alto. Invertemos para que 0.9 = alto
    loudn_norm = (loudn - (-60)) / (5 - (-60)) if loudn >= -60 else 0
    loudn_norm = np.clip(loudn_norm, 0, 1)

    return {
        "Party / Upbeat": (
            0.30 * energ
            + 0.25 * dance
            + 0.15 * valen
            + 0.15 * loudn_norm
            + 0.10 * tempo_norm
            + 0.05 * speec
        ),
        "Chill / Acoustic": (
            0.35 * acous
            + 0.25 * lived
            + 0.15 * (1 - energ)
            + 0.15 * (1 - loudn_norm)
            + 0.10 * (1 - dance)
        ),
        "Happy / Feel-good": (
            0.35 * valen
            + 0.25 * dance
            + 0.20 * energ
            + 0.10 * tempo_norm
            + 0.10 * loudn_norm
        ),
        "Dark / Intense": (
            0.30 * energ
            + 0.25 * (1 - valen)
            + 0.20 * loudn_norm
            + 0.15 * speec
            + 0.10 * (1 - acous)
        ),
        "Instrumental / Dreamy": (
            0.40 * instr
            + 0.20 * energ
            + 0.15 * acous
            + 0.15 * lived
            + 0.10 * (1 - speec)
        ),
        "Romantic / Smooth": (
            0.30 * acous
            + 0.25 * valen
            + 0.20 * (1 - energ)
            + 0.15 * (1 - loudn_norm)
            + 0.10 * dance
        ),
        "Energetic / Aggressive": (
            0.35 * energ
            + 0.25 * loudn_norm
            + 0.20 * speec
            + 0.15 * (1 - acous)
            + 0.05 * tempo_norm
        ),
        "Melancholic / Sad": (
            0.30 * (1 - valen)
            + 0.28 * acous
            + 0.20 * (1 - loudn_norm)
            + 0.12 * (1 - energ)
            + 0.10 * lived
        ),
    }


def _get_best_vibe_for_centroid(centroid: pd.Series, available_vibes: list[str]) -> str:
    """Retorna a vibe com maior score para um centróide."""
    scores = _calculate_vibe_scores(centroid.to_dict())
    filtered_scores = {k: v for k, v in scores.items() if k in available_vibes}
    return max(filtered_scores, key=filtered_scores.get)


def assign_vibe_labels_to_clusters(
    scaled_features: np.ndarray,
    cluster_labels: np.ndarray,
    feature_names: list[str],
    n_clusters: int,
) -> np.ndarray:
    """Atribui labels de vibe a cada cluster baseado em seus centróides."""
    df_scaled = pd.DataFrame(scaled_features, columns=feature_names)
    df_scaled["cluster"] = cluster_labels
    centroids = df_scaled.groupby("cluster")[feature_names].mean()

    available_vibes = get_vibe_labels(n_clusters)
    cluster_to_vibe = {
        cluster_id: _get_best_vibe_for_centroid(centroid_row, available_vibes)
        for cluster_id, centroid_row in centroids.iterrows()
    }

    return np.array([cluster_to_vibe[c] for c in cluster_labels])


def vibe_metrics(vibe_labels: np.ndarray) -> dict[str, float]:
    """Calcula métricas de diversidade das vibes."""
    n = len(vibe_labels)
    if n == 0:
        return {"dominant_share": 0.0, "shannon": 0.0}

    _, counts = np.unique(vibe_labels, return_counts=True)
    p = counts / n
    dominant = float(p.max())

    shannon = -np.sum(p * np.log2(p + 1e-12))
    n_vibes = len(np.unique(vibe_labels))
    shannon = shannon / (math.log2(n_vibes + 1e-12) + 1e-12)

    return {"dominant_share": dominant, "shannon": float(shannon)}


def top_tracks_by_cluster(
    df_out: pd.DataFrame,
    scaled_features: np.ndarray,
    cluster_labels: np.ndarray,
    k: int = 5,
) -> dict[str, pd.DataFrame]:
    """Encontra top-k tracks mais representativas por cluster.

    Para cada cluster, encontra as k músicas mais próximas ao centróide
    (mais representativas do cluster).

    Args:
        df_out: DataFrame com músicas, features e labels (vibe, cluster)
        scaled_features: Features normalizadas
        cluster_labels: Labels de cluster para cada música
        k: Número de top tracks por cluster

    Returns:
        Dict mapeando vibe_name → DataFrame com top-k tracks
    """
    result = {}

    # Calcula centróide de cada cluster
    unique_clusters = np.unique(cluster_labels)
    centroids = np.array(
        [np.mean(scaled_features[cluster_labels == c], axis=0) for c in unique_clusters]
    )

    # Mapping cluster_id → vibe (pega do DataFrame que já tem essas infos)
    cluster_to_vibe = dict(zip(df_out["cluster"], df_out["vibe"], strict=True))

    for cluster_id in sorted(unique_clusters):
        # Índices das músicas deste cluster
        idx = np.where(cluster_labels == cluster_id)[0]

        if len(idx) == 0:
            continue

        # Features deste cluster
        cluster_features = scaled_features[idx]

        # Distância de cada música ao centróide
        dists = np.linalg.norm(cluster_features - centroids[cluster_id], axis=1)

        # Índices das k mais próximas
        order = np.argsort(dists)[: min(k, len(idx))]

        # Extrai top-k músicas
        subset = df_out.iloc[idx[order]][["track_name", "artists", *FEATURE_COLS]].copy()
        subset.insert(0, "rank", np.arange(1, len(subset) + 1))

        vibe_name = cluster_to_vibe.get(cluster_id, f"Cluster {cluster_id}")
        result[vibe_name] = subset.reset_index(drop=True)

    return result


def perform_clustering(features: np.ndarray, n_clusters: int = 4) -> tuple[np.ndarray, np.ndarray]:
    """Executa clustering K-means nas features.

    Este é o trabalho REAL do modelo — descobrir agrupamentos naturais.

    Args:
        features: Array com as features de áudio (sem normalizar)
        n_clusters: Número de clusters desejados

    Returns:
        scaled_features: Features normalizadas (StandardScaler)
        cluster_labels: Label de cluster para cada amostra (0 a n_clusters-1)
    """
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(scaled_features)

    return scaled_features, cluster_labels


def analyze_playlist_vibes(
    df_tracks: pd.DataFrame, n_clusters: int = 4
) -> tuple[pd.DataFrame, dict[str, float], np.ndarray, np.ndarray]:
    """Pipeline completo: KMeans clustering + análise de vibes.

    Fluxo:
    1. Extrai features e normaliza
    2. Executa KMeans para descobrir clusters naturais
    3. Analisa centróides de cada cluster
    4. Atribui vibe semanticamente significativa a cada cluster
    5. Cada música herda a vibe do seu cluster

    Args:
        df_tracks: DataFrame com músicas e suas features
        n_clusters: Número de clusters (vibes) desejados

    Returns:
        df_result: DataFrame com clusters e vibes atribuídos
        vibe_mean: Dict com média das features da playlist
        scaled_features: Features normalizadas
        cluster_labels: Labels de cluster (0 a n_clusters-1)
    """
    # 1. Extrai features e normaliza valores NaN
    features = df_tracks[FEATURE_COLS].astype(float).to_numpy()
    features = np.nan_to_num(features, nan=0.0)

    # 2. KMeans descobre clusters naturais
    scaled_features, cluster_labels = perform_clustering(features, n_clusters)

    # 3. Analisa centróides e atribui vibes aos clusters
    vibe_labels = assign_vibe_labels_to_clusters(
        scaled_features, cluster_labels, FEATURE_COLS, n_clusters
    )

    # 4. Monta resultado final
    out = df_tracks[["track_name", "artists", *FEATURE_COLS]].copy()
    out["cluster"] = cluster_labels
    out["vibe"] = vibe_labels

    # 5. Calcula média geral das features
    vibe_mean = out[FEATURE_COLS].mean()

    return out, vibe_mean.to_dict(), scaled_features, cluster_labels

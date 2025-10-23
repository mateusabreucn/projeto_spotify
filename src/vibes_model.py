"""Módulo para análise de vibes, clustering e métricas de playlist."""

import math

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from .config import FEATURE_COLS, get_vibe_labels


def _soft_norm(x: np.ndarray) -> np.ndarray:
    """Normaliza por z-score e comprime extremos para [0,1] via tanh."""
    z = (x - np.nanmean(x)) / (np.nanstd(x) + 1e-8)
    return 0.5 * (1 + np.tanh(z))


def score_vibes_on_centroid(center: pd.Series, n_vibes: int = 4) -> dict[str, float]:
    """Calcula scores heurísticos de vibe baseado no centróide.

    Args:
        center: Centróide nas features padronizadas (z-score)
        n_vibes: Número de vibes desejadas (3-8)

    Returns:
        dict: Mapeamento label->score para cada vibe
    """
    # Reconstrói dicionário para acessar por nome
    c = center.to_dict()

    # Para itens em z-score, usar sinais intuitivos
    energy = c.get("energy", 0)
    dance = c.get("danceability", 0)
    val = c.get("valence", 0)
    tempo = c.get("tempo", 0)
    acoust = c.get("acousticness", 0)
    instr = c.get("instrumentalness", 0)
    speech = c.get("speechiness", 0)
    loud = c.get("loudness", 0)

    # Heurísticas para cada vibe
    party = 0.35 * energy + 0.35 * dance + 0.20 * val + 0.10 * tempo
    chill = 0.45 * acoust + 0.30 * instr + 0.15 * (-energy) + 0.10 * (-loud)
    happy = 0.5 * val + 0.3 * dance + 0.2 * tempo
    dark = 0.45 * (-val) + 0.30 * energy + 0.15 * loud + 0.10 * speech
    instrumental = 0.6 * instr + 0.2 * acoust + 0.1 * (-energy) + 0.1 * (-speech)
    romantic = 0.4 * val + 0.3 * acoust + 0.2 * instr + 0.1 * (-energy)
    aggressive = 0.4 * energy + 0.3 * loud + 0.2 * dance + 0.1 * speech
    melancholic = 0.5 * (-val) + 0.3 * acoust + 0.1 * instr + 0.1 * (-energy)

    scores = {
        "Party / Upbeat": party,
        "Chill / Acoustic": chill,
        "Happy / Feel-good": happy,
        "Dark / Intense": dark,
        "Instrumental / Dreamy": instrumental,
        "Romantic / Smooth": romantic,
        "Energetic / Aggressive": aggressive,
        "Melancholic / Sad": melancholic,
    }

    # Retorna apenas as vibes solicitadas
    vibe_labels = get_vibe_labels(n_vibes)
    return {k: v for k, v in scores.items() if k in vibe_labels}


def assign_vibe_labels(
    scaled_features: np.ndarray,
    labels: np.ndarray,
    feature_names: list[str],
    n_vibes: int = 4,
) -> tuple[np.ndarray, pd.DataFrame]:
    """Atribui labels de vibe aos clusters.

    Args:
        scaled_features: Features padronizadas
        labels: Labels de cluster
        feature_names: Nomes das features
        n_vibes: Número de vibes

    Returns:
        tuple: (vibe_labels_por_track, df_centroids_com_rotulo)
    """
    df_scaled = pd.DataFrame(scaled_features, columns=feature_names)
    df_scaled["cluster"] = labels
    centroids = df_scaled.groupby("cluster")[feature_names].mean()

    # Rotula por argmax dos scores
    vibe_for_cluster = {}
    for k, row in centroids.iterrows():
        scores = score_vibes_on_centroid(row, n_vibes)
        vibe = max(scores, key=scores.get)
        vibe_for_cluster[k] = vibe

    # Aplica rótulo por faixa
    vibe_labels = np.array([vibe_for_cluster[c] for c in labels])

    # Tabela de centróides com rótulos
    centroids["vibe"] = centroids.index.map(lambda k: vibe_for_cluster[k])
    return vibe_labels, centroids.reset_index()


def vibe_metrics(vibe_labels: np.ndarray) -> dict[str, float]:
    """Calcula métricas de diversidade das vibes.

    Args:
        vibe_labels: Array com labels de vibe

    Returns:
        dict: Métricas calculadas (dominant_share, shannon)
    """
    n = len(vibe_labels)
    if n == 0:
        return {"dominant_share": 0, "shannon": 0}

    # Distribuição
    _, counts = np.unique(vibe_labels, return_counts=True)
    p = counts / n
    dominant = p.max()

    # Shannon entropy normalizada
    shannon = -np.sum(p * np.log2(p + 1e-12))
    shannon /= math.log2(len(np.unique(vibe_labels)) + 1e-12)  # normalizado 0..1

    return {"dominant_share": float(dominant), "shannon": float(shannon)}


def perform_clustering(features: np.ndarray, n_clusters: int = 4) -> tuple[np.ndarray, np.ndarray]:
    """Executa clustering K-means nas features.

    Args:
        features: Array de features
        n_clusters: Número de clusters

    Returns:
        tuple: (features_padronizadas, labels_cluster)
    """
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(scaled_features)

    return scaled_features, cluster_labels


def top_tracks_by_cluster(
    df_out: pd.DataFrame,
    scaled_features: np.ndarray,
    labels: np.ndarray,
    k: int = 5,
    n_vibes: int = 4,
) -> dict[str, pd.DataFrame]:
    """Encontra top-k tracks mais representativas por cluster.

    Args:
        df_out: DataFrame com informações das tracks
        scaled_features: Features padronizadas
        labels: Labels de cluster
        k: Número de tracks por cluster
        n_vibes: Número de vibes

    Returns:
        dict: Mapeamento vibe->DataFrame com top tracks
    """
    feature_cols = FEATURE_COLS
    result = {}

    # Calcula centróides
    centers = []
    for c in sorted(np.unique(labels)):
        centers.append(np.mean(scaled_features[labels == c, :], axis=0))
    centers = np.stack(centers, axis=0)  # [K, D]

    # Mapeia cluster->vibe
    vibe_of_cluster = {}
    _, centroids = assign_vibe_labels(scaled_features, labels, feature_cols, n_vibes=n_vibes)
    for row in centroids.itertuples():
        vibe_of_cluster[row.cluster] = row.vibe

    for c in sorted(np.unique(labels)):
        idx = np.where(labels == c)[0]
        cluster_features = scaled_features[idx]
        center = centers[c]

        # Distância euclidiana ao centróide (menor = mais representativo)
        dists = np.linalg.norm(cluster_features - center, axis=1)
        order = np.argsort(dists)[:k]

        subset = df_out.iloc[idx[order]][["track_name", "artists", *FEATURE_COLS]].copy()
        subset.insert(0, "rank", np.arange(1, len(subset) + 1))
        result[vibe_of_cluster[c]] = subset.reset_index(drop=True)

    return result


def analyze_playlist_vibes(
    df_tracks: pd.DataFrame, n_clusters: int = 4
) -> tuple[pd.DataFrame, dict[str, float], np.ndarray, np.ndarray]:
    """Pipeline completo de análise de vibes em playlist.

    Args:
        df_tracks: DataFrame com tracks e features
        n_clusters: Número de clusters/vibes

    Returns:
        tuple: (df_resultado, vibe_mean, features_padronizadas, cluster_labels)
    """
    # Prepara features para ML
    features = df_tracks[FEATURE_COLS].astype(float).to_numpy()
    features = np.nan_to_num(features, nan=0.0)

    # Clustering
    scaled_features, cluster_labels = perform_clustering(features, n_clusters)

    # Atribui vibes com suporte a n_clusters dinâmico
    vibe_labels, _ = assign_vibe_labels(
        scaled_features, cluster_labels, FEATURE_COLS, n_vibes=n_clusters
    )

    # Constrói DataFrame resultado
    out = df_tracks[["track_name", "artists", *FEATURE_COLS]].copy()
    out["cluster"] = cluster_labels
    out["vibe"] = vibe_labels

    # Calcula médias das features
    vibe_mean = out[FEATURE_COLS].mean()

    return out, vibe_mean.to_dict(), scaled_features, cluster_labels


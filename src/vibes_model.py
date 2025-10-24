"""Análise de vibes, clustering e métricas de playlist."""

import math

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from .config import FEATURE_COLS, get_vibe_labels


def _calculate_vibe_scores(c: dict) -> dict[str, float]:
    """Calcula scores heurísticos para cada vibe baseado em features."""
    e = c.get("energy", 0)
    d = c.get("danceability", 0)
    v = c.get("valence", 0)
    t = c.get("tempo", 0)
    a = c.get("acousticness", 0)
    i = c.get("instrumentalness", 0)
    s = c.get("speechiness", 0)
    l = c.get("loudness", 0)

    return {
        "Party / Upbeat": 0.35 * e + 0.35 * d + 0.20 * v + 0.10 * t,
        "Chill / Acoustic": 0.45 * a + 0.30 * i + 0.15 * (-e) + 0.10 * (-l),
        "Happy / Feel-good": 0.5 * v + 0.3 * d + 0.2 * t,
        "Dark / Intense": 0.45 * (-v) + 0.30 * e + 0.15 * l + 0.10 * s,
        "Instrumental / Dreamy": 0.6 * i + 0.2 * a + 0.1 * (-e) + 0.1 * (-s),
        "Romantic / Smooth": 0.4 * v + 0.3 * a + 0.2 * i + 0.1 * (-e),
        "Energetic / Aggressive": 0.4 * e + 0.3 * l + 0.2 * d + 0.1 * s,
        "Melancholic / Sad": 0.5 * (-v) + 0.3 * a + 0.1 * i + 0.1 * (-e),
    }


def score_vibes_on_centroid(center: pd.Series, n_vibes: int = 4) -> dict[str, float]:
    """Calcula scores de vibe baseado no centróide."""
    scores = _calculate_vibe_scores(center.to_dict())
    vibe_labels = get_vibe_labels(n_vibes)
    return {k: v for k, v in scores.items() if k in vibe_labels}


def assign_vibe_labels(
    scaled_features: np.ndarray,
    labels: np.ndarray,
    feature_names: list[str],
    n_vibes: int = 4,
) -> tuple[np.ndarray, pd.DataFrame]:
    """Atribui labels de vibe aos clusters."""
    df_scaled = pd.DataFrame(scaled_features, columns=feature_names)
    df_scaled["cluster"] = labels
    centroids = df_scaled.groupby("cluster")[feature_names].mean()

    vibe_for_cluster = {}
    for k, row in centroids.iterrows():
        scores = score_vibes_on_centroid(row, n_vibes)
        vibe_for_cluster[k] = max(scores, key=scores.get)

    vibe_labels = np.array([vibe_for_cluster[c] for c in labels])
    centroids["vibe"] = centroids.index.map(vibe_for_cluster)
    
    return vibe_labels, centroids.reset_index()


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


def perform_clustering(features: np.ndarray, n_clusters: int = 4) -> tuple[np.ndarray, np.ndarray]:
    """Executa clustering K-means nas features."""
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
    """Encontra top-k tracks mais representativas por cluster."""
    result = {}
    
    centers = np.array([np.mean(scaled_features[labels == c], axis=0) for c in np.unique(labels)])
    
    _, centroids = assign_vibe_labels(scaled_features, labels, FEATURE_COLS, n_vibes=n_vibes)
    vibe_of_cluster = dict(zip(centroids["cluster"], centroids["vibe"]))

    for c in sorted(np.unique(labels)):
        idx = np.where(labels == c)[0]
        cluster_features = scaled_features[idx]
        dists = np.linalg.norm(cluster_features - centers[c], axis=1)
        order = np.argsort(dists)[:k]

        subset = df_out.iloc[idx[order]][["track_name", "artists", *FEATURE_COLS]].copy()
        subset.insert(0, "rank", np.arange(1, len(subset) + 1))
        result[vibe_of_cluster[c]] = subset.reset_index(drop=True)

    return result


def analyze_playlist_vibes(
    df_tracks: pd.DataFrame, n_clusters: int = 4
) -> tuple[pd.DataFrame, dict[str, float], np.ndarray, np.ndarray]:
    """Pipeline completo de análise de vibes em playlist."""
    features = df_tracks[FEATURE_COLS].astype(float).to_numpy()
    features = np.nan_to_num(features, nan=0.0)

    scaled_features, cluster_labels = perform_clustering(features, n_clusters)
    vibe_labels, _ = assign_vibe_labels(
        scaled_features, cluster_labels, FEATURE_COLS, n_vibes=n_clusters
    )

    out = df_tracks[["track_name", "artists", *FEATURE_COLS]].copy()
    out["cluster"] = cluster_labels
    out["vibe"] = vibe_labels

    vibe_mean = out[FEATURE_COLS].mean()

    return out, vibe_mean.to_dict(), scaled_features, cluster_labels


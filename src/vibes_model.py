"""Analise de vibes usando classificacao supervisionada."""

import math
import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from .config import FEATURE_COLS

MODEL_DIR = Path('models')
MODEL_FILE = MODEL_DIR / 'vibe_classifier.pkl'
SCALER_FILE = MODEL_DIR / 'vibe_scaler.pkl'


def load_vibe_classifier():
    if not MODEL_FILE.exists() or not SCALER_FILE.exists():
        raise FileNotFoundError(
            'Modelo nao encontrado. Execute: python train_vibe_classifier.py'
        )
    with MODEL_FILE.open('rb') as f:
        classifier = pickle.load(f)
    with SCALER_FILE.open('rb') as f:
        scaler = pickle.load(f)
    return classifier, scaler


def predict_vibes(features):
    classifier, scaler = load_vibe_classifier()
    scaled_features = scaler.transform(features)
    vibe_labels = classifier.predict(scaled_features)
    return scaled_features, vibe_labels


def vibe_metrics(vibe_labels):
    n = len(vibe_labels)
    if n == 0:
        return {'dominant_share': 0.0, 'shannon': 0.0}
    _, counts = np.unique(vibe_labels, return_counts=True)
    p = counts / n
    dominant = float(p.max())
    shannon = -np.sum(p * np.log2(p + 1e-12))
    n_vibes = len(np.unique(vibe_labels))
    shannon = shannon / (math.log2(n_vibes + 1e-12) + 1e-12)
    return {'dominant_share': dominant, 'shannon': float(shannon)}


def top_tracks_by_cluster(df_out, scaled_features, cluster_labels, k=5):
    result = {}
    unique_vibes = df_out['vibe'].unique()
    for vibe_name in sorted(unique_vibes):
        idx = df_out['vibe'] == vibe_name
        vibe_indices = np.where(idx)[0]
        if len(vibe_indices) == 0:
            continue
        vibe_features = scaled_features[vibe_indices]
        centroid = np.mean(vibe_features, axis=0)
        dists = np.linalg.norm(vibe_features - centroid, axis=1)
        order = np.argsort(dists)[:min(k, len(vibe_indices))]
        cols_to_show = ['track_name', 'artists']
        for col in FEATURE_COLS:
            if col in df_out.columns:
                cols_to_show.append(col)
        subset = df_out.iloc[vibe_indices[order]][cols_to_show].copy()
        subset.insert(0, 'rank', np.arange(1, len(subset) + 1))
        result[vibe_name] = subset.reset_index(drop=True)
    return result


def analyze_playlist_vibes(df_tracks, n_clusters=None):
    features = df_tracks[FEATURE_COLS].astype(float).to_numpy()
    features = np.nan_to_num(features, nan=0.0)
    scaled_features, vibe_labels = predict_vibes(features)
    out = df_tracks[['track_name', 'artists', *FEATURE_COLS]].copy()
    out['vibe'] = vibe_labels
    unique_vibes = np.unique(vibe_labels)
    vibe_to_cluster = {vibe: idx for idx, vibe in enumerate(unique_vibes)}
    out['cluster'] = out['vibe'].map(vibe_to_cluster)
    cluster_labels = out['cluster'].values
    vibe_mean = out[FEATURE_COLS].mean()
    return out, vibe_mean.to_dict(), scaled_features, cluster_labels

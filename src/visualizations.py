"""Visualizações e gráficos do projeto."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.decomposition import PCA

from .config import FEATURE_COLS

VIBE_COLORS = {
    "Party / Upbeat": "#e41a1c",
    "Chill / Acoustic": "#377eb8",
    "Happy / Feel-good": "#4daf4a",
    "Dark / Intense": "#984ea3",
    "Instrumental / Dreamy": "#ff7f00",
    "Romantic / Smooth": "#e74c3c",
    "Energetic / Aggressive": "#2ecc71",
    "Melancholic / Sad": "#9b59b6",
}


def plot_cluster_scatter(scaled_features: np.ndarray, cluster_labels: np.ndarray, vibe_labels: np.ndarray):
    """Gráfico de dispersão PCA 2D dos clusters por vibe."""
    pca = PCA(n_components=2, random_state=42)
    xy = pca.fit_transform(scaled_features)

    plt.figure(figsize=(6, 5))

    for vibe in np.unique(vibe_labels):
        mask = vibe_labels == vibe
        plt.scatter(
            xy[mask, 0],
            xy[mask, 1],
            s=18,
            alpha=0.75,
            label=vibe,
            c=VIBE_COLORS.get(vibe, "#333"),
        )

    plt.title("Clusters por Vibe (PCA 2D)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend(loc="best", fontsize=8)
    st.pyplot(plt.gcf())


def plot_vibe_bars(vibe_labels: np.ndarray):
    """Gráfico de barras da distribuição de vibes."""
    vals = pd.Series(vibe_labels).value_counts()

    plt.figure(figsize=(6, 3))
    colors = [VIBE_COLORS.get(v, "#333") for v in vals.index]
    plt.bar(range(len(vals)), vals.values, color=colors)
    plt.xticks(range(len(vals)), vals.index, rotation=15, ha="right")
    plt.ylabel("Número de Faixas")
    plt.title("Distribuição de Faixas por Vibe")
    plt.tight_layout()
    st.pyplot(plt.gcf())


def plot_radar_by_vibe(df_out: pd.DataFrame):
    """Gráfico radar com perfil médio de features por vibe."""
    feats = FEATURE_COLS

    mm = df_out[feats].astype(float)
    mm = (mm - mm.min()) / (mm.max() - mm.min() + 1e-9)
    means = mm.join(df_out["vibe"]).groupby("vibe")[feats].mean()

    angles = np.linspace(0, 2 * np.pi, len(feats), endpoint=False)
    angles = np.concatenate([angles, angles[:1]])

    plt.figure(figsize=(8, 6))
    ax = plt.subplot(111, polar=True)

    for vibe, row in means.iterrows():
        vals = np.concatenate([row.values, row.values[:1]])
        ax.plot(angles, vals, "o-", linewidth=2, label=vibe, c=VIBE_COLORS.get(vibe, "#333"))
        ax.fill(angles, vals, alpha=0.15, c=VIBE_COLORS.get(vibe, "#333"))

    ax.set_thetagrids(angles[:-1] * 180 / np.pi, feats, fontsize=9)
    ax.set_title("Perfil Médio de Features por Vibe")
    ax.grid(True)
    plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.05), fontsize=9)
    st.pyplot(plt.gcf())


def plot_feature_distributions(df_out: pd.DataFrame):
    """Histogramas das distribuições de audio features."""
    fig, axes = plt.subplots(3, 3, figsize=(12, 10))
    axes = axes.flatten()

    for i, feat in enumerate(FEATURE_COLS):
        if i < len(axes):
            axes[i].hist(df_out[feat], bins=20, alpha=0.7, color="#1DB954", edgecolor="black")
            axes[i].set_title(feat)
            axes[i].set_ylabel("Frequência")

    for j in range(len(FEATURE_COLS), len(axes)):
        axes[j].remove()

    plt.tight_layout()
    st.pyplot(fig)


def plot_correlation_matrix(df_out: pd.DataFrame):
    """Matriz de correlação das audio features."""
    corr = df_out[FEATURE_COLS].corr()

    plt.figure(figsize=(8, 6))
    im = plt.imshow(corr, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1)

    plt.colorbar(im)
    plt.xticks(range(len(FEATURE_COLS)), FEATURE_COLS, rotation=45, ha="right", fontsize=9)
    plt.yticks(range(len(FEATURE_COLS)), FEATURE_COLS, fontsize=9)
    plt.title("Correlação entre Audio Features")

    for i in range(len(FEATURE_COLS)):
        for j in range(len(FEATURE_COLS)):
            text_color = "white" if abs(corr.iloc[i, j]) > 0.5 else "black"
            plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color=text_color, fontsize=8)

    plt.tight_layout()
    st.pyplot(plt.gcf())


def plot_vibe_comparison(df_out: pd.DataFrame):
    """Comparação de features entre vibes com boxplot."""
    main_features = ["energy", "valence", "danceability", "acousticness"]
    vibes_present = df_out["vibe"].unique()

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for i, feat in enumerate(main_features):
        data_by_vibe = [df_out[df_out["vibe"] == v][feat].values for v in vibes_present]

        if data_by_vibe:
            axes[i].boxplot(data_by_vibe, labels=[v[:15] for v in vibes_present])
            axes[i].set_title(f"{feat.title()} por Vibe")
            axes[i].tick_params(axis="x", rotation=15)

    plt.tight_layout()
    st.pyplot(fig)


def display_top_tracks_tables(top_tracks_dict: dict[str, pd.DataFrame]):
    """Exibe tabelas com top tracks por vibe."""
    st.subheader("Top Faixas por Vibe")
    for vibe, table in top_tracks_dict.items():
        if not table.empty:
            st.markdown(f"**{vibe}**")
            st.dataframe(table, use_container_width=True)


def create_metrics_cards(metrics: dict[str, float], total_tracks: int):
    """Cria cards de métricas principais."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Vibe Dominante", f"{metrics['dominant_share'] * 100:.1f}%")
    with col2:
        st.metric("Diversidade", f"{metrics['shannon']:.2f}")
    with col3:
        st.metric("Total de Faixas", f"{total_tracks}")


def show_vibe_summary_table(df_result: pd.DataFrame):
    """Tabela resumo das vibes encontradas."""
    summary = (
        df_result.groupby("vibe")
        .agg({
            "track_name": "count",
            "energy": "mean",
            "valence": "mean",
            "danceability": "mean",
            "acousticness": "mean",
        })
        .round(3)
    )

    summary.columns = ["Quantidade", "Energy", "Valence", "Dance", "Acoustic"]
    summary["Percentual %"] = (summary["Quantidade"] / len(df_result) * 100).round(1)
    summary = summary.sort_values("Quantidade", ascending=False)

    st.dataframe(summary, use_container_width=True)

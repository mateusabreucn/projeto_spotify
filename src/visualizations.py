"""Módulo para visualizações e gráficos do projeto."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.decomposition import PCA

from .config import FEATURE_COLS


def plot_cluster_scatter(scaled_features: np.ndarray, labels: np.ndarray, vibe_labels: np.ndarray):
    """Gráfico de dispersão dos clusters em projeção PCA 2D.

    Args:
        scaled_features: Features padronizadas
        labels: Labels de cluster
        vibe_labels: Labels de vibe por track
    """
    pca = PCA(n_components=2, random_state=42)
    xy = pca.fit_transform(scaled_features)

    plt.figure(figsize=(6, 5))

    # Mapeamento de cores por vibe
    palette = {
        "Party / Upbeat": "#e41a1c",
        "Chill / Acoustic": "#377eb8",
        "Happy / Feel-good": "#4daf4a",
        "Dark / Intense": "#984ea3",
    }

    for vibe in np.unique(vibe_labels):
        ix = vibe_labels == vibe
        plt.scatter(
            xy[ix, 0], xy[ix, 1], s=18, alpha=0.75, label=vibe, c=palette.get(vibe, "#333333")
        )

    plt.title("Projeção PCA (2D) por Vibe")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend(loc="best", fontsize=8)
    st.pyplot(plt.gcf())


def plot_vibe_bars(vibe_labels: np.ndarray):
    """Gráfico de barras da distribuição de vibes.

    Args:
        vibe_labels: Labels de vibe por track
    """
    vals = pd.Series(vibe_labels).value_counts()

    plt.figure(figsize=(6, 3))
    plt.bar(vals.index, vals.values)
    plt.xticks(rotation=15, ha="right")
    plt.title("Distribuição de faixas por Vibe")
    plt.tight_layout()
    st.pyplot(plt.gcf())


def plot_radar_by_vibe(df_out: pd.DataFrame):
    """Gráfico radar com perfil médio de features por vibe.

    Args:
        df_out: DataFrame com tracks, vibes e features
    """
    feats = FEATURE_COLS

    # Normalização min-max por coluna (dentro da playlist)
    mm = df_out[feats].astype(float)
    mm = (mm - mm.min()) / (mm.max() - mm.min() + 1e-9)

    means = mm.join(df_out["vibe"]).groupby("vibe")[feats].mean()

    labels = feats
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    angles = np.concatenate([angles, angles[:1]])

    plt.figure(figsize=(8, 6))
    ax = plt.subplot(111, polar=True)

    for vibe, row in means.iterrows():
        vals = row.values
        vals = np.concatenate([vals, vals[:1]])
        ax.plot(angles, vals, linewidth=2, label=vibe)
        ax.fill(angles, vals, alpha=0.15)

    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_title("Perfil (radar) médio por Vibe — normalizado dentro da playlist")
    ax.grid(True)
    plt.legend(loc="upper right", bbox_to_anchor=(1.35, 1.05))
    st.pyplot(plt.gcf())


def plot_feature_distributions(df_out: pd.DataFrame):
    """Histogramas das distribuições de audio features.

    Args:
        df_out: DataFrame com features
    """
    fig, axes = plt.subplots(3, 3, figsize=(12, 10))
    axes = axes.flatten()

    for i, feat in enumerate(FEATURE_COLS):
        if i < len(axes):
            axes[i].hist(df_out[feat], bins=20, alpha=0.7, color="skyblue", edgecolor="black")
            axes[i].set_title(f"{feat}")
            axes[i].set_xlabel("Valor")
            axes[i].set_ylabel("Frequência")

    # Remove axes extras se houver
    for j in range(len(FEATURE_COLS), len(axes)):
        axes[j].remove()

    plt.tight_layout()
    st.pyplot(fig)


def plot_correlation_matrix(df_out: pd.DataFrame):
    """Matriz de correlação das audio features.

    Args:
        df_out: DataFrame com features
    """
    corr = df_out[FEATURE_COLS].corr()

    plt.figure(figsize=(8, 6))
    im = plt.imshow(corr, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1)

    plt.colorbar(im)
    plt.xticks(range(len(FEATURE_COLS)), FEATURE_COLS, rotation=45, ha="right")
    plt.yticks(range(len(FEATURE_COLS)), FEATURE_COLS)
    plt.title("Matriz de Correlação das Audio Features")

    # Adiciona valores na matriz
    for i in range(len(FEATURE_COLS)):
        for j in range(len(FEATURE_COLS)):
            plt.text(
                j,
                i,
                f"{corr.iloc[i, j]:.2f}",
                ha="center",
                va="center",
                color="white" if abs(corr.iloc[i, j]) > 0.5 else "black",
            )

    plt.tight_layout()
    st.pyplot(plt.gcf())


def plot_vibe_comparison(df_out: pd.DataFrame):
    """Comparação das médias de features entre vibes (boxplot).

    Args:
        df_out: DataFrame com tracks, vibes e features
    """
    # Seleciona algumas features principais para visualização
    main_features = ["energy", "valence", "danceability", "acousticness"]
    vibes_present = df_out["vibe"].unique()

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for i, feat in enumerate(main_features):
        if i < len(axes):
            data_by_vibe = [
                df_out[df_out["vibe"] == vibe][feat].values
                for vibe in vibes_present
            ]
            labels_present = list(vibes_present)

            if data_by_vibe:  # Se há dados
                axes[i].boxplot(data_by_vibe, labels=labels_present)
                axes[i].set_title(f"{feat.title()} por Vibe")
                axes[i].tick_params(axis="x", rotation=15)

    plt.tight_layout()
    st.pyplot(fig)


def display_top_tracks_tables(top_tracks_dict: dict[str, pd.DataFrame]):
    """Exibe tabelas com top tracks por vibe.

    Args:
        top_tracks_dict: Dicionário vibe -> DataFrame com top tracks
    """
    st.subheader("Top 5 faixas representativas por Vibe")

    for vibe, table in top_tracks_dict.items():
        if not table.empty:
            st.markdown(f"**{vibe}**")
            st.table(table)


def create_metrics_cards(metrics: dict[str, float], total_tracks: int):
    """Cria cards de métricas principais.

    Args:
        metrics: Dicionário com métricas calculadas
        total_tracks: Número total de tracks
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Dominant Vibe Share", f"{metrics['dominant_share'] * 100:.1f}%")
    with col2:
        st.metric("Vibe Diversity (Shannon)", f"{metrics['shannon']:.2f}")
    with col3:
        st.metric("Total de Faixas", f"{total_tracks}")


def show_vibe_summary_table(df_result: pd.DataFrame):
    """Tabela resumo das vibes encontradas.

    Args:
        df_result: DataFrame com resultados da análise
    """
    summary = (
        df_result.groupby("vibe")
        .agg(
            {
                "track_name": "count",
                "energy": "mean",
                "valence": "mean",
                "danceability": "mean",
                "acousticness": "mean",
            }
        )
        .round(3)
    )

    summary.columns = [
        "Quantidade",
        "Energy Média",
        "Valence Média",
        "Dance Média",
        "Acoustic Média",
    ]
    summary["Percentual"] = (summary["Quantidade"] / len(df_result) * 100).round(1)

    st.dataframe(summary, width="stretch")

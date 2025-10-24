"""Aplicação principal do Spotify Playlist Analyzer."""

import contextlib

import pandas as pd
import streamlit as st

from src.config import FEATURE_COLS, LAYOUT, PAGE_TITLE, validate_config
from src.custom_css import inject_custom_css
from src.data_processing import analyze_playlist_with_dataset
from src.dataset_manager import load_kaggle_dataset
from src.spotify_api import extract_playlist_id, fetch_playlist_tracks
from src.ui_components import (
    chart_section_with_description,
    custom_alert,
    dataset_search_card,
    feature_highlight,
    info_section,
    progress_bar_custom,
    section_divider,
    section_separator,
    show_vibe_averages,
    spotify_hero_header,
    stats_row,
)
from src.vibes_model import (
    analyze_playlist_vibes,
    top_tracks_by_cluster,
    vibe_metrics,
)
from src.visualizations import (
    create_metrics_cards,
    display_top_tracks_tables,
    plot_cluster_scatter,
    plot_radar_by_vibe,
    plot_vibe_bars,
    show_vibe_summary_table,
)


def main():
    """Função principal da aplicação."""
    # Configuração da página
    st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT)

    # Inicializa estado de carregamento do dataset
    if "dataset_loaded" not in st.session_state:
        st.session_state.dataset_loaded = False
    if "dataset_error" not in st.session_state:
        st.session_state.dataset_error = None

    # CSS customizado
    inject_custom_css()

    # Header hero novo
    spotify_hero_header()

    # Valida configurações
    is_valid, errors = validate_config()
    if not is_valid:
        for error in errors:
            custom_alert("Erro de Configuração", error, "error")
        st.stop()

    # Carrega dataset (SEM MOSTRAR AQUI - será carregado em background)
    local_df = load_spotify_dataset_auto(show_section=False)

    # Marca dataset como carregado
    st.session_state.dataset_loaded = True

    # Seção de análise (PRIMEIRA - foco principal)
    show_analysis_section(local_df)

    # Separador visual forte entre seções
    section_separator()

    # Seção de exploração dataset (ÚLTIMA - complementar)
    show_dataset_explorer_section(local_df)


def _format_playlist_error(exc: Exception) -> tuple[str, str]:
    """Returna um título e mensagem amigável para erros de playlist.

    Detecta respostas 404/Resource not found e sugestões para o usuário.
    """
    msg = str(exc)
    # Casos comuns retornados pela API: '404', 'Resource not found', 'status": 404'
    low = msg.lower()
    if "404" in low or "resource not found" in low or "not found" in low:
        title = "Playlist Não Encontrada"
        body = (
            "Não foi possível acessar essa playlist. Tente usar uma "
            "playlist pública (não criada/gerenciada pela conta oficial do Spotify) "
            "e verifique se a URL/ID está correta. Exemplos funcionam: playlists "
            "públicas de usuários ou playlists oficiais (não privadas)."
        )
        return title, body

    # Fallback genérico (sem expor payloads JSON)
    title = "Erro Durante a Análise"
    body = (
        "Ocorreu um problema ao acessar a playlist. Verifique se a URL/ID está correta, "
        "se a playlist é pública e se suas credenciais do Spotify estão válidas."
    )
    return title, body


def _resolve_track_col(df) -> str:
    """Resolve o nome da coluna de título de música no dataset local.

    Prioriza 'track_name', depois 'name'. Levanta ValueError se nenhuma existir.
    """
    if df is None:
        raise ValueError("Dataset ausente")
    if "track_name" in df.columns:
        return "track_name"
    if "name" in df.columns:
        return "name"
    raise ValueError("Dataset não contém coluna 'track_name' nem 'name'.")


def load_spotify_dataset_auto(show_section: bool = True):
    """Carrega dataset Kaggle automaticamente com cache.

    Args:
        show_section: Se True, mostra seção de busca. Se False, apenas carrega.

    Returns:
        DataFrame com o dataset carregado
    """
    try:
        # Carrega dataset do Kaggle (com cache automático)
        with st.spinner("Carregando dataset Kaggle..."):
            local_df = load_kaggle_dataset()

        if not show_section:
            return local_df

        custom_alert(
            "Dataset Carregado com Sucesso",
            f"Identificadas {len(local_df):,} faixas no dataset Kaggle",
            "success",
        )

        # Seção de busca no dataset
        section_divider("Explorar Dataset")
        search_result = dataset_search_card()

        if search_result["execute"] and search_result["query"]:
            query = search_result["query"].lower()
            search_type = search_result["type"]

            # Resolve coluna de título (compatibilidade com diferentes arquivos)
            try:
                track_col = _resolve_track_col(local_df)
            except ValueError as ve:
                custom_alert("Erro no Dataset", str(ve), "error")
                return local_df

            if search_type == "Musica":
                matches = local_df[
                    local_df[track_col].astype(str).str.lower().str.contains(query, na=False)
                ]
            else:
                matches = local_df[local_df["artists"].str.lower().str.contains(query, na=False)]

            if not matches.empty:
                st.success(f"Encontradas {len(matches):,} musicas!")
                cols_show = [track_col, "artists", "energy", "danceability", "valence"]
                available = [c for c in cols_show if c in matches.columns]
                st.dataframe(matches[available].head(20), width="stretch")
            else:
                st.info(f"Nenhuma musica encontrada para '{query}'")

        return local_df

    except Exception as e:
        custom_alert(
            "Erro ao Carregar Dataset",
            (
                f"Nao foi possivel carregar o dataset: {e!s}. "
                "Certifique-se de que o kagglehub esta instalado."
            ),
            "error",
        )
        st.stop()


def show_analysis_section(local_df=None):
    """Exibe seção principal de análise de playlist (SEM dataset).

    Args:
        local_df: DataFrame do dataset (para verificar se está carregado)
    """
    section_divider("🎵 Analisar Sua Playlist")

    # Verifica se dataset está carregando
    dataset_is_loading = not st.session_state.dataset_loaded

    if dataset_is_loading:
        st.warning(
            "⏳ Carregando dataset... Os inputs serão habilitados em breve. "
            "Por favor, aguarde alguns segundos."
        )

    info_section(
        "Cole sua URL de playlist Spotify para descobrir suas vibes musicais. "
        "O sistema analisará cada música e agrupará em clusters temáticos (Vibes).",
        icon="📊",
    )

    # Desabilita o formulário enquanto dataset não carrega
    with st.form("form", border=False):
        pl_url = st.text_input(
            "URL ou ID da Playlist",
            placeholder="https://open.spotify.com/playlist/... ou ID direto",
            disabled=dataset_is_loading,
        )
        k = st.slider(
            "Quantas Vibes Você Quer? (3-8)",
            3,
            8,
            5,
            1,
            disabled=dataset_is_loading,
        )

        col1, col2, col3 = st.columns([1.5, 1, 1])
        with col1:
            st.write("")  # Espaçamento
        with col2:
            run = st.form_submit_button(
                "▶️ Analisar",
                use_container_width=True,
                disabled=dataset_is_loading,
            )
        with col3:
            if st.form_submit_button(
                "🔄 Limpar",
                use_container_width=True,
                disabled=dataset_is_loading,
            ):
                st.rerun()

    # Exemplos de playlists (também desabilitados se carregando)
    with st.expander("💡 Sugestões de Playlists para Testar", expanded=False):
        if dataset_is_loading:
            st.info("Aguarde o carregamento do dataset para ver sugestões...")
        else:
            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown("### ✅ Excelente Compatibilidade (>80%)")
                feature_highlight(
                    "Peaceful Piano",
                    "ID: 37i9dQZF1DX4sWSpwFbBpm",
                    icon="🎹",
                )
                feature_highlight(
                    "Rock Classics",
                    "ID: 37i9dQZF1DXcF1ynTFLUQH",
                    icon="🎸",
                )

            with col_right:
                st.markdown("### ⭐ Boa Compatibilidade (60-80%)")
                feature_highlight(
                    "Hoje em Destaque",
                    "ID: 37i9dQZF1DXcBWIGoYBM5M",
                    icon="🎤",
                )
                feature_highlight(
                    "Oitenta para Sempre",
                    "ID: 37i9dQZF1DX4UtSsGT1Sbe",
                    icon="📻",
                )

    # Processamento da análise (só executa se dataset está carregado e form foi submetido)
    if run and not dataset_is_loading and local_df is not None:
        if local_df.empty:
            custom_alert(
                "Erro ao Processar",
                "Dataset não foi carregado corretamente.",
                "error",
            )
            st.stop()

        try:
            # Análise da playlist
            with st.spinner("Analisando sua playlist... Isso pode levar alguns segundos"):
                pid = extract_playlist_id(pl_url)
                _tracks, _names, _artists = fetch_playlist_tracks(pid)
                total_playlist_tracks = len(_tracks)

                df_tracks = analyze_playlist_with_dataset(pl_url, local_df)

                # Validação: precisa de pelo menos n_clusters músicas encontradas
                matched_count = len(df_tracks)
                n_clusters_requested = int(k)

                if matched_count < n_clusters_requested:
                    max_clusters = max(1, matched_count)
                    raise ValueError(
                        f"Insuficientes músicas encontradas no dataset. "
                        f"Encontradas: {matched_count}, "
                        f"Clusters solicitados: {n_clusters_requested}. "
                        f"Máximo de clusters recomendado: {max_clusters}. "
                        "Tente com um valor menor de clusters ou uma "
                        "playlist com mais músicas."
                    )


                df_result, vibe_mean, scaled_features, cluster_labels = analyze_playlist_vibes(
                    df_tracks, n_clusters=n_clusters_requested
                )

            custom_alert(
                "✅ Análise Concluída com Sucesso!",
                f"Foram analisadas {len(df_result):,} faixas encontradas no dataset!",
                "success",
            )

            # Resumo da análise
            n_vibes_unique = df_result["vibe"].nunique()
            vibes_list = sorted(df_result["vibe"].unique())

            # Tamanhos e taxas
            matched = len(df_result)
            dataset_size = len(local_df)
            total_playlist_tracks = (
                total_playlist_tracks if "total_playlist_tracks" in locals() else matched
            )

            pct_by_playlist = (matched / max(1, total_playlist_tracks)) * 100
            pct_by_dataset = (matched / max(1, dataset_size)) * 100

            # Métricas em cards customizados
            section_divider("📊 Resumo da Análise")
            stats_row(
                [
                    {"label": "Clusters", "value": int(k), "icon": "🎭"},
                    {"label": "Vibes Únicas", "value": n_vibes_unique, "icon": "✨"},
                    {
                        "label": "Faixas Encontradas",
                        "value": f"{matched}/{total_playlist_tracks}",
                        "icon": "🎵",
                    },
                    {"label": "Compatibilidade", "value": f"{pct_by_playlist:.1f}%", "icon": "📈"},
                ]
            )

            # Barra de progresso visual
            progress_bar_custom(
                "Compatibilidade da sua playlist",
                pct_by_playlist,
                100.0,
                icon="📊",
            )

            # Explicação das taxas de match
            with st.expander("Entender as Taxas de Match", expanded=False):
                st.markdown("""
                **Duas taxas aparecem nos resultados:**

                1. **Compatibilidade (playlist)** — `faixas encontradas / total da playlist`
                   - Relevante para você: quantas musicas da sua playlist estao no dataset?
                   - Exemplo: 1.810 / 3.200 = **56.6%** (a maioria das suas musicas foi encontrada!)

                2. **Match relativo ao dataset** — `faixas encontradas / tamanho do dataset`
                   - Informativo: quantas do nosso dataset vieram dessa playlist?
                   - Exemplo: 1.810 / 169.907 = **1.065%** (uma pequena fracao do dataset)

                **Por que a primeira taxa é importante:**
                Se você submete uma playlist com 3.200 musicas e apenas 56.6% é encontrada,
                isso significa que ~1.400 faixas nao estao no dataset (musicas muito novas,
                obscuras, ou locais).

                **Por que a segunda taxa é pequena:**
                O dataset tem 169.907 musicas! Entao até com 1.810 matches, a porcentagem
                parece pequena (~1%). Isso é normal — é apenas contextual.

                **Use a primeira taxa para avaliar a cobertura da sua playlist.**
                """)

            # Mostra também a taxa relativa ao dataset inteiro (informativa)
            st.caption(
                f"Dataset local: {dataset_size:,} faixas | "
                f"Match relativo ao dataset: {pct_by_dataset:.3f}%"
            )

            # Info sobre as vibes
            with st.expander("💭 Sobre as Vibes Identificadas", expanded=False):
                st.write(f"**Vibes encontradas:** {', '.join(vibes_list)}")

                if n_vibes_unique < int(k):
                    st.info(
                        f"""
                        **🎯 Explicação:**

                        Você selecionou **{k} clusters**, mas foram identificadas
                        **{n_vibes_unique} vibes únicas**.

                        **Por quê?** O algoritmo KMeans descobriu {k} agrupamentos
                        naturais e distintos em sua playlist. Depois, cada cluster
                        foi mapeado para a vibe mais apropriada baseado em suas
                        características.

                        Alguns clusters compartilham características similares e
                        mapeiam para a **mesma vibe semântica**, o que é completamente
                        normal! Indica que sua playlist tem variações de um mesmo
                        estilo musical.

                        **Exemplo:**
                        - Cluster 1 e Cluster 4 → ambos "Party / Upbeat"
                          (mas com características ligeiramente diferentes)
                        - Cluster 2 e Cluster 5 → ambos "Dark / Intense"
                          (intensidades diferentes)

                        Isso é um **sinal de que o clustering está funcionando corretamente!** ✅
                        """
                    )
                else:
                    st.success(
                        f"Você selecionou {k} clusters e foram identificadas {n_vibes_unique} vibes únicas. "
                        "Cada cluster mapeou para uma vibe diferente! 🎉"
                    )  # Métricas principais
            metrics = vibe_metrics(df_result["vibe"].values)
            create_metrics_cards(metrics, len(df_result))

            # Tabela principal
            section_divider("Faixas e Vibes")
            st.dataframe(
                df_result[["track_name", "artists", "vibe", "cluster"]],
                width="stretch",
            )

            # Tabela resumo por vibe
            section_divider("Resumo por Vibe")
            show_vibe_summary_table(df_result)

            # Visualizações
            section_divider("Visualizacoes")

            # Gráfico 1: Projeção PCA (Scatter)
            chart_section_with_description(
                "Projeção PCA 2D",
                "🎨",
                "Cada ponto representa uma música reduzida a 2 dimensões principais usando PCA (Principal Component Analysis). "
                "Músicas próximas compartilham características similares. As cores indicam a Vibe atribuída.",
            )
            col_a, col_b = st.columns([1, 1])
            with col_a:
                plot_cluster_scatter(scaled_features, cluster_labels, df_result["vibe"].values)
            with col_b:
                st.markdown(
                    """
                <div style="
                    background: rgba(29, 185, 84, 0.05);
                    border-left: 3px solid #1DB954;
                    border-radius: 8px;
                    padding: 16px;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <div style="color: #1DB954; font-weight: 700; margin-bottom: 12px; font-size: 14px;">
                        📌 O que significa?
                    </div>
                    <ul style="
                        color: rgba(255, 255, 255, 0.8);
                        font-size: 13px;
                        margin: 0;
                        padding-left: 20px;
                        line-height: 1.8;
                    ">
                        <li><strong>Clusters</strong>: Agrupamentos de músicas com características similares</li>
                        <li><strong>Cores</strong>: Cada Vibe recebe uma cor diferente</li>
                        <li><strong>Proximidade</strong>: Pontos próximos = músicas similares</li>
                        <li><strong>Dispersão</strong>: Maior dispersão = maior variedade na playlist</li>
                    </ul>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Gráfico 2: Distribuição de Vibes
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            chart_section_with_description(
                "Distribuição de Faixas por Vibe",
                "📈",
                "Mostra quantas músicas foram atribuídas a cada Vibe. Vibes com mais barras indicam que sua playlist tem muitas músicas com essas características.",
            )
            col_c, col_d = st.columns([1, 1])
            with col_c:
                plot_vibe_bars(df_result["vibe"].values)
            with col_d:
                st.markdown(
                    """
                <div style="
                    background: rgba(29, 185, 84, 0.05);
                    border-left: 3px solid #1DB954;
                    border-radius: 8px;
                    padding: 16px;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <div style="color: #1DB954; font-weight: 700; margin-bottom: 12px; font-size: 14px;">
                        📌 Interpretação
                    </div>
                    <ul style="
                        color: rgba(255, 255, 255, 0.8);
                        font-size: 13px;
                        margin: 0;
                        padding-left: 20px;
                        line-height: 1.8;
                    ">
                        <li><strong>Barras altas</strong>: Vibes dominantes na sua playlist</li>
                        <li><strong>Distribuição balanceada</strong>: Playlist diversa e eclética</li>
                        <li><strong>Uma vibe dominante</strong>: Playlist temática e focada</li>
                    </ul>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Gráfico 3: Radar Profile
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            chart_section_with_description(
                "Perfil de Características por Vibe",
                "🎯",
                "Gráfico radar mostrando o perfil médio de cada Vibe. Cada eixo representa uma feature de áudio "
                "(Energy, Danceability, Valence, etc). Perfis maiores indicam características mais fortes naquela Vibe.",
            )
            plot_radar_by_vibe(df_result)
            st.info(
                """
                **💡 Como ler o Radar:**
                - Cada linha = uma Vibe diferente
                - Cada eixo = uma característica de áudio (1 a 9)
                - Extensão da linha = força dessa característica na vibe
                - Exemplo: "Party/Upbeat" com energia alta vai ter linha expandida no eixo "energy"
                """
            )

            # Top tracks por vibe
            tops = top_tracks_by_cluster(
                df_result,
                scaled_features,
                cluster_labels,
                k=5,
            )
            section_divider("Top Faixas por Vibe")
            display_top_tracks_tables(tops)

            # Médias gerais das features
            section_divider("Vibe Media da Playlist")
            show_vibe_averages(vibe_mean)

        except RuntimeError as e:
            # Erros originados de chamadas à API (ex: 404 playlist not found)
            title, body = _format_playlist_error(e)
            custom_alert(title, body, "error")
        except Exception:
            # Fallback genérico — mostra mensagem amigável e expõe detalhes em um expander para debug
            import traceback

            custom_alert(
                "Erro Durante a Analise",
                (
                    "Ocorreu um erro inesperado durante a análise. Verifique a URL/ID da playlist, "
                    "se a playlist é pública e se as credenciais do Spotify estão configuradas corretamente."
                ),
                "error",
            )

            # Log no terminal (útil quando executando localmente)
            tb = traceback.format_exc()
            print("[DEBUG] Exception during playlist analysis:")
            print(tb)

            # Mostra detalhes técnicos em um expander para facilitar debug local
            with st.expander("🔧 Detalhes técnicos (apenas para debugging)", expanded=False):
                st.text(tb)


def show_dataset_explorer_section(local_df):
    """Exibe seção de exploração do dataset (última seção)."""
    if local_df is None or local_df.empty:
        return

    # Verifica se dataset está carregado
    dataset_is_loading = not st.session_state.dataset_loaded

    section_divider("🔍 Explorar o Dataset")

    if dataset_is_loading:
        st.warning("⏳ Dataset ainda está carregando... Aguarde um momento.")
        return

    custom_alert(
        "Dataset Carregado",
        f"Disponíveis {len(local_df):,} faixas para exploração",
        "success",
    )

    search_result = dataset_search_card()

    # Resolve coluna de título (compatibilidade com diferentes arquivos)
    try:
        track_col = _resolve_track_col(local_df)
    except ValueError as ve:
        custom_alert("Erro no Dataset", str(ve), "error")
        return

    # Processa a busca quando o botão é clicado
    if search_result["execute"] and search_result["query"].strip():
        query = search_result["query"].lower().strip()

        # Busca unificada: música E artista
        # Encontra todas as faixas que contêm o termo na música OU no artista
        matches_by_track = local_df[
            local_df[track_col].astype(str).str.lower().str.contains(query, na=False)
        ]

        matches_by_artist = local_df[
            local_df["artists"].astype(str).str.lower().str.contains(query, na=False)
        ]

        # Combina os resultados (remove duplicatas)
        matches = pd.concat(
            [matches_by_track, matches_by_artist], ignore_index=False
        ).drop_duplicates()

        # Exibe resultados
        if not matches.empty:
            st.success(f"✅ Encontradas {len(matches):,} músicas!")

            # Colunas para exibição (com mais atributos)
            display_cols = [track_col, "artists", *FEATURE_COLS]
            available_cols = [c for c in display_cols if c in matches.columns]

            # Renomeia colunas para exibição mais amigável
            display_df = matches[available_cols].copy()
            display_df.columns = [
                c.replace("_", " ").title() if c != track_col else "🎵 Música"
                for c in display_df.columns
            ]

            # Formata números com 2 casas decimais
            for col in display_df.columns:
                if col not in ["🎵 Música", "Artists"]:
                    with contextlib.suppress(TypeError, AttributeError):
                        display_df[col] = display_df[col].round(2)

            st.dataframe(
                display_df.head(50),
                use_container_width=True,
                height=400,
            )

            # Opção de download
            csv = matches[available_cols].to_csv(index=False)
            st.download_button(
                label="📥 Baixar Resultados (CSV)",
                data=csv,
                file_name=f"spotify_search_{query[:20]}.csv",
                mime="text/csv",
            )

            # Estatísticas dos resultados
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            st.subheader("📊 Estatísticas dos Resultados")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total de Faixas", f"{len(matches):,}")
            with col2:
                unique_artists = matches["artists"].nunique()
                st.metric("Artistas Únicos", f"{unique_artists:,}")
            with col3:
                unique_tracks = matches[track_col].nunique()
                st.metric("Músicas Únicas", f"{unique_tracks:,}")
            with col4:
                st.metric("Compatibilidade", f"{(len(matches) / len(local_df) * 100):.2f}%")

            # Médias dos atributos
            st.markdown("### Médias dos Atributos")
            stats_cols = [c for c in FEATURE_COLS if c in matches.columns]

            if stats_cols:
                stats_data = {}
                for col in stats_cols:
                    try:
                        mean_val = matches[col].astype(float).mean()
                        stats_data[col.replace("_", " ").title()] = f"{mean_val:.2f}"
                    except (TypeError, ValueError):
                        pass

                # Exibe em colunas
                stats_cols_display = st.columns(len(stats_data))
                for idx, (stat_name, stat_val) in enumerate(stats_data.items()):
                    with stats_cols_display[idx]:
                        st.metric(stat_name, stat_val)
        else:
            st.info(f"❌ Nenhuma música ou artista encontrado para '{query}'")
    else:
        # Mostra estatísticas do dataset enquanto não há busca
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.info("💡 Digite um termo de busca acima e clique em 🔍 Buscar para explorar o dataset!")

        # Estatísticas gerais do dataset
        st.markdown("### 📊 Estatísticas Gerais do Dataset")

        # Primeira linha: Números gerais
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🎵 Total de Faixas", f"{len(local_df):,}")

        with col2:
            unique_artists = local_df["artists"].nunique()
            st.metric("👥 Artistas Únicos", f"{unique_artists:,}")

        with col3:
            unique_tracks = local_df[track_col].nunique()
            st.metric("🎶 Músicas Únicas", f"{unique_tracks:,}")

        with col4:
            try:
                avg_duration = local_df["duration_ms"].mean() / 60000
                st.metric("⏱️ Duração Média", f"{avg_duration:.2f}m")
            except (KeyError, TypeError):
                st.metric("⏱️ Duração Média", "N/A")

        # Segunda linha: Atributos de áudio
        st.markdown("### 🎼 Médias de Atributos de Áudio")

        # Cria colunas para os atributos
        stats_cols = [c for c in FEATURE_COLS if c in local_df.columns]

        if stats_cols:
            # Divide em 3 linhas se houver muitos atributos
            cols_per_row = 4
            num_rows = (len(stats_cols) + cols_per_row - 1) // cols_per_row

            for row in range(num_rows):
                cols = st.columns(cols_per_row)
                for col_idx in range(cols_per_row):
                    stat_idx = row * cols_per_row + col_idx
                    if stat_idx < len(stats_cols):
                        stat_col = stats_cols[stat_idx]
                        try:
                            mean_val = local_df[stat_col].astype(float).mean()
                            stat_name = stat_col.replace("_", " ").title()
                            with cols[col_idx]:
                                st.metric(stat_name, f"{mean_val:.2f}")
                        except (TypeError, ValueError):
                            pass

        # Terceira seção: Distribuição de características (expandível)
        with st.expander("� Distribuição Detalhada dos Atributos", expanded=False):
            st.markdown("**Estatísticas completas por atributo:**")

            # Tabela com min, max, média, mediana
            stats_summary = []
            for col in stats_cols:
                try:
                    data = local_df[col].astype(float)
                    stats_summary.append(
                        {
                            "Atributo": col.replace("_", " ").title(),
                            "Mínimo": f"{data.min():.2f}",
                            "Máximo": f"{data.max():.2f}",
                            "Média": f"{data.mean():.2f}",
                            "Mediana": f"{data.median():.2f}",
                            "Desvio Padrão": f"{data.std():.2f}",
                        }
                    )
                except (TypeError, ValueError):
                    pass

            if stats_summary:
                stats_df = pd.DataFrame(stats_summary)
                st.dataframe(stats_df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()

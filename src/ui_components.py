"""Componentes UI reutilizáveis para Streamlit com design Spotify."""

from collections.abc import Sequence
from contextlib import contextmanager

import streamlit as st


@contextmanager
def section_card(card_type: str = "analysis"):
    """Context manager para renderizar cards de seção.

    Args:
        card_type: Tipo de card ('analysis' ou 'dataset')
    """
    class_name = f"section-card-wrapper section-card-{card_type}"
    wrapper = st.container()
    wrapper.markdown(f"<div class='{class_name}'>", unsafe_allow_html=True)

    with wrapper.container():
        yield

    wrapper.markdown("</div>", unsafe_allow_html=True)


def section_divider(title: str) -> None:
    """Renderiza divisor de seção com título destacado."""
    st.markdown(
        f"""
        <div style="margin: 40px 0 24px 0;">
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 16px;">
                <div style="
                    width: 4px;
                    height: 32px;
                    background: linear-gradient(180deg, #1DB954 0%, #1aa34a 100%);
                    border-radius: 2px;
                "></div>
                <h2 style="
                    margin: 0;
                    color: white;
                    font-size: 24px;
                    font-weight: 700;
                    letter-spacing: -0.5px;
                ">
                    {title}
                </h2>
            </div>
            <div style="
                height: 1px;
                background: linear-gradient(90deg, rgba(29, 185, 84, 0.3) 0%, transparent 100%);
                margin-bottom: 16px;
            "></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def spotify_hero_header() -> None:
    """Renderiza cabeçalho principal com visual premium."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1DB954 0%, #1aa34a 50%, #0F1419 100%); padding: 48px 32px; border-radius: 16px; margin-bottom: 40px; box-shadow: 0 20px 60px rgba(29, 185, 84, 0.2); position: relative; overflow: hidden;">
            <div style="position: absolute; top: -50%; right: -10%; width: 500px; height: 500px; background: radial-gradient(circle, rgba(29, 185, 84, 0.15) 0%, transparent 70%); border-radius: 50%; pointer-events: none;"></div>
            <div style="position: relative; z-index: 10;">
                <div style="display: flex; align-items: center; gap: 24px; margin-bottom: 32px;">
                    <div style="width: 64px; height: 64px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 900; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3); flex-shrink: 0;">
                        🎵
                    </div>
                    <div>
                        <h1 style="margin: 0; color: white; font-size: 48px; font-weight: 900; letter-spacing: -1px; text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); line-height: 1.1;">
                            Spotify Vibes - Classificação
                        </h1>
                        <p style="margin: 8px 0 0 0; color: rgba(255, 255, 255, 0.95); font-size: 18px; font-weight: 600; letter-spacing: 0.5px;">
                            Analise as vibes da sua música com IA
                        </p>
                    </div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 28px; backdrop-filter: blur(10px);">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 28px;">
                        <div>
                            <div style="color: #FFFFFF; font-weight: 700; font-size: 16px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">
                                🎭 O que são Vibes?
                            </div>
                            <p style="margin: 0; color: rgba(255, 255, 255, 0.85); font-size: 14px; line-height: 1.6;">
                                Categorias semânticas que representam a atmosfera emocional de suas músicas. Usando 9 atributos de áudio (energia, danceabilidade, valence e mais), classificamos sua playlist em categorias significativas.
                            </p>
                        </div>
                        <div>
                            <div style="color: #FFFFFF; font-weight: 700; font-size: 16px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">
                                ⚙️ Como Funciona?
                            </div>
                            <p style="margin: 0; color: rgba(255, 255, 255, 0.85); font-size: 14px; line-height: 1.6;">
                                Modelo de IA (Random Forest) treinado com 955 mil músicas classifica automaticamente cada faixa. O sistema extrai features de áudio e prediz a vibe mais adequada com 85% de acurácia.
                            </p>
                        </div>
                        <div>
                            <div style="color: #FFFFFF; font-weight: 700; font-size: 16px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">
                                📊 O Dataset
                            </div>
                            <p style="margin: 0; color: rgba(255, 255, 255, 0.85); font-size: 14px; line-height: 1.6;">
                                Dataset Kaggle de 900k+ músicas com atributos pré-extraídos. Permite comparar sua playlist contra base massiva, identificando padrões musicais únicos.
                            </p>
                        </div>
                        <div>
                            <div style="color: #FFFFFF; font-weight: 700; font-size: 16px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">
                                ✨ O que Agrega?
                            </div>
                            <p style="margin: 0; color: rgba(255, 255, 255, 0.85); font-size: 14px; line-height: 1.6;">
                                Descubra padrões em suas preferências, entenda estilo da playlist, crie recomendações precisas, compartilhe insights únicos sobre vibes musicais.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dataset_search_card(disabled: bool = False) -> dict:
    """Renderiza card de busca no dataset com formulário integrado."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #1A1F26 0%, #141820 100%);
            border: 1px solid rgba(29, 185, 84, 0.2);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
        ">
            <div style="
                color: #1DB954;
                font-weight: 700;
                font-size: 18px;
                margin-bottom: 16px;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">
                🎵 Explorar Dataset
            </div>
            <p style="
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                margin-bottom: 16px;
            ">
                Procure por qualquer música, artista ou característica no dataset de 900k+ faixas
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("dataset_search_form", clear_on_submit=False):
        col1, col2 = st.columns([5, 1], gap="small")

        with col1:
            search_query = st.text_input(
                "Buscar",
                placeholder="Digite o nome de uma música, artista ou qualquer termo...",
                key="dataset_search_input",
                disabled=disabled,
            )

        with col2:
            st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
            do_search = st.form_submit_button(
                "🔍 Buscar",
                use_container_width=True,
                disabled=disabled,
                type="primary",
            )

    return {"query": search_query, "execute": do_search}


def stats_row(stats: Sequence[dict]) -> None:
    """Renderiza linha de estatísticas em cards."""
    if not stats:
        return

    cols = st.columns(len(stats))
    for col, stat in zip(cols, stats, strict=False):
        with col:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #1A1F26 0%, #141820 100%);
                    border: 1px solid rgba(29, 185, 84, 0.15);
                    border-radius: 12px;
                    padding: 16px;
                    text-align: center;
                ">
                    <div style="font-size: 32px; margin-bottom: 8px;">{stat.get("icon", "")}</div>
                    <div style="
                        color: rgba(255, 255, 255, 0.6);
                        font-size: 12px;
                        font-weight: 600;
                        text-transform: uppercase;
                        margin-bottom: 8px;
                    ">{stat.get("label", "")}</div>
                    <div style="
                        color: #1DB954;
                        font-size: 24px;
                        font-weight: 800;
                    ">{stat.get("value", "-")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def chart_section_with_description(title: str, icon: str = "📊", description: str = "") -> None:
    """Renderiza cabeçalho com descrição para gráficos."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(29, 185, 84, 0.1) 0%, rgba(29, 185, 84, 0.05) 100%);
            border-left: 4px solid #1DB954;
            border-radius: 8px;
            padding: 16px;
            margin: 20px 0 16px 0;
        ">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="font-size: 28px;">{icon}</span>
                <h3 style="margin: 0; color: #1DB954; font-size: 18px; font-weight: 700;
                letter-spacing: -0.5px;">
                    {title}
                </h3>
            </div>
            <div style="color: rgba(255, 255, 255, 0.7); font-size: 13px; line-height: 1.6;
            padding-left: 40px;">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_separator() -> None:
    """Renderiza separador visual entre seções."""
    st.markdown(
        """
        <div style="margin-top: 40px; padding: 20px 0;">
            <div style="
                height: 2px;
                background: linear-gradient(90deg,
                    transparent 0%,
                    rgba(29, 185, 84, 0.3) 20%,
                    rgba(29, 185, 84, 0.6) 50%,
                    rgba(29, 185, 84, 0.3) 80%,
                    transparent 100%);
            "></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def alert_card(title: str, message: str, alert_type: str = "info") -> None:
    """Renderiza card de alerta/informação."""
    colors = {
        "info": "#1DB954",
        "warning": "#FFA500",
        "error": "#FF6B6B",
    }
    color = colors.get(alert_type, "#1DB954")

    st.markdown(
        f"""
        <div style="
            background-color: rgba(29, 185, 84, 0.1);
            border-left: 4px solid {color};
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
        ">
            <div style="font-weight: 600; font-size: 16px; color: {color}; margin-bottom: 8px;">
                {title}
            </div>
            <div style="font-size: 14px; color: #E0E0E0; line-height: 1.6;">
                {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def custom_alert(title: str, message: str, alert_type: str = "info") -> None:
    """Renderiza alerta customizado."""
    alert_card(title, message, alert_type)


def info_section(text: str, icon: str = "i") -> None:
    """Renderiza seção de informação."""
    st.markdown(
        f"""
        <div style="
            background: rgba(29, 185, 84, 0.05);
            border-left: 3px solid #1DB954;
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
        ">
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 14px; margin: 0;
            line-height: 1.6;">
                <span style="font-size: 18px; margin-right: 8px;">{icon}</span>
                {text}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_highlight(title: str, subtitle: str, icon: str = "✨") -> None:
    """Renderiza destaque de feature."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1A1F26 0%, #141820 100%);
            border: 1px solid rgba(29, 185, 84, 0.2);
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
        ">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="font-size: 28px;">{icon}</div>
                <div>
                    <div style="color: #1DB954; font-weight: 600; font-size: 14px;">{title}</div>
                    <div style="color: rgba(255, 255, 255, 0.6); font-size: 12px;">{subtitle}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def progress_bar_custom(label: str, value: float, max_value: float = 100, icon: str = "📊") -> None:
    """Renderiza barra de progresso customizada."""
    percentage = (value / max(1, max_value)) * 100
    color = "#1DB954" if percentage >= 60 else "#FFA500" if percentage >= 30 else "#FF6B6B"

    st.markdown(
        f"""
        <div style="margin: 20px 0;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 18px;">{icon}</span>
                <span style="color: rgba(255, 255, 255, 0.8); font-weight: 600; font-size: 14px;">
                    {label}
                </span>
                <span style="color: {color}; font-weight: 700; font-size: 14px; margin-left: auto;">
                    {percentage:.1f}%
                </span>
            </div>
            <div style="
                width: 100%;
                height: 24px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                overflow: hidden;
                border: 1px solid rgba(29, 185, 84, 0.2);
            ">
                <div style="
                    width: {min(percentage, 100)}%;
                    height: 100%;
                    background: linear-gradient(90deg, {color} 0%, {color}cc 100%);
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_vibe_averages(vibe_mean: dict) -> None:
    """Exibe as médias das audio features de forma visual."""
    if not vibe_mean:
        return

    st.markdown(
        """
        <div style="margin: 20px 0;">
            <p style="color: rgba(255, 255, 255, 0.7); font-size: 13px; margin-bottom: 16px;">
                Perfil médio de todas as características de áudio da sua playlist:
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols_per_row = 3
    features = list(vibe_mean.items())
    num_rows = (len(features) + cols_per_row - 1) // cols_per_row

    for row in range(num_rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            feat_idx = row * cols_per_row + col_idx
            if feat_idx < len(features):
                feat_name, feat_value = features[feat_idx]
                with cols[col_idx]:
                    feat_display = feat_name.replace("_", " ").title()
                    try:
                        val = float(feat_value)
                        val_pct = (val / 1.0) * 100 if val <= 1.0 else val
                        color = (
                            "#1DB954"
                            if val_pct >= 60
                            else "#FFA500"
                            if val_pct >= 40
                            else "#FF6B6B"
                        )
                    except (TypeError, ValueError):
                        val = feat_value
                        val_pct = 0
                        color = "#1DB954"

                    st.markdown(
                        f"""
                        <div style="
                            background: linear-gradient(135deg, #1A1F26 0%, #141820 100%);
                            border: 1px solid rgba(29, 185, 84, 0.15);
                            border-radius: 12px;
                            padding: 16px;
                            text-align: center;
                        ">
                            <div style="
                                color: rgba(255, 255, 255, 0.6);
                                font-size: 11px;
                                font-weight: 600;
                                text-transform: uppercase;
                                margin-bottom: 8px;
                                letter-spacing: 0.5px;
                            ">{feat_display}</div>
                            <div style="
                                color: {color};
                                font-size: 28px;
                                font-weight: 800;
                                margin-bottom: 8px;
                            ">{val:.2f}</div>
                            <div style="
                                width: 100%;
                                height: 4px;
                                background: rgba(255, 255, 255, 0.1);
                                border-radius: 2px;
                                overflow: hidden;
                            ">
                                <div style="
                                    width: {min(val_pct, 100)}%;
                                    height: 100%;
                                    background: linear-gradient(90deg, {color} 0%, {color}cc 100%);
                                "></div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


def playlist_suggestion_card(
    name: str,
    playlist_id: str,
    spotify_url: str,
    track_count: int,
    icon: str = "🎵",
) -> None:
    """Renderiza card de playlist sugerida com botões.

    Args:
        name: Nome da playlist
        playlist_id: ID da playlist no Spotify
        spotify_url: URL para abrir no Spotify
        track_count: Quantidade de músicas
        icon: Emoji para o card
    """
    import streamlit as st

    col1, col2, col3 = st.columns([2, 1.2, 1.2])

    with col1:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #1A1F26 0%, #141820 100%);
                border-left: 3px solid #1DB954;
                border-radius: 8px;
                padding: 12px;
                margin: 8px 0;
                height: 70px;
                display: flex;
                align-items: center;
            ">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-size: 28px;">{icon}</div>
                    <div>
                        <div style="color: white; font-weight: 600; font-size: 14px;">{name}</div>
                        <div style="color: rgba(255, 255, 255, 0.6); font-size: 12px;">
                        {track_count} músicas
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        if st.button(
            "🎵 Abrir",
            key=f"open_{playlist_id}",
            use_container_width=True,
            help="Abrir no Spotify"
        ):
            st.markdown(
                f"[Abrir no Spotify]({spotify_url})", unsafe_allow_html=True
            )

    with col3:
        if st.button(
            "📋 ID",
            key=f"copy_{playlist_id}",
            use_container_width=True,
            help="Copiar ID",
        ):
            st.write(f"`{playlist_id}`")


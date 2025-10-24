"""Componentes reutilizáveis para UI/UX melhorada com design Spotify premium."""

from typing import Any

import streamlit as st


def custom_alert(title: str, message: str, alert_type: str = "info") -> None:
    """Renderiza alertas customizados e bonitos.

    Args:
        title: Título do alerta
        message: Mensagem do alerta
        alert_type: Tipo de alerta ('info', 'success', 'warning', 'error')
    """
    icons = {
        "info": "[i]",
        "success": "[✓]",
        "warning": "[!]",
        "error": "[x]",
    }

    colors = {
        "info": "#1DB954",  # Verde Spotify
        "success": "#1DB954",  # Verde
        "warning": "#FFA500",  # Laranja
        "error": "#FF6B6B",  # Vermelho
    }

    icon = icons.get(alert_type, "[i]")
    color = colors.get(alert_type, "#1DB954")

    st.markdown(
        f"""
        <div style="
            background-color: rgba(29, 185, 84, 0.1);
            border-left: 4px solid {color};
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
            backdrop-filter: blur(10px);
        ">
            <div style="font-weight: 600; font-size: 16px; margin-bottom: 8px; color: {color};">
                {icon} {title}
            </div>
            <div style="font-size: 14px; color: #E0E0E0; line-height: 1.6;">
                {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def spotify_header() -> None:
    """Renderiza header customizado com logo Spotify."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #1DB954 0%, #1aa34a 100%);
            padding: 32px 24px;
            border-radius: 12px;
            margin-bottom: 32px;
            box-shadow: 0 8px 32px rgba(29, 185, 84, 0.15);
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 16px;
            ">
                <div style="
                    font-size: 48px;
                    font-weight: bold;
                    color: white;
                ">
                    🎵
                </div>
                <div>
                    <h1 style="
                        margin: 0;
                        color: white;
                        font-size: 32px;
                        font-weight: 800;
                        letter-spacing: -0.5px;
                    ">
                        Spotify Playlist Analyzer
                    </h1>
                    <p style="
                        margin: 8px 0 0 0;
                        color: rgba(255, 255, 255, 0.9);
                        font-size: 14px;
                        font-weight: 500;
                    ">
                        Descubra as vibes da sua playlist com Machine Learning
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: Any, description: str = "", icon: str = "📊") -> None:
    """Renderiza card de métrica customizado.

    Args:
        label: Rótulo da métrica
        value: Valor a exibir
        description: Descrição opcional
        icon: Emoji para o card
    """
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1A1F26 0%, #141820 100%);
            border: 1px solid rgba(29, 185, 84, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 12px;
            ">
                <div style="font-size: 28px;">{icon}</div>
                <div style="
                    color: rgba(255, 255, 255, 0.7);
                    font-size: 12px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                ">
                    {label}
                </div>
            </div>
            <div style="
                font-size: 28px;
                font-weight: 800;
                color: #1DB954;
                margin-bottom: 8px;
                letter-spacing: -0.5px;
            ">
                {value}
            </div>
            {f'<div style="font-size: 12px; color: rgba(255, 255, 255, 0.5);">{description}</div>' if description else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_divider(title: str) -> None:
    """Renderiza divisor de seção customizado.

    Args:
        title: Título da seção
    """
    st.markdown(
        f"""
        <div style="
            margin: 40px 0 24px 0;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 16px;
                margin-bottom: 16px;
            ">
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


def feature_highlight(title: str, description: str, icon: str = "✨") -> None:
    """Renderiza destaque de feature.

    Args:
        title: Título da feature
        description: Descrição
        icon: Emoji da feature
    """
    st.markdown(
        f"""
        <div style="
            background: rgba(29, 185, 84, 0.05);
            border: 1px solid rgba(29, 185, 84, 0.15);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            transition: all 0.2s ease;
        ">
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 12px;
            ">
                <div style="font-size: 24px; flex-shrink: 0;">{icon}</div>
                <div>
                    <div style="
                        color: #1DB954;
                        font-weight: 600;
                        font-size: 14px;
                        margin-bottom: 4px;
                    ">
                        {title}
                    </div>
                    <div style="
                        color: rgba(255, 255, 255, 0.7);
                        font-size: 13px;
                        line-height: 1.5;
                    ">
                        {description}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def progress_bar_custom(label: str, value: float, total: float = 100.0, icon: str = "📊") -> None:
    """Renderiza barra de progresso customizada.

    Args:
        label: Rótulo
        value: Valor atual
        total: Valor total
        icon: Emoji
    """
    percentage = (value / max(1, total)) * 100
    st.markdown(
        f"""
        <div style="margin-bottom: 24px;">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    color: rgba(255, 255, 255, 0.8);
                    font-weight: 600;
                    font-size: 14px;
                ">
                    <span>{icon}</span>
                    <span>{label}</span>
                </div>
                <div style="
                    color: #1DB954;
                    font-weight: 700;
                    font-size: 14px;
                ">
                    {percentage:.1f}%
                </div>
            </div>
            <div style="
                background: #1A1F26;
                border-radius: 8px;
                height: 8px;
                overflow: hidden;
                border: 1px solid rgba(29, 185, 84, 0.2);
            ">
                <div style="
                    background: linear-gradient(90deg, #1DB954 0%, #1aa34a 100%);
                    height: 100%;
                    width: {percentage}%;
                    transition: width 0.3s ease;
                    box-shadow: 0 0 10px rgba(29, 185, 84, 0.5);
                "></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def spotify_hero_header() -> None:
    """Renderiza header hero premium com logo, título e grid de explicações (4 colunas)."""
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
                            Spotify Vibes
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
                                Clusters semânticos que representam a atmosfera emocional de suas músicas. Usando 9 atributos de áudio (energia, danceabilidade, valence e mais), agrupamos sua playlist em categorias como Party, Chill, Romantic, Dark e outras vibrações únicas.
                            </p>
                        </div>
                        <div>
                            <div style="color: #FFFFFF; font-weight: 700; font-size: 16px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">
                                ⚙️ Como Funciona?
                            </div>
                            <p style="margin: 0; color: rgba(255, 255, 255, 0.85); font-size: 14px; line-height: 1.6;">
                                Nosso modelo de Machine Learning (K-means) analisa cada música, extraindo features de áudio via Spotify. Os dados são normalizados e agrupados em clusters dinâmicos (3-8), cada um mapeando para uma vibe semântica.
                            </p>
                        </div>
                        <div>
                            <div style="color: #FFFFFF; font-weight: 700; font-size: 16px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">
                                📊 O Dataset
                            </div>
                            <p style="margin: 0; color: rgba(255, 255, 255, 0.85); font-size: 14px; line-height: 1.6;">
                                Utilizamos um dataset Kaggle de 900k+ músicas com atributos pré-extraídos. Isso permite comparar sua playlist contra uma base massiva, calculando compatibilidade e identificando padrões musicais únicos.
                            </p>
                        </div>
                        <div>
                            <div style="color: #FFFFFF; font-weight: 700; font-size: 16px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">
                                ✨ O que Agrega?
                            </div>
                            <p style="margin: 0; color: rgba(255, 255, 255, 0.85); font-size: 14px; line-height: 1.6;">
                                Descubra padrões invisíveis em suas preferências, entenda melhor o estilo da sua playlist, crie recomendações mais precisas, e compartilhe insights únicos sobre suas vibes musicais com amigos e comunidade.
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
    """Renderiza card de busca inteligente no dataset (busca unificada).

    Args:
        disabled: Se True, desabilita os inputs (dataset ainda carregando)

    Returns:
        Dicionário com resultado da busca (sem tipo de busca)
    """
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
        # Cria colunas sem gap para melhor controle
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

    return {
        "query": search_query,
        "execute": do_search
    }


def vibe_info_card(vibe_name: str, description: str, color: str = "#1DB954", icon: str = "[*]") -> None:
    """Renderiza card informativo sobre uma vibe.

    Args:
        vibe_name: Nome da vibe
        description: Descrição
        color: Cor da vibe
        icon: Ícone/emoji
    """
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(29, 185, 84, 0.1) 0%, rgba(29, 185, 84, 0.05) 100%);
            border-left: 4px solid {color};
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        ">
            <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="
                    font-size: 28px;
                    min-width: 40px;
                    text-align: center;
                ">{icon}</div>
                <div>
                    <div style="
                        color: {color};
                        font-weight: 700;
                        font-size: 16px;
                        margin-bottom: 4px;
                    ">{vibe_name}</div>
                    <div style="
                        color: rgba(255, 255, 255, 0.8);
                        font-size: 14px;
                        line-height: 1.5;
                    ">{description}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stats_row(stats: list) -> None:
    """Renderiza uma linha de estatísticas com cards lado-a-lado.

    Args:
        stats: Lista de dicts com 'label', 'value', 'icon'
    """
    cols = st.columns(len(stats))
    for col, stat in zip(cols, stats, strict=True):
        with col:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #1A1F26 0%, #141820 100%);
                    border: 1px solid rgba(29, 185, 84, 0.15);
                    border-radius: 12px;
                    padding: 16px;
                    text-align: center;
                    transition: all 0.3s ease;
                ">
                    <div style="font-size: 32px; margin-bottom: 8px;">{stat.get('icon', '[*]')}</div>
                    <div style="
                        color: rgba(255, 255, 255, 0.6);
                        font-size: 12px;
                        font-weight: 600;
                        text-transform: uppercase;
                        margin-bottom: 8px;
                    ">{stat.get('label', '')}</div>
                    <div style="
                        color: #1DB954;
                        font-size: 24px;
                        font-weight: 800;
                    ">{stat.get('value', '-')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def info_section(title: str, icon: str = "[i]") -> None:
    """Renderiza seção informativa expandível.

    Args:
        title: Título da seção
        icon: Ícone
    """
    st.markdown(
        f"""
        <div style="
            background: rgba(29, 185, 84, 0.05);
            border: 1px solid rgba(29, 185, 84, 0.15);
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
        ">
            <div style="
                color: #1DB954;
                font-weight: 700;
                font-size: 15px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">
                {icon} {title}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def input_field_styled(
    label: str, placeholder: str = "", input_type: str = "text", key: str | None = None
) -> str:
    """Campo de entrada customizado com estilo Spotify.

    Args:
        label: Rótulo do campo
        placeholder: Texto de placeholder
        input_type: Tipo do input (text, password)
        key: Chave única do Streamlit

    Returns:
        Valor digitado pelo usuário
    """
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <label style="
                color: rgba(255, 255, 255, 0.8);
                font-weight: 600;
                font-size: 14px;
                display: block;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">
                {label}
            </label>
        </div>
        """,
        unsafe_allow_html=True,
    )
    value = st.text_input(
        label, placeholder=placeholder, type=input_type, key=key, label_visibility="collapsed"
    )
    return value


def card_hover(title: str, content: str, icon: str = "📌") -> None:
    """Card com efeito hover premium.

    Args:
        title: Título do card
        content: Conteúdo
        icon: Emoji do card
    """
    html = f"""
    <div style="
        background: rgba(29, 185, 84, 0.08);
        border: 1px solid rgba(29, 185, 84, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.3s ease;
        cursor: pointer;
    "
    onmouseover="this.style.background='rgba(29, 185, 84, 0.12)'; this.style.borderColor='rgba(29, 185, 84, 0.4)'; this.style.boxShadow='0 8px 24px rgba(29, 185, 84, 0.15)';"
    onmouseout="this.style.background='rgba(29, 185, 84, 0.08)'; this.style.borderColor='rgba(29, 185, 84, 0.2)'; this.style.boxShadow='none';"
    >
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        ">
            <div style="font-size: 24px;">{icon}</div>
            <div style="
                color: #1DB954;
                font-weight: 700;
                font-size: 16px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">
                {title}
            </div>
        </div>
        <div style="
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
            line-height: 1.6;
            padding-left: 36px;
        ">
            {content}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def badge(text: str, style: str = "success") -> None:
    """Badge customizado.

    Args:
        text: Texto do badge
        style: Estilo (success, warning, info, danger)
    """
    colors = {
        "success": "#1DB954",
        "warning": "#FFA500",
        "info": "#00BCD4",
        "danger": "#FF6B6B",
    }
    bg_colors = {
        "success": "rgba(29, 185, 84, 0.15)",
        "warning": "rgba(255, 165, 0, 0.15)",
        "info": "rgba(0, 188, 212, 0.15)",
        "danger": "rgba(255, 107, 107, 0.15)",
    }

    color = colors.get(style, "#1DB954")
    bg_color = bg_colors.get(style, "rgba(29, 185, 84, 0.15)")

    html = f"""
    <span style="
        background: {bg_color};
        color: {color};
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: 1px solid {color};
        display: inline-block;
        margin: 4px 4px 4px 0;
    ">
        {text}
    </span>
    """
    st.markdown(html, unsafe_allow_html=True)


def divider_gradient(margin: str = "32px 0") -> None:
    """Divisor com gradiente Spotify.

    Args:
        margin: Margem do divisor
    """
    html = f"""
    <div style="
        height: 2px;
        background: linear-gradient(90deg, transparent, #1DB954, transparent);
        margin: {margin};
        border-radius: 1px;
    "></div>
    """
    st.markdown(html, unsafe_allow_html=True)


def stat_card_compact(label: str, value: str, unit: str = "", icon: str = "📊") -> None:
    """Card de stat compacto e minimalista.

    Args:
        label: Rótulo
        value: Valor
        unit: Unidade
        icon: Emoji
    """
    html = f"""
    <div style="
        background: rgba(29, 185, 84, 0.05);
        border-left: 3px solid #1DB954;
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <div style="
                    color: rgba(255, 255, 255, 0.6);
                    font-size: 12px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 4px;
                ">
                    {label}
                </div>
                <div style="
                    color: #1DB954;
                    font-size: 24px;
                    font-weight: 800;
                    letter-spacing: -0.5px;
                ">
                    {value}<span style="font-size: 14px; margin-left: 4px;">{unit}</span>
                </div>
            </div>
            <div style="font-size: 32px; opacity: 0.3;">{icon}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def chart_section_with_description(
    title: str,
    icon: str = "📊",
    description: str = "",
) -> None:
    """Renderiza um header de seção de gráfico com descrição expandível.

    Args:
        title: Título da seção
        icon: Emoji para o ícone
        description: Descrição longa do que o gráfico mostra
    """
    html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.1) 0%, rgba(29, 185, 84, 0.05) 100%);
        border-left: 4px solid #1DB954;
        border-radius: 8px;
        padding: 16px;
        margin: 20px 0 16px 0;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        ">
            <span style="font-size: 28px;">{icon}</span>
            <h3 style="
                margin: 0;
                color: #1DB954;
                font-size: 18px;
                font-weight: 700;
                letter-spacing: -0.5px;
            ">
                {title}
            </h3>
        </div>
        <div style="
            color: rgba(255, 255, 255, 0.7);
            font-size: 13px;
            line-height: 1.6;
            padding-left: 40px;
        ">
            {description}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def section_separator() -> None:
    """Renderiza um separador visual forte entre seções principais."""
    st.markdown(
        """
        <div style="
            margin-top: 40px;
            padding: 20px 0;
            position: relative;
        ">
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


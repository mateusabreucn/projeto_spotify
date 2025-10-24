"""Componente de sugestão de playlists para teste."""

import webbrowser
import streamlit as st


def render_playlist_suggestions() -> None:
    """Renderiza a seção de playlists sugeridas com layout 2 por linha."""
    playlists = [
        {
            "name": "Huge variety of music",
            "id": "31wHtANXfkX9JrhQwmMW9I",
            "url": "https://open.spotify.com/playlist/31wHtANXfkX9JrhQwmMW9I",
            "count": 520,
            "icon": "🎵",
        },
        {
            "name": "Rock Teste",
            "id": "4qVR8loVabg49B2UMDJ2Se",
            "url": "https://open.spotify.com/playlist/4qVR8loVabg49B2UMDJ2Se",
            "count": 101,
            "icon": "🎸",
        },
        {
            "name": "Acoustic Teste",
            "id": "30NlOslZ5qNJHDJLfABViH",
            "url": "https://open.spotify.com/playlist/30NlOslZ5qNJHDJLfABViH",
            "count": 199,
            "icon": "🎶",
        },
        {
            "name": "Instrumental Teste",
            "id": "2WACMz7hae0Qra9n9ZGfr5",
            "url": "https://open.spotify.com/playlist/2WACMz7hae0Qra9n9ZGfr5",
            "count": 680,
            "icon": "🎹",
        },
        {
            "name": "Top 500 Rock and Roll Songs",
            "id": "4YygUsUEglDPrYIUmrdNVT",
            "url": "https://open.spotify.com/playlist/4YygUsUEglDPrYIUmrdNVT",
            "count": 502,
            "icon": "🤘",
        },
        {
            "name": "All musics",
            "id": "0qhOhfr5Udc7c11bht1q3s",
            "url": "https://open.spotify.com/playlist/0qhOhfr5Udc7c11bht1q3s",
            "count": 3306,
            "icon": "🌟",
        },
        {
            "name": "The Best Songs of All Time",
            "id": "414t6povgf4zf7FDHfVgDA",
            "url": "https://open.spotify.com/playlist/414t6povgf4zf7FDHfVgDA",
            "count": 3845,
            "icon": "👑",
        },
        {
            "name": "Top 1000 músicas da história",
            "id": "74MRwiSERYoZhREnJGzkwo",
            "url": "https://open.spotify.com/playlist/74MRwiSERYoZhREnJGzkwo",
            "count": 634,
            "icon": "🏆",
        },
    ]

    # Renderizar 2 playlists por linha
    for i in range(0, len(playlists), 2):
        col1, col2 = st.columns(2)

        # Primeira playlist
        with col1:
            playlist = playlists[i]
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #1A1F26 0%, #141820 100%);
                    border-left: 4px solid #1DB954;
                    border-radius: 12px;
                    padding: 16px;
                    margin: 8px 0;
                    transition: all 0.3s ease;
                ">
                    <div style="display: flex; align-items: flex-start; gap: 12px;">
                        <div style="font-size: 32px; flex-shrink: 0;">
                        {playlist['icon']}</div>
                        <div style="flex: 1;">
                            <div style="color: white; font-weight: 600;
                            font-size: 15px;">{playlist['name']}</div>
                            <div style="color: rgba(255, 255, 255, 0.7);
                            font-size: 13px; margin-top: 4px;">
                            📊 {playlist['count']} músicas</div>
                            <div style="color: #1DB954; font-size: 12px;
                            margin-top: 4px; font-family: monospace;">
                            ID: {playlist['id']}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Botões abaixo com melhor espaçamento
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            btn_col1, btn_col2 = st.columns([1, 1], gap="medium")
            with btn_col1:
                if st.button(
                    "🎵 Abrir",
                    key=f"open_{playlist['id']}",
                    use_container_width=True,
                ):
                    webbrowser.open(playlist["url"], new=2)

            with btn_col2:
                if st.button(
                    "📋 Copiar",
                    key=f"copy_{playlist['id']}",
                    use_container_width=True,
                ):
                    st.code(playlist["id"], language="text")

            # Divisor entre playlists
            st.markdown(
                "<div style='height: 16px; border-bottom: 1px solid rgba(29, 185, 84, "
                "0.2); margin: 12px 0;'></div>",
                unsafe_allow_html=True,
            )

        # Segunda playlist (se existir)
        if i + 1 < len(playlists):
            with col2:
                playlist = playlists[i + 1]
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(135deg, #1A1F26 0%, #141820 100%);
                        border-left: 4px solid #1DB954;
                        border-radius: 12px;
                        padding: 16px;
                        margin: 8px 0;
                        transition: all 0.3s ease;
                    ">
                        <div style="display: flex; align-items: flex-start;
                        gap: 12px;">
                            <div style="font-size: 32px; flex-shrink: 0;">
                            {playlist['icon']}</div>
                            <div style="flex: 1;">
                                <div style="color: white; font-weight: 600;
                                font-size: 15px;">{playlist['name']}</div>
                                <div style="color: rgba(255, 255, 255, 0.7);
                                font-size: 13px; margin-top: 4px;">
                                📊 {playlist['count']} músicas</div>
                                <div style="color: #1DB954; font-size: 12px;
                                margin-top: 4px; font-family: monospace;">
                                ID: {playlist['id']}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Botões abaixo com melhor espaçamento
                st.markdown(
                    "<div style='height: 8px;'></div>", unsafe_allow_html=True
                )
                btn_col1, btn_col2 = st.columns(
                    [1, 1], gap="medium"
                )
                with btn_col1:
                    if st.button(
                        "🎵 Abrir",
                        key=f"open2_{playlist['id']}",
                        use_container_width=True,
                    ):
                        webbrowser.open(playlist["url"], new=2)

                with btn_col2:
                    if st.button(
                        "📋 Copiar",
                        key=f"copy2_{playlist['id']}",
                        use_container_width=True,
                    ):
                        st.code(playlist["id"], language="text")

                # Divisor entre playlists
                st.markdown(
                    "<div style='height: 16px; border-bottom: 1px solid rgba(29, 185, 84, "
                    "0.2); margin: 12px 0;'></div>",
                    unsafe_allow_html=True,
                )

    # Espaço e dica final
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="
            background: rgba(29, 185, 84, 0.1);
            border-left: 3px solid #1DB954;
            border-radius: 8px;
            padding: 12px;
            margin: 16px 0 24px 0;
        ">
            <div style="color: rgba(255, 255, 255, 0.9); font-size: 13px;">
            💡 <strong>Dica:</strong> Use "Abrir" para acessar a playlist no Spotify,
            ou "Copiar" para usar o ID!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


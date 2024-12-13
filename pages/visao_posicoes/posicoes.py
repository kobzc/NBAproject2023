import streamlit as st
from data.dataset import df_posicoes, column_mapping
from graphics import (
    generate_hist_player_position,
    generate_dist_pts_each_pos_bar,
    generate_dist_each_pos_box,
    generate_dist_pts_gp,
    generate_graph_mean_ast_ft_3p,
    generate_graph_3pm_pos,
    generate_graph_stl_blk_reb_pos,
    generate_graph_dist_stl_pos,
    generate_graph_defact_pos,
    generate_graph_mean_stl_blk_reb_pos,
    generate_graph_mean_blk_stl_reb_3D_pos,
)
from styles import (
    centralizar_texto,
    centralizar_titulo,
    rename_columns_for_presentation,
    break_line,
)


## ATAQUE

# 1. Quantos jogadores há em cada posição
histogram = generate_hist_player_position()

# 2. Distribuição de pontos em cada posição na temporada, em um gráfico de barras ou gráfico de caixa.
# 2.1 Gráfico em barras
graph_dist_each_pos_bar = generate_dist_pts_each_pos_bar()

# 2.1.2 Gáfico em caixa
graph_dist_each_pos_box = generate_dist_each_pos_box()

# 3. Distribuição de pontos por jogo em cada posição, em um gráfico de caixa.
graph_dist_pts_gp = generate_dist_pts_gp()

# 4. Como estão distribuídas as médias de bolas de 3, assistências e lances livres em cada posição? Em uma tabela e um gráfico de dispersão.
# 4.1 Tabela
tabl_mean_3p_ast_ft = df_posicoes[["POS", "3P%", "AST%", "FT%"]]

# 4.2 Gráfico de dispersão 3d
graph_mean_ast_ft_3p = generate_graph_mean_ast_ft_3p()

# 5. Distribuiçoes das bolas de 3 convertidas de acordo com as posições, em um gráfico de caixa
graph_3pm_pos = generate_graph_3pm_pos()

## DEFESA

# 1. Distribuição de bloqueios, roubos de bola e rebotes em cada posição, em uma tabela e um gráfico de dispersão.
tabl_blk_stl_reb = df_posicoes[["POS", "BLK", "STL", "REB"]]
tabl_blk_stl_reb = rename_columns_for_presentation(tabl_blk_stl_reb, column_mapping)
graph_blk_stl_reb = generate_graph_stl_blk_reb_pos()

# 2. Distribuição dos valores de roubos de bola por posição, em um grafico de caixa
graph_dist_stl_pos = generate_graph_dist_stl_pos()

# 3. Distribuição das ações defensivas por posição, em um gráfico de caixa
graph_defact_pos = generate_graph_defact_pos()

# 4. Distribuição das médias de bloqueios, roubos de bola e rebotes em cada posição, em um tabela e gráficos de dispersão e dispersão 3D.
tabl_mean_blk_stl_reb_pos = df_posicoes[["POS", "BLK%", "STL%", "REB%"]]
tabl_mean_blk_stl_reb_pos = rename_columns_for_presentation(
    tabl_mean_blk_stl_reb_pos, column_mapping
)
graph_mean_blk_stl_reb_pos = generate_graph_mean_stl_blk_reb_pos()
graph_mean_blk_stl_reb_3D_pos = generate_graph_mean_blk_stl_reb_3D_pos(600)


def show_page():
    # Página de posições
    st.sidebar.subheader("SUBMENU VISÃO POSIÇÕES")
    view_mode = st.sidebar.radio("Selecione a visão:", ("Ataque", "Defesa"))

    if view_mode == "Ataque":
        st.markdown(
            centralizar_titulo("VISÃO DE POSIÇÕES: ATAQUE"),  # Título centralizado
            unsafe_allow_html=True,
        )
        st.markdown(
            centralizar_texto("Estátisticas de ataque por posição na liga."),
            unsafe_allow_html=True,
        )
        break_line()

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("**QUANTIDADE DE JOGADORES POR POSIÇÃO:**")
            st.plotly_chart(histogram, use_container_width=True)
            st.subheader("**DISTRIBUIÇÃO DE PONTOS POR JOGO EM CADA POSIÇÃO:**")
            st.plotly_chart(graph_dist_pts_gp)

        with col2:
            st.subheader("**DISTRIBUIÇÃO DE PONTOS POR POSIÇÃO NA TEMPORADA:**")
            st.markdown(
                centralizar_texto("Gráfico de barras"),  # st.write centralizado
                unsafe_allow_html=True,
            )
            st.altair_chart(graph_dist_each_pos_bar, use_container_width=True)
            st.markdown(
                centralizar_texto("Gráfico de caixa"),  # st.write centralizado
                unsafe_allow_html=True,
            )
            st.plotly_chart(graph_dist_each_pos_box, use_container_width=True)

        col3, col4 = st.columns([1, 1])
        with col3:

            st.subheader(
                "**DISTRIBUIÇÃO DAS MÉDIAS DE BOLAS DE TRÊS, ASSISTÊNCIAS E LANCES LIVRES POR POSIÇÃO:**"
            )
            st.markdown(
                centralizar_texto("Tabela"),  # st.write centralizado
                unsafe_allow_html=True,
            )
            st.table(tabl_mean_3p_ast_ft)
            st.markdown(
                centralizar_texto("Gráfico de dispersão 3D"),  # st.write centralizado
                unsafe_allow_html=True,
            )
            st.plotly_chart(graph_mean_ast_ft_3p, use_container_width=True)

        with col4:
            st.subheader("**DISTRIBUIÇÃO DE BOLAS DE TRÊS CONVERTIDAS POR POSIÇÃO:**")
            st.plotly_chart(graph_3pm_pos, use_container_width=True)

    elif view_mode == "Defesa":
        st.markdown(
            centralizar_titulo("VISÃO DE POSIÇÕES: DEFESA"),  # Título centralizado
            unsafe_allow_html=True,
        )
        st.markdown(
            centralizar_texto("Estátisticas de defesa por posição na liga."),
            unsafe_allow_html=True,
        )
        break_line()

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader(
                "**DISTRIBUIÇÃO DE BLOQUEIOS, ROUBOS DE BOLA E REBOTES EM CADA POSIÇÃO:**"
            )
            st.markdown(
                centralizar_texto("Tabela"),  # st.write centralizado
                unsafe_allow_html=True,
            )
            st.table(tabl_blk_stl_reb)
            st.markdown(
                centralizar_texto("Gráfico de dispersão"),  # st.write centralizado
                unsafe_allow_html=True,
            )
            st.plotly_chart(graph_blk_stl_reb, use_container_width=True)
        with col2:
            st.subheader(
                "**DISTRIBUIÇÃO DAS MÉDIAS DE BLOQUEIOS, ROUBOS DE BOLA E REBOTES EM CADA POSIÇÃO**"
            )
            st.markdown(
                centralizar_texto("Tabela"),  # st.write centralizado
                unsafe_allow_html=True,
            )
            st.table(tabl_mean_blk_stl_reb_pos)
            st.markdown(
                centralizar_texto("Gráfico de dispersão"),  # st.write centralizado
                unsafe_allow_html=True,
            )
            st.plotly_chart(graph_mean_blk_stl_reb_pos, use_container_width=True)
        graphbox_col1, graphbox_col2 = st.columns([1, 1])
        with graphbox_col1:
            st.subheader("**DISTRIBUIÇÃO DOS VALORES DE ROUBOS DE BOLA POR POSIÇÃO:**")
            st.plotly_chart(graph_dist_stl_pos, use_container_width=True)
        with graphbox_col2:
            st.subheader("**DISTRIBUIÇÃO DE AÇÕES DEFENSIVAS POR POSIÇÃO:**")
            st.plotly_chart(graph_defact_pos, use_container_width=True)

        st.markdown(
            centralizar_texto("Gráfico de dispersão 3D"),  # st.write centralizado
            unsafe_allow_html=True,
        )
        st.plotly_chart(graph_mean_blk_stl_reb_3D_pos, use_container_width=True)

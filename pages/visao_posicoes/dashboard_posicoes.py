import streamlit as st

# Gráficos
from pages.visao_posicoes.posicoes import (
    histogram,
    graph_dist_each_pos_bar,
    tabl_mean_3p_ast_ft,
    graph_mean_ast_ft_3p,
    graph_blk_stl_reb,
)

from graphics import (
    generate_graf_pizza_3pm_pos,
    generate_graf_pizza_reb_pos,
    generate_graph_bars_defact_pos,
    generate_graph_bars_defact_tov_pos,
    generate_graph_bars_stl_pf_pos,
    generate_graf_pizza_dreb_pos,
    generate_graph_mean_blk_stl_reb_3D_pos,
)
from styles import centralizar_titulo, centralizar_texto


def show_dashboard():

    st.sidebar.subheader("Submenu Visão Posições")
    view_mode = st.sidebar.radio("Selecione a visão:", ("Ataque", "Defesa"))

    st.markdown(
        centralizar_titulo(f"DASHBOARD POSIÇÕES: {view_mode}"), unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.3, 2.4, 1])

    if view_mode == "Ataque":

        with col1:
            st.subheader(
                "**DISTRIBUIÇÃO DAS MÉDIAS DE BOLAS DE TRÊS, ASSISTÊNCIAS E LANCES LIVRES POR POSIÇÃO:**"
            )
            st.markdown(
                centralizar_texto("Tabela"),  # st.write centralizado
                unsafe_allow_html=True,
            )
            st.table(tabl_mean_3p_ast_ft)
            st.subheader("Gráfico de dispersão 3D")
            st.plotly_chart(graph_mean_ast_ft_3p, use_container_width=True)

        with col2:
            st.subheader("**QUANTIDADE DE PLAYERS POR POSIÇÃO:**")
            st.plotly_chart(histogram, use_container_width=True)
            st.subheader("**RANKING DE PONTOS POR POSIÇÃO:**")
            st.altair_chart(graph_dist_each_pos_bar, use_container_width=True)

        with col3:
            st.subheader("**TOP 3 CESTAS DE TRÊS POR POSIÇÃO:**")
            chart_pizza_ast_pos = generate_graf_pizza_3pm_pos()
            st.altair_chart(chart_pizza_ast_pos)
            st.subheader("**TOP 3 REBOTES POR POSIÇÃO:**")
            chart_pizza_reb_pos = generate_graf_pizza_reb_pos()
            st.altair_chart(chart_pizza_reb_pos)

    elif view_mode == "Defesa":

        with col1:
            st.subheader("**RANKING POR AÇÕES DEFENSIVAS:**")
            graph_bars_defact_pos = generate_graph_bars_defact_pos()
            st.altair_chart(graph_bars_defact_pos, use_container_width=True)
            st.subheader("**DISTRIBUIÇÃO DE STEALS E BLOQUEIOS POR POSIÇÃO:**")
            st.plotly_chart(graph_blk_stl_reb)

        with col2:
            st.subheader("**RELAÇÃO ENTRE AÇÕES DEFENSIVAS E TURNOVERS POR POSIÇÃO:**")
            graph_bars_defact_tov_pos = generate_graph_bars_defact_tov_pos()
            st.plotly_chart(graph_bars_defact_tov_pos, use_container_width=True)
            st.subheader(
                "**RELAÇÃO ENTRE O TOTAL DE ROUBOS DE BOLA E FALTAS PESSOAIS POR POSIÇÃO:**"
            )
            graph_bars_stl_pf_pos = generate_graph_bars_stl_pf_pos()
            st.altair_chart(graph_bars_stl_pf_pos, use_container_width=True)

        with col3:
            st.subheader("**TOP 3 POSIÇÕES COM MAIS REBOTES DEFENSIVOS:**")
            graf_pizza_dreb_pos = generate_graf_pizza_dreb_pos()
            st.altair_chart(graf_pizza_dreb_pos, use_container_width=True)
            st.subheader("**RELAÇÃO ENTRE BLOQUEIOS, STEALS E REBOTES:**")
            graph_mean_blk_stl_reb_3D_pos = generate_graph_mean_blk_stl_reb_3D_pos(430)
            st.plotly_chart(graph_mean_blk_stl_reb_3D_pos, use_container_width=True)

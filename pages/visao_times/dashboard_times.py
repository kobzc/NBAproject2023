import streamlit as st
from data.dataset import df_times
from graphics import (
    generate_graph_points_rank,
    generate_graph_efetive_3pm_2pm,
    generate_graph_3pm_2pm_altair,
    generate_graf_pizza_pts,
    generate_graf_pizza_ast,
    generate_graf_pizza_reb,
    generate_graph_bars_grp,
    generate_graph_def_acts_rank,
    generate_graph_stl_dreb_altair,
    generate_graph_blk_pf,
    generate_graph_pizza_stl,
    generate_graph_pizza_blk,
    generate_graph_bars_grp_def,
)
from styles import centralizar_titulo


def render_team_dashboard():
    pass


def show_dashboard(is_dashboard_mode=False):

    # Dashboard de times
    st.sidebar.subheader("Submenu Visão Times")
    view_mode = st.sidebar.radio("Selecione a visão:", ("Ataque", "Defesa"))

    if not is_dashboard_mode:
        # Menu de filtro para selecionar o time
        team_name = st.sidebar.selectbox(
            "Selecione o Time", ["Nenhum"] + list(df_times["Team"].unique())
        )
    else:
        # Modo "apenas dashboard" não mostra o menu de seleção
        team_name = "Nenhum"

    # Verifica se um time específico foi selecionado (diferente de "Nenhum")
    if team_name != "Nenhum":
        # Renderiza a página específica do time
        render_team_dashboard(df_times, team_name, view_mode)
    else:
        # Se nenhum time específico for selecionado, renderiza a visão geral
        if view_mode == "Ataque":

            st.markdown(
                centralizar_titulo("DASHBOARD DE TIMES: ATAQUE"), unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns([1.3, 2.4, 1])

            with col1:
                st.subheader("RANKING POR PONTOS:")
                graph_points_rank = generate_graph_points_rank()
                st.altair_chart(graph_points_rank, use_container_width=True)

                st.subheader("VITÓRIAS E DERROTAS POR TIME:")
                graph_bars_emp = generate_graph_bars_grp()
                st.plotly_chart(graph_bars_emp, use_container_width=True)

            with col2:
                st.subheader("RELAÇÃO ENTRE BOLAS DE DOIS E TRÊS DOS TIMES:")
                graph_3pm_2pm_alt = generate_graph_3pm_2pm_altair()
                st.altair_chart(graph_3pm_2pm_alt, use_container_width=True)

                st.subheader("EFETIVIDADE DOS TIMES EM BOLAS DE DOIS E TRÊS:")
                graph_efetive_3pm_2pm = generate_graph_efetive_3pm_2pm()
                st.plotly_chart(graph_efetive_3pm_2pm, use_container_width=True)
            with col3:
                # st.subheader("COLUNA INTERATIVA:")
                # st.subheader("TOP 3 TIMES COM MAIS PONTOS:")
                # graf_pizza_pts = generate_graf_pizza_pts()
                # st.altair_chart(graf_pizza_pts)
                st.subheader("TOP 3 TIMES COM MAIS ASSISTÊNCIAS:")
                graf_pizza_ast = generate_graf_pizza_ast()
                st.altair_chart(graf_pizza_ast)

                st.subheader("TOP 3 TIMES COM MAIS REBOTES:")
                graf_pizza_reb = generate_graf_pizza_reb()
                st.altair_chart(graf_pizza_reb)

        elif view_mode == "Defesa":

            st.markdown(
                centralizar_titulo("DASHBOARD DE TIMES: DEFESA"), unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns([1.3, 2.4, 1])

            with col1:
                st.subheader("RANKING POR ATOS DEFENSIVOS:")
                graph_def_acts_rank = generate_graph_def_acts_rank()
                st.plotly_chart(graph_def_acts_rank)

                st.subheader("AÇÕES DEFENSIVAS VS TURN-OVER CONCEDIDOS:")
                graph_bars_grp_def = generate_graph_bars_grp_def()
                st.plotly_chart(graph_bars_grp_def)

            with col2:
                st.subheader(
                    "RELAÇÃO ENTRE ROUBOS DE BOLA E REBOTES DEFENSIVOS POR TIME:"
                )
                graph_stl_dreb_altair = generate_graph_stl_dreb_altair()
                st.altair_chart(graph_stl_dreb_altair, use_container_width=True)

                st.subheader("DISTRIBUIÇÃO DOS TIMES EM BLOQUEIOS E FALTAS PESSOAIS:")
                graph_blk_pf = generate_graph_blk_pf()
                st.plotly_chart(graph_blk_pf, use_container_width=True)

            with col3:
                st.subheader("TOP 3 TIMES COM MAIS ROUBOS DE BOLA:")
                graph_pizza_stl = generate_graph_pizza_stl()
                st.altair_chart(graph_pizza_stl)

                st.subheader("TOP 3 TIMES COM MAIS BLOQUEIOS:")
                graph_pizza_blk = generate_graph_pizza_blk()
                st.altair_chart(graph_pizza_blk)

import streamlit as st
from data.dataset import df, column_mapping
from graphics import (
    gen_graph_players_dist_vol_3pm_2pm_ftm,
    gen_graph_players_dist_ast_pts_min,
    gen_graph_players_dist_blk_pf_min,
    gen_graph_players_dist_stl_dreb_gp,
)
from styles import (
    centralizar_titulo,
    custom_info,
    custom_subheader,
    rename_columns_for_presentation,
    centralizar_texto,
    break_line,
)


# 1. Quantos jogadores há na liga?
total_players = df.shape[0]

# 2. Qual é o jogador com o maior número de pontos?
player_most_pts = df.sort_values(by="PTS", ascending=False).iloc[0, 0]

# 3. Qual é o jogador com maior número de bolas de três pontos?
player_most_3pm = df.sort_values(by="3PM", ascending=False).iloc[0, 0]

# 4. Qual é o jogador com maior número de cestas de quadra?
player_most_2pm = df.sort_values(by="FGM", ascending=False).iloc[0, 0]

# 5. Qual é o jogador com maior número de lances livres arremessados (FTA)?
player_most_fta = df.sort_values(by="FTA", ascending=False).iloc[0, 0]

# 6. Qual é o jogador com maior número de assistências?
player_most_ast = df.sort_values(by="AST", ascending=False).iloc[0, 0]

# 7. Como estão distribuídas os jogadores em termos de percentual de bolas de 3 pontos, percentual de bolas de quadra e de lances livres? Em uma tabela.
tabl_percent_3pm_2pm_ft = df[["PName", "Team", "3P%", "FG%", "FT%"]]
tabl_percent_3pm_2pm_ft = rename_columns_for_presentation(
    tabl_percent_3pm_2pm_ft, column_mapping
)

# 8. Como estão distribuídos os jogadores em termos de volume de bolas de 3 pontos feitas, volume de bolas de 2 pontos feitas e lances livres convertidos? Em um gráfico de disperção 3d.
graph_players_dist_vol_3pm_2pm_ftm = gen_graph_players_dist_vol_3pm_2pm_ftm()

# 9. Como estão distribuídos os jogadores em termos de assistências feitas e pontos em relação ao número de minutos que estiveram em quadra? Em um gráfico de dispersão.
graph_players_dist_ast_pts_min = gen_graph_players_dist_ast_pts_min()

# 10. Quais foram os 10 jogadores com mais triplos duplos (TD3)? Em uma tabela.
tabl_10players_most_td3 = (
    df[["PName", "Team", "TD3"]]
    .sort_values(by="TD3", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

tabl_10players_most_td3 = rename_columns_for_presentation(
    tabl_10players_most_td3, column_mapping
)
# --------------------------------------------------------------------------------------------------------------------------------
# DEFESA

# 1. Quantos jogadores há na liga?
# total_players

# 2. Qual é o jogador com maior número de rebotes defensivos?
player_most_dreb = df.sort_values(by="DREB", ascending=False).iloc[0, 0]

# 3.Qual é o jogador com maior número de roubos de bola?
player_most_stl = df.sort_values(by="STL", ascending=False).iloc[0, 0]

# 4 Qual é o jogador com maior número de bloqueios?
player_most_blk = df.sort_values(by="BLK", ascending=False).iloc[0, 0]

# 5 Qual é o jogador com maior número de faltas pessoais?
player_most_pf = df.sort_values(by="PF", ascending=False).iloc[0, 0]

# 6. Qual é a média de rebotes defensivos, roubos de bola e bloqueios dos jogadores por jogo. Em uma tabela
tabl_average_stl_blk = df[["PName", "Team", "DREBperGP", "STLperGP", "BLKperGP"]]
tabl_average_stl_blk = rename_columns_for_presentation(
    tabl_average_stl_blk, column_mapping
)

# 7. Como estão distribuídos os jogadores em termos de bloqueios e faltas pessoais proporcional à minutagem do jogador? Em um gráfico de dispersão.
graph_players_dist_blk_pf_min = gen_graph_players_dist_blk_pf_min()

# 8. Como estão distribuídos os jogadores em termos de roubos de bola e de rebotes defensivos proporcional ao número de jogos em que participaram? Em um gráfico de dispersão.
graph_players_dist_stl_dreb_gp = gen_graph_players_dist_stl_dreb_gp()


def show_page():
    # Pagina de jogadores
    st.sidebar.subheader("SUBMENU VISÃO JOGADORES")
    view_mode = st.sidebar.radio("Selecione a visão:", ("Ataque", "Defesa"))

    if view_mode == "Ataque":
        st.markdown(
            centralizar_titulo("VISÃO DE JOGADORES: ATAQUE"),  # Título centralizado
            unsafe_allow_html=True,
        )
        st.markdown(
            centralizar_texto("Estátisticas de ataque dos jogadores na liga."),
            unsafe_allow_html=True,
        )
        break_line()

        st.markdown(
            centralizar_titulo("DESTAQUES:"),  # Título centralizado
            unsafe_allow_html=True,
        )

        dst1, dst2, dst3 = st.columns([1, 1, 1])

        with dst1:
            custom_subheader("TOTAL DE", "JOGADORES:"),
            custom_info(total_players)
        with dst2:
            custom_subheader("JOGADOR COM", "MAIS PONTOS:"),
            custom_info(player_most_pts)
        with dst3:
            custom_subheader("JOGADOR COM MAIS", "CESTAS DE TRÊS:"),
            custom_info(player_most_3pm)

        st.markdown("---")

        dst4, dst5, dst6 = st.columns([1, 1, 1])

        with dst4:
            custom_subheader("JOGADOR COM MAIS", "CESTAS DE QUADRA:"),
            custom_info(player_most_2pm)
        with dst5:
            custom_subheader("JOGADOR COM MAIS LANCES", "LIVRES ARREMESSADOS:"),
            custom_info(player_most_fta)
        with dst6:
            custom_subheader("JOGADOR COM MAIS", "ASSISTÊNCIAS:"),
            custom_info(player_most_ast)

        st.markdown("---")

        graph1, graph2 = st.columns([1, 1])
        with graph1:
            st.subheader(
                "DISTRIBUIÇÃO DOS JOGADORES EM TERMOS DE VOLUME DE BOLAS DE TRÊS, QUADRA E LANCES LIVRES FEITOS:"
            )
            st.plotly_chart(
                graph_players_dist_vol_3pm_2pm_ftm, use_container_width=True
            )
        with graph2:
            st.subheader(
                "DISTRIBUIÇÃO DOS JOGADORES EM TERMOS DE ASSISTÊNCIAS E PONTOS EM RELAÇÃO AO TEMPO EM QUADRA:"
            )
            st.plotly_chart(graph_players_dist_ast_pts_min)

        tabl1, tabl2 = st.columns([1, 1])
        with tabl1:
            st.subheader(
                "DISTRIBUIÇÃO DOS JOGADORES EM TERMOS DE BOLAS DE TRÊS, QUADRA E LANCES LIVRES:"
            )
            st.dataframe(tabl_percent_3pm_2pm_ft, use_container_width=True)
        with tabl2:
            custom_subheader("TOP 10 JOGADORES COM", "MAIS TRIPLO DUPLOS(TD3):")
            st.table(tabl_10players_most_td3)
    elif view_mode == "Defesa":
        st.markdown(
            centralizar_titulo("VISÃO DE JOGADORES: DEFESA"),  # Título centralizado
            unsafe_allow_html=True,
        )
        st.markdown(
            centralizar_texto("Estátisticas de defesa dos jogadores na liga."),
            unsafe_allow_html=True,
        )
        break_line()

        st.markdown(
            centralizar_titulo("DESTAQUES:"),  # Título centralizado
            unsafe_allow_html=True,
        )

        dst1, dst2, dst3 = st.columns([1, 1, 1])

        with dst1:
            custom_subheader("TOTAL DE", "JOGADORES:"),
            custom_info(total_players)
        with dst2:
            custom_subheader("JOGADOR COM MAIS", "REBOTES DEFENSIVOS:"),
            custom_info(player_most_dreb)
        with dst3:
            custom_subheader("JOGADOR COM MAIS", "ROUBOS DE BOLA:"),
            custom_info(player_most_stl)

        st.markdown("---")

        dst4, dst5 = st.columns([1, 1])

        with dst4:
            custom_subheader("JOGADOR COM MAIS", "BLOQUEIOS:"),
            custom_info(player_most_blk)
        with dst5:
            custom_subheader("JOGADOR COM MAIS", "FALTAS PESSOAIS:"),
            custom_info(player_most_pf)

        st.markdown("---")

        st.subheader(
            "MÉDIA DE REBOTES DEFENSIVOS, ROUBOS DE BOLA E BLOQUEIOS DOS JOGADORES POR PARTIDA:"
        )
        st.dataframe(tabl_average_stl_blk, use_container_width=True)

        graph1, graph2 = st.columns([1, 1])
        with graph1:
            custom_subheader(
                "DISTRIBUIÇÃO DOS JOGADORES EM TERMOS DE BLOQUEIOS",
                "E FALTAS PESSOAIS EM RELAÇÃO AO TEMPO EM QUADRA:",
            )
            st.plotly_chart(graph_players_dist_blk_pf_min)
        with graph2:
            custom_subheader(
                "DISTRIBUIÇÃO DE ROUBOS DE BOLA E REBOTES DEFENSIVOS",
                "POR JOGADOR, PROPORCIONAL AO NÚMERO DE JOGOS:",
            )
            st.plotly_chart(graph_players_dist_stl_dreb_gp)

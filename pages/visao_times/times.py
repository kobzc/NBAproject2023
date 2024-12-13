import streamlit as st
import plotly.express as px
from utils import (
    get_team_data,
    get_players_team_data,
    load_image,
    image_to_base64,
    display_image,
)
from data.dataset import df, df_times, column_mapping
from graphics import (
    generate_graph_points_rank,
    generate_graph_3pm_2pm,
    generate_graph_efetive_3pm_2pm,
    generate_graph_def_acts_rank,
    generate_graph_stl_dreb,
    generate_graph_blk_pf,
    graphic_pattern_color,
    graphic_pattern_height,
)
from styles import (
    centralizar_titulo,
    centralizar_texto,
    custom_info,
    url_to_img_tag,
    format_dataframe_to_html,
    rename_columns_for_presentation,
    custom_subheader,
    break_line,
    url_to_img_tag_logo_team,
)

##ATAQUE

# 1. Total de times
total_times = df_times.shape[0]
image_path = "assets/pngegg.png"
logo_nba = load_image(image_path)
logo_nba_base64 = image_to_base64(logo_nba)


# 2. Time com mais pontos
team_most_points = df_times.sort_values(by="PTS", ascending=False).iloc[0, 0]
team_most_points_img = df_times.sort_values(by="PTS", ascending=False).iloc[0][
    "team_img"
]
team_most_points_img = url_to_img_tag(team_most_points_img)

# 3. Time com mais bolas de três pontos
team_most_three_pointers = df_times.sort_values(by="3PM", ascending=False).iloc[0, 0]
team_most_three_pointers_img = df_times.sort_values(by="3PM", ascending=False).iloc[0][
    "team_img"
]
team_most_three_pointers_img = url_to_img_tag(team_most_three_pointers_img)

# 4. Time com mais FG
team_most_fg = df_times.sort_values(by="FGM", ascending=False).iloc[0, 0]
team_most_fg_img = df_times.sort_values(by="FGM", ascending=False).iloc[0]["team_img"]
team_most_fg_img = url_to_img_tag(team_most_fg_img)

# 5. Time com mais TO
team_most_tov = df_times.sort_values(by="TOV", ascending=False).iloc[0, 0]
team_most_tov_img = df_times.sort_values(by="TOV", ascending=False).iloc[0]["team_img"]
team_most_tov_img = url_to_img_tag(team_most_tov_img)

# 6. Tabela de porcentagem de bolas de três e de lances livres por time
percentage_table_of_three_fT = df_times[["Team", "3P%", "FT%"]]
percentage_table_of_three_fT = rename_columns_for_presentation(
    percentage_table_of_three_fT, column_mapping
)

# 7. Ranking de total de pontos
aux = df_times.sort_values(by="PTS", ascending=False)
ranking_points = aux[["Team", "PTS", "3PM", "FGM", "FTM"]]
# -------------------------------------------------------------------------------------
##DEFESA

# 1. Total de times
# total_times = df_times.shape[0]

# 2. DREB?
team_most_dreb = df_times.sort_values(by="DREB", ascending=False).iloc[0, 0]
team_most_dreb_img = df_times.sort_values(by="DREB", ascending=False).iloc[0][
    "team_img"
]
team_most_dreb_img = url_to_img_tag(team_most_dreb_img)

# 3. BLK?
team_most_blk = df_times.sort_values(by="BLK", ascending=False).iloc[0, 0]
team_most_blk_img = df_times.sort_values(by="BLK", ascending=False).iloc[0]["team_img"]
team_most_blk_img = url_to_img_tag(team_most_blk_img)

# 4. STL?
team_most_stl = df_times.sort_values(by="STL", ascending=False).iloc[0, 0]
team_most_stl_img = df_times.sort_values(by="STL", ascending=False).iloc[0]["team_img"]
team_most_stl_img = url_to_img_tag(team_most_stl_img)

# 5. PF?
team_most_pf = df_times.sort_values(by="PF", ascending=False).iloc[0, 0]
team_most_pf_img = df_times.sort_values(by="PF", ascending=False).iloc[0]["team_img"]
team_most_pf_img = url_to_img_tag(team_most_pf_img)

# 6. Tabela com DREB, STL e BLK?
dreb_stl_blk_tabl = df_times[["Team", "DREB", "STL", "BLK"]]
dreb_stl_blk_tabl = rename_columns_for_presentation(dreb_stl_blk_tabl, column_mapping)

# ------------------------------------------------------------------------------


# Específico, página filtrada
def render_team_page(df_times, team, view_mode):
    # Obtendo o dataframe específio para o time e seus jogadores
    team_selected = get_team_data(df_times, team)
    players_data = get_players_team_data(df, team)
    team_name = team_selected.iloc[0]["team_name"]

    # Obtendo uma cópia de df do time selecionado para apresentação
    team_selected_rename = rename_columns_for_presentation(
        team_selected, column_mapping
    )

    # Obtendo a imagem do time selecionado
    team_selected_img = team_selected_rename[["Logo"]].copy()

    team_title, space, team_logo = st.columns([1, 2, 1])

    with team_title:
        # Exibição da logo e do título da página
        title = f"ANÁLISE DO TIME: {team_name}"
        # display_image(logo_nba_base64)
        st.title(title)
    with team_logo:
        team_selected_img["Logo"] = team_selected_img["Logo"].apply(
            url_to_img_tag_logo_team
        )
        st.write(
            team_selected_img.to_html(escape=False, index=False),
            unsafe_allow_html=True,
        )

    # 2. Quantos pontos o time fez?
    points_team = team_selected["PTS"].iloc[0]

    # 3. Quantas assistências o time deu?
    ast_team = team_selected["AST"].iloc[0]

    # 4. Quantos rebotes o time teve?
    reb_team = team_selected["REB"].iloc[0]

    # 5. Quantos rebotes ofensivos o time teve?
    oreb_team = team_selected["OREB"].iloc[0]

    # ----------------------------------------------------------------

    # 6. Quantos roubos de bola o time fez?
    stl_team = team_selected["STL"].iloc[0]

    # 7. Quantos bloqueios o time deu?
    blk_team = team_selected["BLK"].iloc[0]

    # 8. Total de rebotes defensivos do time
    dreb_team = team_selected["DREB"].iloc[0]

    # 9. Quantos turn-overs o time concedeu?
    tov_team = team_selected["TOV"].iloc[0]

    # ----------------------------------------------------------------

    # Gráficos do time selecionado

    players_team_selected = get_players_team_data(df, team)

    # 8. Quais jogadores do time tiveram mais volumes em bolas de três e em bolas de dois de acordo com o número de jogos em que participaram? Em um gráfico de dispersão
    def generate_graph_players_3pm_2pm():
        chart = px.scatter(
            data_frame=players_team_selected,
            x="2PM",
            y="3PM",
            size="GP",
            template="plotly_dark",
            hover_data="PName",
            labels={
                "2PM": "2 Points Made",
                "3PM": "3 Points Made",
                "GP": "Games Played",
                "PName": "Player Name",
            },
            title="3PM vs 2PM with size proportional to the number of games played",
        ).update_layout(title_x=0.5)

        chart.update_traces(
            marker=dict(
                color=graphic_pattern_color, line=dict(width=1, color="#724f93")
            )
        )

        return chart

    # 9. Quantos jogadores há em cada posição de cada time? Em um histograma
    def generate_histogram():
        histogram = px.histogram(
            data_frame=players_team_selected,
            x="POS",
            template="plotly_dark",
            color="POS",
            labels={"POS": "Position"},
            title="Players per position",
        ).update_layout(showlegend=False, yaxis_title="Number of players", title_x=0.5)
        return histogram

    # 10. Que parcela dos pontos ficaram nas mão de cada posição de cada time? Em um gráfico de pizza
    def generate_graph_pts_pos():
        chart = px.pie(
            data_frame=players_team_selected,
            values="PTS",
            names="POS",
            labels={"POS": "Position", "PTS": "Points"},
            template="plotly_dark",
            title="Points made by each position",
            hole=0.5,
        ).update_layout(title_x=0.5, showlegend=False)
        return chart

    # ------------------------------------------------------------------------------------------------------------------------
    # DEFESA
    # 11. Quais jogadores de cada time tiveram mais roubos de bola e bloqueios de acordo com quantos rebotes defensivos eles pegam? Em um gráfico de dispersão
    def generate_graph_most_stl_blk():
        chart = px.scatter(
            data_frame=players_team_selected,
            x="STL",
            y="BLK",
            size="DREB",
            template="plotly_dark",
            hover_data="PName",
            height=graphic_pattern_height,
            labels={
                "STL": "Steals",
                "BLK": "Blocks",
                "DREB": "Defensive Rebounds",
                "PName": "Player Name",
            },
            title="Ball steal vs blocks with size proportional to defensive rebounds",
        ).update_layout(title_x=0.5)

        chart.update_traces(
            marker=dict(
                color=graphic_pattern_color,
                line=dict(width=1, color="#724f93"),
            )
        )
        return chart

    def generate_graph_def_actions_pos():
        chart = px.pie(
            data_frame=players_team_selected,
            values="DREB",
            names="POS",
            labels={"POS": "Position", "DREB": "Defensive Rebounds"},
            template="plotly_dark",
            title="Defensive rebounds by each position",
            hole=0.5,
        ).update_layout(title_x=0.5, showlegend=False)

        return chart

    if view_mode == "Ataque":

        st.write("Estatísticas de ataque do time:")
        # Destaques
        dst1, dst2, dst3, dst4 = st.columns([1, 1, 1, 1])

        with dst1:
            st.write("TOTAL DE PONTOS CONQUISTADOS:")
            custom_info(points_team)
        with dst2:
            st.write("TOTAL DE ASSISTÊNCIAS:")
            custom_info(ast_team)
        with dst3:
            st.write("TOTAL DE REBOTES PEGOS:")
            custom_info(reb_team)
        with dst4:
            st.write("TOTAL DE REBOTES OFENSIVOS:")
            custom_info(oreb_team)

        st.markdown("---")

        # Tabelas com status ofensivos
        total_2pm = team_selected["2PM"].iloc[0]
        total_3pm = team_selected["3PM"].iloc[0]
        total_ftm = team_selected["FTM"].iloc[0]

        # Porcentagem dos status ofensivos
        total_2percentage = team_selected_rename["Percentage of 2 points"].iloc[0]
        total_3percentage = team_selected_rename["Percentage of 3 points"].iloc[0]
        total_ftpercentage = team_selected_rename["Percentage of Free Throws"].iloc[0]

        st.subheader("STATUS OFENSIVOS DO TIME:")
        stats1, stats2 = st.columns([1, 1])
        with stats1:
            st.write("Concluídos:")
            st.write("**Total 2 Points Made:**")
            custom_info(total_2pm)

            st.write("**Total 3 Points Made:**")
            custom_info(total_3pm)

            st.write("**Total Free Throws Made:**")
            custom_info(total_ftm)

        with stats2:
            st.write("Porcentagem:")
            st.write("**Total Percentage of 2 Points:**")
            custom_info(total_2percentage)

            st.write("**Total Percentage of 3 Points:**")
            custom_info(total_3percentage)

            st.write("**Total Percentage of Free Throws:**")
            custom_info(total_ftpercentage)

        st.markdown("---")

        col1, col2 = st.columns([1, 1])
        with col1:
            # Gráficos ofensivos
            st.subheader(
                "**MAIOR VOLUME EM BOLAS DE TRÊS E EM BOLAS DE DOIS DE ACORDO COM A PARTICIPAÇÃO EM JOGOS:**"
            )
            graph_players_3pm_2pm = generate_graph_players_3pm_2pm()
            st.plotly_chart(graph_players_3pm_2pm, use_container_width=True)
        with col2:
            st.subheader("**PARCELA DE PONTOS DO TIME POR POSIÇÃO:**")
            graph_pts_pos = generate_graph_pts_pos()
            st.plotly_chart(graph_pts_pos)

        colg1, colg2 = st.columns([1, 1])
        with colg1:
            # Histograma
            st.subheader("**QUANTIDADE DE JOGADORES POR POSIÇÃO:**")
            histogram = generate_histogram()
            st.plotly_chart(histogram)
        with colg2:
            players_data = players_data.reset_index(drop=True)
            players_data = rename_columns_for_presentation(players_data, column_mapping)
            st.subheader("STATUS OFENSIVOS DOS JOGADORES DO TIME:")
            st.write("Jogadores do time:")
            table_players_ofensive = players_data[
                [
                    "Position",
                    "Player Name",
                    "Games Played",
                    "Wins",
                    "Losses",
                    "Minutes",
                    "Points",
                    "Assists",
                ]
            ]
            st.dataframe(table_players_ofensive, use_container_width=True)

    elif view_mode == "Defesa":
        st.write("Estatísticas de defesa do time:")
        dst1, dst2, dst3, dst4 = st.columns([1, 1, 1, 1])

        with dst1:
            st.write("TOTAL DE ROUBOS DE BOLA:")
            custom_info(stl_team)
        with dst2:
            st.write("TOTAL DE BLOQUEIOS EFETUADOS:")
            custom_info(blk_team)
        with dst3:
            st.write("TOTAL DE REBOTES DEFENSIVOS:")
            custom_info(dreb_team)
        with dst4:
            st.write("TOTAL DE TURN-OVERS CONCEDIDOS:")
            custom_info(tov_team)

        st.markdown("---")

        # Gráficos defensivos
        graph1, graph2 = st.columns([1, 1])
        with graph1:
            st.subheader(
                "**JOGADORES COM MAIS ROUBOS DE BOLA E BLOQUEIOS DE ACORDO COM QUANTOS REBOTES DEFENSIVOS PEGAM:**"
            )
            graph_most_stl_blk = generate_graph_most_stl_blk()
            st.plotly_chart(graph_most_stl_blk, use_container_width=True)
        with graph2:
            st.subheader("**PARCELA DE REBOTES DEFENSIVOS POR POSIÇÃO:**")
            graph_def_actions_pos = generate_graph_def_actions_pos()
            st.plotly_chart(graph_def_actions_pos, use_container_width=True)

        colg1, colg2 = st.columns([1, 1])
        with colg1:
            # Histograma
            st.subheader("**QUANTIDADE DE JOGADORES POR POSIÇÃO:**")
            histogram = generate_histogram()
            st.plotly_chart(histogram)
        with colg2:
            players_data = players_data.reset_index(drop=True)
            players_data = rename_columns_for_presentation(players_data, column_mapping)
            st.subheader("STATUS DEFENSIVOS DOS JOGADORES DO TIME:")
            st.write("Jogadores do time:")
            table_players_defensive = players_data[
                [
                    "Position",
                    "Player Name",
                    "Games Played",
                    "Wins",
                    "Losses",
                    "Minutes",
                    "Steals",
                    "Blocks",
                ]
            ]
            st.dataframe(table_players_defensive, use_container_width=True)


def show_page():
    # Página de times
    st.sidebar.subheader("Submenu Visão Times")
    view_mode = st.sidebar.radio("Selecione a visão:", ("Ataque", "Defesa"))

    # Menu de filtro para selecionar o time
    team_name = st.sidebar.selectbox(
        "Selecione o Time", ["Nenhum"] + list(df_times["Team"].unique())
    )

    # Verifica se um time específico foi selecionado (diferente de "Nenhum")
    if team_name != "Nenhum":
        # Renderiza a página específica do time
        render_team_page(df_times, team_name, view_mode)
    else:
        # Se nenhum time específico for selecionado, renderiza a visão geral
        if view_mode == "Ataque":
            st.markdown(
                centralizar_titulo("VISÃO DE ATAQUE DOS TIMES:"),  # Título centralizado
                unsafe_allow_html=True,
            )
            st.markdown(
                centralizar_texto("Aqui estão as estatísticas de ataque dos times."),
                unsafe_allow_html=True,
            )
            break_line()

            dst1, dst2, dst3, dst4, dst5 = st.columns([1, 1, 1, 1, 1])
            with dst1:
                custom_subheader("TOTAL DE", "TIMES")
                display_image(logo_nba_base64)
                custom_info(f"{total_times}")
            with dst2:
                custom_subheader("TIME COM", "MAIS PONTOS:")
                st.markdown(
                    f"<div style='text-align:center;'>{team_most_points_img}</div>",
                    unsafe_allow_html=True,
                )
                custom_info(f"{team_most_points}")
            with dst3:
                custom_subheader("TIME COM MAIS", "BOLAS DE TRÊS:")
                st.markdown(
                    f"<div style='text-align:center;'>{team_most_three_pointers_img}</div>",
                    unsafe_allow_html=True,
                )
                custom_info(f"{team_most_three_pointers}")
            with dst4:
                custom_subheader("TIME COM MAIS", "FIELD GOALS:")
                st.markdown(
                    f"<div style='text-align:center;'>{team_most_fg_img}</div>",
                    unsafe_allow_html=True,
                )
                custom_info(f"{team_most_fg}")
            with dst5:
                custom_subheader("TIME COM MAIS", "TURN-OVERS")
                st.markdown(
                    f"<div style='text-align:center;'>{team_most_tov_img}</div>",
                    unsafe_allow_html=True,
                )
                custom_info(f"{team_most_tov}")
            st.markdown("---")

            st.subheader(
                "**TABELA COM A PORCENTAGEM DE BOLAS DE TRÊS E DE LANCES LIVRES POR TIME:**"
            )
            st.dataframe(percentage_table_of_three_fT, use_container_width=True)

            st.subheader(f"**RANKING POR PONTOS:**")
            rank_col1, rank_col2 = st.columns([1, 1])
            with rank_col1:
                st.markdown(
                    centralizar_texto("Gráfico de barras"),  # st.write centralizado
                    unsafe_allow_html=True,
                )
                graph_points_ranking = generate_graph_points_rank()
                st.altair_chart(graph_points_ranking, use_container_width=True)
            with rank_col2:
                st.markdown(
                    centralizar_texto("Tabela"),  # st.write centralizado
                    unsafe_allow_html=True,
                )
                st.dataframe(ranking_points, use_container_width=True)

            graph_col1, graph_col2 = st.columns([1, 1])
            with graph_col1:
                st.subheader(
                    "**TIMES COM MAIOR VOLUME EM BOLAS DE TRÊS, COM MAIORES INFILTRAÇÕES E BOLAS DE MEIA DISTÂNCIA:**"
                )
                st.markdown(
                    centralizar_texto("Gráfico de dispersão"),  # st.write centralizado
                    unsafe_allow_html=True,
                )
                graph_3pm_2pm = generate_graph_3pm_2pm()
                st.plotly_chart(graph_3pm_2pm, use_container_width=True)

            with graph_col2:
                st.subheader(
                    "**TIMES COM MAIOR EFETIVIDADE EM BOLAS DE TRÊS E MAIOR NÚMERO DE INFILTRAÇÕES E BOLAS DE MEIA DISTÂNCIA:**"
                )
                st.markdown(
                    centralizar_texto("Gráfico de dispersão"),  # st.write centralizado
                    unsafe_allow_html=True,
                )
                graph_efetive_3pm_2pm = generate_graph_efetive_3pm_2pm()
                st.plotly_chart(graph_efetive_3pm_2pm, use_container_width=True)

        elif view_mode == "Defesa":
            st.markdown(
                centralizar_titulo("VISÃO DE DEFESA DOS TIMES:"),  # Título centralizado
                unsafe_allow_html=True,
            )
            st.markdown(
                centralizar_texto("Aqui estão as estatísticas de defesa dos times."),
                unsafe_allow_html=True,
            )
            break_line()

            # Destaques
            dst1, dst2, dst3, dst4, dst5 = st.columns([1, 1, 1, 1, 1])
            with dst1:
                custom_subheader("TOTAL DE", "TIMES:")
                display_image(logo_nba_base64)
                custom_info(f"{total_times}")
            with dst2:
                custom_subheader("TIME COM MAIS", "REBOTES DEF:"),
                st.markdown(
                    f"<div style='text-align:center;'>{team_most_dreb_img}</div>",
                    unsafe_allow_html=True,
                )
                custom_info(f"{team_most_dreb}")
            with dst3:
                custom_subheader("TIME COM MAIS", "BLOQUEIOS:"),
                st.markdown(
                    f"<div style='text-align:center;'>{team_most_blk_img}</div>",
                    unsafe_allow_html=True,
                )
                custom_info(f"{team_most_blk}")
            with dst4:
                custom_subheader("TIME COM MAIS", "ROUBOS DE BOLA:"),
                st.markdown(
                    f"<div style='text-align:center;'>{team_most_stl_img}</div>",
                    unsafe_allow_html=True,
                )
                custom_info(f"{team_most_stl}")
            with dst5:
                custom_subheader("TIME COM MAIS", "FALTAS PESSOAIS:"),
                st.markdown(
                    f"<div style='text-align:center;'>{team_most_pf_img}</div>",
                    unsafe_allow_html=True,
                )
                custom_info(f"{team_most_pf}")

            st.markdown("---")

            col1, col2 = st.columns([1, 1])
            with col1:
                # Tabela com DREB, STL e BLK
                st.subheader("**TABELA COM REBOTES DEFENSIVOS, STEALS E BLOQUEIOS:**")
                st.dataframe(dreb_stl_blk_tabl, use_container_width=True)
            with col2:
                # Gráfico de barras por atos defensivos
                st.subheader("**RANKING POR ATOS DEFENSIVOS:**")
                graph_def_acts_rank = generate_graph_def_acts_rank()
                st.plotly_chart(graph_def_acts_rank, use_container_width=True)

            col3, col4 = st.columns([1, 1])
            with col3:
                # Gráfico com mais roubos de bola e mais rebotes defensivos
                st.subheader(
                    "**TIMES COM MAIS ROUBOS DE BOLA E MAIS REBOTES DEFENSIVOS:**"
                )
                graph_stl_dreb = generate_graph_stl_dreb()
                st.plotly_chart(graph_stl_dreb, use_container_width=True)
            with col4:
                # Gráfico com mais bloqueios e personal fouls
                st.subheader("**TIMES COM MAIS BLOQUEIOS E FALTAS PESSOAIS:**")
                graph_blk_pf = generate_graph_blk_pf()
                st.plotly_chart(graph_blk_pf, use_container_width=True)


if __name__ == "__main__":
    show_page()

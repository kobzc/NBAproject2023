import plotly.express as px
import streamlit as st
import altair as alt
import pandas as pd
from data.dataset import df, df_posicoes, df_times

top10_times = df_times.head(10)
top3_times = df_times.head(3)
graphic_pattern_color = "rgb(255,255,255, 1)"
graphic_pattern_height = 430
graphic_pizza_pattern_height = 430
graphic_pizza_pattern_width = 400
graphic_pattern_color_palette = [
    "rgb(29, 66, 138)",
    "rgb(200, 16, 46)",
    "white",  # 7
    "rgb(29, 66, 138)",
    "rgb(29, 66, 138)",
    "rgb(200, 16, 46)",
    "rgb(29, 66, 138)",
    "white",
    "rgb(200, 16, 46)",
    "white",
]
colors = ["rgb(29, 66, 138)", "rgb(255,255,255, 1)", "rgb(200, 16, 46)"]


## VISÃO TIMES ATAQUE
# Gráfico de barras por pontuação
# @st.cache_resource
# def generate_graph_points_rank():
#     chart = px.bar(
#         data_frame=top5_times,
#         x="PTS",
#         y="Team",
#         orientation="h",
#         color="Team",
#         template="plotly_dark",
#         labels={"PTS": "Points"},
#         # height=800,
#         # width=800,
#     ).update_layout(
#         title="Total points made per team",
#         xaxis_title="Points made",
#         yaxis_title="Team",
#         showlegend=False,
#     )
#     return chart


def generate_graph_points_rank():
    # Criação do gráfico com Altair com cantos arredondados
    bars = (
        alt.Chart(top10_times)
        .mark_bar(cornerRadiusBottomRight=10, cornerRadiusTopRight=10)
        .encode(
            x=alt.X("PTS:Q", title="Points made"),
            y=alt.Y("Team:N", title="Team", sort="-x"),
            color=alt.Color(
                "Team:N",
                scale=alt.Scale(range=graphic_pattern_color_palette),
                legend=None,
            ),
        )
    )

    # Adicionar rótulos às barras
    labels = bars.mark_text(
        align="center",
        baseline="middle",
        size=14,
        dx=20,
        color="white",
    ).encode(text="PTS:Q", color=alt.value("white"))

    # Combinar as barras e os rótulos
    chart = (
        alt.layer(bars, labels)
        .properties(
            title="Top 10 teams with the most points", height=graphic_pattern_height
        )
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_title(fontSize=16)
        .configure_view(strokeWidth=0)
    )

    return chart


# 8. Quais times tiveram mais volume em bolas de três e quais tiveram em infiltrações e bolas de meia distância? Em um gráfico de dispersão
@st.cache_resource
def generate_graph_3pm_2pm():
    chart = px.scatter(
        data_frame=df_times,
        x="2PM",
        y="3PM",
        hover_name="Team",
        color="Team",
        color_discrete_sequence=colors,
        template="plotly_dark",
        labels={"2PM": "2 Points made", "3PM": "3 Points made"},
        opacity=0.6,
        title="3PM and 2PM by all players per team",
    ).update_traces(marker_size=40)
    return chart


# 9. Quais times tiveram maior efetividade em bolas de três e quais tiveram maior em infiltrações e bolas de meia distância? Em um grafico de dispersão
@st.cache_resource
def generate_graph_efetive_3pm_2pm():
    df_times["2P%"] = df_times["2P%"] / 100
    df_times["3P%"] = df_times["3P%"] / 100

    chart = (
        px.scatter(
            data_frame=df_times,
            x="2P%",
            y="3P%",
            hover_name="Team",
            template="plotly_dark",
            labels={"2P%": "2 Point percentage ", "3P%": "3 Point percentage"},
            color="Team",
            color_discrete_sequence=colors,
            title="Mean 3P percentage vs mean 2P percentage for all players per team",
            opacity=0.6,
            text="Team",
        )
        .update_layout(
            xaxis_tickformat=".2%",
            yaxis_tickformat=".2%",
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            showlegend=False,
        )
        .update_traces(
            marker_size=40,
            # text=[
            #     f"2P%: {x*100:.2f}%<br>3P%: {y*100:.2f}%"
            #     for x, y in zip(df_times["2P%"], df_times["3P%"])
            # ],
            textposition="middle center",
            mode="markers+text",  # Configura os modos para mostrar marcadores e texto
        )
    )
    return chart


### DASHBOARD ###
# Gráfico de barras empilhadas
@st.cache_resource
def generate_graph_3pm_2pm_altair():
    # Preparação dos dados
    teams = list(df_times["Team"].unique())
    data = {
        "teams": teams,
        "2PM": [df_times[df_times["Team"] == team]["2PM"].sum() for team in teams],
        "3PM": [df_times[df_times["Team"] == team]["3PM"].sum() for team in teams],
    }
    df_data = pd.DataFrame(data)

    # Transformação dos dados para formato longo
    df_long = df_data.melt(id_vars="teams", var_name="Type", value_name="Total")

    # Criação do gráfico
    bars = (
        alt.Chart(df_long)
        .mark_bar()
        .encode(
            x=alt.X("teams:N", title="Team", sort=teams),
            y=alt.Y("Total:Q", title="Total", stack="zero"),
            color=alt.Color(
                "Type:N",
                scale=alt.Scale(
                    domain=["3PM", "2PM"], range=["rgb(29, 66, 138)", "white"]
                ),
            ),
            tooltip=["teams:N", "Type:N", "Total:Q"],
        )
        .properties(title="Total 2PM vs 3PM by Team", height=graphic_pattern_height)
    )

    text = bars.mark_text(
        align="center",
        baseline="middle",
        color="black",
        fontSize=12,
        dy=-5,
    ).encode(
        text=alt.Text("Total:Q", format=".0f")  # Formato do texto
    )

    # Configurações do gráfico
    chart = (
        (bars + text)
        .configure_title(fontSize=14, anchor="start", color="white")
        .configure_axis(
            labelFontSize=10,
            titleFontSize=12,
            grid=False,
            tickColor="white",
            domainColor="white",
            tickSize=5,
        )
        .configure_legend(
            labelFontSize=10,
            titleFontSize=12,
            direction="horizontal",
            orient="top",
            labelColor="white",
            titleColor="white",
        )
    )

    return chart


def generate_line_chart():
    df_long = top10_times.melt(
        id_vars="Team",
        value_vars=["2P%", "3P%"],
        var_name="Type",
        value_name="Percentage",
    )

    chart = (
        alt.Chart(df_long)
        .mark_line(point=True)
        .encode(
            x=alt.X("Type:N", title="Type"),
            y=alt.Y("Percentage:Q", title="Percentage"),
            color="Team:N",
            tooltip=["Team:N", "Type:N", "Percentage:Q"],
        )
        .properties(title="Trend of 2P% and 3P% by Team")
    )

    return chart


@st.cache_resource
def generate_graph_bars_grp():
    # Transformar os dados no formato longo
    df_long = df.head(10).melt(
        id_vars=["Team"], value_vars=["W", "L"], var_name="Result", value_name="Count"
    )

    # Gerar o gráfico de barras com Plotly Express
    chart = (
        px.bar(
            df_long,
            x="Team",
            y="Count",
            color="Result",
            color_discrete_map={
                "W": "rgb(29, 66, 138)",  # Cor para vitórias
                "L": "rgb(200, 16, 46)",  # Cor para derrotas
            },
            barmode="group",
            title="Wins and Losses by Team",
            labels={"Count": "Number of Games", "Team": "Team", "Result": "Outcome"},
        )
        .update_traces(
            text=None,  # Remove os valores de texto nas barras
            texttemplate=None,  # Desativa o template de texto
            textposition="none",  # Remove a posição do texto
            selector=dict(type="bar"),
        )
        .update_layout(
            xaxis_title="Team",
            yaxis_title="Number of Games",
            legend_title="Outcome",
            xaxis=dict(
                tickmode="array",
                tickvals=df["Team"].unique(),
                ticktext=df["Team"].unique(),
            ),
            yaxis=dict(
                title="Number of Games", tickformat=","
            ),  # Formato dos números no eixo Y
        )
    )

    return chart


## COLUNA INTERATIVA DOS GRÁFICOS DE PIZZA
## Gráficos Gerais (PTS, AST, REB)
@st.cache_resource
def generate_graf_pizza_pts():
    # Gráfico de Pizza
    arc = (
        alt.Chart(top3_times)
        .mark_arc(
            innerRadius=0,
            outerRadius=150,
        )
        .encode(
            theta=alt.Theta(field="PTS", type="quantitative", stack=True),
            color=alt.Color(
                "Team:N",
                scale=alt.Scale(range=colors),
                legend=None,
            ),  # Usa a coluna de cores
            tooltip=["PTS", "Team"],
        )
    )

    # Rótulos dos Times
    label1 = arc.mark_text(
        radius=178, size=14, align="left", angle=45, fontWeight="bold"
    ).encode(text="Team")

    # Rótulos dos Pontos
    label2 = arc.mark_text(
        radius=120,
        size=14,
        align="center",
        color="black",  # Cor do texto para contrastar com o fundo
        fontWeight="bold",
    ).encode(text="PTS:Q", color=alt.value("#191d2d"))

    chart = alt.layer(arc, label1, label2).properties(
        height=graphic_pizza_pattern_height,
        width=graphic_pizza_pattern_width,
    )

    return chart


@st.cache_resource
def generate_graf_pizza_ast():
    # Gráfico de Pizza
    arc = (
        alt.Chart(top3_times)
        .mark_arc(
            innerRadius=75,
            outerRadius=150,
        )
        .encode(
            theta=alt.Theta(field="AST", type="quantitative", stack=True),
            color=alt.Color(
                "Team:N",
                scale=alt.Scale(range=colors),
                legend=None,
            ),  # Usa a coluna de cores
            tooltip=["AST", "Team"],
        )
    )

    # Rótulos dos Times
    label1 = arc.mark_text(
        radius=178, size=14, align="left", angle=45, fontWeight="bold"
    ).encode(text="Team")

    # Rótulos dos Pontos
    label2 = arc.mark_text(
        radius=120,
        size=14,
        align="center",
        color="black",  # Cor do texto para contrastar com o fundo
        fontWeight="bold",
    ).encode(text="AST:Q", color=alt.value("#191d2d"))

    chart = alt.layer(arc, label1, label2).properties(
        height=graphic_pizza_pattern_height,
        width=graphic_pizza_pattern_width,
    )

    return chart


@st.cache_resource
def generate_graf_pizza_reb():
    # Gráfico de Pizza
    arc = (
        alt.Chart(top3_times)
        .mark_arc(
            innerRadius=75,
            outerRadius=150,
        )
        .encode(
            theta=alt.Theta(field="REB", type="quantitative", stack=True),
            color=alt.Color(
                "Team:N",
                scale=alt.Scale(range=colors),
                legend=None,
            ),  # Usa a coluna de cores
            tooltip=["REB", "Team"],
        )
    )

    # Rótulos dos Times
    label1 = arc.mark_text(
        radius=178, size=14, align="left", angle=45, fontWeight="bold"
    ).encode(text="Team")

    # Rótulos dos Pontos
    label2 = arc.mark_text(
        radius=120,
        size=14,
        align="center",
        color="black",  # Cor do texto para contrastar com o fundo
        fontWeight="bold",
    ).encode(text="REB:Q", color=alt.value("#191d2d"))

    chart = alt.layer(arc, label1, label2).properties(
        height=graphic_pizza_pattern_height,
        width=graphic_pizza_pattern_width,
    )

    return chart


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
##TIMES DEFESA

# 7. Ranking de atos defensivos
aux = df_times.sort_values(by="DEF_ACTIONS", ascending=False)
top10_aux = aux.head(10)


@st.cache_resource
def generate_graph_def_acts_rank():
    chart = px.bar(
        data_frame=top10_aux,
        x="DEF_ACTIONS",
        y="Team",
        color="Team",
        color_discrete_sequence=graphic_pattern_color_palette,
        template="plotly_dark",
        height=graphic_pattern_height,
        text_auto=True,
    ).update_layout(
        showlegend=False,
        title="Top 10 teams with the most defensive actions",
        xaxis_title="Defensive Actions",
        yaxis_title="Teams",
    )
    return chart


# 8. Quais times tiveram mais roubos de bola e quais tiveram mais rebotes defensivos? Em um gráfico de disperção
@st.cache_resource
def generate_graph_stl_dreb():
    chart = px.scatter(
        data_frame=df_times,
        x="DREB",
        y="STL",
        color="Team",
        color_discrete_sequence=colors,
        labels={"DREB": "Defensive Rebounds", "STL": "Steals"},
        template="plotly_dark",
        title="Ball steal vs defensive rebounds for all players per team",
        opacity=0.6,
    ).update_traces(marker_size=40)
    return chart


# 9. Quais times tiveram mais bloqueios e quais tiveram mais faltas pessoais? Em um gráfico de disperção
@st.cache_resource
def generate_graph_blk_pf():
    chart = (
        px.scatter(
            data_frame=df_times,
            x="BLK",
            y="PF",
            color="Team",
            color_discrete_sequence=colors,
            labels={"BLK": "Blocks", "PF": "Personal Fouls"},
            template="plotly_dark",
            title="Blocks vs personal fouls for all players per team",
            opacity=0.6,
            text="Team",
        )
        .update_layout(
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            showlegend=False,
        )
        .update_traces(
            marker_size=40,
            textposition="middle center",
            mode="markers+text",  # Configura os modos para mostrar marcadores e texto
        )
    )
    return chart


### DASHBOARD ###


@st.cache_resource
def generate_graph_stl_dreb_altair():
    # Preparação dos dados
    teams = list(df_times["Team"].unique())
    data = {
        "teams": teams,
        "STL": [df_times[df_times["Team"] == team]["STL"].sum() for team in teams],
        "DREB": [df_times[df_times["Team"] == team]["DREB"].sum() for team in teams],
    }
    df_data = pd.DataFrame(data)

    # Transformação dos dados para formato longo
    df_long = df_data.melt(id_vars="teams", var_name="Type", value_name="Total")

    # Criação do gráfico
    bars = (
        alt.Chart(df_long)
        .mark_bar()
        .encode(
            x=alt.X("teams:N", title="Team", sort=teams),
            y=alt.Y("Total:Q", title="Total", stack="zero"),
            color=alt.Color(
                "Type:N",
                scale=alt.Scale(
                    domain=["STL", "DREB"], range=["rgb(29, 66, 138)", "white"]
                ),
            ),
            tooltip=["teams:N", "Type:N", "Total:Q"],
        )
        .properties(title="Total STL vs DREB by Team", height=graphic_pattern_height)
    )

    text = bars.mark_text(
        align="center",
        baseline="middle",
        color="black",
        fontSize=12,
        dy=-5,
    ).encode(
        text=alt.Text("Total:Q", format=".0f")  # Formato do texto
    )

    # Configurações do gráfico
    chart = (
        (bars + text)
        .configure_title(fontSize=14, anchor="start", color="white")
        .configure_axis(
            labelFontSize=10,
            titleFontSize=12,
            grid=False,
            tickColor="white",
            domainColor="white",
            tickSize=5,
        )
        .configure_legend(
            labelFontSize=10,
            titleFontSize=12,
            direction="horizontal",
            orient="top",
            labelColor="white",
            titleColor="white",
        )
    )

    return chart


@st.cache_resource
def generate_graph_bars_grp_def():

    df_long = top10_aux.melt(
        id_vars=["Team"],
        value_vars=["DEF_ACTIONS", "TOV"],
        var_name="Result",
        value_name="Count",
    )

    # Converter a coluna 'Count' para uma lista, garantindo que seja serializável
    df_long["Count"] = df_long["Count"].tolist()

    chart = px.bar(
        df_long,
        x="Team",
        y="Count",
        color="Result",
        color_discrete_map={
            "DEF_ACTIONS": "rgb(29, 66, 138)",  # Cor para DEF_ACTIONS
            "TOV": "rgb(200, 16, 46)",  # Cor para TOV
        },
        barmode="group",
        title="Def actions vs TOV",
        labels={"Count": "Number of Actions", "Team": "Team", "Result": "Action"},
    ).update_layout(
        xaxis_title="Team",
        yaxis_title="Number of Actions",
        legend_title="Outcome",
        xaxis=dict(
            tickmode="array",
            tickvals=top10_aux["Team"].unique(),
            ticktext=top10_aux["Team"].unique(),
        ),
        yaxis=dict(title="Number of Actions", tickformat=","),
        margin=dict(t=50, b=50, l=50, r=50),
    )

    return chart


### COLUNA INTERATIVA ###


@st.cache_resource
def generate_graph_pizza_stl():
    # Gráfico de Pizza
    arc = (
        alt.Chart(top3_times)
        .mark_arc(
            innerRadius=75,
            outerRadius=150,
        )
        .encode(
            theta=alt.Theta(field="STL", type="quantitative", stack=True),
            color=alt.Color(
                "Team:N",
                scale=alt.Scale(range=colors),
                legend=None,
            ),  # Usa a coluna de cores
            tooltip=["STL", "Team"],
        )
    )

    # Rótulos dos Times
    label1 = arc.mark_text(
        radius=178, size=14, align="left", angle=45, fontWeight="bold"
    ).encode(text="Team")

    # Rótulos dos Pontos
    label2 = arc.mark_text(
        radius=120,
        size=14,
        align="center",
        fontWeight="bold",
    ).encode(text="STL:Q", color=alt.value("#191d2d"))

    chart = alt.layer(arc, label1, label2).properties(
        height=graphic_pizza_pattern_height,
        width=graphic_pizza_pattern_width,
    )

    return chart


@st.cache_resource
def generate_graph_pizza_blk():
    # Gráfico de Pizza
    arc = (
        alt.Chart(top3_times)
        .mark_arc(
            innerRadius=75,
            outerRadius=150,
        )
        .encode(
            theta=alt.Theta(field="BLK", type="quantitative", stack=True),
            color=alt.Color(
                "Team:N",
                scale=alt.Scale(range=colors),
                legend=None,
            ),  # Usa a coluna de cores
            tooltip=["BLK", "Team"],
        )
    )

    # Rótulos dos Times
    label1 = arc.mark_text(
        radius=178, size=14, align="left", angle=45, fontWeight="bold"
    ).encode(text="Team")

    # Rótulos dos Pontos
    label2 = arc.mark_text(
        radius=120,
        size=14,
        align="center",
        fontWeight="bold",
    ).encode(text="BLK:Q", color=alt.value("#191d2d"))

    chart = alt.layer(arc, label1, label2).properties(
        height=graphic_pizza_pattern_height,
        width=graphic_pizza_pattern_width,
    )

    return chart


# --------------------------------------------------------------------------------------------------------------------------------
## VISÃO POSIÇÕES
## ATAQUE


# 1. Quantos jogadores há em cada posição
@st.cache_resource
def generate_hist_player_position():
    # Definir as cores disponíveis
    colors = ["rgb(29, 66, 138)", "rgb(255,255,255, 1)", "rgb(200, 16, 46)"]

    # Obter as posições únicas do dataframe
    positions = df["POS"].unique()

    # Criar o mapeamento de cores com repetição
    color_map = {pos: colors[i % len(colors)] for i, pos in enumerate(positions)}

    # Criar o histograma com as cores personalizadas
    chart = px.histogram(
        data_frame=df,
        x="POS",
        template="plotly_dark",
        color="POS",
        color_discrete_map=color_map,  # Mapeamento das cores
        labels={
            "POS": "Position",
        },
        height=graphic_pattern_height,
        title="Number of players per position",
    ).update_layout(showlegend=False, yaxis_title="Number of players")

    return chart


# 2. Distribuição de pontos em cada posição na temporada, em um gráfico de barras ou gráfico de caixa.


# 2.1 Gráfico em barras
@st.cache_resource
def generate_dist_pts_each_pos_bar():
    # Gráfico de barras horizontais com rótulos
    bars = (
        alt.Chart(df_posicoes)
        .mark_bar()
        .encode(
            y=alt.Y("POS", title="Position", sort="-x"),  # Eixo y categórico
            x=alt.X("PTS", title="Points"),  # Eixo x com valores
            color=alt.Color(
                "POS",
                scale=alt.Scale(domain=list(df_posicoes["POS"].unique()), range=colors),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("POS", title="Position"),  # Mostra apenas "Position"
                alt.Tooltip("PTS:Q", title="Points"),  # Mostra o valor de "Points"
            ],
        )
        .properties(
            title="Distribution of points in each position",
            height=graphic_pattern_height,
        )
    )

    text = (
        bars.mark_text(
            align="center", baseline="middle", color="white", fontSize=12, dy=-5, dx=15
        )
        .encode(text=alt.Text("PTS:Q", format=".0f"))  # Formato do texto
        .encode(text="PTS:Q", color=alt.value("white"))
    )

    # Configurações do gráfico
    chart = (
        (bars + text)
        .configure_title(fontSize=14, anchor="start", color="white")
        .configure_axis(
            labelFontSize=10,
            titleFontSize=12,
            grid=False,
            tickColor="white",
            domainColor="white",
            tickSize=5,
        )
        .configure_legend(
            labelFontSize=10,
            titleFontSize=12,
            direction="horizontal",
            orient="top",
            labelColor="white",
            titleColor="white",
        )
    )

    return chart


# 2.1.2 Gáfico em caixa
@st.cache_resource
def generate_dist_each_pos_box():
    chart = px.box(
        data_frame=df_posicoes,
        x="POS",
        y="PTS",
        color="POS",
        template="plotly_dark",
        hover_data=["PTS", "POS"],
        height=graphic_pattern_height,
        title="Distribution of points in each position",
        labels={
            "POS": "Position",
            "PTS": "Points",
        },
    ).update_layout(yaxis_title="Points", showlegend=False)
    return chart


# 3. Distribuição de pontos por jogo em cada posição, em um gráfico de caixa.
@st.cache_resource
def generate_dist_pts_gp():
    chart = px.box(
        data_frame=df_posicoes,
        x="POS",
        y="PTSperGP",
        color="POS",
        height=graphic_pattern_height,
        labels={
            "POS": "Position",
        },
        template="plotly_dark",
        title="Distribution of points per game in each position",
    ).update_layout(yaxis_title="Points per game", showlegend=False)
    return chart


# 4.2 Gráfico de dispersão 3d
@st.cache_resource
def generate_graph_mean_ast_ft_3p():
    chart = px.scatter_3d(
        df_posicoes,
        x="AST%",
        y="FT%",
        z="3P%",
        hover_data="POS",
        text="POS",
        title="3P% vs FT% vs AST%",
        template="plotly_dark",
        height=520,
    ).update_traces(
        marker=dict(color=graphic_pattern_color, line=dict(width=1, color="#10111e"))
    )
    return chart


# 5. Distribuiçoes das bolas de 3 convertidas de acordo com as posições, em um gráfico de caixa
@st.cache_resource
def generate_graph_3pm_pos():
    chart = px.box(
        data_frame=df_posicoes,
        x="POS",
        y="3PM",
        color="POS",
        labels={
            "POS": "Position",
        },
        template="plotly_dark",
        title="Distribution of points per game in each position",
    ).update_layout(yaxis_title="3 Points made", showlegend=False)
    return chart


## DASHBOARD
top3_pos = df_posicoes.head(3)


def generate_graf_pizza_3pm_pos():
    # Gráfico de Pizza
    arc = (
        alt.Chart(top3_pos)
        .mark_arc(
            innerRadius=75,
            outerRadius=150,
        )
        .encode(
            theta=alt.Theta(field="3PM", type="quantitative", stack=True),
            color=alt.Color(
                "POS:N",
                scale=alt.Scale(range=colors),
                legend=None,
            ),  # Usa a coluna de cores
            tooltip=["3PM", "POS"],
        )
    )

    # Rótulos dos Times
    label1 = arc.mark_text(
        radius=178, size=14, align="left", angle=45, fontWeight="bold"
    ).encode(text="POS")

    # Rótulos dos Pontos
    label2 = arc.mark_text(
        radius=120,
        size=14,
        align="center",
        color="black",  # Cor do texto para contrastar com o fundo
        fontWeight="bold",
    ).encode(text="3PM:Q", color=alt.value("#191d2d"))

    chart = alt.layer(arc, label1, label2).properties(
        height=graphic_pizza_pattern_height,
        width=graphic_pizza_pattern_width,
    )

    return chart


def generate_graf_pizza_reb_pos():
    # Gráfico de Pizza
    arc = (
        alt.Chart(top3_pos)
        .mark_arc(
            innerRadius=75,
            outerRadius=150,
        )
        .encode(
            theta=alt.Theta(field="REB", type="quantitative", stack=True),
            color=alt.Color(
                "POS:N",
                scale=alt.Scale(range=colors),
                legend=None,
            ),  # Usa a coluna de cores
            tooltip=["REB", "POS"],
        )
    )

    # Rótulos das posições
    label1 = arc.mark_text(
        radius=178, size=14, align="left", angle=45, fontWeight="bold"
    ).encode(text="POS")

    # Rótulos dos Pontos
    label2 = arc.mark_text(
        radius=120,
        size=14,
        align="center",
        color="black",  # Cor do texto para contrastar com o fundo
        fontWeight="bold",
    ).encode(text="REB:Q", color=alt.value("#191d2d"))

    chart = alt.layer(arc, label1, label2).properties(
        height=graphic_pizza_pattern_height,
        width=graphic_pizza_pattern_width,
    )

    return chart


# ----------------------------------------------------------------
## DEFESA


# 1. Gráfico de dispersão de roubos de bolas e bloqueio de acordo com a porcentagem de rebotes.
@st.cache_resource
def generate_graph_stl_blk_reb_pos():
    chart = px.scatter(
        data_frame=df_posicoes,
        x="BLK",
        y="STL",
        size="REB",
        color="POS",
        color_discrete_sequence=colors,
        template="plotly_dark",
        labels={
            "STL": "Steals",
            "BLK": "Blocks",
            "REB": "Rebounds",
            "POS": "Position",
        },
        hover_data="POS",
        title="Steal vs block with size proportional to rebounds",
        opacity=0.6,
        text="POS",
    ).update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        showlegend=False,
    )

    return chart


# 2. Distribuição dos valores de roubos de bola por posição, em um grafico de caixa
@st.cache_resource
def generate_graph_dist_stl_pos():
    chart = px.box(
        data_frame=df_posicoes,
        x="POS",
        y="STL",
        color="POS",
        labels={
            "POS": "Position",
        },
        template="plotly_dark",
        title="Distribution of ball steal values ​​by position",
    ).update_layout(yaxis_title="Steals", title_x=0.5, showlegend=False)
    return chart


# 3. Distribuição das ações defensivas por posição, em um gráfico de caixa
@st.cache_resource
def generate_graph_defact_pos():

    chart = px.box(
        data_frame=df_posicoes,
        x="POS",
        y="DEF_ACTIONS",
        color="POS",
        labels={
            "POS": "Position",
        },
        template="plotly_dark",
        title="Distribution of defensive actions by position",
    ).update_layout(yaxis_title="Defensive actions", title_x=0.5, showlegend=False)
    return chart


def generate_graph_bars_defact_pos():

    bars = (
        alt.Chart(df_posicoes)
        .mark_bar()
        .encode(
            y=alt.Y("POS", title="Position", sort="-x"),  # Eixo y categórico
            x=alt.X("DEF_ACTIONS", title="Defensive Actions"),  # Eixo x com valores
            color=alt.Color(
                "POS",
                scale=alt.Scale(domain=list(df_posicoes["POS"].unique()), range=colors),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("POS", title="Position"),  # Mostra apenas "Position"
                alt.Tooltip(
                    "DEF_ACTIONS:Q", title="Defensive Actions"
                ),  # Mostra o valor de "Points"
            ],
        )
        .properties(
            title="Distribution of points in each position",
            height=graphic_pattern_height,
        )
    )

    text = (
        bars.mark_text(
            align="center", baseline="middle", color="white", fontSize=12, dy=-5, dx=15
        )
        .encode(text=alt.Text("DEF_ACTIONS:Q", format=".0f"))  # Formato do texto
        .encode(text="DEF_ACTIONS:Q", color=alt.value("white"))
    )

    # Configurações do gráfico
    chart = (
        (bars + text)
        .configure_title(fontSize=14, anchor="start", color="white")
        .configure_axis(
            labelFontSize=10,
            titleFontSize=12,
            grid=False,
            tickColor="white",
            domainColor="white",
            tickSize=5,
        )
        .configure_legend(
            labelFontSize=10,
            titleFontSize=12,
            direction="horizontal",
            orient="top",
            labelColor="white",
            titleColor="white",
        )
    )

    return chart


# 4. Distribuição das médias de bloqueios, roubos de bola e rebotes em cada posição, em um gráfico de dispersão e dispersão 3D.
@st.cache_resource
def generate_graph_mean_stl_blk_reb_pos():
    chart = px.scatter(
        data_frame=df_posicoes,
        x="BLK%",
        y="STL%",
        size="REB%",
        color="POS",
        color_discrete_sequence=colors,
        template="plotly_dark",
        hover_data="POS",
        labels={
            "STL%": "Percentage of Steals",
            "BLK%": "Percentage of Blocks",
            "REB%": "Percentage of Rebounds",
        },
        title="Steal percentage vs block percentage with size proportional to rebounds percentage",
        text="POS",
        opacity=0.6,
    ).update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        showlegend=False,
    )

    return chart


@st.cache_resource
def generate_graph_mean_blk_stl_reb_3D_pos(height):
    chart = px.scatter_3d(
        df_posicoes,
        x="BLK%",
        y="STL%",
        z="REB%",
        hover_data="POS",
        title="Distribution of Average Blocks, Steals and Rebounds by Position",
        template="plotly_dark",
        height=height,
        text="POS",
    ).update_traces(
        marker=dict(
            color=graphic_pattern_color, line=dict(width=1, color="DarkSlateGrey")
        )
    )
    return chart


### DASHBOARD ###


def generate_graph_bars_defact_tov_pos():
    df_long = df_posicoes.melt(
        id_vars=["POS"],
        value_vars=["DEF_ACTIONS", "TOV"],
        var_name="Result",
        value_name="Count",
    )

    # Converter a coluna 'Count' para uma lista, garantindo que seja serializável
    df_long["Count"] = df_long["Count"].tolist()

    chart = px.bar(
        df_long,
        x="POS",
        y="Count",
        color="Result",
        color_discrete_map={
            "DEF_ACTIONS": "rgb(29, 66, 138)",  # Cor para DEF_ACTIONS
            "TOV": "rgb(200, 16, 46)",  # Cor para TOV
        },
        barmode="group",
        title="Def actions vs TOV",
        labels={"Count": "Number of Actions", "POS": "Position", "Result": "Action"},
        height=graphic_pattern_height,
    ).update_layout(
        xaxis_title="POS",
        yaxis_title="Number of Actions",
        legend_title="Outcome",
        legend=dict(
            orientation="h",  # Orientação horizontal
            y=1.1,  # Posição vertical acima do gráfico
            x=0.5,  # Centralizar horizontalmente
            xanchor="center",  # Âncora horizontal
            yanchor="bottom",  # Âncora vertical
        ),
        xaxis=dict(
            tickmode="array",
            tickvals=df_posicoes["POS"].unique(),
            ticktext=df_posicoes["POS"].unique(),
        ),
        yaxis=dict(title="Number of Actions", tickformat=","),
        margin=dict(t=50, b=50, l=50, r=50),
    )

    return chart


@st.cache_resource
def generate_graph_bars_stl_pf_pos():
    # Preparação dos dados
    positions = list(df_posicoes["POS"].unique())
    data = {
        "Position": positions,
        "STL": [
            df_posicoes[df_posicoes["POS"] == pos]["STL"].sum() for pos in positions
        ],
        "PF": [df_posicoes[df_posicoes["POS"] == pos]["PF"].sum() for pos in positions],
    }
    df_data = pd.DataFrame(data)

    # Transformação dos dados para formato longo
    df_long = df_data.melt(id_vars="Position", var_name="Action", value_name="Total")

    # Criação do gráfico
    bars = (
        alt.Chart(df_long)
        .mark_bar()
        .encode(
            x=alt.X("Position:N", title="Position", sort=positions),
            y=alt.Y("Total:Q", title="Total", stack="zero"),
            color=alt.Color(
                "Action:N",
                scale=alt.Scale(
                    domain=["PF", "STL"], range=["#fff", "rgb(29, 66, 138)"]
                ),
            ),
            tooltip=["Position:N", "Action:N", "Total:Q"],
        )
        .properties(title="Total STL vs PF by POS", height=graphic_pattern_height)
    )

    text = bars.mark_text(
        align="center",
        baseline="middle",
        color="black",
        fontSize=12,
        dy=-5,
    ).encode(
        text=alt.Text("Total:Q", format=".0f")  # Formato do texto
    )

    # Configurações do gráfico
    chart = (
        (bars + text)
        .configure_title(fontSize=14, anchor="start", color="white")
        .configure_axis(
            labelFontSize=10,
            titleFontSize=12,
            grid=False,
            tickColor="white",
            domainColor="white",
            tickSize=5,
        )
        .configure_legend(
            labelFontSize=10,
            titleFontSize=12,
            direction="horizontal",
            orient="top",
            labelColor="white",
            titleColor="white",
        )
    )

    return chart


@st.cache_resource
def generate_graf_pizza_dreb_pos():
    # Gráfico de Pizza
    arc = (
        alt.Chart(top3_pos)
        .mark_arc(
            innerRadius=75,
            outerRadius=150,
        )
        .encode(
            theta=alt.Theta(field="DREB", type="quantitative", stack=True),
            color=alt.Color(
                "POS:N",
                scale=alt.Scale(range=colors),
                legend=None,
            ),  # Usa a coluna de cores
            tooltip=["DREB", "POS"],
        )
    )

    # Rótulos das posições
    label1 = arc.mark_text(
        radius=178, size=14, align="left", angle=45, fontWeight="bold"
    ).encode(text="POS")

    # Rótulos dos Pontos
    label2 = arc.mark_text(
        radius=120,
        size=14,
        align="center",
        color="black",  # Cor do texto para contrastar com o fundo
        fontWeight="bold",
    ).encode(text="DREB:Q", color=alt.value("#191d2d"))

    chart = alt.layer(arc, label1, label2).properties(
        height=graphic_pizza_pattern_height,
        width=graphic_pizza_pattern_width,
    )

    return chart


# --------------------------------------------------------------------------------------------------------------------------------

## VISÃO JOGADORES
## ATAQUE


# 1 (8). Como estão distribuídos os jogadores em termos de volume de bolas de 3 pontos feitas, volume de bolas de 2 pontos feitas e lances livres convertidos? Em um gráfico de disperção 3d.
@st.cache_resource
def gen_graph_players_dist_vol_3pm_2pm_ftm():
    chart = px.scatter_3d(
        data_frame=df,
        x="3PM",
        y="2PM",
        z="FTM",
        hover_data="PName",
        title="Distribution of players, 3PM vs 2PM vs FTM",
        labels={
            "PName": "Player Name",
            "FTM": "Free trows made",
            "3PM": "3 Points made",
            "2PM": "2 Points made",
        },
        template="plotly_dark",
        height=graphic_pattern_height,
    ).update_traces(
        marker=dict(color=graphic_pattern_color, line=dict(width=1, color="#724f93"))
    )
    return chart


# 2 (9). Como estão distribuídos os jogadores em termos de assistências feitas e pontos em relação ao número de minutos que estiveram em quadra? Em um gráfico de dispersão.
@st.cache_resource
def gen_graph_players_dist_ast_pts_min():
    chart = px.scatter(
        data_frame=df,
        x="AST",
        y="PTS",
        size="Min",
        hover_data="PName",
        labels={
            "AST": "Assists",
            "PTS": "Points",
            "Min": "Minutes",
            "PName": "Player Name",
        },
        template="plotly_dark",
        height=graphic_pattern_height,
    ).update_traces(
        marker=dict(color=graphic_pattern_color, line=dict(width=1, color="#724f93"))
    )

    return chart


# --------------------------------------------------------------------------------------------------------------------------------
## DEFESA


# 1 (7). Como estão distribuídos os jogadores em termos de bloqueios e faltas pessoais proporcional à minutagem do jogador? Em um gráfico de dispersão.
@st.cache_resource
def gen_graph_players_dist_blk_pf_min():
    chart = px.scatter(
        data_frame=df,
        x="BLK",
        y="PF",
        size="Min",
        template="plotly_dark",
        hover_data="PName",
        labels={
            "BLK": "Blocks",
            "PF": "Personal Fouls",
            "Min": "Minutes",
            "PName": "Player Name",
        },
    ).update_traces(marker=dict(color=graphic_pattern_color))

    return chart


# 2 (8). Como estão distribuídos os jogadores em termos de roubos de bola e de rebotes defensivos proporcional ao número de jogos em que participaram? Em um gráfico de dispersão.
@st.cache_resource
def gen_graph_players_dist_stl_dreb_gp():
    chart = px.scatter(
        data_frame=df,
        x="STL",
        y="DREB",
        size="GP",
        template="plotly_dark",
        hover_data="PName",
        labels={
            "STL": "Steals",
            "DREB": "Defensive Rebounds",
            "GP": "Games Played",
            "PName": "Player Name",
        },
    ).update_traces(
        marker=dict(color=graphic_pattern_color, line=dict(width=1, color="#724f93"))
    )

    return chart

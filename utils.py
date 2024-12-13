import pandas as pd
import streamlit as st
import base64
from PIL import Image
from io import BytesIO
from styles import width_img_pattern, height_img_pattern


@st.cache_data
def load_data_df():
    # Carregar dados do arquivo CSV
    df = pd.read_csv("./data/data_merged.csv")
    return df


@st.cache_data
def load_data_df_times():
    # Carregar dados do arquivo CSV
    df_times = pd.read_csv("./data/df_times.csv")
    return df_times


@st.cache_data
def get_team_data(df_times, team_name):
    # Filtra os dados para o time selecionado
    return df_times[df_times["Team"] == team_name]


@st.cache_data
def get_players_team_data(df, team_name):
    # Filtra os dados para os jogadores do time selecionado
    return df[df["Team"] == team_name].copy()


@st.cache_data
def get_player_data(df, player_name):
    # Filtra os dados para o jogador do time selecionado
    return df[df["Team"] == player_name]


@st.cache_data
def load_data_df_posicoes():
    df = pd.read_csv("./data/data_merged.csv")

    df_posicoes = (
        df[
            [
                "POS",
                "PTS",
                "3PM",
                "3PA",
                "3P%",
                "FGM",
                "FGA",
                "FG%",
                "FTM",
                "FTA",
                "FT%",
                "OREB",
                "DREB",
                "REB",
                "AST",
                "TOV",
                "STL",
                "BLK",
                "PF",
                "2PM",
                "2PA",
                "2P%",
                "PTSperGP",
            ]
        ]
        .groupby("POS")
        .agg(
            {
                "PTS": "sum",
                "3PM": "sum",
                "3PA": "sum",
                "FGM": "sum",
                "FGA": "sum",
                "FTM": "sum",
                "FTA": "sum",
                "3P%": "mean",
                "FG%": "mean",
                "FT%": "mean",
                "OREB": "sum",
                "DREB": "sum",
                "REB": "sum",
                "AST": "sum",
                "TOV": "sum",
                "STL": "sum",
                "BLK": "sum",
                "PF": "sum",
                "2PM": "sum",
                "2PA": "sum",
                "2P%": "mean",
                "PTSperGP": "sum",
            }
        )
        .sort_values(by="PTS", ascending=False)
        .round(2)
        .reset_index()
    )
    return df_posicoes


# Função para abrir a imagem usando PIL
@st.cache_resource
def load_image(image_path):
    # Abre a imagem usando PIL
    img = Image.open(image_path)
    return img


# Função para converter a imagem para base64 com caching de dados
def image_to_base64(img):
    # Converte a imagem para base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


# Função para mostrar a imagem no Streamlit com largura fixa
def display_image(image_base64, width=width_img_pattern, height=height_img_pattern):
    # Exibe a imagem no Streamlit com ajuste de CSS
    st.markdown(
        f"<div style='text-align:center;'><img src='data:image/png;base64,{image_base64}' style='width:{width};height:{height};'></div>",
        unsafe_allow_html=True,
    )

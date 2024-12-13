import streamlit as st

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="APP NBA",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://x.com/Kobzc1",
        "Report a bug": "https://x.com/Kobzc1",
        "About": "Esse app foi desenvolvido por Lucas Constantino (Kobz)",
    },
)

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from pages.visao_times.times import show_page as tshow_page
from pages.visao_posicoes.posicoes import show_page as pshow_page
from pages.visao_jogadores.jogadores import show_page as jshow_page

with st.sidebar:
    # Menu principal
    st.sidebar.title("MENU")
    page_select = st.sidebar.selectbox(
        "Selecione a página", ["Visão Times", "Visão Posições", "Visão Jogadores"]
    )

# Renderizar a página selecionada
if page_select == "Visão Times":
    tshow_page()
elif page_select == "Visão Posições":
    pshow_page()
elif page_select == "Visão Jogadores":
    jshow_page()

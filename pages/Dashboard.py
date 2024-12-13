import streamlit as st


st.set_page_config(
    page_title="DASBOARD NBA📈",
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

from pages.visao_times.dashboard_times import show_dashboard as tshow_dashboard
from pages.visao_posicoes.dashboard_posicoes import show_dashboard as pshow_dashboard
from pages.visao_jogadores.dashboard_jogadores import show_dashboard as jshow_dashboard

with st.sidebar:
    # Menu principal
    st.sidebar.title("MENU")
    page_select = st.sidebar.selectbox(
        "Selecione o dashboard",
        ["Dashboard Times", "Dashboard Posições"],
    )

# Renderizar a página selecionada
if page_select == "Dashboard Times":
    tshow_dashboard(is_dashboard_mode=True)
elif page_select == "Dashboard Posições":
    pshow_dashboard()
# elif page_select == "Dashboard Jogadores":
#     jshow_dashboard()

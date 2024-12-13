import streamlit as st

width_img_pattern = "150px"
height_img_pattern = "150px"


def apply_custom_css():
    st.markdown(
        """
        <style>
        .custom-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 400px; /* Ajuste conforme necessário */
            padding-top: 10px;
        }
        .custom-info {
            text-align: center;
            margin-top: 10px; /* Ajuste conforme necessário */
        }
        .adjust-margin {
            margin-bottom: 20px; /* Ajuste conforme necessário */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def centralizar_titulo(titulo):
    """Retorna uma string de HTML para centralizar um título."""
    return f"""
        <h1 style="text-align:center;"><strong>{titulo}<strong/></h1>
    """


def centralizar_texto(texto: str) -> str:
    """Retorna uma string de HTML para centralizar texto."""
    return f"<div style='text-align: center;'><strong>{texto}<strong/></div>"


def break_line():
    st.markdown(
        f"<br>",
        unsafe_allow_html=True,
    )


def custom_subheader(line1, line2):
    # HTML e CSS para o subcabeçalho formatado
    subheader_html = f"""
    <div style="
        font-size: 26px; 
        font-weight: bold; 
        margin-bottom: 10px; 
        color: white;
        ">
        <div>{line1}</div>
        <div>{line2}</div>
    </div>
    """
    # Exibir o subcabeçalho no Streamlit
    st.markdown(subheader_html, unsafe_allow_html=True)


def custom_info(message):
    html = f"""
    <div class='custom_info' style='
        background-color: rgb(200, 16, 46, 0.5);
        font-size: 17px;
        font-weight: bold;
        color: rgb(255,255,255, 1);
        padding: 15px;
        border-radius: 5px;
    '>
        {message}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def format_with_line_break_bold(line1, line2, line3):
    return f"<div style='font-family:Source Sans Pro, sans-serif;font-size:1.75rem; font-weight:600; line-height: 1.2; margin: 0 0 10px;'><strong>{line1}<br>{line2}<br>{line3}</strong></div>"


# Função para converter URLs em tags HTML <img>
# def url_to_img_tag(url):
#     return f"<img src='{url}' alt='team logo' style='width:auto;height:auto;'>"
def url_to_img_tag(url, width=width_img_pattern, height=height_img_pattern):
    return f"<img src='{url}' alt='team logo' style='width:{width};height:{height};'>"


def url_to_img_tag_logo_team(url, width="100%", height="350px"):
    return f"<img src='{url}' alt='team logo' style='width:{width};height:{height};'>"


def format_dataframe_to_html(df):
    # Aplicar a função para transformar URLs em HTML
    df["Logo"] = df["Logo"].apply(url_to_img_tag)

    # Converte o DataFrame para HTML
    html = df.to_html(escape=False, index=False)

    # Aplica o CSS para estilizar a tabela
    html = f"""
            <style>
                .dataframe {{
                    width: 100%; /* Define a largura total do container */
                    margin: auto; /* Centraliza a tabela */
                }}
                table {{
                    border-collapse: collapse; /* Remove espaçamentos entre as células */
                }}
                th, td {{
                    padding: 8px; /* Adiciona espaçamento interno nas células */
                    text-align: center; /* Centraliza o texto */
                }}
                {html}
            </style>
        """
    return html


def rename_columns_for_presentation(df, column_mapping):
    """
    Renomeia as colunas de um DataFrame de acordo com um mapeamento fornecido.

    Parâmetros:
    - df: DataFrame a ser renomeado.
    - column_mapping: Dicionário de mapeamento de colunas no formato {coluna_antiga: nova_coluna}.

    Retorna:
    - DataFrame com as colunas renomeadas.
    """
    return df.rename(columns=column_mapping)

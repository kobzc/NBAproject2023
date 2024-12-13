from utils import load_data_df, load_data_df_times, load_data_df_posicoes

df = load_data_df()
df_times = load_data_df_times()
df_posicoes = load_data_df_posicoes()


## POSIÇÕES ATAQUE
# 1. Criação da coluna de porcentagem de assistências por posição
df_posicoes["ASTperc"] = round((df_posicoes["AST"] / df_posicoes["AST"].sum()) * 100, 2)
df_posicoes.rename(columns={"ASTperc": "AST%"}, inplace=True)

## POSIÇÕES DEFESA
# 1. Criação das colunas de médias de bloqueios, roubos de bola e rebotes por posição
df_posicoes["BLKperc"] = round((df_posicoes["BLK"] / df_posicoes["BLK"].sum()) * 100, 2)
df_posicoes["STLperc"] = round((df_posicoes["STL"] / df_posicoes["STL"].sum()) * 100, 2)
df_posicoes["REBperc"] = round((df_posicoes["REB"] / df_posicoes["REB"].sum()) * 100, 2)

df_posicoes.rename(columns={"BLKperc": "BLK%"}, inplace=True)
df_posicoes.rename(columns={"STLperc": "STL%"}, inplace=True)
df_posicoes.rename(columns={"REBperc": "REB%"}, inplace=True)


# 2. Criação da coluna de ações defensivas no data frame df_posicoes
df_posicoes["DEF_ACTIONS"] = (
    df_posicoes["DREB"] + df_posicoes["STL"] + df_posicoes["BLK"]
)

column_mapping = {
    "PName": "Player Name",
    "STL": "Steals",
    "BLK": "Blocks",
    "DREB": "Defensive Rebounds",
    "POS": "Position",
    "team_img": "Logo",
    "AST": "Assists",
    "PTS": "Points",
    "OREB": "Offensive Rebounds",
    "REB": "Rebounds",
    # "2PM": "2 Points Made",
    # "3PM": "3 Points Made",
    # "FTM": "Free Throws Made",
    "TOV": "Turn-over",
    # "PF": "Personal Fouls",
    "BLK%": "Blocks%",
    "STL%": "Steals%",
    "REB%": "Rebounds%",
    "2P%": "Percentage of 2 points",
    "3P%": "Percentage of 3 points",
    "FT%": "Percentage of Free Throws",
    "team_name": "Team Name",
    "GP": "Games Played",
    "W": "Wins",
    "L": "Losses",
    "Min": "Minutes",
    # "PTSperGP": "PTS per GP",
    # "FGMperGP": "FGM per GP",
    # "FGAperGP": "FGA per GP",
    # "FG%perGP": "FG% per GP",
    # "3PMperGP": "3PM per GP",
    # "3PAperGP": "3PA per GP",
    # "3P%perGP": "3P% per GP",
    # "FTMperGP": "FTM per GP",
    # "FT%perGP": "FTM per GP",
    # "OREBperGP": "OREB per GP",
    # "DREBperGP": "DREB per GP",
    # "REBperGP": "REB per GP",
    # "ASTperGP": "AST per GP",
    # "TOVperGP": "TOV per GP",
    # "STLperGP": "STL per GP",
    # "BLKperGP": "BLK per GP",
    # "PFperGP": "PF per GP",
    # "FPperGP": "FP per GP",
    # "2PMperGP": "2PM per GP",
    # "2PAperGP": "2PA per GP",
    # "2P%perGP": "2P% per GP",
}

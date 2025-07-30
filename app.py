import streamlit as st
import pandas as pd
import plotly.express as px

# URL corrigida da planilha
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# Tratamento de dados
df["PERÍODO"] = df["PERÍODO"].astype(str).str.upper()
df["TURNO"] = df["TURNO"].astype(str).str.upper()

# Tema escuro com CSS customizado
st.set_page_config(layout="wide", page_title="Dashboard Coleta Centro")

with open("style.css", "w") as f:
    f.write("""
    <style>
        body, .stApp {
            background-color: #000000;
            color: white;
        }
        .css-1cpxqw2, .stSelectbox, .stRadio, .stMarkdown, .css-1d391kg, .stNumberInput {
            color: white !important;
        }
        div[data-testid="metric-container"] {
            background-color: #111111;
            border-radius: 15px;
            padding: 10px;
            box-shadow: 0px 0px 8px #5d00ff;
            transition: transform 0.3s ease;
        }
        div[data-testid="metric-container"]:hover {
            transform: scale(1.02);
            box-shadow: 0px 0px 15px #7d00ff;
        }
        div[data-testid="stHorizontalBlock"] > div {
            padding: 0.5rem;
        }
        .stRadio > div {
            flex-direction: row;
        }
        label[data-baseweb="radio"] {
            border: 2px solid #5d00ff;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            margin: 0.2rem;
            color: white;
        }
        label[data-baseweb="radio"]:hover {
            background-color: #5d00ff22;
        }
        label[data-baseweb="radio"][aria-checked="true"] {
            background-color: #5d00ff;
            color: white;
        }
    </style>
    """)

with open("style.css", "r") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

# Filtros
meses = df["PERÍODO"].unique().tolist()
meses.sort()
mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True)

df_filtrado = df[df["PERÍODO"] == mes_selecionado]

# KPIs
qtd_total = int(df_filtrado["QTD"].sum())
qtd_am = int(df_filtrado[df_filtrado["TURNO"] == "AM"]["QTD"].sum())
qtd_pm = int(df_filtrado[df_filtrado["TURNO"] == "PM"]["QTD"].sum())

# Cards (sem linhas)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Coletas", value=f"{qtd_total}")
with col2:
    st.metric(label="Turno AM", value=f"{qtd_am}")
with col3:
    st.metric(label="Turno PM", value=f"{qtd_pm}")

# Gráfico de barras
fig_bar = px.bar(
    df_filtrado,
    x="HORÁRIO",
    y="QTD",
    color="TURNO",
    title="Coletas por Horário",
    color_discrete_sequence=["#6a0dad", "#00bfff"]
)
fig_bar.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de linhas
fig_line = px.line(
    df_filtrado,
    x="HORÁRIO",
    y="QTD",
    color="TURNO",
    markers=True,
    title="Evolução das Coletas",
    color_discrete_sequence=["#ff66cc", "#66ccff"]
)
fig_line.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white"
)
st.plotly_chart(fig_line, use_container_width=True)

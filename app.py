import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# CSS customizado
st.markdown("""
    <style>
        body {
            background-color: black;
            color: white;
        }
        .main {
            background-color: black;
        }
        div[data-testid="metric-container"] {
            background-color: #1a1a1a;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #8000ff;
            color: white;
            text-align: center;
            box-shadow: 0 0 10px #8000ff;
            transition: 0.3s;
        }
        div[data-testid="metric-container"]:hover {
            transform: scale(1.02);
            box-shadow: 0 0 20px #9f51ff;
        }
        h1, h2, h3, h4, h5, h6, p, span {
            color: white !important;
        }
        .stRadio > div {
            flex-direction: row;
            gap: 10px;
        }
        .st-eb {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Leitura da planilha correta
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# Garantir que a coluna Mês seja string
df["Mês"] = df["Mês"].astype(str).str.upper()

# Filtro por mês
meses = df["Mês"].unique()
mes_selecionado = st.radio("Selecione o mês:", meses, index=0)

df_filtrado = df[df["Mês"] == mes_selecionado]

# Métricas interativas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Coleta AM", f"{int(df_filtrado['Coleta Am'].sum())} sacos")
with col2:
    st.metric("Coleta PM", f"{int(df_filtrado['Coleta PM'].sum())} sacos")
with col3:
    st.metric("Total de Sacos", f"{int(df_filtrado['Total de Sacos'].sum())} sacos")

# Gráfico de distribuição AM vs PM
fig_bar = px.bar(
    df_filtrado.melt(id_vars="Mês", value_vars=["Coleta Am", "Coleta PM"]),
    x="variable", y="value", color="variable",
    color_discrete_sequence=["#ab47bc", "#7e57c2"],
    labels={"variable": "Turno", "value": "Quantidade"},
    title="Distribuição Geral AM vs PM"
)
fig_bar.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')

# Gráfico de linha: evolução por mês
fig_linha = px.line(
    df,
    x="Mês", y="Total de Sacos",
    markers=True,
    title="Evolução da Quantidade de Sacos por Mês",
    color_discrete_sequence=["#00e5ff"]
)
fig_linha.update_traces(line=dict(width=3))
fig_linha.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')

# Exibir gráficos
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_linha, use_container_width=True)

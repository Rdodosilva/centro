import streamlit as st
import pandas as pd
import plotly.express as px

# Estilo visual (modo escuro, texto branco)
st.set_page_config(page_title="Dashboard Coleta Centro", layout="wide")

# CSS personalizado
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .stApp {
            background-color: #000000;
            color: white;
        }
        .metric-container {
            background-color: #111111;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin: 10px 0;
        }
        .css-1v0mbdj p {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Leitura da planilha (versão funcionando local ou do GitHub) ----
@st.cache_data
def carregar_dados():
    url_github = "https://github.com/Rdodosilva/centro/raw/main/Coleta%20centro2.xlsx"
    df = pd.read_excel(url_github)
    return df

df = carregar_dados()

# Pré-visualização
st.subheader("Pré-visualização dos dados")
st.dataframe(df, use_container_width=True)

# Verificar se as colunas estão presentes
colunas_esperadas = ["Mês", "Coleta AM", "Coleta PM", "Total de Sacos"]
if not all(coluna in df.columns for coluna in colunas_esperadas):
    st.error("❌ A planilha não possui as colunas esperadas.")
    st.stop()

# Filtro de mês
meses = df["Mês"].unique()
mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True, index=0)

df_filtrado = df[df["Mês"] == mes_selecionado]

# ---- Métricas ----
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Coleta AM", int(df_filtrado["Coleta AM"].values[0]))
with col2:
    st.metric("Coleta PM", int(df_filtrado["Coleta PM"].values[0]))
with col3:
    st.metric("Total de Sacos", int(df_filtrado["Total de Sacos"].values[0]))

# ---- Gráfico de Barras ----
st.subheader("Gráfico de Coleta (AM vs PM)")
fig_bar = px.bar(
    df_filtrado.melt(id_vars=["Mês"], value_vars=["Coleta AM", "Coleta PM"]),
    x="variable", y="value", color="variable",
    color_discrete_sequence=["#AA00FF", "#6200EA"],
    labels={"variable": "Turno", "value": "Quantidade"},
    text="value"
)
fig_bar.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ---- Gráfico de Linha (Histórico) ----
st.subheader("Evolução da Coleta por Mês")
fig_linha = px.line(
    df,
    x="Mês",
    y="Total de Sacos",
    markers=True,
    title="Histórico de Total de Sacos por Mês",
    labels={"Total de Sacos": "Total", "Mês": "Mês"},
    color_discrete_sequence=["#00E5FF"]
)
fig_linha.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white"
)
st.plotly_chart(fig_linha, use_container_width=True)

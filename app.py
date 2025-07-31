import streamlit as st
import pandas as pd
import plotly.express as px

# === CONFIGURAÇÃO ===
st.set_page_config(page_title="Dashboard Coleta Centro", layout="wide")

# === TÍTULO ===
st.title("📊 Dashboard de Coleta - Centro da Cidade")

# === LEITURA DOS DADOS ===
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Coleta centro2.xlsx", engine='openpyxl')  # garante compatibilidade com xlsx
    df.columns = df.columns.str.strip()  # remove espaços extras nos nomes das colunas
    return df

df = carregar_dados()

# === EXIBIR COLUNAS PARA VERIFICAÇÃO ===
st.sidebar.markdown("### Colunas detectadas:")
st.sidebar.write(df.columns.tolist())

# === FILTRAR DADOS (remover linha Total, se houver) ===
if "Mês" in df.columns:
    df = df[~df["Mês"].astype(str).str.lower().str.contains("total")]
else:
    st.error("❌ Coluna 'Mês' não encontrada na planilha. Verifique o nome da coluna.")
    st.stop()

# === TRATAMENTO DE DADOS ===
df["Total de Sacos"] = df["Total de Sacos"].fillna(0)
df["Coleta AM"] = df["Coleta AM"].fillna(0)
df["Coleta PM"] = df["Coleta PM"].fillna(0)

# === FILTRO POR MÊS ===
meses_disponiveis = df["Mês"].unique().tolist()
mes_selecionado = st.sidebar.radio("Selecione o mês:", meses_disponiveis, horizontal=True)

df_filtrado = df[df["Mês"] == mes_selecionado]

# === MÉTRICAS ===
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Sacos", int(df_filtrado["Total de Sacos"].sum()))
with col2:
    st.metric("Coleta AM", int(df_filtrado["Coleta AM"].sum()))
with col3:
    st.metric("Coleta PM", int(df_filtrado["Coleta PM"].sum()))

# === GRÁFICO DE BARRAS ===
fig_barras = px.bar(
    df,
    x="Mês",
    y=["Coleta AM", "Coleta PM"],
    title="Coleta AM vs PM por Mês",
    barmode="group",
    color_discrete_sequence=["#6A0DAD", "#00BFFF"]
)
st.plotly_chart(fig_barras, use_container_width=True)

# === GRÁFICO DE LINHA DO TOTAL ===
fig_linha = px.line(
    df,
    x="Mês",
    y="Total de Sacos",
    markers=True,
    title="Evolução do Total de Sacos por Mês",
    line_shape="linear"
)
st.plotly_chart(fig_linha, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# Título
st.set_page_config(page_title="Dashboard de Coleta", layout="wide")
st.title("📊 Dashboard de Coleta - Centro")

# Upload manual da planilha
arquivo = st.file_uploader("Selecione o arquivo de coleta (.csv ou .xlsx)", type=["csv", "xlsx"])

if arquivo:
    # Detecta o tipo de arquivo
    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)

    # Verifica se a coluna 'Mês' existe
    if "Mês" not in df.columns:
        st.error("A planilha enviada não contém a coluna 'Mês'. Verifique o formato do arquivo.")
        st.stop()

    # Remove linhas totais ou títulos extras
    df = df[~df["Mês"].astype(str).str.lower().str.contains("total", na=False)]

    # Filtros por mês
    meses = df["Mês"].unique()
    mes_selecionado = st.radio("Selecione o mês", options=meses, horizontal=True)

    df_filtrado = df[df["Mês"] == mes_selecionado]

    # KPIs
    total_am = df_filtrado["Coleta AM"].sum()
    total_pm = df_filtrado["Coleta PM"].sum()
    total_sacos = df_filtrado["Total de Sacos"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("🟣 Coleta AM", f"{total_am}")
    col2.metric("🟡 Coleta PM", f"{total_pm}")
    col3.metric("⚪ Total de Sacos", f"{total_sacos}")

    # Gráfico de barras
    fig = px.bar(
        df_filtrado,
        x="Mês",
        y=["Coleta AM", "Coleta PM"],
        barmode="group",
        title="Coleta AM vs PM",
        labels={"value": "Quantidade", "variable": "Turno"},
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Por favor, envie um arquivo com os dados para visualizar o dashboard.")

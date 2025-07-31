import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard de Coleta - Centro")

st.markdown("<h1 style='color:white;'>🚛 Dashboard de Coleta - Centro</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Faça o upload da planilha de coleta (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Lê a primeira aba da planilha
        df = pd.read_excel(uploaded_file)

        # Verifica e exibe colunas detectadas
        st.write("Colunas encontradas:", df.columns.tolist())

        # Ajuste para garantir que as colunas esperadas existam
        colunas_esperadas = ['Mês', 'Coleta AM', 'Coleta PM', 'Total de Sacos']
        for col in colunas_esperadas:
            if col not in df.columns:
                st.error(f"Coluna ausente na planilha: {col}")
                st.stop()

        # Remove linhas que contenham "total" na coluna "Mês"
        df = df[~df["Mês"].astype(str).str.lower().str.contains("total", na=False)]

        # Filtros
        meses = df["Mês"].unique()
        mes_selecionado = st.radio("Selecione o mês", meses, horizontal=True)

        df_filtrado = df[df["Mês"] == mes_selecionado]

        # Métricas principais
        total_am = df_filtrado["Coleta AM"].sum()
        total_pm = df_filtrado["Coleta PM"].sum()
        total_geral = df_filtrado["Total de Sacos"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total AM", f"{total_am}")
        col2.metric("Total PM", f"{total_pm}")
        col3.metric("Total de Sacos", f"{total_geral}")

        # Gráfico
        fig = px.bar(
            df_filtrado,
            x="Mês",
            y=["Coleta AM", "Coleta PM"],
            title="Coletas por Período",
            labels={"value": "Quantidade", "variable": "Turno"},
            barmode="group",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("Erro ao processar o arquivo. Verifique se está no formato correto (.xlsx) e com colunas esperadas.")
        st.exception(e)

else:
    st.warning("⚠️ Faça o upload do arquivo XLSX para visualizar o dashboard.")

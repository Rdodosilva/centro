import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard de Coleta - Centro", page_icon="🚛")
st.markdown("<h1 style='color: white;'>Dashboard de Coleta - Centro</h1>", unsafe_allow_html=True)

# Upload do arquivo
file = st.file_uploader("📤 Faça o upload da planilha de coleta (.xlsx)", type=["xlsx"])

if file:
    try:
        df = pd.read_excel(file)

        # Verificar se a coluna 'Mês' existe
        if "Mês" not in df.columns:
            st.error("❌ A planilha precisa conter a coluna 'Mês'.")
        else:
            # Remover linhas com 'total' na coluna Mês
            df = df[~df["Mês"].astype(str).str.lower().str.contains("total", na=False)]

            # Converter colunas numéricas, se necessário
            colunas_esperadas = ["Coleta AM", "Coleta PM", "Total de Sacos"]
            for coluna in colunas_esperadas:
                if coluna not in df.columns:
                    st.warning(f"⚠️ Coluna '{coluna}' não encontrada na planilha.")
                    df[coluna] = 0  # Cria a coluna com zeros
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0)

            # Filtros
            meses = df["Mês"].unique().tolist()
            mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True)

            df_filtrado = df[df["Mês"] == mes_selecionado]

            # Métricas
            total_am = int(df_filtrado["Coleta AM"].sum())
            total_pm = int(df_filtrado["Coleta PM"].sum())
            total_geral = int(df_filtrado["Total de Sacos"].sum())

            col1, col2, col3 = st.columns(3)
            col1.metric("🟣 Coleta AM", f"{total_am} sacos")
            col2.metric("🔵 Coleta PM", f"{total_pm} sacos")
            col3.metric("⚫ Total do Dia", f"{total_geral} sacos")

            # Gráfico de barras
            fig_bar = px.bar(
                df_filtrado,
                x="Mês",
                y=["Coleta AM", "Coleta PM"],
                barmode="group",
                title="Coletas por Período",
                labels={"value": "Quantidade de Sacos", "variable": "Turno"}
            )
            fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig_bar, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.warning("⚠️ Faça o upload do arquivo XLSX para visualizar o dashboard.")

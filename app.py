import streamlit as st
import pandas as pd
import plotly.express as px

# Corrigir a URL para acessar o conteúdo raw do GitHub
url = "https://raw.githubusercontent.com/Rdodosilva/centro/main/Coleta%20centro2.xlsx"

# Tenta carregar o arquivo Excel
try:
    df = pd.read_excel(url)
except Exception as e:
    st.error(f"Erro ao carregar o arquivo: {e}")
    st.stop()

# Exibe os dados para ver se está tudo certo
st.subheader("Pré-visualização dos dados")
st.dataframe(df)

# Verifica colunas esperadas
colunas_esperadas = ["Mês", "Coleta AM", "Coleta PM", "Total de Sacos"]
if not all(col in df.columns for col in colunas_esperadas):
    st.error("As colunas esperadas não foram encontradas no arquivo. Verifique se são: 'Mês', 'Coleta AM', 'Coleta PM', 'Total de Sacos'.")
    st.stop()

# Remove linha "Total" se existir
df = df[df["Mês"] != "Total"]

# Filtro por mês
meses = df["Mês"].unique()
mes_selecionado = st.selectbox("Selecione o mês:", meses)

df_filtrado = df[df["Mês"] == mes_selecionado]

# Métricas
st.subheader("Resumo do Mês")
col1, col2, col3 = st.columns(3)
col1.metric("Coleta AM", int(df_filtrado["Coleta AM"]))
col2.metric("Coleta PM", int(df_filtrado["Coleta PM"]))
col3.metric("Total de Sacos", int(df_filtrado["Total de Sacos"]))

# Gráfico de barras (AM e PM)
df_bar = df_filtrado.melt(id_vars="Mês", value_vars=["Coleta AM", "Coleta PM"])
fig_bar = px.bar(df_bar, x="variable", y="value", color="variable", text_auto=True)
st.plotly_chart(fig_bar)

# Gráfico de linha com todos os meses
st.subheader("Evolução Mensal das Coletas")
fig_line = px.line(df, x="Mês", y=["Coleta AM", "Coleta PM", "Total de Sacos"], markers=True)
st.plotly_chart(fig_line)

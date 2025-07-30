import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Dashboard Coleta", layout="wide")

st.markdown("<h1 style='color: white;'>📊 Dashboard Futurista - Coleta AM/PM</h1>", unsafe_allow_html=True)

# 🧠 Carregamento dos dados
@st.cache_data
def carregar_dados(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)
    df['Mês'] = pd.Categorical(df['Mês'], categories=df['Mês'], ordered=True)
    return df

# 📁 Upload alternativo caso o arquivo não esteja presente
arquivo_padrao = "dados_coleta.xlsx"
if os.path.exists(arquivo_padrao):
    df = carregar_dados(arquivo_padrao)
else:
    st.warning("⚠️ Arquivo 'dados_coleta.xlsx' não encontrado. Faça o upload abaixo:")
    uploaded_file = st.file_uploader("Upload do arquivo Excel com os dados", type=["xlsx"])
    if uploaded_file:
        df = carregar_dados(uploaded_file)
    else:
        st.stop()

# 🎯 Filtros
meses = df['Mês'].unique()
filtro_mes = st.radio("Selecione o mês:", meses, horizontal=True)

df_filtrado = df[df['Mês'] == filtro_mes]

# 🎨 Estilo
st.markdown("""<style>
    .stRadio > div {
        flex-direction: row;
    }
</style>""", unsafe_allow_html=True)

# 📦 Cartões de total
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Coleta AM", int(df_filtrado['Coleta AM'].values[0]))
with col2:
    st.metric("Coleta PM", int(df_filtrado['Coleta PM'].values[0]))
with col3:
    st.metric("Total de Sacos", int(df_filtrado['Total de Sacos'].values[0]))

# 📊 Gráfico de barras animado
fig_bar = px.bar(
    df,
    x="Mês",
    y=["Coleta AM", "Coleta PM"],
    title="Comparativo de Coletas por Mês",
    barmode="group",
    template="plotly_dark",
    color_discrete_sequence=["#AA00FF", "#00BFFF"]
)
st.plotly_chart(fig_bar, use_container_width=True)

# 🍕 Gráfico de pizza
fig_pizza = px.pie(
    df_filtrado,
    values=["Coleta AM", "Coleta PM"],
    names=["Coleta AM", "Coleta PM"],
    title=f"Distribuição AM vs PM - {filtro_mes}",
    template="plotly_dark",
    color_discrete_sequence=["#AA00FF", "#00BFFF"]
)
st.plotly_chart(fig_pizza, use_container_width=True)

# 📈 Gráfico de linha de evolução total
fig_linha = px.line(
    df,
    x="Mês",
    y="Total de Sacos",
    title="📈 Evolução da Quantidade de Sacos por Mês",
    markers=True,
    template="plotly_dark",
    line_shape="spline"
)
fig_linha.update_traces(line=dict(color="white", width=3))
st.plotly_chart(fig_linha, use_container_width=True)

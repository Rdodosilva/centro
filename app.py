import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial do layout
st.set_page_config(page_title="Dashboard Coleta - Centro", layout="wide")

# Estilo escuro e futurista com CSS customizado
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .block-container {
            padding: 2rem;
        }
        .stRadio > div {
            flex-direction: row;
        }
        .css-1cpxqw2 {
            background-color: #1a1a1a !important;
            border: 1px solid #6a0dad !important;
            border-radius: 10px;
        }
        h1, h2, h3, h4 {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Leitura da planilha online
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# Garantir colunas corretas
df.columns = df.columns.str.strip()

# Filtro por Mês
meses = df["Mês"].unique()
mes_selecionado = st.radio("Selecione o mês:", options=meses, horizontal=True)

df_filtrado = df[df["Mês"] == mes_selecionado]

# Título
st.markdown("<h1 style='text-align: center;'>♻️ Coleta - Centro ({} )</h1>".format(mes_selecionado), unsafe_allow_html=True)

# Métricas com texto branco
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Coleta AM", int(df_filtrado["Coleta Am"].sum()))
with col2:
    st.metric("Coleta PM", int(df_filtrado["Coleta PM"].sum()))
with col3:
    st.metric("Total de Sacos", int(df_filtrado["Total de Sacos"].sum()))

# Gráfico de Linhas (AM e PM)
df_grafico = df_filtrado.melt(id_vars=["Mês"], value_vars=["Coleta Am", "Coleta PM"],
                              var_name="Período", value_name="Quantidade")

fig = px.line(df_grafico, x="Mês", y="Quantidade", color="Período",
              markers=True, line_shape="spline", color_discrete_sequence=["#6a0dad", "#00ffff"])

fig.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white",
    title_font_color="white",
    xaxis_title="Mês",
    yaxis_title="Qtd Coletada",
)

st.plotly_chart(fig, use_container_width=True)

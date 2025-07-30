import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração do layout
st.set_page_config(page_title="Dashboard Coleta - Centro", layout="wide")

# Estilo dark com CSS
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
        h1, h2, h3, h4, .stMetric label {
            color: white !important;
        }
        .stMetric {
            background-color: #111111;
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #6a0dad;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Leitura da planilha
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# Corrigir espaços e tipos
df.columns = df.columns.str.strip()
df["Mês"] = df["Mês"].astype(str)

# Filtro por mês
meses = df["Mês"].unique().tolist()
mes_escolhido = st.radio("📅 Selecione o Mês:", options=meses, horizontal=True)

# Filtrar dados
df_filtrado = df[df["Mês"] == mes_escolhido]

# Título
st.markdown(f"<h1 style='text-align: center;'>📊 Coleta - Centro ({mes_escolhido})</h1>", unsafe_allow_html=True)

# Cards com métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Coleta AM", f"{int(df_filtrado['Coleta Am'].sum())} sacos")
with col2:
    st.metric("Coleta PM", f"{int(df_filtrado['Coleta PM'].sum())} sacos")
with col3:
    st.metric("Total de Sacos", f"{int(df_filtrado['Total de Sacos'].sum())} sacos")

# Preparar dados para gráfico
df_grafico = df_filtrado[["Mês", "Coleta Am", "Coleta PM"]].melt(id_vars="Mês", 
                                                                  var_name="Período", 
                                                                  value_name="Quantidade")

# Gráfico de linhas
fig = px.line(
    df_grafico,
    x="Mês",
    y="Quantidade",
    color="Período",
    markers=True,
    line_shape="spline",
    color_discrete_sequence=["#6a0dad", "#00ffff"]
)

fig.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white",
    xaxis_title="Mês",
    yaxis_title="Quantidade de Sacos",
    title_font_color="white",
)

st.plotly_chart(fig, use_container_width=True)

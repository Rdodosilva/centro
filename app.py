import streamlit as st
import pandas as pd
import plotly.express as px

# URL direto para o arquivo .xlsx (modo RAW do GitHub)
url = "https://raw.githubusercontent.com/Rdodosilva/centro/main/Coleta%20centro2.xlsx"

# Lê o arquivo Excel corretamente
df = pd.read_excel(url)

# Remove linha de total (se existir)
df = df[df["Mês"] != "Total"]

# Configurações gerais do layout
st.set_page_config(page_title="Dashboard Coleta Centro", layout="wide")
st.markdown(
    """
    <style>
        body { background-color: #000000; }
        .stApp { background-color: #000000; }
        h1, h2, h3, .stRadio, .stMetric { color: white !important; }
        .css-1v0mbdj p { color: white !important; }
        .stRadio > div { flex-direction: row; }
        .stRadio label { color: white; font-weight: bold; border: 1px solid #6c2dc7; border-radius: 10px; padding: 6px 12px; margin: 5px; }
        .stRadio input:checked + label {
            background-color: #6c2dc7;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título
st.markdown("<h1 style='text-align: center; color:white;'>📊 Dashboard de Coleta - Centro</h1>", unsafe_allow_html=True)
st.markdown("---")

# Filtro por mês
meses = df["Mês"].unique()
mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True)

# Dados filtrados
df_filtrado = df[df["Mês"] == mes_selecionado]

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("🕗 Coleta AM", int(df_filtrado["Coleta AM"]))
col2.metric("🌙 Coleta PM", int(df_filtrado["Coleta PM"]))
col3.metric("🧺 Total de Sacos", int(df_filtrado["Total de Sacos"]))

# Gráfico de barras
fig_bar = px.bar(
    df_filtrado.melt(id_vars=["Mês"], value_vars=["Coleta AM", "Coleta PM"]),
    x="variable",
    y="value",
    color="variable",
    title=f"Distribuição de Coletas - {mes_selecionado}",
    text_auto=True,
    template="plotly_dark",
    color_discrete_sequence=["#6c2dc7", "#b478f1"]
)
fig_bar.update_layout(showlegend=False, title_font_color="white")
fig_bar.update_xaxes(title_text="", color="white")
fig_bar.update_yaxes(color="white")

st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de linha com todos os meses
st.markdown("---")
st.markdown("<h3 style='color:white;'>📈 Evolução Mensal das Coletas</h3>", unsafe_allow_html=True)

fig_line = px.line(
    df,
    x="Mês",
    y=["Coleta AM", "Coleta PM", "Total de Sacos"],
    markers=True,
    template="plotly_dark",
    color_discrete_sequence=["#6c2dc7", "#b478f1", "#ffffff"]
)
fig_line.update_layout(
    title="Tendência de Coletas por Mês",
    xaxis_title="Mês",
    yaxis_title="Quantidade",
    title_font_color="white",
    xaxis=dict(color="white"),
    yaxis=dict(color="white")
)

st.plotly_chart(fig_line, use_container_width=True)

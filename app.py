import pandas as pd
import streamlit as st
import plotly.express as px

# Configurações de página
st.set_page_config(page_title="Dashboard Coleta Centro", page_icon="🚛", layout="wide")

# Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")

# Remover linhas onde não há dados nos sacos
df = df.dropna(subset=["Total de Sacos"])

# Layout principal
st.markdown(
    """
    <h1 style='text-align: center; color: white;'>🚛 Dashboard - Coleta Centro</h1>
    """,
    unsafe_allow_html=True
)

# Métricas
total_sacos = int(df["Total de Sacos"].sum())
peso_total = total_sacos * 20  # Cada saco = 20kg
total_am = int(df["Coleta AM"].sum())
total_pm = int(df["Coleta PM"].sum())

col1, col2, col3 = st.columns(3)

col1.metric("🧺 Total de Sacos", total_sacos)
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

# Dados para gráfico
df_melt = df.melt(id_vars="Mês", value_vars=["Coleta AM", "Coleta PM"],
                  var_name="Periodo", value_name="Quantidade de Sacos")

# Mapear cores
cores = {
    "Coleta AM": "#00BFFF",  # Azul
    "Coleta PM": "#FFA500",  # Laranja
}

# Gráfico interativo
fig = px.bar(
    df_melt,
    x="Mês",
    y="Quantidade de Sacos",
    color="Periodo",
    barmode="group",
    color_discrete_map=cores,
    title="🪣 Coleta de Sacos por Mês e Período"
)

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    title_x=0.5,
    xaxis=dict(
        color='white',
        showgrid=False,
    ),
    yaxis=dict(
        color='white',
        showgrid=False,
    )
)

st.plotly_chart(fig, use_container_width=True)

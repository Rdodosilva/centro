import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Coleta Centro", page_icon="🚛", layout="wide")

# CSS moderno — dark premium + glass effect
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #0F0F0F;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    .stApp {
        background-color: #0F0F0F;
    }

    h1, h2, h3, h4, h5, h6 {
        color: white;
    }

    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 255, 0.4);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(5px);
    }

    .stMetric > div {
        color: white !important;
    }

    .stSelectbox, .stMultiSelect {
        background-color: #1F1F1F !important;
        color: white !important;
    }

    label {
        color: white !important;
    }

    .st-cj, .st-cg {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Carregar dados
df = pd.read_excel("Coleta centro2.xlsx")
df.columns = df.columns.str.strip()
df.rename(columns={"Mês": "Mes"}, inplace=True)
df = df.dropna(subset=["Total de Sacos"])

# Filtro de mês
meses = sorted(df["Mes"].unique().tolist())
meses_selecionados = st.multiselect(
    "🗓️ Selecione os meses para visualizar:",
    options=meses,
    default=meses
)
df_filtrado = df[df["Mes"].isin(meses_selecionados)]

# Cálculo de métricas
total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

# Título
st.markdown(
    "<h1 style='text-align: center; color: white;'>🚛 Dashboard Coleta Centro</h1>",
    unsafe_allow_html=True
)

# Métricas em cards
col1, col2, col3 = st.columns(3)
col1.metric("🧺 Total de Sacos", f"{total_sacos}")
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

# Preparação dos dados para gráficos
df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

# Paleta de cores neon premium
cores = {
    "Coleta AM": "#00FFFF",  # Azul neon
    "Coleta PM": "#FF8C00",  # Laranja neon
}

# Gráfico de Barras
fig_bar = px.bar(
    df_melt,
    x="Mes",
    y="Quantidade de Sacos",
    color="Periodo",
    barmode="group",
    color_discrete_map=cores,
    title="🪣 Coleta de Sacos por Mês e Período"
)

fig_bar.update_layout(
    plot_bgcolor="#0F0F0F",
    paper_bgcolor="#0F0F0F",
    font_color="white",
    title_font=dict(size=22),
    xaxis=dict(color='white', showgrid=False),
    yaxis=dict(color='white', showgrid=False),
    legend=dict(font=dict(color='white')),
    title_x=0.5,
    bargap=0.25
)

# Gráfico de Pizza
fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am, total_pm],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title="🌅 vs 🌇 Coleta AM vs PM"
)

fig_pie.update_traces(
    textinfo='percent+label',
    textfont=dict(color='white', size=16),
    pull=[0.05, 0.05]
)
fig_pie.update_layout(
    plot_bgcolor='#0F0F0F',
    paper_bgcolor='#0F0F0F',
    font_color='white',
    title_x=0.5,
    legend=dict(font=dict(color='white'))
)

# Layout dos gráficos
col4, col5 = st.columns(2)
col4.plotly_chart(fig_bar, use_container_width=True)
col5.plotly_chart(fig_pie, use_container_width=True)

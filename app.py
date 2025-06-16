import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Configuração da página (tem que ser o primeiro comando Streamlit)
st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# ✅ Estilo CSS personalizado
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: white;
    }
    .stSelectbox > div {
        background-color: rgba(128, 0, 128, 0.4); /* Roxo neon transparente */
        color: black !important;
        border-radius: 10px;
        padding: 8px;
    }
    label, .css-17eq0hr {
        color: white !important;
        font-weight: bold;
    }
    .stMetric {
        background-color: #111111;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")

# ✅ Limpeza dos dados
df = df.dropna(subset=["Total de Sacos"])

# ✅ Filtrar apenas os meses com dados
meses_disponiveis = df["Mês"].dropna().unique().tolist()

# ✅ Título
st.markdown("<h1 style='text-align: center;'>🚛 Coleta Centro</h1>", unsafe_allow_html=True)

# ✅ Filtro centralizado
filtro_col1, filtro_col2, filtro_col3 = st.columns([1, 2, 1])
with filtro_col2:
    mes_selecionado = st.selectbox("Selecione o mês", meses_disponiveis)

# ✅ Filtrar dataframe pelo mês
df_filtrado = df[df["Mês"] == mes_selecionado]

# ✅ Métricas
total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20  # 1 saco = 20kg
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

col1, col2, col3 = st.columns(3)

col1.metric("🧺 Total de Sacos", total_sacos)
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

# ✅ Dados para gráfico de barras
df_melt = df_filtrado.melt(
    id_vars="Mês",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Período",
    value_name="Quantidade de Sacos"
)

# ✅ Gráfico de barras
cores = {
    "Coleta AM": "#00FFFF",   # Azul neon
    "Coleta PM": "#FFA500",   # Laranja neon
}

fig_bar = px.bar(
    df_melt,
    x="Mês",
    y="Quantidade de Sacos",
    color="Período",
    barmode="group",
    color_discrete_map=cores,
    title="🪣 Coleta de Sacos por Período"
)

fig_bar.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    title_x=0.5,
)

st.plotly_chart(fig_bar, use_container_width=True)

# ✅ Gráfico de pizza (Distribuição AM vs PM)
fig_pizza = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am, total_pm],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title="Distribuição Geral AM vs PM"
)

fig_pizza.update_traces(textinfo='percent+label')

fig_pizza.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    title_x=0.5,
)

st.plotly_chart(fig_pizza, use_container_width=True)

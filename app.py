import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard Coleta Centro",
    page_icon="🚛",
    layout="wide",
)

# Estilo CSS personalizado para fundo preto total e texto branco
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stApp {
        background-color: black;
    }
    .stMarkdown, .stDataFrame, .stTable, .stMetric {
        color: white !important;
    }
    .css-18ni7ap, .css-1dp5vir, .st-bw, .st-bz {
        background-color: black !important;
        color: white !important;
    }
    .stSelectbox, .stMultiSelect, .stButton, .stSlider {
        background-color: black !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")

# Limpar colunas
df.columns = df.columns.str.strip()
df.rename(columns={"Mês": "Mes"}, inplace=True)

# Remover linhas sem dados
df = df.dropna(subset=["Total de Sacos"])

# ------------------------------
# Filtro de mês
meses_disponiveis = df["Mes"].unique().tolist()

meses_selecionados = st.multiselect(
    "Selecione os meses que deseja visualizar:",
    options=meses_disponiveis,
    default=meses_disponiveis
)

df_filtrado = df[df["Mes"].isin(meses_selecionados)]

# ------------------------------
# Cálculos com dados filtrados
total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20  # Cada saco = 20kg
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

# ------------------------------
# Título
st.markdown(
    """
    <h1 style='text-align: center; color: white;'>
        🚛 Dashboard - Coleta Centro
    </h1>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Métricas
col1, col2, col3 = st.columns(3)

col1.metric("🧺 Total de Sacos", total_sacos)
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

# ------------------------------
# Dados para gráficos
df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

# ------------------------------
# Cores neon
cores = {
    "Coleta AM": "#00FFFF",  # Neon Azul (Ciano)
    "Coleta PM": "#FFA500",  # Neon Laranja
}

# ------------------------------
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
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
    title_x=0.5,
    xaxis=dict(color='white', showgrid=False),
    yaxis=dict(color='white', showgrid=False),
    legend=dict(font=dict(color='white'))
)

# ------------------------------
# Gráfico de Pizza
fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am, total_pm],
    color_discrete_sequence=[cores["Coleta AM"], cores["Coleta PM"]],
    title="🌅 vs 🌇 Coleta AM vs PM"
)

fig_pie.update_traces(
    textinfo='percent+label',
    textfont=dict(color='white', size=14)
)

fig_pie.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_x=0.5,
    legend=dict(font=dict(color='white'))
)

# ------------------------------
# Mostrar os gráficos lado a lado
col_bar, col_pie = st.columns(2)

col_bar.plotly_chart(fig_bar, use_container_width=True)
col_pie.plotly_chart(fig_pie, use_container_width=True)

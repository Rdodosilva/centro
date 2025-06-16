import pandas as pd
import streamlit as st
import plotly.express as px

# 🎯 Configuração da página (TEM QUE SER A PRIMEIRA LINHA)
st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# 🎨 CSS personalizado com roxo neon
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #000000;
            color: white;
        }
        h1, h2, h3, label, span, div {
            color: white !important;
        }
        /* Estilo do selectbox */
        div[data-baseweb="select"] > div {
            background-color: rgba(155, 48, 255, 0.8) !important;  /* roxo neon translúcido */
            border: 2px solid #9b30ff !important;  /* borda roxo neon */
            border-radius: 10px;
        }
        div[data-baseweb="select"] span {
            color: white !important;  /* texto branco no select fechado */
            font-weight: bold;
        }
        label, .stSelectbox label {
            color: white !important;
            font-weight: bold;
        }
        div[role="listbox"] {
            background-color: #9b30ff !important;  /* fundo da lista roxo neon */
            color: black !important;  /* texto preto para contraste */
            font-weight: bold;
            border-radius: 10px;
        }
        div[role="option"]:hover {
            background-color: #d580ff !important; /* roxo mais claro no hover */
            color: black !important;
        }
        div[role="option"][aria-selected="true"] {
            background-color: #d580ff !important;
            color: black !important;
        }
        /* Estilo para métricas */
        .stMetric {
            background-color: #111111;
            border: 1px solid #9b30ff;
            border-radius: 12px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 📥 Carregar dados
df = pd.read_excel("Coleta centro2.xlsx")
df.columns = df.columns.str.strip()

# 🗓️ Normalizar meses
df["Mes"] = df["Mês"].astype(str).str.lower().str.strip()

# 🟣 Lista oficial de meses para ordenar e validar
meses_ordem = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
]

# Filtrar meses com dados válidos (Total de Sacos preenchido)
meses_com_dados = df.loc[df["Total de Sacos"].notna(), "Mes"].unique()

# Filtrar só meses válidos e ordenar
meses_disponiveis = [m for m in meses_ordem if m in meses_com_dados]

# 🏷️ Título
st.markdown("<h1 style='text-align:center; font-size: 3em;'>🚛 Coleta Centro</h1>", unsafe_allow_html=True)

# 🎛️ Filtro de mês centralizado
st.markdown("<h2 style='text-align:center;'>📅 Selecione o mês:</h2>", unsafe_allow_html=True)
filtro_col1, filtro_col2, filtro_col3 = st.columns([1, 2, 1])
with filtro_col2:
    mes_selecionado = st.selectbox(
        "",
        meses_disponiveis,
        format_func=lambda x: x.capitalize()
    )

# 📑 Filtrar dados para o mês selecionado
df_filtrado = df[(df["Mes"] == mes_selecionado) & (df["Total de Sacos"].notna())]

# 📊 Calcular métricas
total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

# 📈 Totais gerais para pizza
total_am_geral = int(df["Coleta AM"].sum())
total_pm_geral = int(df["Coleta PM"].sum())

# 🎯 Exibir métricas
col1, col2, col3 = st.columns(3)
col1.metric("🧺 Total de Sacos", f"{total_sacos}")
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

# 🔧 Dados para gráfico de barras
df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

# 🎨 Cores
cores = {
    "Coleta AM": "#00FFFF",  # Azul neon
    "Coleta PM": "#FFA500"   # Laranja neon
}

# 📊 Gráfico de barras
fig_bar = px.bar(
    df_melt,
    x="Mes",
    y="Quantidade de Sacos",
    color="Periodo",
    color_discrete_map=cores,
    barmode="group",
    title="📦 Quantidade de Sacos por Período"
)
fig_bar.update_traces(
    hovertemplate='%{y} sacos - %{color}',
    marker_line_color='white',
    marker_line_width=1.5,
    opacity=0.9
)
fig_bar.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white",
    title_font=dict(size=22),
    title_x=0.5,
    xaxis=dict(title="Mês", color="white", showgrid=False, tickfont=dict(color="white")),
    yaxis=dict(title="Quantidade de Sacos", color="white", showgrid=False, tickfont=dict(color="white")),
    legend=dict(
        title="Período",
        font=dict(color="white", size=14),
        bgcolor="#000000"
    ),
    bargap=0.2,
    bargroupgap=0.1
)

# 🥧 Gráfico de pizza
fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am_geral, total_pm_geral],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title="🔄 Distribuição Geral AM vs PM"
)
fig_pie.update_traces(
    textfont=dict(color='white', size=14),
    textinfo='label+percent+value',
    pull=[0.05, 0],
    marker=dict(line=dict(color='white', width=2)),
    hoverinfo='label+percent+value'
)
fig_pie.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white",
    title_font=dict(size=22),
    title_x=0.5,
    legend=dict(
        font=dict(color="white", size=14),
        bgcolor="#000000"
    )
)

# 📊 Mostrar gráficos lado a lado
col4, col5 = st.columns(2)
col4.plotly_chart(fig_bar, use_container_width=True)
col5.plotly_chart(fig_pie, use_container_width=True)

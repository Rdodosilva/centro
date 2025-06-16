import pandas as pd
import streamlit as st
import plotly.express as px

# ⚙️ Configuração da página
st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# 🎨 Estilo visual aprimorado
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #000000;
            color: white;
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: white !important;
        }
        .stSelectbox > div {
            background-color: #111111 !important;
            border: 1px solid #00FFFF;
            padding: 8px;
            border-radius: 10px;
        }
        .stSelectbox label {
            font-weight: bold;
            color: #00FFFF !important;
        }
        .stMetric {
            background-color: #111111;
            border: 1px solid #00FFFF;
            border-radius: 12px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 📥 Carregar dados
df = pd.read_excel("Coleta centro2.xlsx")
df.columns = df.columns.str.strip()
df.rename(columns={"Mês": "Mes"}, inplace=True)
df = df.dropna(subset=["Total de Sacos"])

# 🎯 Filtro: mostrar apenas meses com dados
meses_disponiveis = sorted(df["Mes"].dropna().unique())

# 🧠 Filtro centralizado
st.markdown("<h2 style='text-align:center;'>📅 Selecione o mês:</h2>", unsafe_allow_html=True)
mes_selecionado = st.selectbox("", meses_disponiveis, index=0)

# 🔍 Filtrar dados do mês selecionado
df_filtrado = df[df["Mes"] == mes_selecionado]

# 📊 Totais
total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

# 📈 Totais gerais para Pizza
total_am_geral = int(df["Coleta AM"].sum())
total_pm_geral = int(df["Coleta PM"].sum())

# 🚛 Título
st.markdown("<h1 style='text-align: center; font-size: 3em;'>🚛 Coleta - Centro</h1>", unsafe_allow_html=True)

# 🔢 Métricas
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

# 🎨 Cores neon
cores = {
    "Coleta AM": "#00FFFF",  # Azul neon
    "Coleta PM": "#FFA500"   # Laranja neon
}

# 📊 Gráfico de Barras com animação (hover, realce)
fig_bar = px.bar(
    df_melt,
    x="Mes",
    y="Quantidade de Sacos",
    color="Periodo",
    color_discrete_map=cores,
    barmode="group",
    title="📦 Quantidade de Sacos por Período",
    animation_frame=None
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

# 🥧 Gráfico de Pizza com animação ao passar o mouse
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

# 🎯 Mostrar gráficos lado a lado
col4, col5 = st.columns(2)
col4.plotly_chart(fig_bar, use_container_width=True)
col5.plotly_chart(fig_pie, use_container_width=True)

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# CSS total para fundo preto puro e texto branco puro, filtro totalmente preto com letras brancas
st.markdown("""
<style>
    /* Fundo geral preto sólido */
    html, body, .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    /* Textos e títulos brancos puros */
    h1, h2, h3, label, span, div, p {
        color: #FFFFFF !important;
    }
    /* Estilo do selectbox (filtro) */
    div.stSelectbox > div[role="combobox"] {
        background-color: #000000 !important;
        border: 2px solid #00FFFF !important; /* azul neon */
        border-radius: 8px !important;
        padding: 6px 12px !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    div.stSelectbox > div[role="combobox"] > div {
        color: #FFFFFF !important;
    }
    div[role="listbox"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    div[role="option"]:hover {
        background-color: #00FFFF !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }
    div[role="option"][aria-selected="true"] {
        background-color: #00FFFF !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }
    /* Métricas fundo escuro com borda azul neon */
    div[data-testid="metric-container"] {
        background-color: #111111 !important;
        border: 2px solid #00FFFF !important;
        border-radius: 12px !important;
        padding: 15px !important;
        color: #FFFFFF !important;
    }
    /* Ajusta cor de textos dentro das métricas */
    div[data-testid="metric-container"] > div > div {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")
df.columns = df.columns.str.strip()
df["Mes"] = df["Mês"].str.lower()

# Meses fixos para filtro
meses_filtro = ["janeiro", "fevereiro", "março", "abril", "maio"]

# Título principal
st.markdown("<h1 style='text-align:center; font-size: 3em;'>🚛 Coleta Centro</h1>", unsafe_allow_html=True)

# Filtro centralizado e estilizado
st.markdown("<h2 style='text-align:center;'>📅 Selecione o mês:</h2>", unsafe_allow_html=True)
mes_selecionado = st.selectbox(
    "",
    meses_filtro,
    index=0,
    format_func=lambda x: x.capitalize()
)

# Filtra dados do mês selecionado
df_filtrado = df[(df["Mes"] == mes_selecionado) & (df["Total de Sacos"].notna())]

# Métricas
total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

# Totais gerais para gráfico pizza
total_am_geral = int(df["Coleta AM"].sum())
total_pm_geral = int(df["Coleta PM"].sum())

# Métricas alinhadas
col1, col2, col3 = st.columns(3)
col1.metric("🧺 Total de Sacos", f"{total_sacos}")
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

# Preparar dados para gráfico de barras
df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

cores = {
    "Coleta AM": "#00FFFF",  # azul neon
    "Coleta PM": "#FFA500"   # laranja neon
}

# Gráfico de barras
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
    font_color="#FFFFFF",
    title_font=dict(size=22),
    title_x=0.5,
    xaxis=dict(title="Mês", color="#FFFFFF", showgrid=False, tickfont=dict(color="#FFFFFF")),
    yaxis=dict(title="Quantidade de Sacos", color="#FFFFFF", showgrid=False, tickfont=dict(color="#FFFFFF")),
    legend=dict(
        title="Período",
        font=dict(color="#FFFFFF", size=14),
        bgcolor="#000000"
    ),
    bargap=0.2,
    bargroupgap=0.1
)

# Gráfico de pizza AM vs PM geral
fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am_geral, total_pm_geral],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title="🔄 Distribuição Geral AM vs PM"
)
fig_pie.update_traces(
    textfont=dict(color='#FFFFFF', size=14),
    textinfo='label+percent+value',
    pull=[0.05, 0],
    marker=dict(line=dict(color='#FFFFFF', width=2)),
    hoverinfo='label+percent+value'
)
fig_pie.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="#FFFFFF",
    title_font=dict(size=22),
    title_x=0.5,
    legend=dict(
        font=dict(color="#FFFFFF", size=14),
        bgcolor="#000000"
    )
)

# Mostrar gráficos lado a lado
col4, col5 = st.columns(2)
col4.plotly_chart(fig_bar, use_container_width=True)
col5.plotly_chart(fig_pie, use_container_width=True)

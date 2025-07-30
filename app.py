import pandas as pd
import streamlit as st
import plotly.express as px

# 🎯 Configuração da página
st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# 🎨 CSS personalizado
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #000000;
            color: white;
        }
        h1, h2, h3, label, span, div {
            color: white !important;
        }
        /* 🎨 Radio estilizado como dropdown neon */
        section[data-testid="stRadio"] > div {
            background-color: rgba(155, 48, 255, 0.15);
            border: 2px solid #9b30ff;
            border-radius: 10px;
            padding: 8px;
        }
        label[data-testid="stMarkdownContainer"] {
            color: white;
            font-weight: bold;
        }
        div[role="radiogroup"] > label {
            background-color: rgba(0,0,0,0.6);
            padding: 5px 10px;
            border-radius: 8px;
            border: 1px solid #9b30ff;
            margin-right: 8px;
        }
        div[role="radiogroup"] > label:hover {
            background-color: #9b30ff;
            color: black;
        }
        div[role="radiogroup"] > label[data-selected="true"] {
            background-color: #9b30ff;
            color: black;
            font-weight: bold;
        }
        /* 🎯 Estilo para métricas */
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

# 🗓️ Normalizar meses
df["Mes"] = df["Mês"].str.lower().str.strip()

# 🔍 Definir meses disponíveis
meses_disponiveis = ["janeiro", "fevereiro", "março", "abril", "maio"]

# 🏷️ Título
st.markdown("<h1 style='text-align:center; font-size: 3em;'>🚛 Coleta Centro</h1>", unsafe_allow_html=True)

# 🎛️ Filtro de mês (dropdown radio estilizado)
st.markdown("<h2 style='text-align:center;'>📅 Selecione o mês:</h2>", unsafe_allow_html=True)
filtro_col1, filtro_col2, filtro_col3 = st.columns([1, 2, 1])
with filtro_col2:
    mes_selecionado = st.radio(
        "",
        meses_disponiveis,
        horizontal=True,
        index=0,
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
    textinfo='label+percent+value',
    pull=[0.05, 0],
    marker=dict(line=dict(color='white', width=2)),
    textfont=dict(color='white', size=14),
    hovertemplate='%{label}: %{value} kg (%{percent})<extra></extra>'
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

# 📈 NOVO: Gráfico de linha com evolução mensal
df_linha = df[df["Total de Sacos"].notna()]
df_linha["Mes"] = pd.Categorical(df_linha["Mes"], categories=meses_disponiveis, ordered=True)

fig_linha = px.line(
    df_linha.sort_values("Mes"),
    x="Mes",
    y="Total de Sacos",
    markers=True,
    title="📈 Evolução da Quantidade de Sacos Coletados por Mês"
)
fig_linha.update_traces(line_color="#9b30ff", marker=dict(color='white', size=8))
fig_linha.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white",
    title_font=dict(size=22),
    title_x=0.5,
    xaxis=dict(color="white", showgrid=False),
    yaxis=dict(color="white", showgrid=False)
)

# 📉 Mostrar gráfico de linha abaixo
st.plotly_chart(fig_linha, use_container_width=True)

import pandas as pd
import streamlit as st
import plotly.express as px

# 🔧 Configuração da página
st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# 🎨 Estilo visual aprimorado: fundo preto, textos brancos e detalhes legíveis
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .stApp {
            background-color: #000000;
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: white !important;
        }
        .stSelectbox div, .stSelectbox label {
            background-color: #111111 !important;
            color: white !important;
        }
        .stMetric {
            background-color: #111111;
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 12px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 🚚 Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")
df.columns = df.columns.str.strip()  # Limpar espaços
df.rename(columns={"Mês": "Mes"}, inplace=True)

# 🔍 Remover linhas sem dados nos sacos
df = df.dropna(subset=["Total de Sacos"])

# 📅 Gerar lista de meses que têm dados
meses_com_dados = sorted(df["Mes"].dropna().unique())

# 🏷️ Título
st.markdown("<h1 style='text-align: center;'>🚛 Coleta - Centro</h1>", unsafe_allow_html=True)

# 🎯 Filtro de mês (Dropdown com meses válidos)
mes_selecionado = st.selectbox("📅 Selecione o mês:", meses_com_dados)

# 🔍 Dados filtrados para o mês
df_filtrado = df[df["Mes"] == mes_selecionado]

# 📊 Dados gerais (para o gráfico de pizza)
total_am_geral = int(df["Coleta AM"].sum())
total_pm_geral = int(df["Coleta PM"].sum())

# 📈 Métricas do mês selecionado
total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20  # Cada saco = 20kg
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

col1, col2, col3 = st.columns(3)
col1.metric("🧺 Total de Sacos", f"{total_sacos}")
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

# 🔧 Dados para o gráfico de barras
df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

# 🎨 Definir cores neon
cores = {
    "Coleta AM": "#00FFFF",  # Azul neon
    "Coleta PM": "#FFA500"   # Laranja neon
}

# 📊 Gráfico de Barras
fig_bar = px.bar(
    df_melt,
    x="Mes",
    y="Quantidade de Sacos",
    color="Periodo",
    color_discrete_map=cores,
    barmode="group",
    title="📊 Coleta por Período (Mês Selecionado)"
)
fig_bar.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white",
    title_x=0.5,
    xaxis=dict(title="Mês", color="white", showgrid=False),
    yaxis=dict(title="Quantidade de Sacos", color="white", showgrid=False),
    legend=dict(
        title="Período",
        font=dict(color="white"),
        bgcolor="#000000",
        bordercolor="#FFFFFF"
    )
)

# 🥧 Gráfico de Pizza com total geral (AM vs PM)
fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am_geral, total_pm_geral],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title="🧭 Distribuição Geral AM vs PM"
)
fig_pie.update_traces(
    textfont=dict(color='white'),
    textinfo='label+percent+value'
)
fig_pie.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white",
    title_x=0.5,
    legend=dict(
        font=dict(color="white"),
        bgcolor="#000000",
        bordercolor="#FFFFFF"
    )
)

# 🔥 Layout dos Gráficos
col4, col5 = st.columns(2)
col4.plotly_chart(fig_bar, use_container_width=True)
col5.plotly_chart(fig_pie, use_container_width=True)

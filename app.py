import pandas as pd
import streamlit as st
import plotly.express as px

# Configurações de página com tema escuro
st.set_page_config(page_title="Dashboard Coleta Centro", page_icon="🚛", layout="wide")

# Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")

# Limpar nomes de colunas
df.columns = df.columns.str.strip()

# Renomear colunas para evitar acentos (se necessário)
df.rename(columns={"Mês": "Mes"}, inplace=True)

# Remover linhas sem dados em 'Total de Sacos'
df = df.dropna(subset=["Total de Sacos"])

# --- Não exibir colunas para o usuário (comentado) ---
# st.write("Colunas originais:", df.columns.tolist())
# st.write("Colunas após limpeza:", df.columns.tolist())

# Layout principal com título estilizado (branco)
st.markdown(
    """
    <h1 style='text-align: center; color: white; font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;'>
        🚛 Dashboard - Coleta Centro
    </h1>
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

# Dados para gráfico de barras
df_melt = df.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

# Cores neon
cores = {
    "Coleta AM": "#00FFFF",  # Neon Azul claro (ciano)
    "Coleta PM": "#FFA500",  # Neon Laranja
}

# Gráfico de barras com tema escuro e neon
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
    xaxis=dict(
        color='white',
        showgrid=False,
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        color='white',
        showgrid=False,
        tickfont=dict(color='white')
    ),
    legend=dict(
        font=dict(color='white')
    )
)

# Gráfico de pizza AM vs PM
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
    legend=dict(
        font=dict(color='white')
    )
)

# Exibir gráficos lado a lado
col_bar, col_pie = st.columns(2)

col_bar.plotly_chart(fig_bar, use_container_width=True)
col_pie.plotly_chart(fig_pie, use_container_width=True)

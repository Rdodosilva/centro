import pandas as pd
import streamlit as st
import plotly.express as px

# Configurações de página
st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# CSS customizado para tema escuro e filtro estilizado
st.markdown("""
<style>
/* Fundo e texto gerais */
body, .block-container {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Métricas: texto branco */
[data-testid="metric-container"] {
    color: #FFFFFF !important;
}

/* Título centralizado e branco */
h1 {
    color: #FFFFFF !important;
    text-align: center;
    font-weight: 800;
}

/* Estilo filtro meses */
div.stSelectbox > div[role="combobox"] {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 2px solid #00BFFF !important;  /* azul neon */
    border-radius: 8px !important;
    padding: 6px 12px !important;
    font-weight: 600 !important;
    width: 250px !important;
    margin: auto;
}

/* Texto dentro do filtro */
div.stSelectbox > div[role="combobox"] > div {
    color: #FFFFFF !important;
}

/* Fundo e texto na lista suspensa */
div[role="listbox"] {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}

/* Hover azul neon com texto preto */
div[role="option"]:hover {
    background-color: #00BFFF !important;
    color: #000000 !important;
    font-weight: 700 !important;
}

/* Seleção azul neon com texto preto */
div[role="option"][aria-selected="true"] {
    background-color: #00BFFF !important;
    color: #000000 !important;
    font-weight: 700 !important;
}

/* Legendas do gráfico - texto branco */
.legendtext, .legendtitle {
    color: #FFFFFF !important;
}

/* Tooltip texto branco */
[role="tooltip"] {
    color: #FFFFFF !important;
    background-color: #222222 !important;
    border: 1px solid #00BFFF !important;
}

/* Scrollbar para o filtro, se houver */
div[role="listbox"]::-webkit-scrollbar {
    width: 8px;
}
div[role="listbox"]::-webkit-scrollbar-thumb {
    background-color: #00BFFF;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")

# Remover linhas sem dados em "Total de Sacos"
df = df.dropna(subset=["Total de Sacos"])

# Título do app
st.markdown("<h1>Coleta Centro 🚛</h1>", unsafe_allow_html=True)

# Meses fixos e só os que tem dados no DF
meses_possiveis = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"]
meses_com_dados = [mes for mes in meses_possiveis if mes in df["Mês"].dropna().unique()]

# Filtro de meses centralizado e estilizado
mes_selecionado = st.selectbox(
    "Selecione o mês",
    options=meses_com_dados,
    index=0
)

# Filtrar dados pelo mês selecionado
df_mes = df[df["Mês"] == mes_selecionado]

# Cálculos métricas
total_sacos = int(df_mes["Total de Sacos"].sum())
peso_total = total_sacos * 20  # Cada saco 20kg
total_am = int(df_mes["Coleta AM"].sum())
total_pm = int(df_mes["Coleta PM"].sum())

# Exibir métricas em 3 colunas
col1, col2, col3 = st.columns(3)
col1.metric("🧺 Total de Sacos", f"{total_sacos}")
col2.metric("⚖️ Peso Total (kg)", f"{peso_total}")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} / {total_pm}")

# Preparar dados para gráfico de barras
df_melt = df_mes.melt(id_vars="Mês", value_vars=["Coleta AM", "Coleta PM"],
                      var_name="Período", value_name="Quantidade de Sacos")

cores = {
    "Coleta AM": "#00BFFF",  # Azul neon
    "Coleta PM": "#FFA500",  # Laranja neon
}

# Gráfico de barras interativo
fig_bar = px.bar(
    df_melt,
    x="Mês",
    y="Quantidade de Sacos",
    color="Período",
    barmode="group",
    color_discrete_map=cores,
    title=f"🪣 Coleta de Sacos - {mes_selecionado}"
)

fig_bar.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
    title_x=0.5,
    legend_title_font_color="white",
    legend_font_color="white",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de pizza AM vs PM no mês selecionado
fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am, total_pm],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title=f"🌅 vs 🌇 Distribuição - {mes_selecionado}",
    hole=0.4
)

fig_pie.update_traces(textinfo='percent+label', textfont_color='white')
fig_pie.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
    title_x=0.5,
    legend_title_font_color="white",
    legend_font_color="white",
)

st.plotly_chart(fig_pie, use_container_width=True)

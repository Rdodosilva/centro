import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Configuração da página — TEM QUE SER A PRIMEIRA CHAMADA DO STREAMLIT
st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# ✅ CSS personalizado
st.markdown("""
<style>
/* Fundo geral preto e texto branco */
body, .block-container {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Métricas */
[data-testid="metric-container"] {
    color: #FFFFFF !important;
}

/* Título */
h1 {
    color: #FFFFFF !important;
    text-align: center;
    font-weight: 800;
}

/* Filtro dos meses com fundo roxo neon transparente e texto preto */
div.stSelectbox > div[role="combobox"] {
    background-color: rgba(128, 0, 128, 0.7) !important;
    color: black !important;
    border: 2px solid #8A2BE2 !important;
    border-radius: 8px !important;
    padding: 6px 12px !important;
    font-weight: 600 !important;
    width: 250px !important;
    margin: auto;
}

/* Texto dentro do filtro */
div.stSelectbox > div[role="combobox"] > div {
    color: black !important;
}

/* Lista suspensa */
div[role="listbox"] {
    background-color: rgba(128, 0, 128, 0.7) !important;
    color: black !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}

/* Hover */
div[role="option"]:hover {
    background-color: #8A2BE2 !important;
    color: white !important;
    font-weight: 700 !important;
}

/* Seleção */
div[role="option"][aria-selected="true"] {
    background-color: #8A2BE2 !important;
    color: white !important;
    font-weight: 700 !important;
}

/* Scrollbar */
div[role="listbox"]::-webkit-scrollbar {
    width: 8px;
}
div[role="listbox"]::-webkit-scrollbar-thumb {
    background-color: #8A2BE2;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ✅ Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")

# ✅ Definir a coluna dos meses corretamente
col_mes = "Mês"

# ✅ Limpar dados
df = df.dropna(subset=["Total de Sacos"])

# ✅ Título
st.markdown("<h1>Coleta Centro 🚛</h1>", unsafe_allow_html=True)

# ✅ Filtro de meses — apenas os que têm dados
meses_possiveis = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"]
meses_com_dados = [mes for mes in meses_possiveis if mes in df[col_mes].dropna().unique()]

mes_selecionado = st.selectbox(
    "Selecione o mês",
    options=meses_com_dados,
    index=0
)

# ✅ Filtrar dados pelo mês selecionado
df_mes = df[df[col_mes] == mes_selecionado]

# ✅ Métricas
total_sacos = int(df_mes["Total de Sacos"].sum())
peso_total = total_sacos * 20  # Cada saco = 20kg
total_am = int(df_mes["Coleta AM"].sum())
total_pm = int(df_mes["Coleta PM"].sum())

col1, col2, col3 = st.columns(3)
col1.metric("🧺 Total de Sacos", f"{total_sacos}")
col2.metric("⚖️ Peso Total (kg)", f"{peso_total}")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} / {total_pm}")

# ✅ Dados para gráfico de barras
df_melt = df_mes.melt(id_vars=col_mes, value_vars=["Coleta AM", "Coleta PM"],
                      var_name="Período", value_name="Quantidade de Sacos")

cores = {
    "Coleta AM": "#00BFFF",  # Azul neon
    "Coleta PM": "#FFA500",  # Laranja neon
}

# ✅ Gráfico de barras
fig_bar = px.bar(
    df_melt,
    x=col_mes,
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

# ✅ Gráfico de pizza AM vs PM
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

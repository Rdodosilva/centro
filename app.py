import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# CSS personalizado
st.markdown("""
    <style>
    body { background-color: #000000; color: white; }
    .stSelectbox > div {
        background-color: rgba(128, 0, 128, 0.4);
        color: black !important;
        border-radius: 10px;
        padding: 8px;
    }
    label, .css-17eq0hr {
        color: white !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")
df.columns = df.columns.str.strip()  # Remove espaços

# ✅ Verificar colunas
st.write("Colunas disponíveis:", df.columns.tolist())

# ✅ Checar se coluna "Mês" existe
if "Mês" not in df.columns:
    st.error("🚨 A coluna 'Mês' não foi encontrada. Verifique o nome no arquivo Excel.")
    st.stop()

# ✅ Filtrar meses disponíveis
meses_disponiveis = df["Mês"].dropna().unique().tolist()

# ✅ Filtro central
filtro_col1, filtro_col2, filtro_col3 = st.columns([1, 2, 1])
with filtro_col2:
    mes_selecionado = st.selectbox("Selecione o mês", meses_disponiveis)

# ✅ Filtrar dataframe
df_filtrado = df[df["Mês"] == mes_selecionado]

# ✅ Métricas
total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

col1, col2, col3 = st.columns(3)

col1.metric("🧺 Total de Sacos", total_sacos)
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

# ✅ Gráfico de barras
cores = {
    "Coleta AM": "#00FFFF",
    "Coleta PM": "#FFA500",
}

df_melt = df_filtrado.melt(
    id_vars="Mês",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Período",
    value_name="Quantidade de Sacos"
)

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

# ✅ Gráfico de pizza
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

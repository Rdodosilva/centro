import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard Coleta", page_icon="🧹")

# Estilo visual dark total (tema preto e letras brancas)
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .stApp {
            background-color: #000000;
        }
        .block-container {
            padding-top: 1rem;
        }
        .css-1v0mbdj p, .css-1v0mbdj h1, .css-1v0mbdj h2, .css-1v0mbdj h3 {
            color: white !important;
        }
        .css-18e3th9 {
            background-color: #000000;
        }
        .css-1v0mbdj {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("📊 Dashboard de Coleta - Centro")
st.markdown("---")

# Carregando os dados
df = pd.read_excel("Coleta centro2.xlsx")

# Garantir que o nome da coluna está correto (corrigindo espaços)
df.columns = df.columns.str.strip()
df['Mês'] = df['Mês'].astype(str)

# Filtro por mês
meses_disponiveis = df['Mês'].unique().tolist()
mes_selecionado = st.selectbox("🗓️ Selecione o Mês", options=meses_disponiveis)

df_filtrado = df[df['Mês'] == mes_selecionado]

# Cartões de total
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🧺 Coleta AM", int(df_filtrado["Coleta AM"].sum()))

with col2:
    st.metric("🌙 Coleta PM", int(df_filtrado["Coleta PM"].sum()))

with col3:
    st.metric("🧮 Total de Sacos", int(df_filtrado["Total de Sacos"].sum()))

st.markdown("")

# Gráfico de barras
fig_bar = px.bar(
    df_filtrado.melt(id_vars="Mês", value_vars=["Coleta AM", "Coleta PM"]),
    x="variable",
    y="value",
    color="variable",
    text="value",
    color_discrete_sequence=["#00C9A7", "#FF6B6B"],
    title="Comparativo: AM x PM",
    labels={"variable": "Período", "value": "Quantidade"}
)
fig_bar.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white",
    title_font_color="white"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de pizza
fig_pie = px.pie(
    df_filtrado.melt(id_vars="Mês", value_vars=["Coleta AM", "Coleta PM"]),
    names="variable",
    values="value",
    color_discrete_sequence=["#00C9A7", "#FF6B6B"],
    title="Distribuição de Sacos Coletados"
)
fig_pie.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white",
    title_font_color="white"
)
st.plotly_chart(fig_pie, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("<center><sub>Desenvolvido por Rodrigo • 2025</sub></center>", unsafe_allow_html=True)

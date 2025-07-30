import streamlit as st
import pandas as pd
import plotly.express as px

# ---- CONFIGURAÇÃO DA PÁGINA ----
st.set_page_config(layout="wide", page_title="Dashboard de Coleta - Centro", page_icon="📊")

# ---- ESTILO PERSONALIZADO ----
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .css-1v0mbdj p, .css-1v0mbdj h1, .css-1v0mbdj h2, .css-1v0mbdj h3 {
            color: white !important;
        }
        .stMetric {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 1rem;
            box-shadow: 0 0 15px #6a00ff33;
            transition: 0.3s;
        }
        .stMetric:hover {
            transform: scale(1.03);
            box-shadow: 0 0 25px #6a00ffaa;
        }
        .css-1n76uvr, .stRadio > div {
            border: 2px solid #6a00ff;
            border-radius: 10px;
            padding: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---- LEITURA DE DADOS ----
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# ---- GARANTIR QUE NOMES DAS COLUNAS ESTÃO CORRETOS ----
df.columns = df.columns.str.strip()  # Remove espaços
colunas_esperadas = ['Mês', 'Coleta Am', 'Coleta PM', 'Total de Sacos']
if not all(col in df.columns for col in colunas_esperadas):
    st.error("Erro: A planilha não possui as colunas esperadas.")
    st.stop()

# ---- FILTRO DE MÊS ----
meses = df['Mês'].dropna().unique()
mes_selecionado = st.radio("Selecione o mês", sorted(meses), horizontal=True)

df_filtrado = df[df['Mês'] == mes_selecionado]

# ---- CÁLCULOS ----
total_am = int(df_filtrado['Coleta Am'].sum())
total_pm = int(df_filtrado['Coleta PM'].sum())
total_sacos = int(df_filtrado['Total de Sacos'].sum())

# ---- LAYOUT DE MÉTRICAS ----
col1, col2, col3 = st.columns(3)
col1.metric("Coleta AM", f"{total_am} sacos")
col2.metric("Coleta PM", f"{total_pm} sacos")
col3.metric("Total de Sacos", f"{total_sacos} sacos")

# ---- GRÁFICO DE LINHA ----
fig = px.line(df, x='Mês', y=['Coleta Am', 'Coleta PM'], markers=True,
              title="Coleta AM vs PM por Mês", template='plotly_dark')
fig.update_layout(title_font_color="white", legend_title_text="Turno", font=dict(color="white"))

st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# CSS futurista com contorno nas métricas
st.markdown("""
    <style>
    body {background-color: #000000;}
    .metric-box {
        border: 2px solid #8000FF;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #111111;
        color: white;
        text-align: center;
        animation: pulse 1.5s infinite;
    }
    .metric-value {
        font-size: 30px;
        font-weight: bold;
        color: white;
    }
    .metric-label {
        font-size: 16px;
        color: white;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 5px #8000FF; }
        50% { box-shadow: 0 0 20px #8000FF; }
        100% { box-shadow: 0 0 5px #8000FF; }
    }
    </style>
""", unsafe_allow_html=True)

# Carregar planilha do GitHub
url = "https://raw.githubusercontent.com/Rdodosilva/coleta/main/coleta_centro.csv"
df = pd.read_csv(url)

# Corrigir nomes das colunas
df.columns = df.columns.str.strip()

# Verificar colunas obrigatórias
colunas_esperadas = {"Mês", "Coleta Am", "Coleta PM", "Total de Sacos"}
if not colunas_esperadas.issubset(set(df.columns)):
    st.error("Erro: A planilha não possui as colunas esperadas.")
    st.write("Colunas encontradas:", df.columns.tolist())
    st.stop()

# Filtro por mês
meses = df["Mês"].unique()
mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True)

df_filtrado = df[df["Mês"] == mes_selecionado]

# Cálculos
total_sacos = int(df_filtrado["Total de Sacos"].sum())
total_am = int(df_filtrado["Coleta Am"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

# Métricas com animação e contorno
st.markdown(f"""
<div class='metric-box'>
    <div class='metric-label'>Total de Sacos</div>
    <div class='metric-value'>{total_sacos} sacos</div>
</div>
<div class='metric-box'>
    <div class='metric-label'>Coleta AM</div>
    <div class='metric-value'>{total_am} sacos</div>
</div>
<div class='metric-box'>
    <div class='metric-label'>Coleta PM</div>
    <div class='metric-value'>{total_pm} sacos</div>
</div>
""", unsafe_allow_html=True)

# Gráfico de linhas (AM/PM)
fig = px.line(df_filtrado, x="Mês", y=["Coleta Am", "Coleta PM"],
              markers=True,
              labels={"value": "Quantidade", "variable": "Turno"},
              title="Evolução da Coleta por Turno")

fig.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font=dict(color="white"),
    legend=dict(bgcolor="black"),
    title_font=dict(size=18, color="white")
)

st.plotly_chart(fig, use_container_width=True)

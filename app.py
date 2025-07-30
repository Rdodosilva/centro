import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurações da página
st.set_page_config(page_title="Coleta Centro", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .metric-container {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-top: 20px;
        }
        .card {
            background-color: #1a1a1a;
            border: 2px solid #6A0DAD;
            border-radius: 15px;
            padding: 25px;
            flex: 1;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px #6A0DAD;
        }
        .card-title {
            font-size: 20px;
            color: #cccccc;
            margin-bottom: 10px;
        }
        .card-value {
            font-size: 36px;
            font-weight: bold;
            color: white;
        }
        .filtro {
            color: white;
            font-size: 18px;
        }
        .stRadio > label {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Carregando a planilha
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# Garantir que os nomes das colunas estejam como esperado
df.columns = [col.strip() for col in df.columns]

# Filtro de mês
meses = df["Mês"].dropna().unique().tolist()
mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True)

# Filtrar os dados pelo mês
df_filtrado = df[df["Mês"] == mes_selecionado]

# Métricas principais
total_am = int(df_filtrado["Coleta Am"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())
total_geral = int(df_filtrado["Total de Sacos"].sum())

# Cards animados
st.markdown('<div class="metric-container">', unsafe_allow_html=True)

st.markdown(f"""
    <div class="card">
        <div class="card-title">Total de Sacos</div>
        <div class="card-value">{total_geral} sacos</div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="card">
        <div class="card-title">Coleta AM</div>
        <div class="card-value">{total_am} sacos</div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="card">
        <div class="card-title">Coleta PM</div>
        <div class="card-value">{total_pm} sacos</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Gráfico interativo
fig = go.Figure()
fig.add_trace(go.Bar(
    x=["Coleta AM", "Coleta PM"],
    y=[total_am, total_pm],
    marker_color=["#6A0DAD", "#9A32CD"]
))
fig.update_layout(
    paper_bgcolor="#000000",
    plot_bgcolor="#000000",
    font=dict(color="white", size=14),
    title=f"Distribuição de Coletas - {mes_selecionado}"
)

st.plotly_chart(fig, use_container_width=True)

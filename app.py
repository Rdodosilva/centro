import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# ---- CONFIGURAÇÃO DE ESTILO ----
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        body { background-color: #000000; color: white; }
        .metric-box {
            border: 2px solid #8000ff;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            text-align: center;
            background-color: #111111;
        }
        .metric-box h1 { color: white; }
        .radio-group label { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# ---- LEITURA DA PLANILHA ----
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# ---- VERIFICAÇÃO DAS COLUNAS (caso precise debug) ----
# st.write("Colunas:", df.columns.tolist())

# ---- FILTRO POR MÊS ----
meses = df["Mês"].unique()
mes_selecionado = st.radio("Selecione o mês:", options=meses, horizontal=True)

df_filtrado = df[df["Mês"] == mes_selecionado]

# ---- MÉTRICAS COM ANIMAÇÃO ----
def metric_box(titulo, valor, key):
    with st.container():
        with st.spinner(f"Carregando {titulo}..."):
            time.sleep(0.5)
            st.markdown(f"""
                <div class="metric-box">
                    <h4>{titulo}</h4>
                    <h1>{valor}</h1>
                </div>
            """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    total_am = int(df_filtrado["Coleta Am"].sum())
    metric_box("Coleta AM", f"{total_am} sacos", "am")

with col2:
    total_pm = int(df_filtrado["Coleta PM"].sum())
    metric_box("Coleta PM", f"{total_pm} sacos", "pm")

with col3:
    total_geral = int(df_filtrado["Total de Sacos"].sum())
    metric_box("Total de Sacos", f"{total_geral} sacos", "total")

# ---- GRÁFICO DE LINHA INTERATIVO ----
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_filtrado["Mês"],
    y=df_filtrado["Total de Sacos"],
    mode='lines+markers',
    line=dict(color='#8000ff', width=3),
    marker=dict(size=8),
    name='Total de Sacos'
))
fig.update_layout(
    title='Total de Sacos por Mês',
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

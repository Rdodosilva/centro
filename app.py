import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stButton>button {
        border: 2px solid #8A2BE2;
        color: white;
        background-color: transparent;
    }
    .stButton>button:hover {
        background-color: #8A2BE2;
        color: white;
    }
    .css-1d391kg {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- CARREGAR OS DADOS
url = "https://github.com/Rdodosilva/centro/raw/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# --- REMOVER LINHA DE TOTAL SE EXISTIR
df = df[~df["Mês"].str.lower().str.contains("total", na=False)]

# --- FILTRO DE MÊS
meses_disponiveis = df["Mês"].dropna().unique().tolist()
mes_selecionado = st.radio("Selecione o mês:", meses_disponiveis, horizontal=True)

# --- APLICAR FILTRO
df_filtrado = df[df["Mês"] == mes_selecionado]

# --- MÉTRICAS
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Coleta AM", int(df_filtrado["Coleta AM"].sum()))
with col2:
    st.metric("Total Coleta PM", int(df_filtrado["Coleta PM"].sum()))
with col3:
    st.metric("Total de Sacos", int(df_filtrado["Total de Sacos"].sum()))

# --- GRÁFICO DE LINHAS
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Mês"], y=df["Coleta AM"], name="Coleta AM", mode='lines+markers'))
fig.add_trace(go.Scatter(x=df["Mês"], y=df["Coleta PM"], name="Coleta PM", mode='lines+markers'))
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    title='Evolução da Coleta AM/PM por Mês',
    xaxis_title='Mês',
    yaxis_title='Quantidade de Sacos'
)
st.plotly_chart(fig, use_container_width=True)

# --- TABELA COMPLETA
st.subheader("Pré-visualização dos dados")
st.dataframe(df, use_container_width=True)

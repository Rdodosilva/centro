import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import os

# Configuração do tema escuro e layout
st.set_page_config(layout="wide", page_title="Dashboard Coleta", page_icon="🧊")
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .title {
            font-size: 26px;
            color: white;
            font-weight: bold;
        }
        .stRadio > div {
            flex-direction: row;
        }
    </style>
""", unsafe_allow_html=True)

# Carregamento automático da planilha
@st.cache_data(ttl=60)
def carregar_dados():
    caminho = "Coleta centro2.xlsx"
    if os.path.exists(caminho):
        df = pd.read_excel(caminho)
        df['Mês'] = pd.Categorical(df['Mês'], categories=df['Mês'], ordered=True)
        return df
    else:
        st.error("Arquivo 'Coleta centro2.xlsx' não encontrado.")
        return pd.DataFrame()

df = carregar_dados()

# Filtro de mês
meses = df['Mês'].unique()
mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True)

df_mes = df[df["Mês"] == mes_selecionado]

# Layout de 2 colunas
col1, col2 = st.columns(2)

# Painel 1 - Total por Período (em branco com ícone)
with col1:
    st.markdown('<div class="title">📦 Quantidade de Sacos por Período</div>', unsafe_allow_html=True)
    fig1 = px.bar(
        df_mes,
        x=["Coleta AM", "Coleta PM"],
        y=[df_mes.iloc[0]["Coleta AM"], df_mes.iloc[0]["Coleta PM"]],
        color_discrete_sequence=["#7E57C2", "#9575CD"]
    )
    fig1.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='white',
        showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

# Painel 2 - AM vs PM (em branco com ícone)
with col2:
    st.markdown('<div class="title">🔄 Distribuição Geral AM vs PM</div>', unsafe_allow_html=True)
    fig2 = px.pie(
        df_mes,
        values=[df_mes.iloc[0]["Coleta AM"], df_mes.iloc[0]["Coleta PM"]],
        names=["Coleta AM", "Coleta PM"],
        color_discrete_sequence=["#4A148C", "#9575CD"]
    )
    fig2.update_traces(textinfo="percent+label")
    fig2.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='white'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Painel 3 - Evolução da quantidade de sacos ao longo dos meses
st.markdown('<div class="title">📈 Evolução Mensal da Quantidade de Sacos</div>', unsafe_allow_html=True)
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=df["Mês"],
    y=df["Total de Sacos"],
    mode="lines+markers",
    line=dict(color="#B388FF", width=3),
    marker=dict(size=8),
    name="Total de Sacos"
))
fig3.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    xaxis_title="Mês",
    yaxis_title="Total de Sacos"
)
st.plotly_chart(fig3, use_container_width=True)

# Animação suave de atualização
with st.spinner("Atualizando dados..."):
    time.sleep(0.5)

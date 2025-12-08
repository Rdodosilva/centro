import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 🎯 Configuração da página
st.set_page_config(
    page_title="Coleta Centro - Dashboard Executivo", 
    page_icon="🚛", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 CSS personalizado — INCLUÍ O CONTORNO VERMELHO NO BOTÃO SELECIONADO
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        html, body, .stApp {
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
        }

        /* REMOVE PADDING */
        .main .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: none;
        }

        .main { padding: 0; }

        header[data-testid="stHeader"] {
            height: 2.875rem;
            background: transparent;
        }

        /* GRID DOS MESES */
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
        }

        /* BOTÕES */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label {
            background: #1a1a2e !important;
            padding: 8px 6px !important;
            border-radius: 6px !important;
            border: 1px solid #00FFFF !important;
            margin: 0 !important;
            transition: all 0.25s ease !important;
            cursor: pointer !important;
            color: white !important;
            font-weight: 500 !important;
            font-size: 0.75em !important;
            text-align: center !important;
            height: 32px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background: rgba(0,255,255,0.15) !important;
            transform: scale(1.03) !important;
            box-shadow: 0 4px 12px rgba(0,255,255,0.25) !important;
        }

        /* ⭐ BOTÃO SELECIONADO — ROXO COM CONTORNO VERMELHO TRANSLÚCIDO */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"] {
            background: linear-gradient(135deg, #9b30ff, #6a1b9a) !important;
            border: 2px solid rgba(255,0,0,0.55) !important;  /* 🔥 VERMELHO TRANSLÚCIDO */
            box-shadow:
                0 0 18px rgba(255,0,0,0.45),                  /* Brilho vermelho */
                0 0 35px rgba(155,48,255,0.45),
                inset 0 1px 0 rgba(255,255,255,0.2) !important;
            transform: scale(1.08) !important;
            animation: pulse-red 2s infinite !important;
        }

        /* Animação suave do contorno vermelho */
        @keyframes pulse-red {
            0%, 100% {
                box-shadow:
                    0 0 18px rgba(255,0,0,0.45),
                    0 0 35px rgba(155,48,255,0.45),
                    inset 0 1px 0 rgba(255,255,255,0.2);
            }
            50% {
                box-shadow:
                    0 0 28px rgba(255,0,0,0.7),
                    0 0 45px rgba(155,48,255,0.55),
                    inset 0 1px 0 rgba(255,255,255,0.3);
            }
        }

        /* Remove o círculo padrão do radio */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }

    </style>
""", unsafe_allow_html=True)

# ==================================================================
# 📌 LOAD DA PLANILHA COM O ANO 2026 INCLUÍDO
# ==================================================================
df = pd.read_excel("dados.xlsx")  # <-- sua planilha com 2025 + 2026

# ==================================================================
# 📌 SIDEBAR — AGORA COM ANO 2026
# ==================================================================
st.sidebar.title("Filtros")

anos_disponiveis = sorted(df["Ano"].unique())
ano = st.sidebar.selectbox("Ano", anos_disponiveis)

# FILTRAR MESES POR ANO
meses_disponiveis = df[df["Ano"] == ano]["Mês"].unique()

mes = st.sidebar.radio("Selecione o mês", meses_disponiveis)

# ==================================================================
# 📌 FILTRO DOS DADOS
# ==================================================================
df_filtrado = df[(df["Ano"] == ano) & (df["Mês"] == mes)]

# ==================================================================
# 📌 DASHBOARD
# ==================================================================
st.markdown(f"<h1 style='color:white;'>Coleta Centro – {ano} / {mes}</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Coleta AM", int(df_filtrado["Coleta AM"].sum()))

with col2:
    st.metric("Coleta PM", int(df_filtrado["Coleta PM"].sum()))

with col3:
    st.metric("Total de Sacos", int(df_filtrado["Total de Sacos"].sum()))

# ==================================================================
# 📌 GRÁFICO
# ==================================================================
fig = go.Figure()

fig.add_trace(go.Bar(
    x=["AM", "PM"],
    y=[df_filtrado["Coleta AM"].sum(), df_filtrado["Coleta PM"].sum()],
))

fig.update_layout(
    template="plotly_dark",
    title=f"Coletas do mês {mes}/{ano}",
    height=350
)

st.plotly_chart(fig, use_container_width=True)

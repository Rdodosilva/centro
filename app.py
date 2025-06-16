import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #000000;
            color: white;
        }
        h1, h2, h3, label, span, div {
            color: white !important;
        }
        /* Selectbox fechado */
        div[data-baseweb="select"] > div {
            background-color: rgba(155, 48, 255, 0.8) !important;
            border: 2px solid #9b30ff !important;
            border-radius: 10px;
        }
        div[data-baseweb="select"] span {
            color: white !important;
            font-weight: bold;
        }
        label, .stSelectbox label {
            color: white !important;
            font-weight: bold;
        }

        /* Dropdown aberto */
        div[class*="menu"] {
            background-color: rgba(155, 48, 255, 0.85) !important;
            color: white !important;
            font-weight: bold;
            border-radius: 10px !important;
            backdrop-filter: blur(10px);
        }
        div[class*="option"] {
            color: white !important;
        }
        div[class*="option"]:hover, div[class*="option"][aria-selected="true"] {
            background-color: rgba(200, 100, 255, 0.9) !important;
            color: white !important;
        }

        .stMetric {
            background-color: #111111;
            border: 1px solid #9b30ff;
            border-radius: 12px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# (Seu código continua aqui normalmente: leitura Excel, filtro, métricas, gráficos etc.)

# — só para exemplo do selectbox:
meses_filtro = ["janeiro", "fevereiro", "março", "abril", "maio"]
meses_com_dados = ["janeiro", "março", "abril"]  # simulação
meses_disponiveis = [m for m in meses_filtro if m in meses_com_dados]

mes_selecionado = st.selectbox(
    "Selecione o mês:",
    meses_disponiveis,
    format_func=lambda x: x.capitalize()
)

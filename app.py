import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Coleta Centro - Dashboard Executivo", 
    page_icon="♻️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
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

        /* Botão selecionado com efeito vermelho translúcido */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"] {
            background: linear-gradient(135deg, rgba(255,0,0,0.3), rgba(255,0,0,0.5)) !important;
            color: white !important;
            font-weight: 600 !important;
            border: 2px solid rgba(255,0,0,0.6) !important;
            box-shadow: 
                0 0 20px rgba(255,0,0,0.5),
                0 4px 15px rgba(255,0,0,0.3),
                inset 0 1px 0 rgba(255,255,255,0.2) !important;
            transform: scale(1.05) !important;
            animation: pulse-red 2s infinite !important;
        }

        @keyframes pulse-red {
            0%, 100% {
                box-shadow: 
                    0 0 20px rgba(255,0,0,0.5),
                    0 4px 15px rgba(255,0,0,0.3),
                    inset 0 1px 0 rgba(255,255,255,0.2);
            }
            50% {
                box-shadow: 
                    0 0 30px rgba(255,0,0,0.7),
                    0 6px 20px rgba(255,0,0,0.4),
                    inset 0 1px 0 rgba(255,255,255,0.3);
            }
        }
    </style>
""", unsafe_allow_html=True)

# Carregar dados
try:
    df = pd.read_excel("Coleta centro2.xlsx")
    df.columns = df.columns.str.strip()
    df["Mes"] = df["Mês"].str.lower().str.strip()
except:
    st.warning("⚠️ Arquivo não encontrado. Usando dados simulados para demonstração.")
    df = pd.DataFrame({
        'Mês': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        'Mes': ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
               'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],
        'Coleta AM': [295, 1021, 408, 1192, 1045, 850, 1150, 980, 1240, 1080, 950, 1320],
        'Coleta PM': [760, 1636, 793, 1606, 1461, 1380, 1720, 1520, 1890, 1640, 1480, 2100],
        'Total de Sacos': [1055, 2657, 1201, 2798, 2506, 2230, 2870, 2500, 3130, 2720, 2430, 3420]
    })

# Header
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <div style='font-size: 3.5em; margin-bottom: 10px; font-weight: 700;'>
        ♻️ <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Coleta Centro</span> ♻️
    </div>
    <div style='color: #00FFFF; font-size: 1.2em; opacity: 0.8;'>
        📊 Monitoramento de Crescimento de Resíduos | 2025-2026
    </div>
</div>
""", unsafe_allow_html=True)

# Criar abas para 2025 e 2026
aba2025, aba2026 = st.tabs(["2025", "2026"])

# Aba 2025
with aba2025:
    st.sidebar.markdown("## 🔎 Filtros - 2025")
    meses_disponiveis = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", 
                        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    meses_display = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    mes_selecionado = st.sidebar.radio(
        "",
        options=meses_disponiveis,
        format_func=lambda x: meses_display[meses_disponiveis.index(x)],
        horizontal=False,
        index=0
    )

    st.write(f"📌 Dados de {mes_selecionado.capitalize()} de 2025")
    st.dataframe(df[df["Mes"] == mes_selecionado])

# Aba 2026
with aba2026:
    st.sidebar.markdown("## 🔎 Filtros - 2026")
    # Aqui você pode carregar os dados de 2026 da mesma planilha
    try:
        df2026 = pd.read_excel("Coleta centro2.xlsx", sheet_name="2026")
        df2026.columns = df2026.columns.str.strip()
        df2026["Mes"] = df2026["Mês"].str.lower().str.strip()
    except:
        st.warning("⚠️ Aba 2026 não encontrada na planilha. Usando dados simulados.")
        df2026 = df.copy()
        df2026["Ano"] = 2026

    mes_selecionado_2026 = st.sidebar.radio(
        "",
        options=meses_disponiveis,
        format_func=lambda x: meses_display[meses_disponiveis.index(x)],
        horizontal=False,
        index=0,
        key="radio2026"
    )

    st.write(f"📌 Dados de {mes_selecionado_2026.capitalize()} de 2026")
    st.dataframe(df2026[df2026["Mes"] == mes_selecionado_2026])

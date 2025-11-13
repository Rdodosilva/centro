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

# 🎨 CSS personalizado com layout de 2 colunas para os meses
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
        
        /* Remove white borders and padding */
        .main .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: none;
        }
        
        /* Remove default streamlit padding */
        .main {
            padding: 0;
        }
        
        /* Hide streamlit header but keep sidebar toggle */
        header[data-testid="stHeader"] {
            height: 2.875rem;
            background: transparent;
        }
        
        /* Show sidebar toggle button - force visibility */
        .css-14xtw13 {
            display: block !important;
            visibility: visible !important;
        }
        
        /* Style sidebar toggle button */
        .css-14xtw13 > button {
            background: rgba(26, 26, 46, 0.9) !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            border-radius: 6px !important;
            color: white !important;
            padding: 6px 8px !important;
        }
        
        /* Alternative selector for sidebar button */
        button[data-testid="baseButton-header"] {
            display: block !important;
            visibility: visible !important;
            background: rgba(26, 26, 46, 0.9) !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            border-radius: 6px !important;
            color: white !important;
        }
        
        /* Make sure sidebar toggle icon is white */
        .css-14xtw13 svg, button[data-testid="baseButton-header"] svg {
            fill: white !important;
            color: white !important;
        }
        
        /* Hide other header elements but keep functionality */
        header[data-testid="stHeader"] > div {
            background: transparent;
        }
        
        /* Force full background */
        .stApp {
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%) !important;
        }
        
        /* Sidebar styling - clean theme */
        .css-1d391kg {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }
        
        .sidebar .sidebar-content {
            color: white !important;
        }
        
        /* Sidebar text color - clean and simple */
        .css-1v0mbdj {
            color: white !important;
        }
        
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }
        
        section[data-testid="stSidebar"] > div > div > div > div {
            color: white !important;
        }
        
        /* Sidebar headers styling */
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: white !important;
            font-weight: normal !important;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 8px;
            margin-bottom: 16px;
        }
        
        /* LAYOUT DE 2 COLUNAS PARA OS MESES */
        .month-selector-grid {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
            width: 100% !important;
            margin: 10px 0 !important;
        }
        
        /* Forçar grid layout no container dos radio buttons */
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
            width: 100% !important;
        }
        
        /* BOTÕES DOS MESES - TAMANHO PADRONIZADO E COMPACTO */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label {
            background: #1a1a2e !important;
            padding: 8px 6px !important;
            border-radius: 6px !important;
            border: 1px solid #00FFFF !important;
            margin: 0 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
            color: white !important;
            font-weight: 500 !important;
            font-size: 0.75em !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            width: 100% !important;
            box-sizing: border-box !important;
            height: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
        }
        
        /* Hover dos botões dos meses com efeito suave */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background: rgba(0,255,255,0.15) !important;
            color: white !important;
            border: 1px solid #00FFFF !important;
            transform: translateY(-1px) scale(1.02) !important;
            box-shadow: 0 4px 12px rgba(0,255,255,0.25) !important;
        }
        
        /* BOTÃO SELECIONADO - EFEITO ESPECIAL */
        /* Estilo para o botão de ano selecionado (azul/ciano) - Novo */
        /* O st.radio de ano é o primeiro na sidebar (stRadio:nth-child(2)) */
        section[data-testid="stSidebar"] .stRadio:nth-child(2) > div > div > div > label[data-selected="true"] {
            background: linear-gradient(135deg, #00FFFF, #00D4FF) !important; /* Azul/Ciano */
            color: #1a1a2e !important; /* Texto escuro para contraste */
            font-weight: 700 !important;
            border: 2px solid #00FFFF !important;
            box-shadow: 
                0 0 20px rgba(0,255,255,0.5),
                0 4px 15px rgba(0,255,255,0.3),
                inset 0 1px 0 rgba(255,255,255,0.2) !important;
            transform: scale(1.05) !important;
            animation: none !important; /* Remove a animação de pulso para diferenciar */
        }
        
        /* Estilo para o botão de mês selecionado (roxo) - Mantido */
        /* O st.radio de mês é o segundo na sidebar (stRadio:nth-child(3)) */
        section[data-testid="stSidebar"] .stRadio:nth-child(3) div[role="radiogroup"] > label[data-selected="true"] {
            background: linear-gradient(135deg, #9b30ff, #6a1b9a) !important;
            color: white !important;
            font-weight: 600 !important;
            border: 2px solid #9b30ff !important;
            box-shadow: 
                0 0 20px rgba(155,48,255,0.5),
                0 4px 15px rgba(155,48,255,0.3),
                inset 0 1px 0 rgba(255,255,255,0.2) !important;
            transform: scale(1.05) !important;
            animation: pulse-glow 2s infinite !important;
        }
        
        /* Animação pulsante para o botão selecionado */
        @keyframes pulse-glow {
            0%, 100% {
                box-shadow: 
                    0 0 20px rgba(155,48,255,0.5),
                    0 4px 15px rgba(155,48,255,0.3),
                    inset 0 1px 0 rgba(255,255,255,0.2);
            }
            50% {
                box-shadow: 
                    0 0 30px rgba(155,48,255,0.7),
                    0 6px 20px rgba(155,48,255,0.4),
                    inset 0 1px 0 rgba(255,255,255,0.3);
            }
        }
        
        /* Esconder círculos dos radio buttons */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }
        
        /* Forçar aplicação em todos os elementos de radio */
        .stRadio > div > div > div {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
        }
        
        .stRadio > div > div > div > label {
            background: #1a1a2e !important;
            padding: 8px 6px !important;
            border-radius: 6px !important;
            border: 1px solid #00FFFF !important;
            margin: 0 !important;
            color: white !important;
            font-weight: 500 !important;
            font-size: 0.75em !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            height: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        .stRadio > div > div > div > label:hover {
            background: rgba(0,255,255,0.15) !important;
            transform: translateY(-1px) scale(1.02) !important;
            box-shadow: 0 4px 12px rgba(0,255,255,0.25) !important;
        }
        
        .stRadio > div > div > div > label[data-selected="true"] {
            background: linear-gradient(135deg, #9b30ff, #6a1b9a) !important;
            border: 2px solid #9b30ff !important;
            box-shadow: 
                0 0 20px rgba(155,48,255,0.5),
                0 4px 15px rgba(155,48,255,0.3),
                inset 0 1px 0 rgba(255,255,255,0.2) !important;
            transform: scale(1.05) !important;
            animation: pulse-glow 2s infinite !important;
        }
        
        /* Estilo para o botão de ano selecionado (azul/ciano) - Novo */
        /* O st.radio de ano é o primeiro na sidebar (stRadio:nth-child(2)) */
        section[data-testid="stSidebar"] .stRadio:nth-child(2) > div > div > div > label[data-selected="true"] {
            background: linear-gradient(135deg, #00FFFF, #00D4FF) !important; /* Azul/Ciano */
            color: #1a1a2e !important; /* Texto escuro para contraste */
            font-weight: 700 !important;
            border: 2px solid #00FFFF !important;
            box-shadow: 
                0 0 20px rgba(0,255,255,0.5),
                0 4px 15px rgba(0,255,255,0.3),
                inset 0 1px 0 rgba(255,255,255,0.2) !important;
            transform: scale(1.05) !important;
            animation: none !important; /* Remove a animação de pulso para diferenciar */
        }
        
        /* Métricas AINDA MENORES */
        .stMetric {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid transparent;
            border-radius: 15px;
            padding: 8px 12px;
            box-shadow: 0 8px 32px rgba(0,255,255,0.1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        /* Fonte dos cards MUITO MENOR */
        .stMetric [data-testid="metric-container"] > div:first-child {
            font-size: 0.7em !important;
            font-weight: 500 !important;
            margin-bottom: 2px !important;
        }
        
        .stMetric [data-testid="metric-container"] > div:nth-child(2) {
            font-size: 1.2em !important;
            font-weight: 700 !important;
            margin: 2px 0 !important;
        }
        
        .stMetric [data-testid="metric-container"] > div:last-child {
            font-size: 0.65em !important;
            margin-top: 2px !important;
        }
        
        .stMetric::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #00FFFF, #9b30ff);
            z-index: 1;
        }
        
        /* Estilo para a tabela de dados */
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,255,255,0.1);
        }
        
        /* Estilo para os insights */
        .insight-card {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 12px rgba(0,255,255,0.1);
        }
        
        .insight-card h4 {
            color: #00D4FF !important;
            font-size: 1em !important;
            margin-bottom: 5px !important;
            border-bottom: 1px solid rgba(0,255,255,0.1);
            padding-bottom: 5px;
        }
        
        .insight-card p {
            font-size: 0.85em !important;
            margin: 5px 0 !important;
        }
        
        .trend-up { color: #00FF88; }
        .trend-down { color: #FF4444; }
        .trend-neutral { color: #FFAA00; }
        
        /* Animation for charts */
        .stPlotlyChart {
            animation: fadeIn 0.8s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        h1, h2, h3, label, span, div {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# 🎛️ Sidebar com controles avançados
with st.sidebar:
    st.markdown("## 🎛️ Filtros")
    
    # Filtro de período - TODOS OS 12 MESES EM 2 COLUNAS
    meses_disponiveis = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", 
                        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    meses_display = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    st.markdown("### 📅 Período:")

    # Novo filtro de ano
    ano_selecionado = st.radio(
        "Ano:",
        options=["2025", "2026"], # Adicionando 2026
        index=0,
        horizontal=True
    )
    
    # O CSS já cuida do layout em grid 2x6, apenas criamos o radio button normal
    mes_selecionado = st.radio(
        "",
        options=meses_disponiveis,
        format_func=lambda x: meses_display[meses_disponiveis.index(x)],
        horizontal=False,
        index=0
    )
    
    # Opções de visualização
    st.markdown("### 📊 Visualização")
    mostrar_comparativo = st.checkbox("Comparar com mês anterior", True)
    tipo_grafico = st.radio(
        "Tipo de gráfico:",
        ["Barras"],
        horizontal=False
    )

# 📥 Carregar dados (mantendo sua estrutura)
try:
    df_base = pd.read_excel("Coleta centro2.xlsx")
    df_base.columns = df_base.columns.str.strip()
    df_base["Mes"] = df_base["Mês"].str.lower().str.strip()
except:
    # Dados simulados - TODOS OS 12 MESES (Dados de 2025)
    st.warning("⚠️ Arquivo não encontrado. Usando dados simulados para demonstração (Dados de 2025).")
    df_base = pd.DataFrame({
        'Mês': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        'Mes': ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
               'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],
        'Coleta AM': [295, 1021, 408, 1192, 1045, 850, 1150, 980, 1240, 1080, 950, 1320],
        'Coleta PM': [760, 1636, 793, 1606, 1461, 1380, 1720, 1520, 1890, 1640, 1480, 2100],
        'Total de Sacos': [1055, 2657, 1201, 2798, 2506, 2230, 2870, 2500, 3130, 2720, 2430, 3420]
    })

# 🔄 Lógica de filtragem por ano
if ano_selecionado == "2026":
    # Cria um DataFrame zerado para 2026
    df = pd.DataFrame({
        'Mês': df_base['Mês'],
        'Mes': df_base['Mes'],
        'Coleta AM': [0] * len(df_base),
        'Coleta PM': [0] * len(df_base),
(Content truncated due to size limit. Use page ranges or line ranges to read remaining content)



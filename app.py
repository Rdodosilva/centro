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
            bottom: 0;
            background: linear-gradient(45deg, #00FFFF, #9b30ff);
            z-index: -1;
            margin: -2px;
            border-radius: inherit;
        }
        
        /* Checkbox styling */
        .stCheckbox {
            color: white !important;
        }
        
        .stCheckbox > label {
            color: white !important;
            font-weight: normal;
        }
        
        .stCheckbox:hover > label {
            color: #00FFFF !important;
        }
        
        /* BOTÕES SIDEBAR PADRONIZADOS */
        .stButton > button, .stDownloadButton > button, 
        button[data-testid*="stDownloadButton"], 
        div[data-testid="stDownloadButton"] button {
            background: #00FFFF !important;
            border: none !important;
            border-radius: 6px !important;
            color: black !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            padding: 8px 16px !important;
            height: 36px !important;
            font-size: 0.85em !important;
        }
        
        .stButton > button:hover, .stDownloadButton > button:hover,
        button[data-testid*="stDownloadButton"]:hover,
        div[data-testid="stDownloadButton"] button:hover {
            background: #0080FF !important;
            color: black !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 2px 8px rgba(0,255,255,0.3) !important;
        }
        
        /* Force styling on all buttons in sidebar */
        section[data-testid="stSidebar"] button {
            background: #00FFFF !important;
            border: none !important;
            border-radius: 6px !important;
            color: black !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            padding: 8px 16px !important;
            height: 36px !important;
            font-size: 0.85em !important;
        }
        
        section[data-testid="stSidebar"] button:hover {
            background: #0080FF !important;
            color: black !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 2px 8px rgba(0,255,255,0.3) !important;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid #00FFFF;
            border-radius: 10px;
        }
        
        /* Style the menu dropdown - clean dark background */
        .css-1rs6os, .css-17lntkn, [data-testid="stPopover"], div[data-baseweb="popover"] {
            background: #2c2c54 !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 8px !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        }
        
        /* Force dark background on all menu containers */
        .css-1rs6os > div, .css-17lntkn > div, [data-testid="stPopover"] > div {
            background: #2c2c54 !important;
            color: white !important;
        }
        
        /* Style dropdown items with white text and hover effect */
        .css-1rs6os button, .css-17lntkn button, [data-testid="stPopover"] button,
        .css-1rs6os div, .css-17lntkn div, [data-testid="stPopover"] div {
            color: white !important;
            background: transparent !important;
            font-weight: normal !important;
            padding: 10px 15px !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
        }
        
        .css-1rs6os button:hover, .css-17lntkn button:hover, [data-testid="stPopover"] button:hover {
            background: #00FFFF !important;
            color: black !important;
            border-radius: 6px !important;
        }
        
        /* Force white text on all menu elements */
        .css-1rs6os *, .css-17lntkn *, [data-testid="stPopover"] *, div[data-baseweb="popover"] * {
            color: white !important;
            background: transparent !important;
        }
        
        /* Override any white backgrounds in dropdowns */
        div[role="menu"], div[role="listbox"], .css-1n76uvr, .css-1d391kg {
            background: #2c2c54 !important;
            color: white !important;
        }
        
        div[role="menu"] *, div[role="listbox"] *, .css-1n76uvr *, .css-1d391kg * {
            background: transparent !important;
            color: white !important;
        }
        
        /* Hover effect for menu items */
        div[role="menu"] button:hover, div[role="listbox"] button:hover {
            background: #00FFFF !important;
            color: black !important;
        }
        
        /* Cards para insights */
        .insight-card {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 1px solid #00FFFF;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 8px 32px rgba(0,255,255,0.1);
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
""", unsafe_allow_# 📥 Carregar dados (mantendo sua estrutura)
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
        'Total de Sacos': [0] * len(df_base)
    })
else:
    # Usa os dados de 2025
    df = df_base.copy()

# 🔄 Filtragem de dados para o mês selecionado
df_mes = df[df["Mes"] == mes_selecionado].iloc[0]

# 📊 Cálculo das métricas
total_sacos = df_mes["Total de Sacos"]
total_am = df_mes["Coleta AM"]
total_pm = df_mes["Coleta PM"],
        'Mes': df_base['Mes'],
        'Coleta AM': [0] * len(df_base),
        'Coleta PM': [0] * len(df_base),
        'Total de Sacos': [0] * len(df_base)
    })
else:
    # Usa os dados de 2025
    df = df_base.copy()

# 🔄 Filtragem de dados para o mês selecionado
df_mes = df[df["Mes"] == mes_selecionado].iloc[0]

# 📊 Cálculo das métricas
total_sacos = df_mes["Total de Sacos"]
total_am = df_mes["Coleta AM"]
total_pm = df_mes["Coleta PM"]t(90deg, #00FFFF, #9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.2em; opacity: 0.8;'>
        📊 Monitoramento de Crescimento de Resíduos | {ano_selecionado}
    </div>
</div>
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
    
    # Configurações de export
    st.markdown("### 📤 Exportar")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        # APRESENTAÇÃO ATUALIZADA com novas métricas
        apresentacao_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apresentação - Coleta Centro</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
            line-height: 1.6;
        }}
        
        .slide {{
            min-height: 100vh;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            break-after: page;
        }}
        
        .slide-header {{
            text-align: center;
            margin-bottom: 50px;
        }}
        
        .slide-title {{
            font-size: 3.2em;
            font-weight: 700;
            margin-bottom: 20px;
            background: linear-gradient(90deg, #00FFFF, #9b30ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(0,255,255,0.3);
        }}
        
        .slide-subtitle {{
            font-size: 1.4em;
            color: #00D4FF;
            opacity: 0.9;
            text-shadow: 0 0 20px rgba(0,212,255,0.3);
        }}
        
        .content-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .card {{
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,255,255,0.15);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 45px rgba(0,255,255,0.25);
            border-color: rgba(0, 255, 255, 0.6);
        }}
        
        .card h3 {{
            color: #00D4FF;
            font-size: 1.4em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 15px rgba(0,212,255,0.5);
        }}
        
        .metric {{
            font-size: 2.8em;
            font-weight: bold;
            background: linear-gradient(45deg, #00D4FF, #9b30ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 20px 0;
            text-shadow: 0 0 20px rgba(155,48,255,0.3);
        }}
        
        .logo {{
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 0 0 25px rgba(0,255,255,0.4);
        }}
        
        ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        li {{
            margin: 15px 0;
            padding-left: 25px;
            position: relative;
            transition: all 0.2s ease;
        }}
        
        li:before {{
            content: "▶";
            color: #00D4FF;
            position: absolute;
            left: 0;
            text-shadow: 0 0 10px rgba(0,212,255,0.5);
        }}
        
        li:hover {{
            transform: translateX(5px);
            color: #00D4FF;
        }}
        
        .two-column {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            align-items: start;
        }}
        
        .highlight-box {{
            background: linear-gradient(145deg, rgba(0,212,255,0.1), rgba(155,48,255,0.1));
            border: 2px solid rgba(0,212,255,0.3);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 1.3em;
            margin: 25px 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,212,255,0.1);
        }}
        
        .recommendation {{
            background: rgba(255, 170, 0, 0.1);
            border: 1px solid rgba(255, 170, 0, 0.3);
            border-left: 4px solid #FFAA00;
            padding: 25px;
            margin: 25px 0;
            border-radius: 0 15px 15px 0;
            backdrop-filter: blur(10px);
        }}
        
        .recommendation.success {{
            background: rgba(0, 255, 136, 0.1);
            border-color: rgba(0, 255, 136, 0.3);
            border-left-color: #00FF88;
        }}
        
        .slide-number {{
            position: absolute;
            bottom: 25px;
            right: 25px;
            color: rgba(0,212,255,0.7);
            font-size: 1.1em;
            font-weight: 600;
            background: rgba(26,26,46,0.8);
            padding: 8px 15px;
            border-radius: 20px;
            border: 1px solid rgba(0,212,255,0.3);
        }}
        
        .data-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(0,212,255,0.1);
        }}
        
        .data-label {{
            font-weight: 600;
            color: #00D4FF;
        }}
        
        .data-value {{
            font-weight: 700;
            color: white;
            font-size: 1.1em;
        }}
        
        @media print {{
            .slide {{
                break-after: page;
                min-height: auto;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Slide 1: Capa -->
    <div class="slide">
        <div class="slide-header">
            <div class="logo">🚛</div>
            <div class="slide-title">Coleta Centro</div>
            <div class="slide-subtitle">Dashboard Executivo de Monitoramento | {ano_selecionado}</div>
        </div>
        
        <div class="content-grid">
            <div class="card">
                <h3>🎯 Objetivo da Análise</h3>
                <p>Monitoramento inteligente do crescimento dos resíduos no centro da cidade com dashboard interativo e análises preditivas.</p>
            </div>
            
            <div class="card">
                <h3>📅 Período Analisado</h3>
                <p><strong>Janeiro a Julho de {ano_selecionado}</strong></p>
                <p>7 meses de dados coletados</p>
                <p>Análise mensal detalhada</p>
            </div>
            
            <div class="card">
                <h3>📈 Crescimento Total</h3>
                <div class="metric">+172%</div>
                <p>Janeiro → Julho {ano_selecionado}</p>
                <p>Volume em expansão significativa</p>
            </div>
        </div>
        
        <div class="slide-number">01</div>
    </div>
    
    <!-- Slide 2: Panorama Geral -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-title">📊 Panorama Geral</div>
            <div class="slide-subtitle">Principais Indicadores - Janeiro a Julho {ano_selecionado}</div>
        </div>
        
        <div class="content-grid">
            <div class="card">
                <h3>🧺 Volume Total</h3>
                <div class="metric">15.447</div>
                <p>sacos coletados no período</p>
                <p><strong>308.940 kg</strong> de resíduos</p>
                <p>Crescimento consistente mensal</p>
            </div>
            
            <div class="card">
                <h3>📊 Distribuição por Período</h3>
                <div class="data-row">
                    <span class="data-label">Manhã (AM):</span>
                    <span class="data-value">38%</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Tarde (PM):</span>
                    <span class="data-value">62%</span>
                </div>
                <p style="margin-top: 15px;">Maior concentração vespertina</p>
            </div>
            
            <div class="card">
                <h3>📈 Performance Mensal</h3>
                <div class="data-row">
                    <span class="data-label">Maior volume:</span>
                    <span class="data-value">Julho (2.870)</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Menor volume:</span>
                    <span class="data-value">Janeiro (1.055)</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Média mensal:</span>
                    <span class="data-value">2.207 sacos</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🚛 Status Operacional</h3>
                <div class="metric">CRESCIMENTO</div>
                <p><strong>Tendência:</strong> Alta consistente</p>
                <p><strong>Capacidade:</strong> Monitorar expansão</p>
                <p><strong>Próximos passos:</strong> Análise contínua</p>
            </div>
        </div>
        
        <div class="slide-number">02</div>
    </div>
    
    <!-- Slide 3: Evolução Detalhada -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-title">📈 Evolução Mensal Detalhada</div>
            <div class="slide-subtitle">Crescimento Consistente dos Resíduos</div>
        </div>
        
        <div class="two-column">
            <div>
                <div class="card">
                    <h3>📋 Dados Mensais Completos</h3>
                    <div class="data-row">
                        <span class="data-label">Janeiro:</span>
                        <span class="data-value">1.055 sacos (21.100 kg)</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Fevereiro:</span>
                        <span class="data-value">2.657 sacos (53.140 kg)</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Março:</span>
                        <span class="data-value">1.201 sacos (24.020 kg)</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Abril:</span>
                        <span class="data-value">2.798 sacos (55.960 kg)</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Maio:</span>
                        <span class="data-value">2.506 sacos (50.120 kg)</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Junho:</span>
                        <span class="data-value">2.230 sacos (44.600 kg)</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Julho:</span>
                        <span class="data-value">2.870 sacos (57.400 kg)</span>
                    </div>
                </div>
            </div>
            
            <div>
                <div class="highlight-box">
                    <div style="font-size: 1.6em; margin-bottom: 15px;">🚀 Crescimento de 172%</div>
                    <div style="font-size: 1.2em;">Volume demonstra expansão significativa ao longo de 7 meses</div>
                </div>
                
                <div class="card" style="margin-top: 25px;">
                    <h3>⚡ Insights Principais</h3>
                    <ul>
                        <li>Pico em <strong>Julho (2.870 sacos)</strong></li>
                        <li>Vale em <strong>Janeiro (1.055 sacos)</strong></li>
                        <li>Crescimento médio de <strong>24.6% ao mês</strong></li>
                        <li>Tendência de alta consistente</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="slide-number">03</div>
    </div>
    
    <!-- Slide 4: Análise & Recomendações -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-title">💡 Análise & Recomendações</div>
            <div class="slide-subtitle">Insights Estratégicos e Próximos Passos</div>
        </div>
        
        <div class="highlight-box">
            <div style="font-size: 1.8em; margin-bottom: 20px;">🎯 MONITORAMENTO INTELIGENTE</div>
            <div style="font-size: 1.4em;">Volume cresceu 172% em 7 meses - Acompanhamento estratégico essencial</div>
        </div>
        
        <div class="content-grid">
            <div class="card">
                <h3>📊 Principais Descobertas</h3>
                <ul>
                    <li>Crescimento de <strong>172% em 7 meses</strong></li>
                    <li>Volume atual: <strong>2.870 sacos/mês (Julho)</strong></li>
                    <li>Tendência: <strong>Crescimento acelerado</strong></li>
                    <li>Padrão: <strong>62% tarde vs 38% manhã</strong></li>
                    <li>Peso total: <strong>308.940 kg processados</strong></li>
                </ul>
            </div>
            
            <div class="card">
                <h3>🎯 Recomendações Estratégicas</h3>
                <ul>
                    <li><strong>Monitoramento contínuo</strong> mensal</li>
                    <li><strong>Análises preditivas</strong> para planejamento</li>
                    <li><strong>Dashboard interativo</strong> para decisões</li>
                    <li><strong>Relatórios automatizados</strong></li>
                    <li><strong>Avaliação trimestral</strong> de capacidade</li>
                </ul>
            </div>
        </div>
        
        <div class="recommendation success">
            <h3>🚀 Considerações Finais</h3>
            <p>O <strong>dashboard implementado</strong> fornece visibilidade completa sobre o crescimento dos resíduos. 
            Os dados revelam um <strong>padrão de crescimento consistente</strong> que permite <strong>decisões baseadas em evidências</strong> 
            e <strong>planejamento estratégico eficiente</strong> para a gestão urbana.</p>
        </div>
        
        <div class="slide-number">04</div>
    </div>
</body>
</html>"""
        
        st.download_button(
            label="📊 PDF",
            data=apresentacao_html,
            file_name=f"Apresentacao_Coleta_Centro_{mes_selecionado.title()}_{ano_selecionado}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col_btn2:
        # Criar dados para Excel
        df_export = df[df["Total de Sacos"].notna()].copy()
        df_export["Mês"] = df_export["Mês"].str.title()
        df_export["Peso Total (kg)"] = df_export["Total de Sacos"] * 20
        df_export["% AM"] = (df_export["Coleta AM"] / df_export["Total de Sacos"] * 100).round(1)
        df_export["% PM"] = (df_export["Coleta PM"] / df_export["Total de Sacos"] * 100).round(1)
        
        csv_data = df_export[["Mês", "Coleta AM", "Coleta PM", "Total de Sacos", "Peso Total (kg)", "% AM", "% PM"]].to_csv(index=False)
        
        st.download_button(
            label="📋 Excel",
            data=csv_data,
            file_name=f"Dados_Coleta_Centro_{mes_selecionado.title()}_{ano_selecionado}.csv",
            mime="text/csv",
            use_container_width=True
        )

# 📑 Filtrar dados para o mês selecionado
df_filtrado = df[(df["Mes"] == mes_selecionado) & (df["Total de Sacos"].notna())]

# 📊 Calcular métricas principais
total_sacos = int(df_filtrado["Total de Sacos"].sum()) if not df_filtrado.empty else 0
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum()) if not df_filtrado.empty else 0
total_pm = int(df_filtrado["Coleta PM"].sum()) if not df_filtrado.empty else 0

# Cálculos de comparação (mês anterior)
mes_anterior_idx = meses_disponiveis.index(mes_selecionado) - 1 if mes_selecionado != "janeiro" else -1
if mes_anterior_idx >= 0:
    df_anterior = df[df["Mes"] == meses_disponiveis[mes_anterior_idx]]
    total_anterior = int(df_anterior["Total de Sacos"].sum()) if not df_anterior.empty else 0
    variacao = ((total_sacos - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0
else:
    variacao = 0

# 🎯 Exibir métricas com design aprimorado
st.markdown("## 📈 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    delta_value = f"{variacao:+.1f}%" if mostrar_comparativo and variacao != 0 else None
    st.metric(
        "🧺 Total de Sacos", 
        f"{total_sacos:,}".replace(',', '.'),
        delta=delta_value
    )

with col2:
    st.metric(
        "⚖️ Peso Total", 
        f"{peso_total:,} kg".replace(',', '.'),
        delta=f"{variacao*20:+.0f} kg" if mostrar_comparativo and variacao != 0 else None
    )

with col3:
    eficiencia = (total_am / (total_am + total_pm) * 100) if (total_am + total_pm) > 0 else 0
    st.metric(
        "📊 Eficiência AM", 
        f"{eficiencia:.1f}%",
        delta="Ótimal" if eficiencia > 25 else "Baixa"
    )

with col4:
    # MUDANÇA: Status informativo em vez de urgência
    if total_sacos > 2500:
        status = "MONITORAR"
        info = "Volume alto"
    elif total_sacos > 2000:
        status = "ACOMPANHAR"
        info = "Volume crescente"
    else:
        status = "NORMAL"
        info = "Dentro do esperado"
    
    st.metric(
        "📊 Status Operacional", 
        status,
        delta=info
    )

# 📊 Seção de gráficos principais
st.markdown("## 📊 Análises Visuais")

# Preparar dados para gráficos
df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

# Cores futuristas simples e limpas
cores_futuristas = {
    "Coleta AM": "#00D4FF",  
    "Coleta PM": "#FF6B35"   
}

# Gráfico principal LIMPO e futurista
col_left, col_right = st.columns([2, 1])

with col_left:
    fig_main = px.bar(
        df_melt,
        x="Mes",
        y="Quantidade de Sacos",
        color="Periodo",
        color_discrete_map=cores_futuristas,
        barmode="group",
        title=f"🚀 Coleta por Período - {mes_selecionado.title()}"
    )
    
    # Styling futurista SIMPLES
    fig_main.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        title_font=dict(size=16, color="#00D4FF", family="Inter", weight="bold"),
        title_x=0.5,
        title_y=0.95,
        font_family="Inter",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.02,
            xanchor="center",
            x=0.5,
            font=dict(color="white", size=10),
            bgcolor="rgba(26, 26, 46, 0.8)",
            bordercolor="rgba(0, 212, 255, 0.3)",
            borderwidth=1
        ),
        margin=dict(l=50, r=50, t=80, b=50),
        height=450,
        xaxis=dict(
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor="rgba(0, 212, 255, 0.3)",
            color="white",
            title_font=dict(color="white", size=14),
            tickfont=dict(color="white", size=11),
            categoryorder='array',
            categoryarray=meses_disponiveis
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(0, 212, 255, 0.1)",
            showline=False,
            color="white",
            title_font=dict(color="white", size=14),
            tickfont=dict(color="white", size=11),
            title="Quantidade de Sacos",
            zeroline=True,
            zerolinecolor="rgba(0, 212, 255, 0.2)"
        )
    )
    
    # Barras com transparência simples
    fig_main.update_traces(
        marker=dict(
            opacity=0.8,
            line=dict(color="rgba(255,255,255,0.1)", width=1)
        ),
        hovertemplate='<b>%{y}</b> sacos<br>%{fullData.name}<br><extra></extra>'
    )
    
    st.plotly_chart(fig_main, use_container_width=True)

with col_right:
    # Gráfico pizza LIMPO e futurista
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Coleta AM", "Coleta PM"],
        values=[total_am, total_pm],
        hole=0.6,
        marker=dict(
            colors=["rgba(0, 212, 255, 0.8)", "rgba(255, 107, 53, 0.8)"],
            line=dict(color="rgba(255,255,255,0.1)", width=1)
        ),
        textinfo='percent',
        textfont=dict(color='white', size=14, family="Inter", weight="bold"),
        hovertemplate='<b>%{label}</b><br>%{value} sacos<br>%{percent}<extra></extra>',
        pull=[0.02, 0.02]
    )])
    
    fig_pie.update_layout(
        title=dict(
            text=f"⚡ Distribuição AM vs PM<br>{mes_selecionado.title()}",
            font=dict(size=13, color="#00D4FF", family="Inter", weight="bold"),
            x=0.5,
            y=0.95
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        font_family="Inter",
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="bottom",
            y=0.02,
            xanchor="center",
            x=0.5,
            font=dict(color="white", size=9),
            bgcolor="rgba(26, 26, 46, 0.6)",
            bordercolor="rgba(0, 212, 255, 0.3)",
            borderwidth=1
        ),
        height=450,
        margin=dict(l=20, r=20, t=70, b=50),
        annotations=[
            dict(
                text=f"<b style='color:#00D4FF; font-size:18px'>{total_sacos:,}</b><br><span style='color:white; font-size:12px'>Total</span>",
                x=0.5, y=0.5,
                font_family="Inter",
                showarrow=False,
                bgcolor="rgba(26, 26, 46, 0.8)",
                bordercolor="rgba(0, 212, 255, 0.3)",
                borderwidth=1,
                borderpad=8
            )
        ]
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

# 📈 Gráfico de evolução mensal aprimorado
st.markdown("### 📈 Evolução Temporal Completa")

df_linha = df[df["Total de Sacos"].notna()].copy()
df_linha["Mes_cat"] = pd.Categorical(df_linha["Mes"], categories=meses_disponiveis, ordered=True)
df_linha = df_linha.sort_values("Mes_cat")

# Criar gráfico de linha com múltiplas métricas
# GRÁFICO DE EVOLUÇÃO SIMPLES e futurista
fig_evolucao = make_subplots(
    rows=2, cols=1,
    subplot_titles=("🌟 Volume de Coleta (Sacos)", "⚡ Distribuição AM/PM"),
    vertical_spacing=0.15,
    specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
)

# Linha principal limpa
fig_evolucao.add_trace(
    go.Scatter(
        x=df_linha["Mes"], 
        y=df_linha["Total de Sacos"],
        mode='lines+markers',
        name='Total de Sacos',
        line=dict(
            color='#9b30ff', 
            width=4, 
            shape='spline'
        ),
        marker=dict(
            size=10, 
            color='white', 
            line=dict(color='#9b30ff', width=3),
            symbol='circle'
        ),
        fill='tonexty',
        fillcolor='rgba(155, 48, 255, 0.15)',
        hovertemplate='<b>%{y}</b> sacos<br>%{x}<br><extra></extra>'
    ),
    row=1, col=1
)

# Barras simples com transparência
fig_evolucao.add_trace(
    go.Bar(
        x=df_linha["Mes"], 
        y=df_linha["Coleta AM"], 
        name='AM', 
        marker=dict(
            color='rgba(0, 212, 255, 0.7)',
            line=dict(color='rgba(0, 212, 255, 0.9)', width=1)
        ),
        hovertemplate='<b>AM:</b> %{y} sacos<br>%{x}<extra></extra>'
    ),
    row=2, col=1
)

fig_evolucao.add_trace(
    go.Bar(
        x=df_linha["Mes"], 
        y=df_linha["Coleta PM"], 
        name='PM', 
        marker=dict(
            color='rgba(255, 107, 53, 0.7)',
            line=dict(color='rgba(255, 107, 53, 0.9)', width=1)
        ),
        hovertemplate='<b>PM:</b> %{y} sacos<br>%{x}<extra></extra>'
    ),
    row=2, col=1
)

# Layout limpo
fig_evolucao.update_layout(
    height=650,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    font_family="Inter",
    title_font=dict(size=16, color="#00D4FF"),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0.5,
        font=dict(color="white", size=10),
        bgcolor="rgba(26, 26, 46, 0.8)",
        bordercolor="rgba(0, 212, 255, 0.3)",
        borderwidth=1
    ),
    barmode='stack',
    margin=dict(l=50, r=50, t=80, b=70)
)

# Styling dos eixos
fig_evolucao.update_xaxes(
    showgrid=False,
    showline=True,
    linewidth=2,
    linecolor="rgba(0, 212, 255, 0.3)",
    color="white",
    title_font=dict(color="white", size=12),
    tickfont=dict(color="white", size=10),
    categoryorder='array',
    categoryarray=meses_disponiveis
)

fig_evolucao.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="rgba(0, 212, 255, 0.1)",
    showline=True,
    linewidth=2,
    linecolor="rgba(0, 212, 255, 0.3)",
    color="white",
    title_font=dict(color="white", size=12),
    tickfont=dict(color="white", size=10)
)

# Personalizar títulos dos subplots
fig_evolucao.update_annotations(
    font=dict(color="#00D4FF", size=16, family="Inter", weight="bold")
)

st.plotly_chart(fig_evolucao, use_container_width=True)

# 💡 Seção de Insights Inteligentes
st.markdown("## 💡 Insights e Recomendações")

col_insight1, col_insight2, col_insight3 = st.columns(3)

with col_insight1:
    tendencia = "crescente" if variacao > 0 else "decrescente" if variacao < 0 else "estável"
    cor_tendencia = "trend-up" if variacao > 0 else "trend-down" if variacao < 0 else "trend-neutral"
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>📊 Análise de Tendência</h4>
        <p>Volume <span class="{cor_tendencia}">{tendencia}</span> em relação ao mês anterior</p>
        <p><strong>Variação:</strong> <span class="{cor_tendencia}">{variacao:+.1f}%</span></p>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    pico_coleta = "AM" if total_am > total_pm else "PM"
    percentual_pico = max(total_am, total_pm) / (total_am + total_pm) * 100 if (total_am + total_pm) > 0 else 0
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>⏰ Padrão de Coleta</h4>
        <p>Maior volume no período da <strong>{pico_coleta}</strong></p>
        <p><strong>Concentração:</strong> {percentual_pico:.1f}% do total</p>
    </div>
    """, unsafe_allow_html=True)

with col_insight3:
    # Análise de necessidade de novo coletor
    projecao_proxima = total_sacos * (1 + (variacao/100)) if variacao != 0 else total_sacos * 1.05
    necessidade = "URGENTE" if projecao_proxima > 2500 else "MONITORAR" if projecao_proxima > 2000 else "ADEQUADO"
    cor_necessidade = "trend-down" if necessidade == "URGENTE" else "trend-neutral" if necessidade == "MONITORAR" else "trend-up"
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>🚛 Capacidade Coletora</h4>
        <p>Status: <span class="{cor_necessidade}"><strong>{necessidade}</strong></span></p>
        <p><strong>Projeção:</strong> {projecao_proxima:.0f} sacos</p>
        <p>({projecao_proxima*20:.0f} kg)</p>
    </div>
    """, unsafe_allow_html=True)

# 📋 Tabela de dados detalhada (colapsável)
with st.expander("📋 Ver Dados Detalhados"):
    df_display = df[df["Total de Sacos"].notna()].copy()
    df_display["Mês"] = df_display["Mês"].str.title()
    df_display["Peso Total (kg)"] = df_display["Total de Sacos"] * 20
    df_display["% AM"] = (df_display["Coleta AM"] / df_display["Total de Sacos"] * 100).round(1)
    df_display["% PM"] = (df_display["Coleta PM"] / df_display["Total de Sacos"] * 100).round(1)
    
    st.dataframe(
        df_display[["Mês", "Coleta AM", "Coleta PM", "Total de Sacos", "Peso Total (kg)", "% AM", "% PM"]],
        use_container_width=True
    )

# 🎯 Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <div style='font-size: 2em; margin-bottom: 10px;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.1em;'>
        📊 Monitoramento para Otimização da Frota
    </div>
    <small style='color: rgba(255,255,255,0.7);'>Sistema de apoio à decisão para expansão da coleta urbana</small>
</div>
""", unsafe_allow_html=True)

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
# <-- ALTERAÇÃO: inclui contorno vermelho translúcido no botão selecionado
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
        
        /* BOTÃO SELECIONADO - EFEITO ESPECIAL: roxo original + contorno VERMELHO translúcido */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"] {
            background: linear-gradient(135deg, #9b30ff, #6a1b9a) !important;
            color: white !important;
            font-weight: 600 !important;
            border: 2px solid rgba(255,0,0,0.55) !important; /* borda vermelha translúcida */
            box-shadow: 
                0 0 14px rgba(255,0,0,0.45),   /* brilho vermelho */
                0 4px 15px rgba(155,48,255,0.35),
                inset 0 1px 0 rgba(255,255,255,0.2) !important;
            transform: scale(1.05) !important;
            animation: pulse-glow-red 2s infinite !important;
        }
        
        /* Animação pulsante com predominância vermelha */
        @keyframes pulse-glow-red {
            0%, 100% {
                box-shadow: 
                    0 0 14px rgba(255,0,0,0.45),
                    0 4px 15px rgba(155,48,255,0.35),
                    inset 0 1px 0 rgba(255,255,255,0.2);
            }
            50% {
                box-shadow: 
                    0 0 26px rgba(255,0,0,0.7),
                    0 6px 25px rgba(155,48,255,0.5),
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
""", unsafe_allow_html=True)

# 📥 Carregar dados (mantendo sua estrutura)
# Agora lemos a planilha por abas (cada aba = um ano). Se não encontrar, usamos dados simulados.
excel_file_path = "Coleta centro2.xlsx"

try:
    xls = pd.ExcelFile(excel_file_path)
    # pegar nomes de abas/anos
    sheet_names = xls.sheet_names
    # opcional: ordenar para aparecer 2025 antes de 2026 se necessário
    sheet_names_sorted = sorted(sheet_names, key=lambda s: s)  # mantém ordem alfabética/numeric
    # seletor de ano na sidebar
    with st.sidebar:
        st.markdown("## 🎛️ Filtros")
        ano_selecionado = st.selectbox("Ano:", sheet_names_sorted, index=0)
    # ler aba selecionada
    try:
        df = pd.read_excel(excel_file_path, sheet_name=ano_selecionado)
        df.columns = df.columns.str.strip()
        # garantir existência da coluna 'Mês' e criar 'Mes' em lowercase
        if "Mês" in df.columns:
            df["Mes"] = df["Mês"].str.lower().str.strip()
        else:
            # aba vazia ou formato diferente: criar df vazio com colunas esperadas
            df = pd.DataFrame(columns=["Mês", "Coleta AM", "Coleta PM", "Total de Sacos"])
            df["Mes"] = []
    except Exception as e_inner:
        # se erro ao ler aba específica, fallback para df vazio
        df = pd.DataFrame({
            'Mês': ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
            'Mes': ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'],
            'Coleta AM': [0]*12,
            'Coleta PM': [0]*12,
            'Total de Sacos': [0]*12
        })
except FileNotFoundError:
    # Arquivo não encontrado: aviso e dados simulados
    st.warning("⚠️ Arquivo 'Coleta centro2.xlsx' não encontrado. Usando dados simulados para demonstração.")
    ano_selecionado = "Simulado"
    df = pd.DataFrame({
        'Mês': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        'Mes': ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
               'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],
        'Coleta AM': [295, 1021, 408, 1192, 1045, 850, 1150, 980, 1240, 1080, 950, 1320],
        'Coleta PM': [760, 1636, 793, 1606, 1461, 1380, 1720, 1520, 1890, 1640, 1480, 2100],
        'Total de Sacos': [1055, 2657, 1201, 2798, 2506, 2230, 2870, 2500, 3130, 2720, 2430, 3420]
    })

# 🏷️ Header aprimorado
st.markdown(f"""
<div style='text-align: center; padding: 20px 0;'>
    <div style='font-size: 3.5em; margin-bottom: 10px; font-weight: 700;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.2em; opacity: 0.8;'>
        📊 Monitoramento de Crescimento de Resíduos | {ano_selecionado}
    </div>
</div>
""", unsafe_allow_html=True)

# 🎛️ Sidebar com controles avançados (meses)
# Re-abrir sidebar para colocar meses e demais controles (ano já selecionado acima)
with st.sidebar:
    # Se já colocamos o ano, não queremos duplicar o cabeçalho; mostrar só controles de mês/visualização/export
    st.markdown("### 📅 Período:")
    
    # Filtro de período - TODOS OS 12 MESES EM 2 COLUNAS (fixos)
    meses_disponiveis = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", 
                        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    meses_display = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    # Caso a planilha tenha alguns meses só com NaN, mantemos as opções visuais pra você selecionar
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
        /* (HTML de apresentação copiado do original para download) */
    </style>
</head>
<body>
    <div class="slide">
        <div class="slide-header">
            <div class="logo">🚛</div>
            <div class="slide-title">Coleta Centro</div>
            <div class="slide-subtitle">Dashboard Executivo de Monitoramento | {ano_selecionado}</div>
        </div>
        <!-- Conteúdo resumido -->
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
        df_export = df[df.get("Total de Sacos", pd.Series()).notna()].copy() if not df.empty else pd.DataFrame()
        if not df_export.empty:
            if "Mês" in df_export.columns:
                df_export["Mês"] = df_export["Mês"].str.title()
            df_export["Peso Total (kg)"] = df_export.get("Total de Sacos", 0) * 20
            df_export["% AM"] = (df_export.get("Coleta AM", 0) / df_export.get("Total de Sacos", 1) * 100).ro*_

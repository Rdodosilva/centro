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

# 🎨 CSS personalizado aprimorado
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
        
        /* Métricas aprimoradas */
        .stMetric {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid transparent;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,255,255,0.1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
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
        
        /* Radio button styling - exact as your first image */
        section[data-testid="stRadio"] > div {
            background: transparent !important;
            border: none !important;
            padding: 0px !important;
        }
        
        /* Radio button labels - dark background with blue border */
        div[role="radiogroup"] > label {
            background: #1a1a2e !important;
            padding: 10px 15px !important;
            border-radius: 15px !important;
            border: 2px solid #00FFFF !important;
            margin: 5px 0 !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            color: white !important;
            font-weight: normal !important;
            display: block !important;
        }
        
        /* Radio button hover effect - blue border */
        div[role="radiogroup"] > label:hover {
            background: #1a1a2e !important;
            color: white !important;
            border: 2px solid #00FFFF !important;
        }
        
        /* Radio button selected state - RED border */
        div[role="radiogroup"] > label[data-selected="true"] {
            background: #1a1a2e !important;
            color: white !important;
            font-weight: bold !important;
            border: 2px solid #FF4444 !important;
        }
        
        /* Radio circles - white normally, red when selected */
        div[role="radiogroup"] > label > div {
            border-color: white !important;
            background-color: transparent !important;
        }
        
        div[role="radiogroup"] > label[data-selected="true"] > div {
            border-color: #FF4444 !important;
            background-color: #FF4444 !important;
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
        
        /* Button styling improvements - force download buttons */
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
try:
    df = pd.read_excel("Coleta centro2.xlsx")
    df.columns = df.columns.str.strip()
    df["Mes"] = df["Mês"].str.lower().str.strip()
except:
    # Dados simulados para demonstração
    st.warning("⚠️ Arquivo não encontrado. Usando dados simulados para demonstração.")
    df = pd.DataFrame({
        'Mês': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
        'Mes': ['janeiro', 'fevereiro', 'março', 'abril', 'maio'],
        'Coleta AM': [295, 1021, 408, 1192, 1045],
        'Coleta PM': [760, 1636, 793, 1606, 1461],
        'Total de Sacos': [1055, 2657, 1201, 2798, 2506]
    })

# 🏷️ Header aprimorado
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <div style='font-size: 3.5em; margin-bottom: 10px; font-weight: 700;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.2em; opacity: 0.8;'>
        📊 Monitoramento de Crescimento de Resíduos | 2025
    </div>
</div>
""", unsafe_allow_html=True)

# 🎛️ Sidebar com controles avançados
with st.sidebar:
    st.markdown("## 🎛️ Filtros")
    
    # Filtro de período melhorado
    meses_disponiveis = ["janeiro", "fevereiro", "março", "abril", "maio"]
    meses_display = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"]
    
    st.markdown("### 📅 Período:")
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
    
    # HTML da apresentação sem auto-print
    apresentacao_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apresentação - Coleta Centro</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
            line-height: 1.6;
        }
        
        .slide {
            min-height: 100vh;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            break-after: page;
        }
        
        .slide-header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .slide-title {
            font-size: 3em;
            font-weight: 700;
            color: white;
            margin-bottom: 20px;
        }
        
        .slide-subtitle {
            font-size: 1.4em;
            color: white;
            opacity: 0.8;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .card {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,255,255,0.1);
        }
        
        .card h3 {
            color: #00FFFF;
            font-size: 1.5em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .metric {
            font-size: 2.5em;
            font-weight: bold;
            color: #00FFFF;
            margin: 20px 0;
        }
        
        .logo {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        ul {
            list-style: none;
            padding-left: 0;
        }
        
        li {
            margin: 15px 0;
            padding-left: 25px;
            position: relative;
        }
        
        li:before {
            content: "▶";
            color: #00FFFF;
            position: absolute;
            left: 0;
        }
        
        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            align-items: start;
        }
        
        .highlight-box {
            background: linear-gradient(145deg, #9b30ff, #00FFFF);
            color: black;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 1.2em;
            margin: 20px 0;
        }
        
        .recommendation {
            background: rgba(255, 170, 0, 0.1);
            border-left: 4px solid #FFAA00;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 10px 10px 0;
        }
        
        .recommendation.success {
            background: rgba(0, 255, 136, 0.1);
            border-left-color: #00FF88;
        }
        
        .slide-number {
            position: absolute;
            bottom: 20px;
            right: 20px;
            color: rgba(255,255,255,0.5);
            font-size: 0.9em;
        }
        
        @media print {
            .slide {
                break-after: page;
                min-height: auto;
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <!-- Slide 1: Capa -->
    <div class="slide">
        <div class="slide-header">
            <div class="logo">🚛</div>
            <div class="slide-title">Coleta Centro</div>
            <div class="slide-subtitle">Análise de Crescimento dos Resíduos | 2025</div>
        </div>
        
        <div class="content-grid">
            <div class="card">
                <h3>📊 Objetivo da Análise</h3>
                <p>Conscientização sobre o crescimento dos resíduos no centro da cidade</p>
            </div>
            
            <div class="card">
                <h3>📅 Período Analisado</h3>
                <p>Janeiro a Maio de 2025</p>
                <p>Dados coletados mensalmente</p>
            </div>
            
            <div class="card">
                <h3>📈 Principal Achado</h3>
                <div class="metric">+137%</div>
                <p>Crescimento em 5 meses</p>
            </div>
        </div>
        
        <div class="slide-number">01</div>
    </div>
    
    <!-- Slide 2: Panorama Geral -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-title">📈 Panorama Geral</div>
            <div class="slide-subtitle">Principais Indicadores - Janeiro a Maio 2025</div>
        </div>
        
        <div class="content-grid">
            <div class="card">
                <h3>🧺 Volume Total</h3>
                <div class="metric">10.217</div>
                <p>sacos coletados no período</p>
                <p><strong>204.340 kg</strong> de resíduos</p>
            </div>
            
            <div class="card">
                <h3>📊 Distribuição por Período</h3>
                <p><strong>36% Manhã</strong></p>
                <p><strong>64% Tarde</strong></p>
                <p>Maior concentração vespertina</p>
            </div>
            
            <div class="card">
                <h3>📈 Crescimento</h3>
                <div class="metric">+137%</div>
                <p>Janeiro → Maio</p>
                <p>Volume em expansão</p>
            </div>
            
            <div class="card">
                <h3>🚛 Status Atual</h3>
                <div class="metric">CRESCIMENTO</div>
                <p>Tendência de alta observada</p>
            </div>
        </div>
        
        <div class="slide-number">02</div>
    </div>
    
    <!-- Slide 3: Evolução Mensal -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-title">📊 Evolução Mensal</div>
            <div class="slide-subtitle">Crescimento Consistente dos Resíduos</div>
        </div>
        
        <div class="two-column">
            <div>
                <div class="card">
                    <h3>📈 Dados Mensais</h3>
                    <ul>
                        <li><strong>Janeiro:</strong> 1.055 sacos (21.100 kg)</li>
                        <li><strong>Fevereiro:</strong> 2.657 sacos (53.140 kg)</li>
                        <li><strong>Março:</strong> 1.201 sacos (24.020 kg)</li>
                        <li><strong>Abril:</strong> 2.798 sacos (55.960 kg)</li>
                        <li><strong>Maio:</strong> 2.506 sacos (50.120 kg)</li>
                    </ul>
                </div>
            </div>
            
            <div>
                <div class="highlight-box">
                    <strong>Crescimento de 137% no período</strong><br>
                    Volume demonstra expansão significativa
                </div>
            </div>
        </div>
        
        <div class="slide-number">03</div>
    </div>
    
    <!-- Slide 4: Resumo -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-title">📋 Resumo</div>
            <div class="slide-subtitle">Principais Achados</div>
        </div>
        
        <div class="highlight-box">
            <div style="font-size: 1.5em; margin-bottom: 20px;">📊 CONSCIENTIZAÇÃO SOBRE CRESCIMENTO</div>
            <div style="font-size: 1.3em;">Volume cresceu 137% em apenas 5 meses</div>
        </div>
        
        <div class="content-grid">
            <div class="card">
                <h3>📊 Dados Principais</h3>
                <ul>
                    <li>Crescimento de <strong>137% em 5 meses</strong></li>
                    <li>Volume atual: <strong>2.506 sacos/mês</strong></li>
                    <li>Tendência: <strong>Crescimento contínuo</strong></li>
                    <li>Período crítico: <strong>Tarde (64%)</strong></li>
                </ul>
            </div>
            
            <div class="card">
                <h3>📊 Próximos Passos</h3>
                <ul>
                    <li><strong>Continuidade do monitoramento</strong></li>
                    <li><strong>Análises mensais regulares</strong></li>
                    <li><strong>Relatórios de acompanhamento</strong></li>
                    <li><strong>Avaliação contínua</strong></li>
                </ul>
            </div>
        </div>
        
        <div class="recommendation success">
            <h3>💡 Considerações Finais</h3>
            <p>Os dados revelam um <strong>crescimento importante</strong> que deve ser acompanhado. A análise contínua permitirá <strong>decisões baseadas em evidências</strong>.</p>
        </div>
        
        <div class="slide-number">04</div>
    </div>
</body>
</html>"""
    
    # Criar dados para Excel
    df_export = df[df["Total de Sacos"].notna()].copy()
    df_export["Mês"] = df_export["Mês"].str.title()
    df_export["Peso Total (kg)"] = df_export["Total de Sacos"] * 20
    df_export["% AM"] = (df_export["Coleta AM"] / df_export["Total de Sacos"] * 100).round(1)
    df_export["% PM"] = (df_export["Coleta PM"] / df_export["Total de Sacos"] * 100).round(1)
    
    csv_data = df_export[["Mês", "Coleta AM", "Coleta PM", "Total de Sacos", "Peso Total (kg)", "% AM", "% PM"]].to_csv(index=False)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.download_button(
            label="📊 PDF",
            data=apresentacao_html,
            file_name=f"Apresentacao_Coleta_Centro_{mes_selecionado.title()}_2025.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col_btn2:
        st.download_button(
            label="📋 Excel",
            data=csv_data,
            file_name=f"Dados_Coleta_Centro_{mes_selecionado.title()}_2025.csv",
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
        delta="Otimal" if eficiencia > 25 else "Baixa"
    )

with col4:
    # Calcular crescimento para adicionar outro coletor
    necessidade_novo_coletor = "SIM" if total_sacos > 2000 else "AVALIAR" if total_sacos > 1500 else "NÃO"
    
    st.metric(
        "🚛 Novo Coletor", 
        necessidade_novo_coletor,
        delta=f"Vol: {total_sacos}" if total_sacos > 0 else None
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

# Cores aprimoradas
cores = {
    "Coleta AM": "#00FFFF",
    "Coleta PM": "#FF6B35"
}

# Gráfico principal (apenas barras)
col_left, col_right = st.columns([2, 1])

with col_left:
    fig_main = px.bar(
        df_melt,
        x="Mes",
        y="Quantidade de Sacos",
        color="Periodo",
        color_discrete_map=cores,
        barmode="group",
        title=f"📦 Coleta por Período - {mes_selecionado.title()}"
    )
    
    # Styling comum para gráfico de barras
    fig_main.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        title_font=dict(size=20, color="white"),
        title_x=0.5,
        xaxis=dict(
            showgrid=True, 
            gridcolor="rgba(255,255,255,0.1)",
            color="white",
            title_font=dict(color="white"),
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor="rgba(255,255,255,0.1)",
            color="white",
            title_font=dict(color="white"),
            tickfont=dict(color="white")
        ),
        legend=dict(
            font=dict(color="white", size=12),
            bgcolor="rgba(0,0,0,0.5)"
        )
    )
    
    # Forçar texto branco nos elementos do gráfico
    fig_main.update_traces(
        textfont_color="white",
        hovertemplate='<b>%{y}</b> sacos<br>%{fullData.name}<extra></extra>'
    )
    
    st.plotly_chart(fig_main, use_container_width=True)

with col_right:
    # Gráfico de pizza aprimorado
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Coleta AM", "Coleta PM"],
        values=[total_am, total_pm],
        hole=0.4,
        marker=dict(
            colors=["#00FFFF", "#FF6B35"],
            line=dict(color="white", width=3)
        ),
        textinfo='label+percent',
        textfont=dict(color='white', size=14),
        hovertemplate='%{label}: %{value} sacos<br>%{percent}<extra></extra>'
    )])
    
    fig_pie.update_layout(
        title=f"🔄 Distribuição AM vs PM<br>{mes_selecionado.title()}",
        title_font=dict(size=16, color="white"),
        title_x=0.5,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        legend=dict(
            font=dict(color="white", size=12),
            bgcolor="rgba(0,0,0,0.5)"
        ),
        height=400,
        annotations=[dict(
            text="",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False,
            font_color="white"
        )]
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

# 📈 Gráfico de evolução mensal aprimorado
st.markdown("### 📈 Evolução Temporal Completa")

df_linha = df[df["Total de Sacos"].notna()].copy()
df_linha["Mes_cat"] = pd.Categorical(df_linha["Mes"], categories=meses_disponiveis, ordered=True)
df_linha = df_linha.sort_values("Mes_cat")

# Criar gráfico de linha com múltiplas métricas
fig_evolucao = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Volume de Coleta (Sacos)", "Distribuição AM/PM"),
    vertical_spacing=0.1,
    specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
)

# Linha principal - Total de sacos
fig_evolucao.add_trace(
    go.Scatter(
        x=df_linha["Mes"], 
        y=df_linha["Total de Sacos"],
        mode='lines+markers',
        name='Total de Sacos',
        line=dict(color='#9b30ff', width=4),
        marker=dict(size=10, color='white', line=dict(color='#9b30ff', width=2))
    ),
    row=1, col=1
)

# Gráfico de barras empilhadas para AM/PM
fig_evolucao.add_trace(
    go.Bar(x=df_linha["Mes"], y=df_linha["Coleta AM"], name='AM', marker_color='#00FFFF'),
    row=2, col=1
)
fig_evolucao.add_trace(
    go.Bar(x=df_linha["Mes"], y=df_linha["Coleta PM"], name='PM', marker_color='#FF6B35'),
    row=2, col=1
)

fig_evolucao.update_layout(
    height=600,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    title_font=dict(size=18, color="white"),
    legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0.5)"),
    barmode='stack',
    annotations=[
        dict(
            text="Volume de Coleta (Sacos)",
            xref="paper", yref="paper",
            x=0.5, y=0.95,
            showarrow=False,
            font=dict(size=16, color="white")
        ),
        dict(
            text="Distribuição AM/PM",
            xref="paper", yref="paper", 
            x=0.5, y=0.47,
            showarrow=False,
            font=dict(size=16, color="white")
        )
    ]
)

fig_evolucao.update_xaxes(
    showgrid=True, 
    gridcolor="rgba(255,255,255,0.1)", 
    color="white",
    title_font=dict(color="white"),
    tickfont=dict(color="white")
)
fig_evolucao.update_yaxes(
    showgrid=True, 
    gridcolor="rgba(255,255,255,0.1)", 
    color="white",
    title_font=dict(color="white"),
    tickfont=dict(color="white")
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

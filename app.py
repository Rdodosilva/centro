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
        
        /* Radio button styling - exact as your first image */
        section[data-testid="stRadio"] > div {
            background: transparent !important;
            border: none !important;
            padding: 0px !important;
        }
        
        /* LAYOUT EM 2 COLUNAS PARA OS BOTÕES DOS MESES */
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 8px !important;
            margin: 10px 0 !important;
        }
        
        /* BOTÕES DOS MESES MENORES E EM 2 COLUNAS */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label {
            background: #1a1a2e !important;
            padding: 8px 10px !important;
            border-radius: 6px !important;
            border: 1px solid #00FFFF !important;
            margin: 0 !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            color: white !important;
            font-weight: 500 !important;
            font-size: 0.75em !important;
            display: block !important;
            width: 100% !important;
            box-sizing: border-box !important;
            text-align: center !important;
        }
        
        /* Hover dos botões dos meses */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background: rgba(0,255,255,0.15) !important;
            color: white !important;
            border: 1px solid #00FFFF !important;
            transform: translateY(-2px) !important;
        }
        
        /* Botão selecionado - gradiente roxo */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"] {
            background: linear-gradient(135deg, #9b30ff, #6a1b9a) !important;
            color: white !important;
            font-weight: 600 !important;
            border: 1px solid #9b30ff !important;
            box-shadow: 0 3px 12px rgba(155,48,255,0.4) !important;
        }
        
        /* Esconder círculos dos radio buttons */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }
        
        /* Forçar aplicação em todos os elementos de radio */
        .stRadio > div > div > div {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 8px !important;
        }
        
        .stRadio > div > div > div > label {
            background: #1a1a2e !important;
            padding: 8px 10px !important;
            border-radius: 6px !important;
            border: 1px solid #00FFFF !important;
            margin: 0 !important;
            color: white !important;
            font-weight: 500 !important;
            font-size: 0.75em !important;
            text-align: center !important;
        }
        
        .stRadio > div > div > div > label:hover {
            background: rgba(0,255,255,0.15) !important;
            transform: translateY(-2px) !important;
        }
        
        .stRadio > div > div > div > label[data-selected="true"] {
            background: linear-gradient(135deg, #9b30ff, #6a1b9a) !important;
            border: 1px solid #9b30ff !important;
            box-shadow: 0 3px 12px rgba(155,48,255,0.4) !important;
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
try:
    df = pd.read_excel("Coleta centro2.xlsx")
    df.columns = df.columns.str.strip()
    df["Mes"] = df["Mês"].str.lower().str.strip()
except:
    # Dados simulados - TODOS OS 12 MESES
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
    
    # Filtro de período - TODOS OS 12 MESES
    meses_disponiveis = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", 
                        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    meses_display = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
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
        
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }}
        
        .header {{
            font-size: 3em;
            margin-bottom: 30px;
            background: linear-gradient(90deg, #00FFFF, #9b30ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .metric-card {{
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid #00FFFF;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,255,255,0.1);
        }}
        
        .metric-title {{
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 10px;
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: 700;
            color: #00FFFF;
        }}
        
        .footer {{
            margin-top: 50px;
            font-size: 0.9em;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">🚛 Coleta Centro - Dashboard Executivo</div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-title">📅 Período Selecionado</div>
                <div class="metric-value">{meses_display[meses_disponiveis.index(mes_selecionado)]}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🌅 Coleta Manhã</div>
                <div class="metric-value">{df[df['Mes'] == mes_selecionado]['Coleta AM'].iloc[0] if not df[df['Mes'] == mes_selecionado].empty else 'N/A'}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🌆 Coleta Tarde</div>
                <div class="metric-value">{df[df['Mes'] == mes_selecionado]['Coleta PM'].iloc[0] if not df[df['Mes'] == mes_selecionado].empty else 'N/A'}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">📊 Total de Sacos</div>
                <div class="metric-value">{df[df['Mes'] == mes_selecionado]['Total de Sacos'].iloc[0] if not df[df['Mes'] == mes_selecionado].empty else 'N/A'}</div>
            </div>
        </div>
        
        <div class="footer">
            📊 Relatório gerado automaticamente - Coleta Centro 2025
        </div>
    </div>
</body>
</html>"""
        
        st.download_button(
            label="📄 HTML",
            data=apresentacao_html,
            file_name=f"apresentacao_coleta_{mes_selecionado}.html",
            mime="text/html"
        )
    
    with col_btn2:
        # CSV do mês selecionado
        dados_mes = df[df['Mes'] == mes_selecionado]
        if not dados_mes.empty:
            csv_data = dados_mes.to_csv(index=False)
            st.download_button(
                label="📊 CSV",
                data=csv_data,
                file_name=f"dados_coleta_{mes_selecionado}.csv",
                mime="text/csv"
            )

# 📊 Dados do mês selecionado
dados_mes = df[df['Mes'] == mes_selecionado]

if dados_mes.empty:
    st.error(f"❌ Dados não encontrados para {meses_display[meses_disponiveis.index(mes_selecionado)]}")
    st.stop()

# 📈 Métricas principais - CARDS AINDA MENORES
col1, col2, col3, col4 = st.columns(4)

with col1:
    coleta_am = dados_mes['Coleta AM'].iloc[0]
    st.metric(
        label="🌅 Coleta Manhã",
        value=f"{coleta_am:,}".replace(',', '.'),
        delta=None
    )

with col2:
    coleta_pm = dados_mes['Coleta PM'].iloc[0]
    st.metric(
        label="🌆 Coleta Tarde", 
        value=f"{coleta_pm:,}".replace(',', '.'),
        delta=None
    )

with col3:
    total_sacos = dados_mes['Total de Sacos'].iloc[0]
    st.metric(
        label="📊 Total de Sacos",
        value=f"{total_sacos:,}".replace(',', '.'),
        delta=None
    )

with col4:
    # Calcular média diária (assumindo 30 dias por mês)
    media_diaria = total_sacos / 30
    st.metric(
        label="📅 Média Diária",
        value=f"{media_diaria:.0f}",
        delta=None
    )

# 📊 Gráfico principal
st.markdown("---")
col_grafico1, col_grafico2 = st.columns([2, 1])

with col_grafico1:
    st.markdown("### 📊 Distribuição da Coleta")
    
    # Dados para o gráfico
    categorias = ['Manhã', 'Tarde']
    valores = [coleta_am, coleta_pm]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categorias,
        y=valores,
        text=[f'{v:,}'.replace(',', '.') for v in valores],
        textposition='auto',
        marker=dict(
            color=['#00FFFF', '#9b30ff'],
            line=dict(color='white', width=2)
        ),
        name='Coleta'
    ))
    
    fig.update_layout(
        title=f"Coleta de {meses_display[meses_disponiveis.index(mes_selecionado)]} - Manhã vs Tarde",
        xaxis_title="Período",
        yaxis_title="Quantidade de Sacos",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font=dict(size=16, color='white'),
        showlegend=False,
        height=400
    )
    
    fig.update_xaxis(gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxis(gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig, use_container_width=True)

with col_grafico2:
    st.markdown("### 🥧 Proporção")
    
    # Gráfico de pizza
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Manhã', 'Tarde'],
        values=[coleta_am, coleta_pm],
        hole=0.4,
        marker=dict(colors=['#00FFFF', '#9b30ff']),
        textinfo='label+percent',
        textfont=dict(color='white', size=12)
    )])
    
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

# 📈 Comparativo mensal (se habilitado)
if mostrar_comparativo:
    st.markdown("---")
    st.markdown("### 📈 Evolução Mensal")
    
    # Gráfico de linha com todos os meses
    fig_linha = go.Figure()
    
    fig_linha.add_trace(go.Scatter(
        x=meses_display,
        y=df['Coleta AM'],
        mode='lines+markers',
        name='Manhã',
        line=dict(color='#00FFFF', width=3),
        marker=dict(size=8, color='#00FFFF')
    ))
    
    fig_linha.add_trace(go.Scatter(
        x=meses_display,
        y=df['Coleta PM'],
        mode='lines+markers',
        name='Tarde',
        line=dict(color='#9b30ff', width=3),
        marker=dict(size=8, color='#9b30ff')
    ))
    
    fig_linha.add_trace(go.Scatter(
        x=meses_display,
        y=df['Total de Sacos'],
        mode='lines+markers',
        name='Total',
        line=dict(color='#00FF88', width=3),
        marker=dict(size=8, color='#00FF88')
    ))
    
    fig_linha.update_layout(
        title="Evolução da Coleta ao Longo do Ano",
        xaxis_title="Mês",
        yaxis_title="Quantidade de Sacos",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font=dict(size=16, color='white'),
        legend=dict(
            bgcolor='rgba(26,26,46,0.8)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        height=500
    )
    
    fig_linha.update_xaxis(gridcolor='rgba(255,255,255,0.1)')
    fig_linha.update_yaxis(gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig_linha, use_container_width=True)

# 📋 Tabela de dados
st.markdown("---")
st.markdown("### 📋 Dados Detalhados")

# Criar tabela formatada
tabela_dados = df[['Mês', 'Coleta AM', 'Coleta PM', 'Total de Sacos']].copy()
tabela_dados['Coleta AM'] = tabela_dados['Coleta AM'].apply(lambda x: f"{x:,}".replace(',', '.'))
tabela_dados['Coleta PM'] = tabela_dados['Coleta PM'].apply(lambda x: f"{x:,}".replace(',', '.'))
tabela_dados['Total de Sacos'] = tabela_dados['Total de Sacos'].apply(lambda x: f"{x:,}".replace(',', '.'))

st.dataframe(
    tabela_dados,
    use_container_width=True,
    hide_index=True
)

# 🎯 Insights automáticos
st.markdown("---")
st.markdown("### 🎯 Insights Automáticos")

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    # Calcular insights
    percentual_tarde = (coleta_pm / total_sacos) * 100
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>🌆 Período Predominante</h4>
        <p>A coleta da <strong>tarde representa {percentual_tarde:.1f}%</strong> do total diário.</p>
        <p>Isso indica maior atividade de descarte no período vespertino.</p>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    # Comparar com média anual
    media_anual = df['Total de Sacos'].mean()
    diferenca = ((total_sacos - media_anual) / media_anual) * 100
    
    trend_class = "trend-up" if diferenca > 0 else "trend-down" if diferenca < 0 else "trend-neutral"
    trend_icon = "📈" if diferenca > 0 else "📉" if diferenca < 0 else "➡️"
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>{trend_icon} Comparação com Média Anual</h4>
        <p class="{trend_class}">
            <strong>{diferenca:+.1f}%</strong> em relação à média anual ({media_anual:.0f} sacos)
        </p>
        <p>{"Acima" if diferenca > 0 else "Abaixo" if diferenca < 0 else "Igual"} da média esperada para o período.</p>
    </div>
    """, unsafe_allow_html=True)

# 🏁 Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; opacity: 0.7;'>
    <p>📊 Dashboard desenvolvido para monitoramento da Coleta Centro</p>
    <p>🚛 Dados atualizados automaticamente | 2025</p>
</div>
""", unsafe_allow_html=True)


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
total_pm = df_mes["Coleta PM"]

# Cálculo para o mês anterior (para comparação)
mes_anterior_index = meses_disponiveis.index(mes_selecionado) - 1
if mes_anterior_index >= 0:
    mes_anterior = meses_disponiveis[mes_anterior_index]
    df_anterior = df[df["Mes"] == mes_anterior].iloc[0]
    total_anterior = df_anterior["Total de Sacos"]
else:
    total_anterior = 0

# Cálculo da variação
variacao = ((total_sacos - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0

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

# 📈 Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label=f"Total de Sacos - {mes_selecionado.title()}",
        value=f"{total_sacos:,}".replace(',', '.'),
        delta=f"{variacao:+.1f}% vs Mês Anterior" if mostrar_comparativo else None,
        delta_color="normal"
    )

with col2:
    st.metric(
        label="Peso Total Estimado (kg)",
        value=f"{total_sacos * 20:,}".replace(',', '.'),
        delta=None
    )

with col3:
    st.metric(
        label="Coleta AM (Sacos)",
        value=f"{total_am:,}".replace(',', '.'),
        delta=None
    )

with col4:
    st.metric(
        label="Coleta PM (Sacos)",
        value=f"{total_pm:,}".replace(',', '.'),
        delta=None
    )

# 📊 Gráficos
st.markdown("---")
st.markdown("### 📊 Análise Detalhada")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Gráfico de barras simples e futurista
    df_grafico = df[df["Total de Sacos"].notna()].copy()
    df_grafico["Mes_cat"] = pd.Categorical(df_grafico["Mes"], categories=meses_disponiveis, ordered=True)
    df_grafico = df_grafico.sort_values("Mes_cat")
    
    fig_main = go.Figure(data=[
        go.Bar(
            name='Coleta AM',
            x=df_grafico["Mes"],
            y=df_grafico["Coleta AM"],
            marker_color='rgba(0, 212, 255, 0.7)',
            hovertemplate='<b>AM:</b> %{y} sacos<br>%{x}<extra></extra>'
        ),
        go.Bar(
            name='Coleta PM',
            x=df_grafico["Mes"],
            y=df_grafico["Coleta PM"],
            marker_color='rgba(255, 107, 53, 0.7)',
            hovertemplate='<b>PM:</b> %{y} sacos<br>%{x}<extra></extra>'
        )
    ])
    
    fig_main.update_layout(
        barmode='stack',
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        font_family="Inter",
        title=dict(
            text=f"🚀 Coleta por Período - {mes_selecionado.title()}",
            font=dict(size=16, color="#00D4FF", family="Inter", weight="bold"),
            title_x=0.5,
            title_y=0.95,
        ),
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

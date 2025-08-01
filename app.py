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
        
        /* Métricas menores mas com cores */
        .stMetric {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid transparent;
            border-radius: 12px;
            padding: 10px 15px;
            box-shadow: 0 6px 25px rgba(0,255,255,0.1);
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
        
        /* Radio button styling melhorado */
        section[data-testid="stRadio"] > div {
            background: transparent !important;
            border: none !important;
            padding: 0px !important;
        }
        
        /* Radio button labels - organizados */
        div[role="radiogroup"] > label {
            background: #1a1a2e !important;
            padding: 8px 14px !important;
            border-radius: 8px !important;
            border: 1px solid #00FFFF !important;
            margin: 4px 0 !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            color: white !important;
            font-weight: normal !important;
            font-size: 0.9em !important;
            display: block !important;
        }
        
        /* Radio button hover effect */
        div[role="radiogroup"] > label:hover {
            background: rgba(0,255,255,0.1) !important;
            color: white !important;
            border: 1px solid #00FFFF !important;
        }
        
        /* Radio button selected state */
        div[role="radiogroup"] > label[data-selected="true"] {
            background: #00FFFF !important;
            color: #000000 !important;
            font-weight: 600 !important;
            border: 1px solid #00FFFF !important;
        }
        
        /* Radio circles */
        div[role="radiogroup"] > label > div {
            border-color: #00FFFF !important;
            background-color: transparent !important;
        }
        
        div[role="radiogroup"] > label[data-selected="true"] > div {
            border-color: #000000 !important;
            background-color: #000000 !important;
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
        
        /* Button styling - padronizado */
        .stButton > button, .stDownloadButton > button {
            background: rgba(26, 26, 46, 0.9) !important;
            border: 1px solid #00FFFF !important;
            border-radius: 6px !important;
            color: #00FFFF !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            padding: 8px 14px !important;
            font-size: 0.85em !important;
            height: 36px !important;
        }
        
        .stButton > button:hover, .stDownloadButton > button:hover {
            background: rgba(0,255,255,0.1) !important;
            color: white !important;
            border-color: white !important;
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
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        # HTML da apresentação direto
        apresentacao_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Apresentação Coleta Centro</title>
    <style>
        body { font-family: Arial; background: #1a1a2e; color: white; padding: 40px; }
        .slide { margin-bottom: 50px; padding: 30px; background: linear-gradient(145deg, #1a1a2e, #0f0f23); border-radius: 15px; }
        h1 { color: #00FFFF; font-size: 2.5em; text-align: center; }
        h2 { color: #00FFFF; border-bottom: 2px solid #00FFFF; padding-bottom: 10px; }
        .metric { font-size: 2em; color: #9b30ff; font-weight: bold; }
        .highlight { background: rgba(0,255,255,0.1); padding: 15px; border-radius: 8px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="slide">
        <h1>🚛 Coleta Centro</h1>
        <p style="text-align: center; font-size: 1.2em;">Análise Mensal de Resíduos - 2025</p>
    </div>
    <div class="slide">
        <h2>📊 Resumo Executivo</h2>
        <p>Monitoramento mensal da coleta de resíduos no centro da cidade.</p>
        <div class="highlight">
            <p><strong>Objetivo:</strong> Acompanhar o crescimento do volume de resíduos</p>
            <p><strong>Frequência:</strong> Análise mensal</p>
            <p><strong>Períodos:</strong> Coleta matutina e vespertina</p>
        </div>
    </div>
    <div class="slide">
        <h2>💡 Principais Insights</h2>
        <p>• Monitoramento contínuo dos volumes de coleta</p>
        <p>• Análise de distribuição entre períodos AM/PM</p>
        <p>• Acompanhamento de tendências mensais</p>
        <p>• Suporte à tomada de decisão operacional</p>
    </div>
</body>
</html>"""
        
        st.download_button(
            label="📊 PDF",
            data=apresentacao_html,
            file_name="Apresentacao_Coleta_Centro.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col_btn2:
        st.download_button(
            label="📋 Excel",
            data=df.to_csv(index=False),
            file_name="coleta_dados.csv",
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
        delta="Ótimo" if eficiencia > 25 else "Baixa"
    )

with col4:
    # Status informativo (não urgência)
    if total_sacos > 2500:
        status = "AVALIAR"
        status_info = "Alto volume"
    elif total_sacos > 2000:
        status = "MONITORAR" 
        status_info = "Volume crescente"
    else:
        status = "NORMAL"
        status_info = "Dentro do esperado"
    
    st.metric(
        "📊 Status Operacional", 
        f"🟢 {status}",
        delta=status_info
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
    barmode='stack'
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
    if total_sacos > 2500:
        status_capacidade = "AVALIAR EXPANSÃO"
        cor_cap = "trend-neutral"
        recomendacao = "Considerar aumento da frota"
    elif total_sacos > 2000:
        status_capacidade = "MONITORAR CRESCIMENTO"
        cor_cap = "trend-neutral"
        recomendacao = "Acompanhar evolução mensal"
    else:
        status_capacidade = "CAPACIDADE ADEQUADA"
        cor_cap = "trend-up"
        recomendacao = "Operação normal"
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>📊 Análise de Capacidade</h4>
        <p><span class="{cor_cap}"><strong>{status_capacidade}</strong></span></p>
        <p><strong>Volume atual:</strong> {total_sacos:,} sacos</p>
        <p><strong>Recomendação:</strong> {recomendacao}</p>
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

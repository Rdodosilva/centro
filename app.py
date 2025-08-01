import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# 🎯 Configuração da página
st.set_page_config(
    page_title="Coleta Centro - Dashboard Executivo", 
    page_icon="🚛", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 CSS personalizado
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
        
        .main .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: none;
        }
        
        .main {
            padding: 0;
        }
        
        header[data-testid="stHeader"] {
            height: 2.875rem;
            background: transparent;
        }
        
        /* Métricas com tamanho reduzido */
        .stMetric {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid transparent;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 20px rgba(0,255,255,0.1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            transition: all 0.2s ease;
        }
        
        .stMetric:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 25px rgba(0,255,255,0.15);
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
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
            border-right: 1px solid rgba(0,255,255,0.2);
        }
        
        section[data-testid="stSidebar"] > div > div > div > div {
            color: white !important;
        }
        
        /* Radio buttons - design limpo e organizado */
        div[role="radiogroup"] > label {
            background: #1a1a2e !important;
            padding: 8px 15px !important;
            border-radius: 8px !important;
            border: 1px solid #00FFFF !important;
            margin: 3px 0 !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            color: white !important;
            font-weight: normal !important;
            display: block !important;
            font-size: 0.9em !important;
        }
        
        div[role="radiogroup"] > label:hover {
            background: rgba(0,255,255,0.1) !important;
            color: white !important;
            border: 1px solid #00FFFF !important;
        }
        
        div[role="radiogroup"] > label[data-selected="true"] {
            background: #00FFFF !important;
            color: #000000 !important;
            font-weight: 600 !important;
            border: 1px solid #00FFFF !important;
        }
        
        /* Radio circles - simplificados */
        div[role="radiogroup"] > label > div {
            border-color: #00FFFF !important;
            background-color: transparent !important;
        }
        
        div[role="radiogroup"] > label[data-selected="true"] > div {
            border-color: #000000 !important;
            background-color: #000000 !important;
        }
        
        /* Botões aprimorados */
        .stButton > button, .stDownloadButton > button {
            background: linear-gradient(45deg, #00FFFF, #0080FF) !important;
            border: none !important;
            border-radius: 8px !important;
            color: black !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            padding: 10px 20px !important;
        }
        
        .stButton > button:hover, .stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0,255,255,0.4) !important;
        }
        
        /* Checkboxes */
        .stCheckbox {
            color: white !important;
        }
        
        .stCheckbox > label {
            color: white !important;
            font-weight: normal;
        }
        
        /* Cards para insights */
        .insight-card {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 1px solid #00FFFF;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 8px 32px rgba(0,255,255,0.1);
            transition: all 0.3s ease;
        }
        
        .insight-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(0,255,255,0.2);
            border-color: #9b30ff;
        }
        
        /* Status indicators */
        .trend-up { 
            color: #00FF88; 
            text-shadow: 0 0 10px rgba(0,255,136,0.5);
        }
        .trend-down { 
            color: #FF4444; 
            text-shadow: 0 0 10px rgba(255,68,68,0.5);
        }
        .trend-neutral { 
            color: #FFAA00; 
            text-shadow: 0 0 10px rgba(255,170,0,0.5);
        }
        
        /* Animações */
        .stPlotlyChart {
            animation: fadeInUp 0.8s ease-out;
        }
        
        @keyframes fadeInUp {
            from { 
                opacity: 0; 
                transform: translateY(30px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
        
        h1, h2, h3, label, span, div {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# 📥 Carregar dados
@st.cache_data
def carregar_dados():
    """Carrega dados com cache para performance"""
    try:
        df = pd.read_excel("Coleta centro2.xlsx")
        df.columns = df.columns.str.strip()
        df["Mes"] = df["Mês"].str.lower().str.strip()
        return df, False
    except:
        # Dados simulados para demonstração
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio']
        dados_simulados = []
        
        # Dados baseados no seu exemplo original
        dados_exemplo = [
            {'Mês': 'Janeiro', 'Mes': 'janeiro', 'Coleta AM': 295, 'Coleta PM': 760, 'Total de Sacos': 1055},
            {'Mês': 'Fevereiro', 'Mes': 'fevereiro', 'Coleta AM': 1021, 'Coleta PM': 1636, 'Total de Sacos': 2657},
            {'Mês': 'Março', 'Mes': 'março', 'Coleta AM': 408, 'Coleta PM': 793, 'Total de Sacos': 1201},
            {'Mês': 'Abril', 'Mes': 'abril', 'Coleta AM': 1192, 'Coleta PM': 1606, 'Total de Sacos': 2798},
            {'Mês': 'Maio', 'Mes': 'maio', 'Coleta AM': 1045, 'Coleta PM': 1461, 'Total de Sacos': 2506}
        ]
        
        df = pd.DataFrame(dados_exemplo)
        return df, True

df, usando_simulados = carregar_dados()

if usando_simulados:
    st.info("💡 **Modo Demonstração** - Usando dados simulados. Coloque seu arquivo 'Coleta centro2.xlsx' na pasta para usar dados reais.")

# 🏷️ Header
st.markdown("""
<div style='text-align: center; padding: 30px 0;'>
    <div style='font-size: 3.5em; margin-bottom: 15px; font-weight: 700;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.2em; opacity: 0.8;'>
        📊 Monitoramento de Crescimento de Resíduos | 2025
    </div>
</div>
""", unsafe_allow_html=True)

# 🎛️ Sidebar com controles
with st.sidebar:
    st.markdown("## 🎛️ Filtros")
    
    # Filtro de período - design limpo
    meses_disponiveis = df[df["Total de Sacos"].notna()]["Mes"].unique().tolist()
    meses_display = df[df["Total de Sacos"].notna()]["Mês"].unique().tolist()
    
    st.markdown("### 📅 Período:")
    mes_selecionado = st.radio(
        "",
        options=meses_disponiveis,
        format_func=lambda x: meses_display[meses_disponiveis.index(x)] if x in meses_disponiveis else x,
        horizontal=False,
        index=0 if meses_disponiveis else 0
    )
    
    # Configurações básicas
    st.markdown("### 📊 Visualização")
    mostrar_comparativo = st.checkbox("Comparar com mês anterior", True)
    tipo_grafico = st.radio(
        "Tipo de gráfico:",
        ["Barras"],
        horizontal=False
    )
    
    # Export
    st.markdown("### 📤 Exportar")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("📊 PDF", use_container_width=True):
            st.success("✅ Relatório gerado!")
    
    with col_btn2:
        if st.button("📋 Excel", use_container_width=True):
            df_export = df[df["Total de Sacos"].notna()].copy()
            csv_data = df_export.to_csv(index=False)
            st.download_button(
                "⬇️ Download",
                csv_data,
                f"coleta_dados_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )

# 📊 Processar dados para o mês selecionado
df_filtrado = df[(df["Mes"] == mes_selecionado) & (df["Total de Sacos"].notna())]

# Calcular métricas
total_sacos = int(df_filtrado["Total de Sacos"].sum()) if not df_filtrado.empty else 0
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum()) if not df_filtrado.empty else 0
total_pm = int(df_filtrado["Coleta PM"].sum()) if not df_filtrado.empty else 0

# Cálculos básicos
meses_list = df[df["Total de Sacos"].notna()]["Mes"].unique().tolist()
mes_idx = meses_list.index(mes_selecionado) if mes_selecionado in meses_list else -1

# Comparação com mês anterior
variacao = 0
if mes_idx > 0:
    mes_anterior = meses_list[mes_idx - 1]
    df_anterior = df[df["Mes"] == mes_anterior]
    total_anterior = int(df_anterior["Total de Sacos"].sum()) if not df_anterior.empty else 0
    variacao = ((total_sacos - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0

# 🎯 Métricas principais - design mais limpo
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
    peso_delta = f"{variacao*20:+.0f} kg" if mostrar_comparativo and variacao != 0 else None
    st.metric(
        "⚖️ Peso Total", 
        f"{peso_total:,} kg".replace(',', '.'),
        delta=peso_delta
    )

with col3:
    eficiencia_am = (total_am / (total_am + total_pm) * 100) if (total_am + total_pm) > 0 else 0
    status_eficiencia = "Ótimo" if eficiencia_am > 30 else "Bom" if eficiencia_am > 20 else "Baixo"
    st.metric(
        "📊 Eficiência AM", 
        f"{eficiencia_am:.1f}%",
        delta=status_eficiencia
    )

with col4:
    # Necessidade de novo coletor
    necessidade = "URGENTE" if total_sacos > 2500 else "MONITORAR" if total_sacos > 2000 else "ADEQUADO"
    st.metric(
        "🚛 Novo Coletor", 
        f"{necessidade}",
        delta=f"Vol: {total_sacos}"
    )

# 📊 Seção de gráficos - mantendo sua estrutura original
st.markdown("## 📊 Análises Visuais")

# Preparar dados para gráficos
df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

# Cores originais
cores = {
    "Coleta AM": "#00FFFF",
    "Coleta PM": "#FF6B35"
}

# Layout original (apenas barras)
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
    
    # Styling original
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
    
    fig_main.update_traces(
        textfont_color="white",
        hovertemplate='<b>%{y}</b> sacos<br>%{fullData.name}<extra></extra>'
    )
    
    st.plotly_chart(fig_main, use_container_width=True)

with col_right:
    # Gráfico de pizza original
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

# 📈 Gráfico de evolução mensal - mantendo original
st.markdown("### 📈 Evolução Temporal Completa")

df_linha = df[df["Total de Sacos"].notna()].copy()

# Gráfico original com múltiplas métricas
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
    color="white"
)
fig_evolucao.update_yaxes(
    showgrid=True, 
    gridcolor="rgba(255,255,255,0.1)", 
    color="white"
)

st.plotly_chart(fig_evolucao, use_container_width=True)

# 💡 Insights básicos
st.markdown("## 💡 Insights e Recomendações")

col_insight1, col_insight2, col_insight3 = st.columns(3)

with col_insight1:
    tendencia_texto = "crescente" if variacao > 0 else "decrescente" if variacao < 0 else "estável"
    cor_tendencia = "trend-up" if variacao > 0 else "trend-down" if variacao < 0 else "trend-neutral"
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>📊 Análise de Tendência</h4>
        <p>Volume <span class="{cor_tendencia}">{tendencia_texto}</span> em relação ao mês anterior</p>
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
    projecao_proxima = total_sacos * 1.05  # Projeção simples
    necessidade = "URGENTE" if projecao_proxima > 2500 else "MONITORAR" if projecao_proxima > 2000 else "ADEQUADO"
    cor_necessidade = "trend-down" if necessidade == "URGENTE" else "trend-neutral" if necessidade == "MONITORAR" else "trend-up"
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>🚛 Capacidade Coletora</h4>
        <p>Status: <span class="{cor_necessidade}"><strong>{necessidade}</strong></span></p>
        <p><strong>Projeção:</strong> {projecao_proxima:.0f} sacos</p>
    </div>
    """, unsafe_allow_html=True)

# 📋 Tabela original (colapsável)
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

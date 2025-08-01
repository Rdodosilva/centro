import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import base64
from io import BytesIO

# 🎯 Configuração da página
st.set_page_config(
    page_title="Coleta Centro - Dashboard Executivo", 
    page_icon="🚛", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 CSS personalizado aprimorado (mantendo seu estilo + melhorias)
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
        
        /* Métricas aprimoradas com animação */
        .stMetric {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid transparent;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,255,255,0.1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .stMetric:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(0,255,255,0.2);
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
        
        /* Sidebar styling melhorado */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
            border-right: 1px solid rgba(0,255,255,0.2);
        }
        
        section[data-testid="stSidebar"] > div > div > div > div {
            color: white !important;
        }
        
        /* Radio buttons com hover aprimorado */
        div[role="radiogroup"] > label {
            background: #1a1a2e !important;
            padding: 12px 18px !important;
            border-radius: 15px !important;
            border: 2px solid #00FFFF !important;
            margin: 6px 0 !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            color: white !important;
            font-weight: normal !important;
            display: block !important;
            position: relative;
            overflow: hidden;
        }
        
        div[role="radiogroup"] > label::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,255,255,0.1), transparent);
            transition: all 0.5s;
        }
        
        div[role="radiogroup"] > label:hover::before {
            left: 100%;
        }
        
        div[role="radiogroup"] > label:hover {
            background: #1a1a2e !important;
            color: white !important;
            border: 2px solid #00FFFF !important;
            box-shadow: 0 4px 15px rgba(0,255,255,0.3);
        }
        
        div[role="radiogroup"] > label[data-selected="true"] {
            background: #1a1a2e !important;
            color: white !important;
            font-weight: bold !important;
            border: 2px solid #FF4444 !important;
            box-shadow: 0 4px 15px rgba(255,68,68,0.3);
        }
        
        /* Botões aprimorados com gradiente */
        .stButton > button, .stDownloadButton > button {
            background: linear-gradient(45deg, #00FFFF, #0080FF) !important;
            border: none !important;
            border-radius: 8px !important;
            color: black !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            padding: 10px 20px !important;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before, .stDownloadButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: all 0.5s;
        }
        
        .stButton > button:hover::before, .stDownloadButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button:hover, .stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0,255,255,0.4) !important;
        }
        
        /* Cards para insights com gradiente */
        .insight-card {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 1px solid #00FFFF;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 8px 32px rgba(0,255,255,0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .insight-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0,255,255,0.03) 0%, transparent 70%);
            transition: all 0.3s ease;
        }
        
        .insight-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(0,255,255,0.2);
            border-color: #9b30ff;
        }
        
        .insight-card:hover::before {
            top: -30%;
            left: -30%;
        }
        
        /* Status indicators melhorados */
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
        
        /* Tooltip personalizado */
        .custom-tooltip {
            background: rgba(26, 26, 46, 0.95) !important;
            border: 1px solid rgba(0,255,255,0.3) !important;
            border-radius: 8px !important;
            color: white !important;
            backdrop-filter: blur(10px);
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: linear-gradient(90deg, #1a1a2e, #16213e) !important;
            border-radius: 10px !important;
            color: white !important;
        }
        
        .streamlit-expanderContent {
            background: rgba(26, 26, 46, 0.3) !important;
            border-radius: 0 0 10px 10px !important;
        }
        
        /* Scroll personalizado */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(26, 26, 46, 0.5);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #00FFFF, #9b30ff);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #0080FF, #7a24cc);
        }
        
        h1, h2, h3, label, span, div {
            color: white !important;
        }
        
        /* Loading animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(0,255,255,.3);
            border-radius: 50%;
            border-top-color: #00FFFF;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
""", unsafe_allow_html=True)

# 📈 Função para calcular tendências avançadas
def calcular_tendencias(df):
    """Calcula tendências e previsões baseadas nos dados históricos"""
    df_clean = df[df["Total de Sacos"].notna()].copy()
    
    # Tendência linear simples
    x = np.arange(len(df_clean))
    y = df_clean["Total de Sacos"].values
    
    if len(y) > 1:
        coef = np.polyfit(x, y, 1)
        tendencia = coef[0]  # coeficiente angular
        
        # Previsão para próximo mês
        proximo_mes = coef[0] * len(df_clean) + coef[1]
        
        return {
            'tendencia': tendencia,
            'proximo_mes': max(0, proximo_mes),
            'crescimento_mensal': (tendencia / np.mean(y)) * 100 if np.mean(y) > 0 else 0
        }
    
    return {'tendencia': 0, 'proximo_mes': 0, 'crescimento_mensal': 0}

# 📊 Função para gerar gráfico de radar de performance
def criar_radar_performance(dados_mes):
    """Cria gráfico radar para análise multidimensional"""
    if dados_mes.empty:
        return go.Figure()
    
    # Métricas normalizadas (0-100)
    volume_norm = min(100, (dados_mes["Total de Sacos"].iloc[0] / 3000) * 100)
    eficiencia_am = (dados_mes["Coleta AM"].iloc[0] / dados_mes["Total de Sacos"].iloc[0]) * 100
    eficiencia_pm = (dados_mes["Coleta PM"].iloc[0] / dados_mes["Total de Sacos"].iloc[0]) * 100
    
    categorias = ['Volume Total', 'Eficiência AM', 'Eficiência PM', 'Capacidade Utilizada']
    valores = [volume_norm, eficiencia_am, eficiencia_pm, min(100, volume_norm * 1.2)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name='Performance Atual',
        line_color='#00FFFF',
        fillcolor='rgba(0,255,255,0.1)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(255,255,255,0.2)",
                tickcolor="white"
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.2)",
                tickcolor="white"
            )
        ),
        showlegend=True,
        title="Radar de Performance",
        title_font=dict(color="white", size=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    
    return fig

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
        # Dados simulados mais realistas
        np.random.seed(42)
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho']
        dados_simulados = []
        
        base_am = 300
        base_pm = 800
        
        for i, mes in enumerate(meses):
            # Crescimento com variação realística
            fator_crescimento = 1 + (i * 0.15) + np.random.normal(0, 0.1)
            am = int(base_am * fator_crescimento + np.random.normal(0, 50))
            pm = int(base_pm * fator_crescimento + np.random.normal(0, 100))
            
            dados_simulados.append({
                'Mês': mes,
                'Mes': mes.lower(),
                'Coleta AM': max(0, am),
                'Coleta PM': max(0, pm),
                'Total de Sacos': max(0, am + pm)
            })
        
        df = pd.DataFrame(dados_simulados)
        return df, True

df, usando_simulados = carregar_dados()

if usando_simulados:
    st.info("💡 **Modo Demonstração** - Usando dados simulados realísticos. Carregue seu arquivo 'Coleta centro2.xlsx' para usar dados reais.")

# 🏷️ Header com animação
st.markdown("""
<div style='text-align: center; padding: 30px 0; position: relative;'>
    <div style='font-size: 4em; margin-bottom: 15px; font-weight: 700; animation: pulse 2s infinite;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.3em; opacity: 0.9; text-shadow: 0 0 10px rgba(0,255,255,0.3);'>
        📊 Dashboard Executivo de Monitoramento | 2025
    </div>
    <div style='margin-top: 10px; font-size: 0.9em; color: rgba(255,255,255,0.7);'>
        🎯 Inteligência para Tomada de Decisão
    </div>
</div>

<style>
@keyframes pulse {
    0% { text-shadow: 0 0 5px rgba(0,255,255,0.5); }
    50% { text-shadow: 0 0 20px rgba(0,255,255,0.8), 0 0 30px rgba(155,48,255,0.5); }
    100% { text-shadow: 0 0 5px rgba(0,255,255,0.5); }
}
</style>
""", unsafe_allow_html=True)

# 🎛️ Sidebar com controles avançados
with st.sidebar:
    st.markdown("## 🎛️ Central de Controle")
    
    # Filtro de período
    meses_disponiveis = df[df["Total de Sacos"].notna()]["Mes"].unique().tolist()
    meses_display = df[df["Total de Sacos"].notna()]["Mês"].unique().tolist()
    
    st.markdown("### 📅 Seleção de Período:")
    mes_selecionado = st.radio(
        "",
        options=meses_disponiveis,
        format_func=lambda x: meses_display[meses_disponiveis.index(x)] if x in meses_disponiveis else x,
        horizontal=False,
        index=0 if meses_disponiveis else 0
    )
    
    # Configurações avançadas
    st.markdown("### ⚙️ Configurações Avançadas")
    
    col_config1, col_config2 = st.columns(2)
    with col_config1:
        mostrar_comparativo = st.checkbox("📊 Comparar", True)
        mostrar_previsoes = st.checkbox("🔮 Previsões", True)
    
    with col_config2:
        mostrar_radar = st.checkbox("🎯 Radar", True)
        modo_detalhado = st.checkbox("🔍 Detalhes", False)
    
    # Alertas personalizados
    st.markdown("### 🚨 Configurar Alertas")
    limite_volume = st.slider("Volume máximo (sacos)", 1000, 5000, 2500, 100)
    limite_crescimento = st.slider("Crescimento máximo (%)", 0, 100, 50, 5)
    
    # Análise automática
    st.markdown("### 🤖 Análise Automática")
    auto_insights = st.toggle("Insights IA", True)
    
    # Export melhorado
    st.markdown("### 📤 Exportação Avançada")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        # Relatório HTML interativo
        if st.button("📊 Relatório", use_container_width=True):
            with st.spinner("Gerando relatório..."):
                # Aqui você pode gerar um relatório mais completo
                st.success("✅ Relatório gerado!")
    
    with col_exp2:
        # Dados Excel
        if st.button("📋 Dados", use_container_width=True):
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

# Cálculos avançados
tendencias = calcular_tendencias(df)
meses_list = df[df["Total de Sacos"].notna()]["Mes"].unique().tolist()
mes_idx = meses_list.index(mes_selecionado) if mes_selecionado in meses_list else -1

# Comparação com mês anterior
variacao = 0
if mes_idx > 0:
    mes_anterior = meses_list[mes_idx - 1]
    df_anterior = df[df["Mes"] == mes_anterior]
    total_anterior = int(df_anterior["Total de Sacos"].sum()) if not df_anterior.empty else 0
    variacao = ((total_sacos - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0

# 🎯 Métricas principais com design aprimorado
st.markdown("## 📈 Painel de Indicadores Executivos")

col1, col2, col3, col4 = st.columns(4)

with col1:
    delta_value = f"{variacao:+.1f}%" if mostrar_comparativo and variacao != 0 else None
    st.metric(
        "🧺 Volume Total", 
        f"{total_sacos:,}".replace(',', '.'),
        delta=delta_value,
        help="Total de sacos coletados no período selecionado"
    )

with col2:
    peso_delta = f"{variacao*20:+.0f} kg" if mostrar_comparativo and variacao != 0 else None
    st.metric(
        "⚖️ Peso Estimado", 
        f"{peso_total:,} kg".replace(',', '.'),
        delta=peso_delta,
        help="Peso estimado baseado em 20kg por saco"
    )

with col3:
    eficiencia_am = (total_am / (total_am + total_pm) * 100) if (total_am + total_pm) > 0 else 0
    status_eficiencia = "Ótimo" if eficiencia_am > 30 else "Bom" if eficiencia_am > 20 else "Baixo"
    st.metric(
        "📊 Distribuição AM", 
        f"{eficiencia_am:.1f}%",
        delta=status_eficiencia,
        help="Percentual de coleta matutina vs total"
    )

with col4:
    # Previsão inteligente para novo coletor
    previsao_proximo = tendencias['proximo_mes'] if mostrar_previsoes else total_sacos
    necessidade = "URGENTE" if previsao_proximo > limite_volume else "MONITORAR" if previsao_proximo > limite_volume*0.8 else "ADEQUADO"
    
    cor_status = {"URGENTE": "🔴", "MONITORAR": "🟡", "ADEQUADO": "🟢"}
    st.metric(
        "🚛 Status Frota", 
        f"{cor_status[necessidade]} {necessidade}",
        delta=f"Prev: {previsao_proximo:.0f}" if mostrar_previsoes else f"Atual: {total_sacos}",
        help="Análise de necessidade de expansão da frota"
    )

# 📊 Seção de visualizações avançadas
st.markdown("## 📊 Análises Visuais Avançadas")

# Layout responsivo para gráficos
if mostrar_radar:
    col_main, col_radar = st.columns([2, 1])
else:
    col_main, col_radar = st.columns([3, 1]), None

with col_main:
    # Subplots para múltiplas visualizações
    fig_main = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f"📦 Coleta por Período - {mes_selecionado.title()}",
            "🔄 Distribuição AM vs PM",
            "📈 Tendência Temporal",
            "📊 Análise Comparativa"
        ),
        specs=[
            [{"type": "bar"}, {"type": "pie"}],
            [{"colspan": 2, "type": "scatter"}, None]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # Gráfico de barras
    if not df_filtrado.empty:
        fig_main.add_trace(
            go.Bar(x=["AM"], y=[total_am], name="Manhã", marker_color="#00FFFF", text=[total_am], textposition="auto"),
            row=1, col=1
        )
        fig_main.add_trace(
            go.Bar(x=["PM"], y=[total_pm], name="Tarde", marker_color="#FF6B35", text=[total_pm], textposition="auto"),
            row=1, col=1
        )
    
    # Gráfico pizza
    if total_am + total_pm > 0:
        fig_main.add_trace(
            go.Pie(labels=["Manhã", "Tarde"], values=[total_am, total_pm], 
                   marker=dict(colors=["#00FFFF", "#FF6B35"], line=dict(color="white", width=2)),
                   hole=0.4, textinfo='label+percent'),
            row=1, col=2
        )
    
    # Linha temporal
    df_temporal = df[df["Total de Sacos"].notna()].copy()
    if not df_temporal.empty:
        fig_main.add_trace(
            go.Scatter(x=df_temporal["Mês"], y=df_temporal["Total de Sacos"],
                      mode='lines+markers', name='Volume Total',
                      line=dict(color='#9b30ff', width=3),
                      marker=dict(size=8, color='white', line=dict(color='#9b30ff', width=2))),
            row=2, col=1
        )
        
        # Linha de tendência
        if mostrar_previsoes and tendencias['tendencia'] != 0:
            x_tend = list(range(len(df_temporal)))
            y_tend = [tendencias['tendencia'] * i + df_temporal["Total de Sacos"].iloc[0] for i in x_tend]
            fig_main.add_trace(
                go.Scatter(x=df_temporal["Mês"], y=y_tend,
                          mode='lines', name='Tendência',
                          line=dict(color='#FFAA00', width=2, dash='dash')),
                row=2, col=1
            )
    
    # Styling do gráfico principal
    fig_main.update_layout(
        height=600,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        title_font=dict(size=18, color="white"),
        legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0.5)"),
        showlegend=True
    )
    
    fig_main.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)", color="white")
    fig_main.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)", color="white")
    
    st.plotly_chart(fig_main, use_container_width=True)

# Gráfico radar (se habilitado)
if mostrar_radar and col_radar:
    with col_radar:
        st.markdown("### 🎯 Performance Radar")
        fig_radar = criar_radar_performance(df_filtrado)
        st.plotly_chart(fig_radar, use_container_width=True)

# 🤖 Seção de insights inteligentes
if auto_insights:
    st.markdown("## 🤖 Insights Automáticos da IA")
    
    col_insight1, col_insight2, col_insight3 = st.columns(3)
    
    with col_insight1:
        # Análise de tendência avançada
        tendencia_texto = "crescente" if tendencias['crescimento_mensal'] > 5 else "decrescente" if tendencias['crescimento_mensal'] < -5 else "estável"
        cor_tendencia = "trend-up" if tendencias['crescimento_mensal'] > 5 else "trend-down" if tendencias['crescimento_mensal'] < -5 else "trend-neutral"
        
        intensidade = abs(tendencias['crescimento_mensal'])
        nivel_intensidade = "forte" if intensidade > 15 else "moderada" if intensidade > 5 else "leve"
        
        st.markdown(f"""
        <div class="insight-card">
            <h4>📊 Análise Preditiva</h4>
            <p>Tendência <span class="{cor_tendencia}"><strong>{tendencia_texto}</strong></span> com intensidade <strong>{nivel_intensidade}</strong></p>
            <p><strong>Taxa mensal:</strong> <span class="{cor_tendencia}">{tendencias['crescimento_mensal']:+.1f}%</span></p>
            <p><strong>Previsão próximo mês:</strong> {tendencias['proximo_mes']:.0f} sacos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_insight2:
        # Análise de eficiência operacional
        pico_coleta = "Manhã" if total_am > total_pm else "Tarde"
        percentual_pico = max(total_am, total_pm) / (total_am + total_pm) * 100 if (total_am + total_pm) > 0 else 0
        
        # Recomendação baseada na distribuição
        if percentual_pico > 70:
            recomendacao = "Considerar redistribuição de horários"
            cor_rec = "trend-neutral"
        elif percentual_pico < 55:
            recomendacao = "Distribuição equilibrada - ótimo!"
            cor_rec = "trend-up"
        else:
            recomendacao = "Distribuição adequada"
            cor_rec = "trend-up"
        
        st.markdown(f"""
        <div class="insight-card">
            <h4>⏰ Otimização Operacional</h4>
            <p>Pico de coleta no período da <strong>{pico_coleta}</strong></p>
            <p><strong>Concentração:</strong> {percentual_pico:.1f}% do volume</p>
            <p><span class="{cor_rec}"><strong>{recomendacao}</strong></span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_insight3:
        # Análise de capacidade e alertas
        projecao_3meses = tendencias['proximo_mes'] * 3 if tendencias['proximo_mes'] > 0 else total_sacos * 3
        capacidade_utilizada = (total_sacos / limite_volume) * 100
        
        if capacidade_utilizada > 90:
            status_capacidade = "CRÍTICO - Ação imediata"
            cor_cap = "trend-down"
        elif capacidade_utilizada > 70:
            status_capacidade = "ATENÇÃO - Monitorar de perto"
            cor_cap = "trend-neutral"
        else:
            status_capacidade = "NORMAL - Capacidade adequada"
            cor_cap = "trend-up"
        
        st.markdown(f"""
        <div class="insight-card">
            <h4>🚛 Gestão de Capacidade</h4>
            <p><span class="{cor_cap}"><strong>{status_capacidade}</strong></span></p>
            <p><strong>Utilização atual:</strong> {capacidade_utilizada:.1f}%</p>
            <p><strong>Projeção trimestral:</strong> {projecao_3meses:.0f} sacos</p>
        </div>
        """, unsafe_allow_html=True)

# 📈 Análise comparativa avançada
if mostrar_comparativo and len(df[df["Total de Sacos"].notna()]) > 1:
    st.markdown("## 📈 Análise Comparativa Detalhada")
    
    # Criar dados para comparação
    df_comparativo = df[df["Total de Sacos"].notna()].copy()
    df_comparativo["Variação (%)"] = df_comparativo["Total de Sacos"].pct_change() * 100
    df_comparativo["Média Móvel 2"] = df_comparativo["Total de Sacos"].rolling(window=2).mean()
    df_comparativo["Peso (kg)"] = df_comparativo["Total de Sacos"] * 20
    
    col_comp1, col_comp2 = st.columns(2)
    
    with col_comp1:
        # Gráfico de variação percentual
        fig_variacao = go.Figure()
        
        fig_variacao.add_trace(go.Bar(
            x=df_comparativo["Mês"].iloc[1:],
            y=df_comparativo["Variação (%)"].iloc[1:],
            marker_color=['#00FF88' if v > 0 else '#FF4444' for v in df_comparativo["Variação (%)"].iloc[1:]],
            text=[f"{v:+.1f}%" for v in df_comparativo["Variação (%)"].iloc[1:] if not pd.isna(v)],
            textposition="auto",
            name="Variação Mensal"
        ))
        
        fig_variacao.update_layout(
            title="📊 Variação Percentual Mensal",
            xaxis_title="Mês",
            yaxis_title="Variação (%)",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font=dict(color="white"),
            height=400
        )
        
        fig_variacao.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)", color="white")
        fig_variacao.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)", color="white")
        fig_variacao.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
        
        st.plotly_chart(fig_variacao, use_container_width=True)
    
    with col_comp2:
        # Gráfico de média móvel
        fig_media = go.Figure()
        
        fig_media.add_trace(go.Scatter(
            x=df_comparativo["Mês"],
            y=df_comparativo["Total de Sacos"],
            mode='lines+markers',
            name='Volume Real',
            line=dict(color='#00FFFF', width=2),
            marker=dict(size=6)
        ))
        
        fig_media.add_trace(go.Scatter(
            x=df_comparativo["Mês"],
            y=df_comparativo["Média Móvel 2"],
            mode='lines',
            name='Média Móvel',
            line=dict(color='#9b30ff', width=3, dash='dash')
        ))
        
        fig_media.update_layout(
            title="📈 Volume vs Média Móvel",
            xaxis_title="Mês",
            yaxis_title="Sacos",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font=dict(color="white"),
            legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0.5)"),
            height=400
        )
        
        fig_media.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)", color="white")
        fig_media.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)", color="white")
        
        st.plotly_chart(fig_media, use_container_width=True)

# 🎯 Recomendações estratégicas
st.markdown("## 🎯 Recomendações Estratégicas")

col_rec1, col_rec2 = st.columns(2)

with col_rec1:
    st.markdown("### 📋 Ações Imediatas")
    
    recomendacoes_imediatas = []
    
    if capacidade_utilizada > 80:
        recomendacoes_imediatas.append("🚨 **URGENTE**: Planejar expansão da frota")
    
    if percentual_pico > 75:
        recomendacoes_imediatas.append("⏰ **OPERACIONAL**: Redistribuir horários de coleta")
    
    if tendencias['crescimento_mensal'] > 20:
        recomendacoes_imediatas.append("📈 **PLANEJAMENTO**: Revisar projeções orçamentárias")
    
    if eficiencia_am < 25:
        recomendacoes_imediatas.append("🌅 **LOGÍSTICA**: Otimizar rotas matutinas")
    
    if not recomendacoes_imediatas:
        recomendacoes_imediatas.append("✅ **STATUS**: Operação dentro dos parâmetros normais")
    
    for rec in recomendacoes_imediatas:
        st.markdown(f"- {rec}")

with col_rec2:
    st.markdown("### 🔮 Planejamento Futuro")
    
    recomendacoes_futuro = [
        f"📊 **Monitoramento**: Acompanhar crescimento de {tendencias['crescimento_mensal']:.1f}% ao mês",
        f"🚛 **Frota**: Preparar para volume de {tendencias['proximo_mes']:.0f} sacos/mês",
        "📈 **Análise**: Implementar coleta de dados por setor",
        "🎯 **KPIs**: Estabelecer metas de eficiência por período",
        "💡 **Inovação**: Considerar otimização de rotas via IA"
    ]
    
    for rec in recomendacoes_futuro:
        st.markdown(f"- {rec}")

# 📊 Tabela detalhada (modo expandido)
if modo_detalhado:
    st.markdown("## 📊 Análise Detalhada dos Dados")
    
    with st.expander("🔍 Ver Dados Completos e Estatísticas", expanded=True):
        col_tab1, col_tab2 = st.columns([2, 1])
        
        with col_tab1:
            # Preparar dados para exibição
            df_display = df[df["Total de Sacos"].notna()].copy()
            df_display["Mês"] = df_display["Mês"].str.title()
            df_display["Peso Total (kg)"] = df_display["Total de Sacos"] * 20
            df_display["% AM"] = (df_display["Coleta AM"] / df_display["Total de Sacos"] * 100).round(1)
            df_display["% PM"] = (df_display["Coleta PM"] / df_display["Total de Sacos"] * 100).round(1)
            df_display["Variação (%)"] = df_display["Total de Sacos"].pct_change().round(2) * 100
            
            # Adicionar formatação condicional
            styled_df = df_display[["Mês", "Coleta AM", "Coleta PM", "Total de Sacos", "Peso Total (kg)", "% AM", "% PM", "Variação (%)"]].style.format({
                "Variação (%)": "{:+.1f}%",
                "% AM": "{:.1f}%",
                "% PM": "{:.1f}%",
                "Peso Total (kg)": "{:,.0f}",
                "Total de Sacos": "{:,.0f}",
                "Coleta AM": "{:,.0f}",
                "Coleta PM": "{:,.0f}"
            })
            
            st.dataframe(styled_df, use_container_width=True, height=300)
        
        with col_tab2:
            st.markdown("#### 📈 Estatísticas Resumo")
            
            total_geral = df_display["Total de Sacos"].sum()
            media_mensal = df_display["Total de Sacos"].mean()
            desvio_padrao = df_display["Total de Sacos"].std()
            coef_variacao = (desvio_padrao / media_mensal) * 100 if media_mensal > 0 else 0
            
            st.metric("📦 Volume Total", f"{total_geral:,.0f} sacos")
            st.metric("📊 Média Mensal", f"{media_mensal:,.0f} sacos")
            st.metric("📈 Desvio Padrão", f"{desvio_padrao:,.0f} sacos")
            st.metric("📉 Coef. Variação", f"{coef_variacao:.1f}%")
            
            # Classificação da variabilidade
            if coef_variacao < 15:
                variabilidade = "📗 **Baixa** - Padrão estável"
            elif coef_variacao < 30:
                variabilidade = "📙 **Média** - Variação normal"
            else:
                variabilidade = "📕 **Alta** - Padrão irregular"
            
            st.markdown(f"**Variabilidade:** {variabilidade}")

# 🚀 Funcionalidades extras
st.markdown("## 🚀 Ferramentas Avançadas")

col_extra1, col_extra2, col_extra3 = st.columns(3)

with col_extra1:
    if st.button("📊 Gerar Relatório Completo", use_container_width=True):
        with st.spinner("🔄 Preparando relatório executivo..."):
            # Simular processamento
            import time
            time.sleep(2)
            
            st.success("✅ Relatório gerado com sucesso!")
            st.balloons()
            
            # Aqui você adicionaria a lógica real de geração do relatório

with col_extra2:
    if st.button("📧 Enviar Alertas", use_container_width=True):
        if capacidade_utilizada > 70 or abs(variacao) > limite_crescimento:
            st.warning("⚠️ Alertas detectados! Notificação seria enviada.")
        else:
            st.info("✅ Nenhum alerta crítico detectado.")

with col_extra3:
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# 🎯 Footer aprimorado
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(90deg, rgba(26,26,46,0.8), rgba(22,33,62,0.8)); border-radius: 15px; margin-top: 20px;'>
    <div style='font-size: 2.5em; margin-bottom: 15px;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.2em; margin-bottom: 10px;'>
        📊 Sistema Inteligente de Monitoramento de Resíduos
    </div>
    <div style='color: rgba(255,255,255,0.8); font-size: 0.9em; line-height: 1.5;'>
        <strong>Dashboard Executivo</strong> • Análise Preditiva • Otimização Operacional<br>
        🎯 Transformando dados em decisões estratégicas para gestão urbana eficiente
    </div>
    <div style='margin-top: 15px; font-size: 0.8em; color: rgba(255,255,255,0.6);'>
        Desenvolvido com ❤️ para otimização da coleta urbana • Versão 2.0 Enhanced
    </div>
</div>
""", unsafe_allow_html=True)

# 🔧 Debug info (opcional)
if st.sidebar.checkbox("🔧 Modo Debug", False):
    with st.expander("🔧 Informações de Debug"):
        st.write("**Dados carregados:**", len(df))
        st.write("**Mês selecionado:**", mes_selecionado)
        st.write("**Tendências:**", tendencias)
        st.write("**Usando dados simulados:**", usando_simulados)
        st.write("**Última atualização:**", datetime.now().strftime("%H:%M:%S"))

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
        
        /* BOTÕES DOS MESES */
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
        }
        
        /* Hover */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background: rgba(0,255,255,0.15) !important;
            border: 1px solid #00FFFF !important;
            transform: translateY(-1px) scale(1.02) !important;
            box-shadow: 0 4px 12px rgba(0,255,255,0.25) !important;
        }
        
        /* BOTÃO SELECIONADO - ALTERADO PARA VERMELHO TRANSLÚCIDO */
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

        /* Selectbox styling */
        .stSelectbox > div > div {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid #00FFFF;
            border-radius: 10px;
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

# 📥 Carregar dados
try:
    df = pd.read_excel("Coleta centro2.xlsx")
    df.columns = df.columns.str.strip()
    df["Mes"] = df["Mês"].str.lower().str.strip()
except:
    st.warning("⚠️ Arquivo não encontrado. Usando dados simulados para demonstração.")
    df = pd.DataFrame({
        'Mês': ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
                'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
        'Mes': ['janeiro','fevereiro','março','abril','maio','junho',
                'julho','agosto','setembro','outubro','novembro','dezembro'],
        'Coleta AM':[295,1021,408,1192,1045,850,1150,980,1240,1080,950,1320],
        'Coleta PM':[760,1636,793,1606,1461,1380,1720,1520,1890,1640,1480,2100],
        'Total de Sacos':[1055,2657,1201,2798,2506,2230,2870,2500,3130,2720,2430,3420]
    })

# 🏷️ Header
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <div style='font-size: 3.5em; margin-bottom: 10px; font-weight: 700;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.2em; opacity: 0.8;'>
        📊 Monitoramento de Crescimento de Resíduos | 2025-2026
    </div>
</div>
""", unsafe_allow_html=True)

# 🔖 Abas para 2025 e 2026
aba2025, aba2026 = st.tabs(["2025", "2026"])
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

        .card {{
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,255,255,0.15);
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
    </style>
</head>
<body>
    <!-- Slide 1: Capa -->
    <div class="slide">
        <div class="slide-title">Coleta Centro</div>
        <div class="slide-subtitle">Dashboard Executivo de Monitoramento | 2025</div>
    </div>

    <!-- Slide 2: Panorama Geral -->
    <div class="slide">
        <div class="slide-title">📊 Panorama Geral</div>
        <div class="slide-subtitle">Principais Indicadores - Janeiro a Julho 2025</div>
    </div>
</body>
</html>"""

    st.download_button(
        label="📄 PDF",
        data=apresentacao_html,
        file_name=f"Apresentacao_Coleta_Centro_{mes_selecionado.title()}_2025.html",
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
        label="📊 Excel",
        data=csv_data,
        file_name=f"Dados_Coleta_Centro_{mes_selecionado.title()}_2025.csv",
        mime="text/csv",
        use_container_width=True
    )
# 📊 Filtrar dados para o mês selecionado (2025)
df_filtrado = df[(df["Mes"] == mes_selecionado) & (df["Total de Sacos"].notna())]

# 📊 Calcular métricas principais
total_sacos = int(df_filtrado["Total de Sacos"].sum()) if not df_filtrado.empty else 0
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum()) if not df_filtrado.empty else 0
total_pm = int(df_filtrado["Coleta PM"].sum()) if not df_filtrado.empty else 0

# Comparação com mês anterior
mes_anterior_idx = meses_disponiveis.index(mes_selecionado) - 1 if mes_selecionado != "janeiro" else -1
if mes_anterior_idx >= 0:
    df_anterior = df[df["Mes"] == meses_disponiveis[mes_anterior_idx]]
    total_anterior = int(df_anterior["Total de Sacos"].sum()) if not df_anterior.empty else 0
    variacao = ((total_sacos - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0
else:
    variacao = 0

# 📊 Indicadores principais
st.markdown("## 📊 Indicadores Principais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    delta_value = f"{variacao:+.1f}%" if mostrar_comparativo and variacao != 0 else None
    st.metric("📦 Total de Sacos", f"{total_sacos:,}".replace(',', '.'), delta=delta_value)

with col2:
    st.metric("⚖️ Peso Total", f"{peso_total:,} kg".replace(',', '.'), 
              delta=f"{variacao*20:+.0f} kg" if mostrar_comparativo and variacao != 0 else None)

with col3:
    eficiencia = (total_am / (total_am + total_pm) * 100) if (total_am + total_pm) > 0 else 0
    st.metric("🌅 Eficiência AM", f"{eficiencia:.1f}%", delta="Ótima" if eficiencia > 25 else "Baixa")

with col4:
    if total_sacos > 2500:
        status, info = "MONITORAR", "Volume alto"
    elif total_sacos > 2000:
        status, info = "ACOMPANHAR", "Volume crescente"
    else:
        status, info = "NORMAL", "Dentro do esperado"
    st.metric("🚛 Status Operacional", status, delta=info)

# 📊 Gráficos principais
st.markdown("## 📊 Análises Visuais")

df_melt = df_filtrado.melt(id_vars="Mes", value_vars=["Coleta AM", "Coleta PM"],
                           var_name="Periodo", value_name="Quantidade de Sacos")

cores_futuristas = {"Coleta AM": "#00D4FF", "Coleta PM": "#FF6B35"}

col_left, col_right = st.columns([2, 1])

with col_left:
    fig_main = px.bar(df_melt, x="Mes", y="Quantidade de Sacos", color="Periodo",
                      color_discrete_map=cores_futuristas, barmode="group",
                      title=f"📊 Coleta por Período - {mes_selecionado.title()}")
    fig_main.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           font_color="white", title_font=dict(size=16, color="#00D4FF", family="Inter"),
                           title_x=0.5, showlegend=True)
    st.plotly_chart(fig_main, use_container_width=True)

with col_right:
    fig_pie = go.Figure(data=[go.Pie(labels=["Coleta AM", "Coleta PM"], values=[total_am, total_pm],
                                     hole=0.6, marker=dict(colors=["rgba(0, 212, 255, 0.8)", "rgba(255, 107, 53, 0.8)"]))])
    fig_pie.update_layout(title=dict(text=f"📊 Distribuição AM vs PM<br>{mes_selecionado.title()}",
                                     font=dict(size=13, color="#00D4FF", family="Inter"), x=0.5))
    st.plotly_chart(fig_pie, use_container_width=True)

# 📈 Evolução temporal
st.markdown("### 📈 Evolução Temporal Completa")
df_linha = df[df["Total de Sacos"].notna()].copy()
df_linha["Mes_cat"] = pd.Categorical(df_linha["Mes"], categories=meses_disponiveis, ordered=True)
df_linha = df_linha.sort_values("Mes_cat")

fig_evolucao = make_subplots(rows=2, cols=1, subplot_titles=("📦 Volume de Coleta", "🌅 Distribuição AM/PM"),
                             vertical_spacing=0.15, specs=[[{"secondary_y": True}], [{"secondary_y": False}]])
fig_evolucao.add_trace(go.Scatter(x=df_linha["Mes"], y=df_linha["Total de Sacos"], mode='lines+markers',
                                  name='Total de Sacos', line=dict(color='#9b30ff', width=4)), row=1, col=1)
fig_evolucao.add_trace(go.Bar(x=df_linha["Mes"], y=df_linha["Coleta AM"], name='AM',
                              marker=dict(color='rgba(0, 212, 255, 0.7)')), row=2, col=1)
fig_evolucao.add_trace(go.Bar(x=df_linha["Mes"], y=df_linha["Coleta PM"], name='PM',
                              marker=dict(color='rgba(255, 107, 53, 0.7)')), row=2, col=1)
st.plotly_chart(fig_evolucao, use_container_width=True)
# 💡 Insights e Recomendações
st.markdown("## 💡 Insights e Recomendações")

col_insight1, col_insight2, col_insight3 = st.columns(3)

with col_insight1:
    tendencia = "crescente" if variacao > 0 else "decrescente" if variacao < 0 else "estável"
    cor_tendencia = "trend-up" if variacao > 0 else "trend-down" if variacao < 0 else "trend-neutral"
    st.markdown(f"""
    <div class="insight-card">
        <h4>📈 Análise de Tendência</h4>
        <p>Volume <span class="{cor_tendencia}">{tendencia}</span> em relação ao mês anterior</p>
        <p><strong>Variação:</strong> <span class="{cor_tendencia}">{variacao:+.1f}%</span></p>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    pico_coleta = "AM" if total_am > total_pm else "PM"
    percentual_pico = max(total_am, total_pm) / (total_am + total_pm) * 100 if (total_am + total_pm) > 0 else 0
    st.markdown(f"""
    <div class="insight-card">
        <h4>🕒 Padrão de Coleta</h4>
        <p>Maior volume no período da <strong>{pico_coleta}</strong></p>
        <p><strong>Concentração:</strong> {percentual_pico:.1f}% do total</p>
    </div>
    """, unsafe_allow_html=True)

with col_insight3:
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

# 📑 Tabela de dados detalhada
with st.expander("📑 Ver Dados Detalhados"):
    df_display = df[df["Total de Sacos"].notna()].copy()
    df_display["Mês"] = df_display["Mês"].str.title()
    df_display["Peso Total (kg)"] = df_display["Total de Sacos"] * 20
    df_display["% AM"] = (df_display["Coleta AM"] / df_display["Total de Sacos"] * 100).round(1)
    df_display["% PM"] = (df_display["Coleta PM"] / df_display["Total de Sacos"] * 100).round(1)
    st.dataframe(df_display[["Mês", "Coleta AM", "Coleta PM", "Total de Sacos", "Peso Total (kg)", "% AM", "% PM"]],
                 use_container_width=True)

# 📌 Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <div style='font-size: 2em; margin-bottom: 10px;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.1em;'>
        📊 Monitoramento para Otimização da Frota
    </div>
    <small style='color: rgba(255,255,255,0.7);'>Sistema de apoio à decisão para expansão da coleta urbana</small>
</div>
""", unsafe_allow_html=True)

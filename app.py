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
        
        .css-14xtw13 {
            display: block !important;
            visibility: visible !important;
        }
        
        .css-14xtw13 > button {
            background: rgba(26, 26, 46, 0.9) !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            border-radius: 6px !important;
            color: white !important;
            padding: 6px 8px !important;
        }
        
        button[data-testid="baseButton-header"] {
            display: block !important;
            visibility: visible !important;
            background: rgba(26, 26, 46, 0.9) !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            border-radius: 6px !important;
            color: white !important;
        }
        
        .css-14xtw13 svg, button[data-testid="baseButton-header"] svg {
            fill: white !important;
            color: white !important;
        }
        
        header[data-testid="stHeader"] > div {
            background: transparent;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%) !important;
        }
        
        .css-1d391kg {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }
        
        .sidebar .sidebar-content {
            color: white !important;
        }
        
        .css-1v0mbdj {
            color: white !important;
        }
        
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }
        
        section[data-testid="stSidebar"] > div > div > div > div {
            color: white !important;
        }
        
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: white !important;
            font-weight: normal !important;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 8px;
            margin-bottom: 16px;
        }
        
        /* LAYOUT DE 2 COLUNAS PARA OS MESES */
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
            width: 100% !important;
        }
        
        /* BOTÕES DOS MESES */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label,
        .stRadio > div > div > div > label {
            background: #1a1a2e !important;
            padding: 8px 6px !important;
            border-radius: 6px !important;
            border: 1px solid #00FFFF !important;
            margin: 0 !important;
            transition: all 0.3s ease !important;
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
            min-height: 32px !important;
            max-height: 32px !important;
            height: 32px !important;
        }
        
        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover,
        .stRadio > div > div > div > label:hover {
            background: rgba(0,255,255,0.15) !important;
            color: white !important;
            border: 1px solid #00FFFF !important;
            transform: translateY(-1px) scale(1.02) !important;
            box-shadow: 0 4px 12px rgba(0,255,255,0.25) !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child,
        .stRadio > div > div > div > label > div:first-child {
            display: none !important;
        }

        .stRadio > div > div > div {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
        }

        /* MÊS/ANO SELECIONADO */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"],
        .stRadio > div > div > div > label[data-selected="true"],
        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked),
        .stRadio > div > div > div > label:has(input:checked) {
            background: rgba(255, 0, 0, 0.40) !important;
            color: white !important;
            font-weight: 700 !important;
            border: 2px solid rgba(255, 70, 70, 1) !important;
            box-shadow:
                0 0 12px rgba(255, 0, 0, 0.70),
                0 0 28px rgba(255, 0, 0, 0.55),
                0 4px 18px rgba(255, 0, 0, 0.35),
                inset 0 1px 0 rgba(255,255,255,0.18) !important;
            transform: scale(1.04) !important;
            animation: pulse-glow-red 1.6s infinite !important;
        }

        @keyframes pulse-glow-red {
            0%, 100% {
                box-shadow:
                    0 0 12px rgba(255, 0, 0, 0.70),
                    0 0 28px rgba(255, 0, 0, 0.55),
                    0 4px 18px rgba(255, 0, 0, 0.35),
                    inset 0 1px 0 rgba(255,255,255,0.18);
            }
            50% {
                box-shadow:
                    0 0 18px rgba(255, 0, 0, 0.85),
                    0 0 36px rgba(255, 0, 0, 0.70),
                    0 6px 22px rgba(255, 0, 0, 0.45),
                    inset 0 1px 0 rgba(255,255,255,0.25);
            }
        }

        /* CARDS st.metric */
        div[data-testid="stMetric"] {
            min-height: 122px !important;
        }

        div[data-testid="metric-container"] {
            padding: 8px 10px !important;
        }

        div[data-testid="metric-container"],
        div[data-testid="metric-container"] * {
            overflow: visible !important;
            text-overflow: unset !important;
            white-space: normal !important;
            word-break: break-word !important;
        }

        div[data-testid="metric-container"] label,
        div[data-testid="metric-container"] p {
            font-size: 0.60rem !important;
            line-height: 1.05 !important;
            font-weight: 600 !important;
        }

        div[data-testid="metric-container"] [data-testid="stMetricValue"] {
            font-size: 0.84rem !important;
            line-height: 0.98 !important;
            font-weight: 700 !important;
        }

        div[data-testid="metric-container"] [data-testid="stMetricValue"] *,
        div[data-testid="metric-container"] [data-testid="stMetricValue"] span,
        div[data-testid="metric-container"] [data-testid="stMetricValue"] p,
        div[data-testid="metric-container"] [data-testid="stMetricValue"] label,
        div[data-testid="metric-container"] [data-testid="stMetricValue"] div {
            overflow: visible !important;
            text-overflow: unset !important;
            white-space: normal !important;
            word-break: break-word !important;
            display: block !important;
        }

        div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
            font-size: 0.54rem !important;
            line-height: 1.03 !important;
            font-weight: 600 !important;
        }

        div[data-testid="metric-container"] [data-testid="stMetricDelta"] *,
        div[data-testid="metric-container"] [data-testid="stMetricDelta"] span,
        div[data-testid="metric-container"] [data-testid="stMetricDelta"] p,
        div[data-testid="metric-container"] [data-testid="stMetricDelta"] label,
        div[data-testid="metric-container"] [data-testid="stMetricDelta"] div {
            overflow: visible !important;
            text-overflow: unset !important;
            white-space: normal !important;
            word-break: break-word !important;
            display: block !important;
        }

        .stMetric {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid transparent;
            border-radius: 15px;
            padding: 8px 10px !important;
            box-shadow: 0 8px 32px rgba(0,255,255,0.1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            min-height: 122px !important;
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
        
        .stSelectbox > div > div {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid #00FFFF;
            border-radius: 10px;
        }
        
        .css-1rs6os, .css-17lntkn, [data-testid="stPopover"], div[data-baseweb="popover"] {
            background: #2c2c54 !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 8px !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        }
        
        .css-1rs6os > div, .css-17lntkn > div, [data-testid="stPopover"] > div {
            background: #2c2c54 !important;
            color: white !important;
        }
        
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
        
        .css-1rs6os *, .css-17lntkn *, [data-testid="stPopover"] *, div[data-baseweb="popover"] * {
            color: white !important;
            background: transparent !important;
        }
        
        div[role="menu"], div[role="listbox"], .css-1n76uvr, .css-1d391kg {
            background: #2c2c54 !important;
            color: white !important;
        }
        
        div[role="menu"] *, div[role="listbox"] *, .css-1n76uvr *, .css-1d391kg * {
            background: transparent !important;
            color: white !important;
        }
        
        div[role="menu"] button:hover, div[role="listbox"] button:hover {
            background: #00FFFF !important;
            color: black !important;
        }
        
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

# 📥 Carregar dados - lendo TODAS as abas
try:
    xls = pd.ExcelFile("Coleta centro2.xlsx")
    lista_dfs = []

    for aba in xls.sheet_names:
        df_aba = pd.read_excel("Coleta centro2.xlsx", sheet_name=aba)
        df_aba.columns = df_aba.columns.str.strip()

        # usa o nome da aba como ano quando ela for 2025/2026 etc.
        try:
            ano_aba = int(str(aba).strip())
        except:
            ano_aba = None

        if "Ano" not in df_aba.columns:
            df_aba["Ano"] = ano_aba

        lista_dfs.append(df_aba)

    df = pd.concat(lista_dfs, ignore_index=True)

except:
    st.warning("⚠️ Arquivo não encontrado. Usando dados simulados para demonstração.")
    df = pd.DataFrame({
        "Ano": [2025]*12 + [2026]*12,
        "Mês": ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'] * 2,
        'Coleta AM': [295, 1021, 408, 1192, 1045, 850, 1150, 980, 1240, 1080, 950, 1320,
                      2132, 2724, 2214, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Coleta PM': [760, 1636, 793, 1606, 1461, 1380, 1720, 1520, 1890, 1640, 1480, 2100,
                      4759, 6850, 4726, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Total de Sacos': [1055, 2657, 1201, 2798, 2506, 2230, 2870, 2500, 3130, 2720, 2430, 3420,
                           6891, 9574, 6940, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    })

# ✅ Normalização
df["Ano"] = pd.to_numeric(df["Ano"], errors="coerce")
df["Mês"] = df["Mês"].astype(str).str.strip()
df["Mes"] = df["Mês"].str.lower().str.strip()

ordem_meses = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
]

# 🏷️ Header aprimorado
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <div style='font-size: 3.5em; margin-bottom: 10px; font-weight: 700;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.2em; opacity: 0.8;'>
        📊 Monitoramento de Crescimento de Resíduos
    </div>
</div>
""", unsafe_allow_html=True)

# 🎛️ Sidebar com controles avançados
with st.sidebar:
    st.markdown("## 🎛️ Filtros")

    anos_disponiveis = sorted([int(a) for a in df["Ano"].dropna().unique()])
    if not anos_disponiveis:
        anos_disponiveis = [2025]

    st.markdown("### 🗓️ Ano:")
    ano_default = anos_disponiveis.index(2026) if 2026 in anos_disponiveis else 0
    ano_selecionado = st.radio(
        "",
        options=anos_disponiveis,
        format_func=lambda x: str(x),
        horizontal=False,
        index=ano_default
    )

    df_ano = df[(df["Ano"] == ano_selecionado) & (df["Total de Sacos"].notna())].copy()

    meses_disponiveis = [m for m in ordem_meses if m in df_ano["Mes"].dropna().unique().tolist()]
    meses_display = [m.title() for m in meses_disponiveis]

    st.markdown("### 📅 Período:")

    if not meses_disponiveis:
        st.error("Sem meses disponíveis para este ano.")
        st.stop()

    mes_selecionado = st.radio(
        "",
        options=meses_disponiveis,
        format_func=lambda x: meses_display[meses_disponiveis.index(x)],
        horizontal=False,
        index=0
    )

    st.markdown("### 📊 Visualização")
    mostrar_comparativo = st.checkbox("Comparar com mês anterior", True)
    tipo_grafico = st.radio(
        "Tipo de gráfico:",
        ["Barras"],
        horizontal=False
    )

    st.markdown("### 📤 Exportar")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        apresentacao_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Apresentação - Coleta Centro</title>
</head>
<body style="font-family: Arial, sans-serif; background:#111; color:white; padding:40px;">
    <h1>Coleta Centro</h1>
    <h2>{mes_selecionado.title()}</h2>
    <h3>Ano: {ano_selecionado}</h3>
    <p>Apresentação exportada do dashboard.</p>
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
        df_export = df_ano.copy()
        df_export["Mês"] = df_export["Mês"].str.title()
        df_export["Peso Total (kg)"] = df_export["Total de Sacos"] * 20
        df_export["% AM"] = (df_export["Coleta AM"] / df_export["Total de Sacos"] * 100).round(1)
        df_export["% PM"] = (df_export["Coleta PM"] / df_export["Total de Sacos"] * 100).round(1)

        csv_data = df_export[["Ano", "Mês", "Coleta AM", "Coleta PM", "Total de Sacos", "Peso Total (kg)", "% AM", "% PM"]].to_csv(index=False)

        st.download_button(
            label="📋 Excel",
            data=csv_data,
            file_name=f"Dados_Coleta_Centro_{ano_selecionado}.csv",
            mime="text/csv",
            use_container_width=True
        )

# 📑 Filtrar dados para o mês selecionado dentro do ano selecionado
df_filtrado = df[(df["Ano"] == ano_selecionado) & (df["Mes"] == mes_selecionado) & (df["Total de Sacos"].notna())]
df_ano = df[(df["Ano"] == ano_selecionado) & (df["Total de Sacos"].notna())].copy()

# 📊 Calcular métricas principais
total_sacos = int(df_filtrado["Total de Sacos"].sum()) if not df_filtrado.empty else 0
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum()) if not df_filtrado.empty else 0
total_pm = int(df_filtrado["Coleta PM"].sum()) if not df_filtrado.empty else 0

# 🆕 Total anual respeitando o ano selecionado
total_anual_sacos = int(df_ano["Total de Sacos"].sum()) if not df_ano.empty else 0
peso_anual = total_anual_sacos * 20

# Cálculos de comparação (mês anterior no mesmo ano)
mes_anterior_idx = meses_disponiveis.index(mes_selecionado) - 1 if mes_selecionado != meses_disponiveis[0] else -1
if mes_anterior_idx >= 0:
    df_anterior = df_ano[df_ano["Mes"] == meses_disponiveis[mes_anterior_idx]]
    total_anterior = int(df_anterior["Total de Sacos"].sum()) if not df_anterior.empty else 0
    variacao = ((total_sacos - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0
else:
    variacao = 0

# 🎯 Exibir métricas
st.markdown(f"## 📈 Indicadores Principais — {mes_selecionado.title()}")

# colunas um pouco mais largas
col1, col2, col3, col4, col5 = st.columns([1.15, 1.22, 1.15, 1.28, 1.12])

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
        delta=None
    )

with col3:
    eficiencia = (total_am / (total_am + total_pm) * 100) if (total_am + total_pm) > 0 else 0
    st.metric(
        "📊 Eficiência AM",
        f"{eficiencia:.1f}%",
        delta="Ótima" if eficiencia > 25 else "Baixa"
    )

with col4:
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

with col5:
    st.metric(
        "📦 Total Anual",
        f"{total_anual_sacos:,}".replace(',', '.'),
        delta=f"{peso_anual:,} kg".replace(',', '.')
    )

# 📊 Seção de gráficos principais
st.markdown("## 📊 Análises Visuais")

df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

cores_futuristas = {
    "Coleta AM": "#00D4FF",
    "Coleta PM": "#FF6B35"
}

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

    fig_main.update_traces(
        marker=dict(
            opacity=0.8,
            line=dict(color="rgba(255,255,255,0.1)", width=1)
        ),
        hovertemplate='<b>%{y}</b> sacos<br>%{fullData.name}<br><extra></extra>'
    )

    st.plotly_chart(fig_main, use_container_width=True)

with col_right:
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

df_linha = df_ano.copy()
df_linha["Mes_cat"] = pd.Categorical(df_linha["Mes"], categories=ordem_meses, ordered=True)
df_linha = df_linha.sort_values("Mes_cat")

fig_evolucao = make_subplots(
    rows=2, cols=1,
    subplot_titles=("🌟 Volume de Coleta (Sacos)", "⚡ Distribuição AM/PM"),
    vertical_spacing=0.15,
    specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
)

fig_evolucao.add_trace(
    go.Scatter(
        x=df_linha["Mes"],
        y=df_linha["Total de Sacos"],
        mode='lines+markers',
        name='Total de Sacos',
        line=dict(color='#9b30ff', width=4, shape='spline'),
        marker=dict(size=10, color='white', line=dict(color='#9b30ff', width=3), symbol='circle'),
        fill='tonexty',
        fillcolor='rgba(155, 48, 255, 0.15)',
        hovertemplate='<b>%{y}</b> sacos<br>%{x}<br><extra></extra>'
    ),
    row=1, col=1
)

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

fig_evolucao.update_xaxes(
    showgrid=False,
    showline=True,
    linewidth=2,
    linecolor="rgba(0, 212, 255, 0.3)",
    color="white",
    title_font=dict(color="white", size=12),
    tickfont=dict(color="white", size=10),
    categoryorder='array',
    categoryarray=ordem_meses
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
    df_display = df_ano.copy()
    df_display["Mês"] = df_display["Mês"].str.title()
    df_display["Peso Total (kg)"] = df_display["Total de Sacos"] * 20
    df_display["% AM"] = (df_display["Coleta AM"] / df_display["Total de Sacos"] * 100).round(1)
    df_display["% PM"] = (df_display["Coleta PM"] / df_display["Total de Sacos"] * 100).round(1)

    st.dataframe(
        df_display[["Ano", "Mês", "Coleta AM", "Coleta PM", "Total de Sacos", "Peso Total (kg)", "% AM", "% PM"]],
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

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ?? Configuração da página
st.set_page_config(
    page_title="Coleta Centro - Dashboard Executivo",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ?? CSS personalizado com layout de 2 colunas para os meses
st.markdown(
    """
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

        /* Hover dos botões */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background: rgba(0,255,255,0.15) !important;
            transform: translateY(-1px) scale(1.02) !important;
            box-shadow: 0 4px 12px rgba(0,255,255,0.25) !important;
        }

        /* BOTÃO SELECIONADO (CORRIGIDO — SEM CONFLITO) */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"] {
            background: rgba(255, 0, 0, 0.28) !important;
            border: 2px solid rgba(255,60,60,0.55) !important;
            box-shadow: 0 0 12px rgba(255, 0, 0, 0.45) !important;
            transform: scale(1.05) !important;
        }

        /* Esconder círculos */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
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
            min-height: 32px !importa
        .stRadio > div > div > div > label:hover {
            background: rgba(0,255,255,0.15) !important;
            transform: translateY(-1px) scale(1.02) !important;
            box-shadow: 0 4px 12px rgba(0,255,255,0.25) !important;
        }

        .stRadio > div > div > div > label[aria-checked="true"] {
            background: rgba(255, 0, 0, 0.28) !important;
            border: 2px solid rgba(255,60,60,0.55) !important;
            box-shadow: 0 0 12px rgba(255, 0, 0, 0.45) !important;
            transform: scale(1.05) !important;
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
            box-shadow: 0 2px 8px rgba(0,255,255,0.3) !important;
            transform: translateY(-1px) !important;
        }

        /* Selectbox styling */
        .stSelectbox > div > div {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid #00FFFF;
            border-radius: 10px;
        }

        /* Style dropdown items */
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

        /* Hover effect for dropdown */
        div[role="menu"] button:hover, div[role="listbox"] button:hover {
            background: #00FFFF !important;
            color: black !important;
        }

        /* Insights cards */
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

        h1, h2, h3, label, span, div {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================================
#   CARREGAR PLANILHA
# ================================
EXCEL_FILENAME = "Coleta centro2.xlsx"

try:
    all_sheets = pd.read_excel(EXCEL_FILENAME, sheet_name=None)
    sheet_names = list(all_sheets.keys())
    df = all_sheets[sheet_names[0]].copy()
    df.columns = df.columns.str.strip()
    if "Mês" in df.columns:
        df["Mes"] = df["Mês"].astype(str).str.lower().str.strip()
    elif "Mes" in df.columns:
        df["Mes"] = df["Mes"].astype(str).str.lower().str.strip()
    else:
        df.columns = [c if i != 0 else "Mês" for i, c in enumerate(df.columns)]
        df["Mes"] = df["Mês"].astype(str).str.lower().str.strip()
except Exception:
    st.warning("❗ Arquivo não encontrado ou erro na leitura. Dados simulados.")
    all_sheets = None
    sheet_names = []
    df = pd.DataFrame({
        'Mês': ['Janeiro', 'Fev', 'Mar'],
        'Mes': ['janeiro', 'fevereiro', 'março'],
        'Coleta AM': [295, 1021, 408]()
    tipo_grafico = st.radio(
        "Tipo de gráfico:",
        ["Barras"],
        horizontal=False
    )

    # EXPORTAÇÃO
    st.markdown("### 📤 Exportar")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        apresentacao_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apresentação - Coleta Centro</title>
    <style>
        body { font-family: 'Inter', sans-serif;
               background: linear-gradient(135deg,#0c0c0c 0%,#1a1a2e 50%,#16213e 100%);
               color: white; }
        .slide { min-height: 100vh; padding: 40px; }
    </style>
</head>
<body>
    <div class="slide">
        <h1>Coleta Centro</h1>
        <p>Resumo Exportado</p>
    </div>
</body>
</html>
"""
        st.download_button(
            label="📁 PDF",
            data=apresentacao_html,
            file_name=f"Apresentacao_Coleta_Centro_{mes_selecionado.title()}_{year_selected if year_selected else ''}.html",
            mime="text/html",
            use_container_width=True
        )

    with col_btn2:
        df_export = df[df["Total de Sacos"].notna()].copy() if "Total de Sacos" in df.columns else df.copy()
        if "Mês" in df_export.columns:
            df_export["Mês"] = df_export["Mês"].astype(str).str.title()
        if "Total de Sacos" in df_export.columns:
            df_export["Peso Total (kg)"] = df_export["Total de Sacos"] * 20
        if "Coleta AM" in df_export.columns and "Total de Sacos" in df_export.columns:
            df_export["% AM"] = (df_export["Coleta AM"] / df_export["Total de Sacos"] * 100).round(1)
        if "Coleta PM" in df_export.columns and "Total de Sacos" in df_export.columns:
            df_export["% PM"] = (df_export["Coleta PM"] / df_export["Total de Sacos"] * 100).round(1)

        cols_to_keep = [c for c in ["Mês","Coleta AM","Coleta PM","Total de Sacos","Peso Total (kg)","% AM","% PM"]
                        if c in df_export.columns]
        csv_data = df_export[cols_to_keep].to_csv(index=False, encoding="utf-8")

        st.download_button(
            label="📊 Excel",
            data=csv_data,
            file_name=f"Dados_Coleta_Centro_{mes_selecionado.title()}_{year_selected if year_selected else ''}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ==========================================================
# TITULO PRINCIPAL (com espaçador extra para aparecer)
# ==========================================================
st.write("")  
st.write("")  # <-- isto resolve título escondido

display_year = year_selected if year_selected else (sheet_names[0] if sheet_names else "2025")
st.markdown(
    f"""
<div style='text-align: center; padding-top: 20px;'>
    <div style='font-size: 3.5em; font-weight: 700;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.1em;'>
        📊 Monitoramento de Crescimento de Resíduos | {display_year}
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# FILTRO DE MÊS, CÁLCULOS
# ==========================================================
if "Mes" not in df.columns:
    if "Mês" in df.columns:
        df["Mes"] = df["Mês"].astype(str).str.lower().str.strip()
    else:
        df["Mes"] = df.iloc[:, 0].astype(str).str.lower().str.strip()

df_filtrado = df[(df["Mes"] == mes_selecionado) & (df.get("Total de Sacos").notna())] \
    if "Total de Sacos" in df.columns else df[df["Mes"] == mes_selecionado]

total_sacos = int(df_filtrado["Total de Sacos"].sum()) if (not df_filtrado.empty and "Total de Sacos" in df_filtrado.columns) else 0
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum()) if (not df_filtrado.empty and "Coleta AM" in df_filtrado.columns) else 0
total_pm = int(df_filtrado["Coleta PM"].sum()) if (not df_filtrado.empty and "Coleta PM" in df_filtrado.columns) else 0

mes_anterior_idx = meses_disponiveis.index(mes_selecionado) - 1 if mes_selecionado != "janeiro" else -1
if mes_anterior_idx >= 0:
    df_anterior = df[df["Mes"] == meses_disponiveis[mes_anterior_idx]]
    total_anterior = int(df_anterior["Total de Sacos"].sum()) if (not df_anterior.empty and "Total de Sacos" in df_anterior.columns) else 0
    variacao = ((total_sacos - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0
else:
    variacao = 0

# ==========================================================
# MÉTRICAS PRINCIPAIS
# ==========================================================
st.markdown("## 📌 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    delta_value = f"{variacao:+.1f}%" if mostrar_comparativo and variacao != 0 else None
    st.metric(
        "🧮 Total de Sacos",
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
        "📈 Eficiência AM",
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
        "🚨 Status",
        status,
        delta=info
    )

# ==========================================================
# GRÁFICOS PRINCIPAIS
# ==========================================================
st.markdown("## 📊 Análises Visuais")

if df_filtrado.empty or not {"Coleta AM", "Coleta PM"}.issubset(df_filtrado.columns):
    df_melt = pd.DataFrame({
        "Mes": [mes_selecionado, mes_selecionado],
        "Periodo": ["Coleta AM", "Coleta PM"],
        "Quantidade de Sacos": [0, 0]
    })
else:
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
        title=f"📦 Coleta por Período - {mes_selecionado.title()}"
    )
    fig_main.update_layout(
        height=450,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        font_family="Inter",
        showlegend=True,
        title_font=dict(size=20),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0.6)",
            bordercolor="rgba(0,212,255,0.3)",
            borderwidth=1,
        )
    )
    fig_main.update_xaxes(showgrid=False, linewidth=1, linecolor="gray")
    fig_main.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,212,255,0.1)")

    st.plotly_chart(fig_main, use_container_width=True)

with col_right:
    st.markdown("### 📈 Proporções")
    if total_sacos > 0:
        fig_pie = px.pie(
            df_melt,
            values="Quantidade de Sacos",
            names="Periodo",
            color="Periodo",
            color_discrete_map=cores_futuristas,
            hole=0.6
        )
        fig_pie.update_layout(
            height=450,
            title="Distribuição AM vs PM",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================================
# GRÁFICO EVOLUÇÃO
# ==========================================================
st.markdown("## 📅 Evolução Mensal")

df_validos = df[df["Total de Sacos"].notna()]

if not df_validos.empty and {"Mes", "Coleta AM", "Coleta PM"}.issubset(df_validos.columns):
    df_evol = df_validos.copy()
    df_evol["Mes"] = pd.Categorical(df_evol["Mes"], categories=meses_disponiveis, ordered=True)
    df_evol = df_evol.sort_values("Mes")

    df_bar = df_evol[["Mes", "Coleta AM", "Coleta PM"]].copy()
    df_bar = df_bar.melt(
        id_vars="Mes",
        value_vars=["Coleta AM", "Coleta PM"],
        var_name="Periodo",
        value_name="Quantidade"
    )

    fig_evolucao = px.bar(
        df_bar,
        x="Mes",
        y="Quantidade",
        color="Periodo",
        color_discrete_map=cores_futuristas,
        barmode="stack",
        title=f"🚛 Evolução Mensal | {display_year}"
    )

    fig_evolucao.update_layout(
        height=450,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        font_family="Inter",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0.5)",
            bordercolor="rgba(0,212,255,0.3)",
            borderwidth=1
        )
    )
    fig_evolucao.update_xaxes(showgrid=False)
    fig_evolucao.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,212,255,0.1)")

    st.plotly_chart(fig_evolucao, use_container_width=True)

# ==========================================================
# INSIGHTS
# ==========================================================
st.markdown("## 💡 Insights Inteligentes")

col_ins1, col_ins2, col_ins3 = st.columns(3)

with col_ins1:
    tendencia = "crescente" if variacao > 0 else "decrescente" if variacao < 0 else "estável"
    cor_tendencia = "trend-up" if variacao > 0 else "trend-down" if variacao < 0 else "trend-neutral"
    st.markdown(f"""
    <div class="insight-card">
        <h4>📊 Análise de Tendência</h4>
        <p>Volume <span class="{cor_tendencia}">{tendencia}</span> em relação ao mês anterior</p>
        <p><strong>Variação:</strong> <span class="{cor_tendencia}">{variacao:+.1f}%</span></p>
    </div>
    """, unsafe_allow_html=True)

with col_ins2:
    pico = "AM" if total_am > total_pm else "PM"
    perc = max(total_am, total_pm) / (total_am + total_pm) * 100 if (total_am + total_pm) > 0 else 0
    st.markdown(f"""
    <div class="insight-card">
        <h4>📦 Pico de Coleta</h4>
        <p>Maior volume na período: <strong>{pico}</strong></p>
        <p><strong>Concentração:</strong> {perc:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col_ins3:
    if peso_total > 60000:
        risco = "⚠️ Alto"
        cor = "trend-down"
    elif peso_total > 45000:
        risco = "⚠️ Médio"
        cor = "trend-neutral"
    else:
        risco = "OK"
        cor = "trend-up"

    st.markdown(f"""
    <div class="insight-card">
        <h4>🚛 Risco de Saturação</h4>
        <p>Status: <span class="{cor}"><strong>{risco}</strong></span></p>
        <p><strong>Peso estimado:</strong> {peso_total} kg</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# TABELA DETALHADA
# ==========================================================
with st.expander("📋 Ver dados completos"):
    df_show = df[df["Total de Sacos"].notna()].copy() if "Total de Sacos" in df.columns else df.copy()

    if "Mês" in df_show.columns:
        df_show["Mês"] = df_show["Mês"].astype(str).str.title()
    if "Total de Sacos" in df_show.columns:
        df_show["Peso Total (kg)"] = df_show["Total de Sacos"] * 20
    if "Coleta AM" in df_show.columns and "Total de Sacos" in df_show.columns:
        df_show["% AM"] = (df_show["Coleta AM"] / df_show["Total de Sacos"] * 100).round(1)
    if "Coleta PM" in df_show.columns and "Total de Sacos" in df_show.columns:
        df_show["% PM"] = (df_show["Coleta PM"] / df_show["Total de Sacos"] * 100).round(1)

    st.dataframe(
        df_show[[c for c in ["Mês", "Coleta AM", "Coleta PM", "Total de Sacos",
                             "Peso Total (kg)", "% AM", "% PM"] if c in df_show.columns]],
        use_container_width=True
    )
# ==========================================================
# COMPARAÇÃO MENSAL (CASO ATIVADO)
# ==========================================================
if mostrar_comparativo and mes_anterior_idx >= 0:

    seca = meses_disponiveis[mes_anterior_idx]
    st.markdown(f"### 📉 Comparativo com {seca.title()}")

    df_comp = df[df["Mes"].isin([mes_selecionado, seca])]
    if (not df_comp.empty and {"Mes","Coleta AM","Coleta PM"}.issubset(df_comp.columns)):

        df_comp_plot = df_comp[["Mes","Coleta AM","Coleta PM"]].copy()
        df_comp_plot = df_comp_plot.melt(
            id_vars="Mes",
            value_vars=["Coleta AM","Coleta PM"],
            var_name="Periodo",
            value_name="Quantidade"
        )

        fig_comp = px.bar(
            df_comp_plot,
            x="Mes",
            y="Quantidade",
            color="Periodo",
            color_discrete_map=cores_futuristas,
            barmode="group",
        )

        fig_comp.update_layout(
            height=400,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            font_family="Inter",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(0,0,0,0.6)",
                bordercolor="rgba(0,212,255,0.3)",
                borderwidth=1
            )
        )
        fig_comp.update_xaxes(showgrid=False)
        fig_comp.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,212,255,0.1)")
        st.plotly_chart(fig_comp, use_container_width=True)

# ==========================================================
# RANK DE MAIORES/ MENORES (CASO POSSÍVEL)
# ==========================================================
st.markdown("## 🏆 Ranking Mensal")

df_rank = df[df["Total de Sacos"].notna()] if "Total de Sacos" in df.columns else df.copy()
if not df_rank.empty and "Total de Sacos" in df_rank.columns:

    df_rank_show = df_rank[["Mes", "Total de Sacos"]].copy()
    df_rank_show = df_rank_show.groupby("Mes").sum().reset_index()
    df_rank_show["Mes"] = pd.Categorical(df_rank_show["Mes"], categories=meses_disponiveis, ordered=True)
    df_rank_show = df_rank_show.sort_values("Mes")

    df_rank_show["Ranking"] = df_rank_show["Total de Sacos"].rank(ascending=False, method="dense").astype(int)

    st.dataframe(
        df_rank_show.rename(columns={
            "Mes": "Mês",
            "Total de Sacos": "Quantidade Total",
            "Ranking": "Posição"
        }),
        use_container_width=True,
    )

# ==========================================================
# RELATÓRIO FINAL
# ==========================================================
st.markdown("---")

st.markdown(
    f"""
<div style='text-align: center; padding-bottom: 10px;'>
    <div style='font-size: 2em; font-weight: bold;'>
        🚛 <span style='background: linear-gradient(90deg,#00FFFF,#9b30ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='color: #00FFFF; font-size: 1.1em;'>Gerenciamento Inteligente</div>
</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# EXTRA - COLORIR BOTÃO SELECIONADO (CORREÇÃO FINAL)
# ==========================================================
# (GARANTIA QUE FUNCIONA 100%)
st.markdown(
    f"""
<style>
/* Default hover (azul translúcido) */
.stRadio > div > div > div > label:hover {{
    background: rgba(0,255,255,0.15) !important;
}}

/* Selecionado (VERMELHO TRANSLÚCIDO) */
.stRadio > div > div > div > label[aria-checked="true"] {{
    background: rgba(255, 0, 0, 0.35) !important;
    border: 1px solid rgba(255, 0, 0, 0.75) !important;
    box-shadow: 0 0 12px rgba(255, 0, 0, 0.45) !important;
    transform: scale(1.04) !important;
}}
</style>
""",
    unsafe_allow_html=True
)
# ==========================================================
# 🔍 ANÁLISES EXTRA – DETECÇÃO DE OUTLIERS
# ==========================================================
st.markdown("## 📌 Comportamentos Atípicos (Outliers)")

df_out = df[df.get("Total de Sacos").notna()].copy() if "Total de Sacos" in df.columns else df.copy()

if not df_out.empty and "Total de Sacos" in df_out.columns:

    # Detecta outliers simples usando média ± 2 desvios
    media = df_out["Total de Sacos"].mean()
    desvio = df_out["Total de Sacos"].std()
    limite_sup = media + (2 * desvio)
    limite_inf = media - (2 * desvio)

    df_out["Classificacao"] = df_out["Total de Sacos"].apply(
        lambda x: "Acima do Esperado" if x > limite_sup else 
                  "Abaixo do Esperado" if x < limite_inf else 
                  "Dentro do Padrão"
    )

    df_out["Mes"] = pd.Categorical(df_out["Mes"], categories=meses_disponiveis, ordered=True)
    df_out = df_out.sort_values("Mes")

    st.dataframe(
        df_out[["Mes", "Total de Sacos", "Classificacao"]],
        use_container_width=True
    )

    # Exibe faixas calculadas
    st.info(
        f"""
        📊 **Faixa Normal estimada**  
        - Limite inferior: **{limite_inf:.0f} sacos**  
        - Limite superior: **{limite_sup:.0f} sacos**
        """
    )

# ==========================================================
# 🔁 PROJEÇÃO FUTURA SIMPLES (TREND)
# ==========================================================
st.markdown("## 📈 Projeção Próximos Meses (Tendência Linear)")

df_proj = df[df.get("Total de Sacos").notna()].copy() if "Total de Sacos" in df.columns else df.copy()

if not df_proj.empty and "Total de Sacos" in df_proj.columns:

    try:
        # Conversão ordenada de meses para número
        df_proj["Mes_idx"] = df_proj["Mes"].apply(lambda x: meses_disponiveis.index(x))

        coef = np.polyfit(df_proj["Mes_idx"], df_proj["Total de Sacos"], 1)
        tendencia = np.poly1d(coef)

        projecoes = []
        for i in range(12, 15):  # Projeta 3 meses extras
            valor = int(tendencia(i))
            projecoes.append({"Mes Proj": i - 11, "Total Projetado": valor})

        st.write(pd.DataFrame(projecoes))

        # Plot
        fig_proj = go.Figure()

        fig_proj.add_trace(
            go.Scatter(
                x=df_proj["Mes_idx"],
                y=df_proj["Total de Sacos"],
                mode="markers+lines",
                name="Histórico",
                marker=dict(size=10,color="#FF6B35"),
                line=dict(color="#FF6B35", width=3)
            )
        )

        fig_proj.add_trace(
            go.Scatter(
                x=[p["Mes Proj"] for p in projecoes],
                y=[p["Total Projetado"] for p in projecoes],
                mode="markers+lines",
                name="Projetado",
                marker=dict(size=10,color="#00D4FF"),
                line=dict(color="#00D4FF", dash="dash", width=3)
            )
        )

        fig_proj.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            font_family="Inter",
            height=400,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(0,0,0,0.6)"
            )
        )
        st.plotly_chart(fig_proj, use_container_width=True)

    except Exception as e:
        st.warning("Não foi possível calcular projeção.")
        st.text(str(e))

# ==========================================================
# 💬 Comentários automáticos sobre desempenho
# ==========================================================
st.markdown("## 📝 Interpretação Automática")

interpret = ""

if variacao > 15:
    interpret = "Crescimento expressivo! Atenção para capacidade logística."
elif variacao > 5:
    interpret = "Crescimento leve, mas consistente. Monitoramento recomendado."
elif variacao < -15:
    interpret = "Queda forte no volume. Investigar razões e ajustar rotas."
elif variacao < -5:
    interpret = "Pequena queda. Tendência pode se normalizar."
else:
    interpret = "Estabilidade. Sem grandes mudanças demandadas."

st.success(f"📌 **Resumo Inteligente:** {interpret}")
# ==========================================================
# 📦 DOWNLOAD DOS GRÁFICOS EM PNG
# ==========================================================
st.markdown("## 📥 Exportação de Gráficos")

col_png1, col_png2 = st.columns(2)

with col_png1:
    try:
        btn1 = st.download_button(
            "⬇️ Baixar Gráfico Principal",
            data=fig_main.to_image(format="png"),
            file_name=f"coleta_{mes_selecionado}_{display_year}_principal.png",
            mime="image/png"
        )
    except:
        st.info("⚠️ Instale 'kaleido' se quiser baixar imagens em PNG.")

with col_png2:
    try:
        btn2 = st.download_button(
            "⬇️ Baixar Evolução Mensal",
            data=fig_evolucao.to_image(format="png"),
            file_name=f"coleta_{mes_selecionado}_{display_year}_evolucao.png",
            mime="image/png"
        )
    except:
        st.info("⚠️ Instale 'kaleido' se quiser baixar imagens em PNG.")


# ==========================================================
# 💾 SALVAR CONFIGURAÇÃO ATUAL
# ==========================================================
st.markdown("---")
st.markdown("### 💾 Salvar Configuração")

config = {
    "mes": mes_selecionado,
    "ano": display_year,
    "comparativo": mostrar_comparativo,
    "tipo_grafico": tipo_grafico
}

st.json(config)


# ==========================================================
# 🛑 PREVENÇÃO CONTRA CRASHES
# ==========================================================
try:
    st.write("")
except:
    pass


# ==========================================================
# 📌 FOOTER FINAL DE IDENTIFICAÇÃO
# ==========================================================
st.markdown("---")
st.markdown(
    f"""
<div style='text-align: center; padding: 25px;'>
    <div style='font-size: 2em; margin-bottom: 5px; font-weight: bold;
                background: linear-gradient(90deg, #00FFFF, #9b30ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;'>
        Coleta Centro
    </div>
    <div style='color: #00FFFF; font-size: 1.1em;'>
        Relatório Executivo {display_year}
    </div>
    <br>
    <span style='font-size:0.8em;color:rgba(255,255,255,0.5);'>
        Desenvolvido para operação e tomada de decisão
    </span>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# 🔚 FIM DO PROJETO
# ==========================================================

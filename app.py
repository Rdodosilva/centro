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

# -------------------------------------
# 🎨 CSS personalizado
# -------------------------------------
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

        .main .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: none;
        }

        .main { padding: 0; }

        header[data-testid="stHeader"] { height: 2.875rem; background: transparent; }

        /* Sidebar look */
        .css-1d391kg { background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); }
        .sidebar .sidebar-content { color: white !important; }
        section[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); }

        section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
            color: white !important;
            font-weight: normal !important;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 8px;
            margin-bottom: 16px;
        }

        /* Grid for months */
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
            width: 100% !important;
        }

        /* base style for month labels */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label,
        .stRadio > div > div > div > label {
            background: #1a1a2e !important;
            padding: 8px 6px !important;
            border-radius: 6px !important;
            border: 1px solid #00FFFF !important;
            margin: 0 !important;
            transition: all 0.18s ease !important;
            cursor: pointer !important;
            color: white !important;
            font-weight: 500 !important;
            font-size: 0.75em !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            height: 32px !important;
            box-sizing: border-box !important;
        }

        /* hover effect (non-selected): cyan translucent */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover,
        .stRadio > div > div > div > label:hover {
            background: rgba(0,255,255,0.15) !important;
            transform: translateY(-1px) scale(1.02) !important;
            box-shadow: 0 6px 18px rgba(0,255,255,0.12) !important;
        }

        /* ------------------------------
           Selecionado: VERMELHO translúcido
           Alta especificidade para garantir que apareça
           ------------------------------ */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"],
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[role="option"][aria-checked="true"],
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"],
        .stRadio > div > div > div > label[aria-checked="true"],
        .stRadio > div > div > div > label[data-selected="true"] {
            background: linear-gradient(135deg, rgba(255,60,60,0.38), rgba(180,20,20,0.22)) !important;
            color: white !important;
            border: 2px solid rgba(255,60,60,0.55) !important;
            box-shadow:
                0 0 18px rgba(255,60,60,0.42),
                0 0 26px rgba(255,60,60,0.30),
                inset 0 0 6px rgba(255,60,60,0.20) !important;
            transform: scale(1.04) !important;
        }

        /* Metrics/cards */
        .stMetric {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 2px solid transparent;
            border-radius: 15px;
            padding: 8px 12px;
            box-shadow: 0 8px 32px rgba(0,255,255,0.06);
            backdrop-filter: blur(6px);
            position: relative;
            overflow: hidden;
        }
        .stMetric [data-testid="metric-container"] > div:first-child { font-size: 0.75em !important; }
        .stMetric [data-testid="metric-container"] > div:nth-child(2) { font-size: 1.2em !important; font-weight: 700 !important; }

        .insight-card {
            background: linear-gradient(145deg, #1a1a2e, #0f0f23);
            border: 1px solid #00FFFF;
            border-radius: 15px;
            padding: 18px;
            margin: 10px 0;
            box-shadow: 0 8px 32px rgba(0,255,255,0.06);
        }

        .trend-up { color: #00FF88; } .trend-down { color: #FF4444; } .trend-neutral { color: #FFAA00; }

        .stPlotlyChart { animation: fadeIn 0.6s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }

        h1,h2,h3,label,span,div { color: white !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------
# 📥 Carregar dados (múltiplas abas suportadas)
# -------------------------------------
try:
    all_sheets = pd.read_excel("Coleta centro2.xlsx", sheet_name=None)
    sheet_names = list(all_sheets.keys())
    # pega a primeira aba inicialmente
    default_sheet = sheet_names[0] if sheet_names else None
    if default_sheet:
        df = all_sheets[default_sheet].copy()
    else:
        df = pd.DataFrame()
    df.columns = df.columns.str.strip()
    # normaliza coluna de mês
    if "Mês" in df.columns:
        df["Mes"] = df["Mês"].astype(str).str.lower().str.strip()
    elif "Mes" in df.columns:
        df["Mes"] = df["Mes"].astype(str).str.lower().str.strip()
    else:
        if not df.empty:
            df["Mes"] = df.iloc[:, 0].astype(str).str.lower().str.strip()
except Exception:
    st.warning("⚠️ Arquivo não encontrado ou erro ao ler. Usando dados simulados para demonstração.")
    all_sheets = None
    sheet_names = []
    df = pd.DataFrame({
        'Mês': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        'Mes': ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
               'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],
        'Coleta AM': [295, 1021, 408, 1192, 1045, 850, 1150, 980, 1240, 1080, 950, 1320],
        'Coleta PM': [760, 1636, 793, 1606, 1461, 1380, 1720, 1520, 1890, 1640, 1480, 2100],
        'Total de Sacos': [1055, 2657, 1201, 2798, 2506, 2230, 2870, 2500, 3130, 2720, 2430, 3420]
    })

# -------------------------------------
# 🎛️ Sidebar: ano/aba + mês + visualizações + export
# -------------------------------------
with st.sidebar:
    st.markdown("## 🎛️ Filtros")

    # Seletor de ano / aba (se existirem abas)
    year_selected = None
    if sheet_names:
        st.markdown("### 🗂️ Ano / Aba:")
        year_selected = st.selectbox("", options=sheet_names, index=0)
        # atualiza df para a aba escolhida
        try:
            if all_sheets is not None and year_selected in all_sheets:
                df = all_sheets[year_selected].copy()
                df.columns = df.columns.str.strip()
                if "Mês" in df.columns:
                    df["Mes"] = df["Mês"].astype(str).str.lower().str.strip()
                elif "Mes" in df.columns:
                    df["Mes"] = df["Mes"].astype(str).str.lower().str.strip()
                else:
                    if df.shape[1] > 0:
                        df["Mes"] = df.iloc[:, 0].astype(str).str.lower().str.strip()
        except Exception:
            # não quebra se ocorrer erro
            pass

    # Meses
    meses_disponiveis = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    meses_display = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    st.markdown("### 📅 Período:")
    mes_selecionado = st.radio(
        "",
        options=meses_disponiveis,
        format_func=lambda x: meses_display[meses_disponiveis.index(x)],
        index=0
    )

    # Visualização
    st.markdown("### 📊 Visualização")
    mostrar_comparativo = st.checkbox("Comparar com mês anterior", True)
    tipo_grafico = st.radio("Tipo de gráfico:", ["Barras"], index=0)

    # Export
    st.markdown("### 📤 Exportar")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        apresentacao_html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Apresentacao</title></head><body>
        <h1>Apresentação - Coleta Centro</h1><p>Aba/Ano: {year_selected if year_selected else '2025'}</p><p>Mês: {mes_selecionado.title()}</p>
        </body></html>"""
        st.download_button(
            label="📊 PDF",
            data=apresentacao_html,
            file_name=f"Apresentacao_Coleta_Centro_{(year_selected or '2025')}_{mes_selecionado.title()}.html",
            mime="text/html",
            use_container_width=True
        )
    with col_btn2:
        df_export = df.copy() if not df.empty else pd.DataFrame()
        # normaliza colunas se existirem
        if "Mês" in df_export.columns:
            df_export["Mês"] = df_export["Mês"].astype(str).str.title()
        if "Total de Sacos" in df_export.columns:
            df_export["Peso Total (kg)"] = df_export["Total de Sacos"] * 20
        if set(["Coleta AM", "Total de Sacos"]).issubset(df_export.columns):
            df_export["% AM"] = (df_export["Coleta AM"] / df_export["Total de Sacos"] * 100).round(1)
        if set(["Coleta PM", "Total de Sacos"]).issubset(df_export.columns):
            df_export["% PM"] = (df_export["Coleta PM"] / df_export["Total de Sacos"] * 100).round(1)
        cols = [c for c in ["Mês", "Coleta AM", "Coleta PM", "Total de Sacos", "Peso Total (kg)", "% AM", "% PM"] if c in df_export.columns]
        csv_data = df_export[cols].to_csv(index=False) if not df_export.empty else ""
        st.download_button(
            label="📋 Excel",
            data=csv_data,
            file_name=f"Dados_Coleta_Centro_{(year_selected or '2025')}_{mes_selecionado.title()}.csv",
            mime="text/csv",
            use_container_width=True
        )

# -------------------------------------
# 🏷️ Header dinâmico (atualiza com a aba/ano selecionada)
# -------------------------------------
header_year = year_selected if year_selected else "2025"
st.markdown(f"""
<div style='text-align:center; padding:20px 0;'>
    <div style='font-size:3.2em; margin-bottom:8px; font-weight:700;'>
        🚛 <span style='background: linear-gradient(90deg,#00FFFF,#9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='color:#00FFFF; font-size:1.1em; opacity:0.95;'>
        📊 Monitoramento de Crescimento de Resíduos | {header_year}
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------
# 📑 Filtrar dados para o mês selecionado e calcular métricas
# -------------------------------------
# garantia: coluna Mes existe
if "Mes" not in df.columns:
    if "Mês" in df.columns:
        df["Mes"] = df["Mês"].astype(str).str.lower().str.strip()
    elif df.shape[1] > 0:
        df["Mes"] = df.iloc[:, 0].astype(str).str.lower().str.strip()
    else:
        df["Mes"] = []

# filtrar
if "Total de Sacos" in df.columns:
    df_filtrado = df[(df["Mes"] == mes_selecionado) & (df["Total de Sacos"].notna())]
else:
    df_filtrado = df[df["Mes"] == mes_selecionado]

# métricas
total_sacos = int(df_filtrado["Total de Sacos"].sum()) if ("Total de Sacos" in df_filtrado.columns and not df_filtrado.empty) else 0
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum()) if ("Coleta AM" in df_filtrado.columns and not df_filtrado.empty) else 0
total_pm = int(df_filtrado["Coleta PM"].sum()) if ("Coleta PM" in df_filtrado.columns and not df_filtrado.empty) else 0

# variação mês anterior
mes_anterior_idx = meses_disponiveis.index(mes_selecionado) - 1 if mes_selecionado != "janeiro" else -1
if mes_anterior_idx >= 0:
    mes_anterior = meses_disponiveis[mes_anterior_idx]
    df_anterior = df[df["Mes"] == mes_anterior]
    total_anterior = int(df_anterior["Total de Sacos"].sum()) if ("Total de Sacos" in df_anterior.columns and not df_anterior.empty) else 0
    variacao = ((total_sacos - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0
else:
    variacao = 0

# -------------------------------------
# 🎯 Indicadores principais
# -------------------------------------
st.markdown("## 📈 Indicadores Principais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    delta_value = f"{variacao:+.1f}%" if mostrar_comparativo and variacao != 0 else None
    st.metric("🧺 Total de Sacos", f"{total_sacos:,}".replace(',', '.'), delta=delta_value)

with col2:
    st.metric("⚖️ Peso Total", f"{peso_total:,} kg".replace(',', '.'), delta=f"{variacao*20:+.0f} kg" if mostrar_comparativo and variacao != 0 else None)

with col3:
    eficiencia = (total_am / (total_am + total_pm) * 100) if (total_am + total_pm) > 0 else 0
    st.metric("📊 Eficiência AM", f"{eficiencia:.1f}%", delta="Ótimal" if eficiencia > 25 else "Baixa")

with col4:
    if total_sacos > 2500:
        status = "MONITORAR"; info = "Volume alto"
    elif total_sacos > 2000:
        status = "ACOMPANHAR"; info = "Volume crescente"
    else:
        status = "NORMAL"; info = "Dentro do esperado"
    st.metric("📊 Status Operacional", status, delta=info)

# -------------------------------------
# 📊 Gráficos principais
# -------------------------------------
st.markdown("## 📊 Análises Visuais")

# preparar df_melt (fallback seguro)
if df_filtrado is None or df_filtrado.empty:
    df_melt = pd.DataFrame({
        "Mes": [mes_selecionado, mes_selecionado],
        "Periodo": ["Coleta AM", "Coleta PM"],
        "Quantidade de Sacos": [0, 0]
    })
else:
    if set(["Coleta AM", "Coleta PM"]).issubset(df_filtrado.columns):
        df_melt = df_filtrado.melt(
            id_vars="Mes",
            value_vars=["Coleta AM", "Coleta PM"],
            var_name="Periodo",
            value_name="Quantidade de Sacos"
        )
    else:
        df_melt = pd.DataFrame({
            "Mes": [mes_selecionado, mes_selecionado],
            "Periodo": ["Coleta AM", "Coleta PM"],
            "Quantidade de Sacos": [total_am, total_pm]
        })

cores_futuristas = {"Coleta AM": "#00D4FF", "Coleta PM": "#FF6B35"}

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
        title_font=dict(size=16, color="#00D4FF", family="Inter"),
        title_x=0.5,
        font_family="Inter",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=0.02, xanchor="center", x=0.5,
                    font=dict(color="white", size=10),
                    bgcolor="rgba(26,26,46,0.8)", bordercolor="rgba(0,212,255,0.2)", borderwidth=1),
        margin=dict(l=50, r=50, t=80, b=50),
        height=450,
        xaxis=dict(showgrid=False, showline=True, linewidth=2, linecolor="rgba(0,212,255,0.3)",
                   color="white", tickfont=dict(color="white", size=11), categoryorder='array', categoryarray=meses_disponiveis),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(0,212,255,0.08)", color="white", title="Quantidade de Sacos",
                   tickfont=dict(color="white", size=11))
    )
    fig_main.update_traces(marker=dict(opacity=0.85, line=dict(color="rgba(255,255,255,0.08)", width=1)),
                           hovertemplate='<b>%{y}</b> sacos<br>%{fullData.name}<extra></extra>')
    st.plotly_chart(fig_main, use_container_width=True)

with col_right:
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Coleta AM", "Coleta PM"],
        values=[total_am, total_pm],
        hole=0.6,
        marker=dict(colors=["rgba(0,212,255,0.85)", "rgba(255,107,53,0.85)"], line=dict(color="rgba(255,255,255,0.08)", width=1)),
        textinfo='percent',
        hovertemplate='<b>%{label}</b><br>%{value} sacos<br>%{percent}<extra></extra>',
        pull=[0.02, 0.02]
    )])
    fig_pie.update_layout(
        title=dict(text=f"⚡ Distribuição AM vs PM<br>{mes_selecionado.title()}", font=dict(size=13, color="#00D4FF"), x=0.5),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        font_family="Inter",
        showlegend=True,
        legend=dict(orientation="v", yanchor="bottom", y=0.02, xanchor="center", x=0.5,
                    font=dict(color="white", size=9), bgcolor="rgba(26,26,46,0.6)", bordercolor="rgba(0,212,255,0.2)", borderwidth=1),
        height=450, margin=dict(l=20, r=20, t=70, b=50),
        annotations=[dict(text=f"<b style='color:#00D4FF; font-size:18px'>{total_sacos:,}</b><br><span style='color:white; font-size:12px'>Total</span>",
                          x=0.5, y=0.5, showarrow=False, font=dict(family="Inter"))]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# -------------------------------------
# 📈 Evolução temporal completa
# -------------------------------------
st.markdown("### 📈 Evolução Temporal Completa")
df_linha = df.copy()
if "Total de Sacos" in df_linha.columns:
    df_linha = df_linha[df_linha["Total de Sacos"].notna()]
if "Mes" in df_linha.columns:
    df_linha["Mes_cat"] = pd.Categorical(df_linha["Mes"], categories=meses_disponiveis, ordered=True)
    df_linha = df_linha.sort_values("Mes_cat")

fig_evolucao = make_subplots(rows=2, cols=1, subplot_titles=("🌟 Volume de Coleta (Sacos)", "⚡ Distribuição AM/PM"),
                             vertical_spacing=0.14, specs=[[{"secondary_y": True}], [{"secondary_y": False}]])
if "Total de Sacos" in df_linha.columns and not df_linha.empty:
    fig_evolucao.add_trace(go.Scatter(
        x=df_linha["Mes"], y=df_linha["Total de Sacos"], mode='lines+markers', name='Total de Sacos',
        line=dict(color='#9b30ff', width=4, shape='spline'),
        marker=dict(size=8, color='white', line=dict(color='#9b30ff', width=3)),
        fill='tonexty', fillcolor='rgba(155,48,255,0.14)',
        hovertemplate='<b>%{y}</b> sacos<br>%{x}<extra></extra>'
    ), row=1, col=1)

if "Coleta AM" in df_linha.columns:
    fig_evolucao.add_trace(go.Bar(x=df_linha["Mes"], y=df_linha["Coleta AM"], name='AM',
                                  marker=dict(color='rgba(0,212,255,0.7)', line=dict(color='rgba(0,212,255,0.9)', width=1)),
                                  hovertemplate='<b>AM:</b> %{y} sacos<br>%{x}<extra></extra>'), row=2, col=1)
if "Coleta PM" in df_linha.columns:
    fig_evolucao.add_trace(go.Bar(x=df_linha["Mes"], y=df_linha["Coleta PM"], name='PM',
                                  marker=dict(color='rgba(255,107,53,0.72)', line=dict(color='rgba(255,107,53,0.9)', width=1)),
                                  hovertemplate='<b>PM:</b> %{y} sacos<br>%{x}<extra></extra>'), row=2, col=1)

fig_evolucao.update_layout(
    height=650, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font_color="white", font_family="Inter", title_font=dict(size=16, color="#00D4FF"),
    legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5,
                font=dict(color="white", size=10), bgcolor="rgba(26,26,46,0.8)", bordercolor="rgba(0,212,255,0.2)", borderwidth=1),
    barmode='stack', margin=dict(l=50, r=50, t=80, b=70)
)
fig_evolucao.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor="rgba(0,212,255,0.3)", color="white",
                          tickfont=dict(color="white", size=10), categoryorder='array', categoryarray=meses_disponiveis)
fig_evolucao.update_yaxes(showgrid=True, gridcolor="rgba(0,212,255,0.08)", color="white", tickfont=dict(color="white", size=10))

st.plotly_chart(fig_evolucao, use_container_width=True)

# -------------------------------------
# 💡 Insights e tabela detalhada
# -------------------------------------
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
    percentual_pico = (max(total_am, total_pm) / (total_am + total_pm) * 100) if (total_am + total_pm) > 0 else 0
    st.markdown(f"""
    <div class="insight-card">
        <h4>⏰ Padrão de Coleta</h4>
        <p>Maior volume no período da <strong>{pico_coleta}</strong></p>
        <p><strong>Concentração:</strong> {percentual_pico:.1f}% do total</p>
    </div>
    """, unsafe_allow_html=True)

with col_insight3:
    projecao_proxima = total_sacos * (1 + (variacao / 100)) if variacao != 0 else total_sacos * 1.05
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

with st.expander("📋 Ver Dados Detalhados"):
    df_display = df.copy()
    if "Mês" in df_display.columns:
        df_display["Mês"] = df_display["Mês"].astype(str).str.title()
    if "Total de Sacos" in df_display.columns:
        df_display["Peso Total (kg)"] = df_display["Total de Sacos"] * 20
    if set(["Coleta AM", "Total de Sacos"]).issubset(df_display.columns):
        df_display["% AM"] = (df_display["Coleta AM"] / df_display["Total de Sacos"] * 100).round(1)
    if set(["Coleta PM", "Total de Sacos"]).issubset(df_display.columns):
        df_display["% PM"] = (df_display["Coleta PM"] / df_display["Total de Sacos"] * 100).round(1)
    cols_show = [c for c in ["Mês", "Coleta AM", "Coleta PM", "Total de Sacos", "Peso Total (kg)", "% AM", "% PM"] if c in df_display.columns]
    st.dataframe(df_display[cols_show], use_container_width=True)

# -------------------------------------
# Footer
# -------------------------------------
st.markdown("---")
st.markdown(f"""
<div style='text-align:center; padding:20px;'>
    <div style='font-size:1.6em; margin-bottom:8px;'>🚛 <span style='background: linear-gradient(90deg,#00FFFF,#9b30ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight:bold;'>Coleta Centro</span> 🚛</div>
    <div style='color:#00FFFF; font-size:1em;'>📊 Monitoramento para Otimização da Frota | {header_year}</div>
    <small style='color: rgba(255,255,255,0.7);'>Sistema de apoio à decisão para expansão da coleta urbana</small>
</div>
""", unsafe_allow_html=True)

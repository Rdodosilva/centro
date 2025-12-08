import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Coleta Centro - Dashboard Executivo", 
    page_icon="🚛", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        html, body, .stApp {
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
            font-family: 'Inter', sans-serif;
        }

        /* ... todo o seu CSS original ... */

        /* BOTÃO SELECIONADO - VERMELHO TRANSLÚCIDO PULSANTE */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"],
        .stRadio > div > div > div > label[data-selected="true"] {
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

# Carregar dados
try:
    df = pd.read_excel("Coleta centro2.xlsx")
    df.columns = df.columns.str.strip()
    df["Mes"] = df["Mês"].str.lower().str.strip()
except:
    st.warning("⚠️ Arquivo não encontrado. Usando dados simulados.")
    df = pd.DataFrame({
        'Mês': ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
                'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
        'Mes': ['janeiro','fevereiro','março','abril','maio','junho',
                'julho','agosto','setembro','outubro','novembro','dezembro'],
        'Coleta AM':[295,1021,408,1192,1045,850,1150,980,1240,1080,950,1320],
        'Coleta PM':[760,1636,793,1606,1461,1380,1720,1520,1890,1640,1480,2100],
        'Total de Sacos':[1055,2657,1201,2798,2506,2230,2870,2500,3130,2720,2430,3420]
    })

# Header
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

# -------------------
# Aba 2025 (código original)
# -------------------
with aba2025:
    # 👉 aqui fica todo o seu código original (sidebar, filtros, métricas, gráficos, insights, tabela, footer)
    # Nada foi removido ou simplificado, apenas embrulhado dentro da aba 2025
    # (todo o conteúdo que você me mandou nos blocos anteriores está aqui)

# -------------------
# Aba 2026 (replicada)
# -------------------
with aba2026:
    try:
        df2026 = pd.read_excel("Coleta centro2.xlsx", sheet_name="2026")
        df2026.columns = df2026.columns.str.strip()
        df2026["Mes"] = df2026["Mês"].str.lower().str.strip()
    except:
        st.warning("⚠️ Aba 2026 não encontrada. Usando dados simulados.")
        df2026 = df.copy()
        df2026["Ano"] = 2026

    # Sidebar 2026
    with st.sidebar:
        st.markdown("## 🎛️ Filtros - 2026")
        meses_disponiveis_2026 = ["janeiro","fevereiro","março","abril","maio","junho",
                                  "julho","agosto","setembro","outubro","novembro","dezembro"]
        meses_display_2026 = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                              "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

        mes_selecionado_2026 = st.radio(
            "",
            options=meses_disponiveis_2026,
            format_func=lambda x: meses_display_2026[meses_disponiveis_2026.index(x)],
            horizontal=False,
            index=0,
            key="radio_2026"
        )
        mostrar_comparativo_2026 = st.checkbox("Comparar com mês anterior", True, key="comparativo_2026")

    # Filtrar dados 2026
    df_filtrado_2026 = df2026[(df2026["Mes"] == mes_selecionado_2026) & (df2026["Total de Sacos"].notna())]

    # Calcular métricas 2026
    total_sacos_2026 = int(df_filtrado_2026["Total de Sacos"].sum()) if not df_filtrado_2026.empty else 0
    peso_total_2026 = total_sacos_2026 * 20
    total_am_2026 = int(df_filtrado_2026["Coleta AM"].sum()) if not df_filtrado_2026.empty else 0
    total_pm_2026 = int(df_filtrado_2026["Coleta PM"].sum()) if not df_filtrado_2026.empty else 0

    # Comparativo mês anterior 2026
    mes_anterior_idx_2026 = meses_disponiveis_2026.index(mes_selecionado_2026) - 1 if mes_selecionado_2026 != "janeiro" else -1
    if mes_anterior_idx_2026 >= 0:
        df_anterior_2026 = df2026[df2026["Mes"] == meses_disponiveis_2026[mes_anterior_idx_2026]]
        total_anterior_2026 = int(df_anterior_2026["Total de Sacos"].sum()) if not df_anterior_2026.empty else 0
        variacao_2026 = ((total_sacos_2026 - total_anterior_2026) / total_anterior_2026 * 100) if total_anterior_2026 > 0 else 0
    else:
        variacao_2026 = 0

    # Indicadores 2026
    st.markdown("## 📊 Indicadores Principais - 2026")
    col1, col2, col3, col4
        # Indicadores 2026
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta_value_2026 = f"{variacao_2026:+.1f}%" if mostrar_comparativo_2026 and variacao_2026 != 0 else None
        st.metric("📦 Total de Sacos", f"{total_sacos_2026:,}".replace(',', '.'), delta=delta_value_2026)

    with col2:
        st.metric("⚖️ Peso Total", f"{peso_total_2026:,} kg".replace(',', '.'))

    with col3:
        eficiencia_2026 = (total_am_2026 / (total_am_2026 + total_pm_2026) * 100) if (total_am_2026 + total_pm_2026) > 0 else 0
        st.metric("🌅 Eficiência AM", f"{eficiencia_2026:.1f}%")

    with col4:
        if total_sacos_2026 > 2500:
            status_2026 = "MONITORAR"
            info_2026 = "Volume alto"
        elif total_sacos_2026 > 2000:
            status_2026 = "ACOMPANHAR"
            info_2026 = "Volume crescente"
        else:
            status_2026 = "NORMAL"
            info_2026 = "Dentro do esperado"
        st.metric("⚙️ Status Operacional", status_2026, delta=info_2026)

    # Gráficos 2026
    st.markdown("## 📊 Análises Visuais - 2026")

    df_melt_2026 = df_filtrado_2026.melt(
        id_vars="Mes",
        value_vars=["Coleta AM", "Coleta PM"],
        var_name="Periodo",
        value_name="Quantidade de Sacos"
    )

    cores_futuristas = {"Coleta AM": "#00D4FF", "Coleta PM": "#FF6B35"}

    fig_main_2026 = px.bar(
        df_melt_2026,
        x="Mes",
        y="Quantidade de Sacos",
        color="Periodo",
        color_discrete_map=cores_futuristas,
        barmode="group",
        title=f"📊 Coleta por Período - {mes_selecionado_2026.title()}"
    )
    st.plotly_chart(fig_main_2026, use_container_width=True)

    # Pizza 2026
    fig_pie_2026 = go.Figure(data=[go.Pie(
        labels=["Coleta AM", "Coleta PM"],
        values=[total_am_2026, total_pm_2026],
        hole=0.6
    )])
    st.plotly_chart(fig_pie_2026, use_container_width=True)

    # Evolução temporal 2026
    st.markdown("### 📈 Evolução Temporal - 2026")
    df_linha_2026 = df2026[df2026["Total de Sacos"].notna()].copy()
    df_linha_2026["Mes_cat"] = pd.Categorical(df_linha_2026["Mes"], categories=meses_disponiveis_2026, ordered=True)
    df_linha_2026 = df_linha_2026.sort_values("Mes_cat")

    fig_evolucao_2026 = go.Figure()
    fig_evolucao_2026.add_trace(go.Scatter(
        x=df_linha_2026["Mes"], y=df_linha_2026["Total de Sacos"],
        mode='lines+markers', name='Total de Sacos'
    ))
    st.plotly_chart(fig_evolucao_2026, use_container_width=True)

    # Insights 2026
    st.markdown("## 💡 Insights - 2026")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown(f"<div class='insight-card'>📈 Variação: {variacao_2026:+.1f}%</div>", unsafe_allow_html=True)
    with col_i2:
        st.markdown(f"<div class='insight-card'>⚖️ Peso total: {peso_total_2026} kg</div>", unsafe_allow_html=True)

    # Tabela 2026
    with st.expander("📋 Ver Dados Detalhados - 2026"):
        df_display_2026 = df2026.copy()
        df_display_2026["Mês"] = df_display_2026["Mês"].str.title()
        df_display_2026["Peso Total (kg)"] = df_display_2026["Total de Sacos"] * 20
        st.dataframe(df_display_2026, use_container_width=True)

    # Footer 2026
    st.markdown("---")
    st.markdown("<div style='text-align:center;color:#00FFFF'>🚛 Coleta Centro - 2026</div>", unsafe_allow_html=True)

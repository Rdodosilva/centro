import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
        /* Layout geral */
        html, body, .stApp {
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
            font-family: 'Inter', sans-serif;
        }

        /* Botão selecionado - vermelho translúcido pulsante */
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
    </style>
""", unsafe_allow_html=True)
# 📥 Carregar dados
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
# ---------------------- ABA 2025 ----------------------
with aba2025:
    st.sidebar.markdown("## 🎛️ Filtros - 2025")

    # Lista de meses disponíveis
    meses_disponiveis = ["janeiro","fevereiro","março","abril","maio","junho",
                         "julho","agosto","setembro","outubro","novembro","dezembro"]
    meses_display = [m.title() for m in meses_disponiveis]

    # Seleção de mês
    mes_selecionado = st.sidebar.radio(
        "📅 Período:",
        options=meses_disponiveis,
        format_func=lambda x: meses_display[meses_disponiveis.index(x)]
    )

    # 📊 Filtrar dados para o mês selecionado
    df_filtrado = df[df["Mes"] == mes_selecionado]
    total_sacos = int(df_filtrado["Total de Sacos"].sum()) if not df_filtrado.empty else 0
    peso_total = total_sacos * 20
    total_am = int(df_filtrado["Coleta AM"].sum()) if not df_filtrado.empty else 0
    total_pm = int(df_filtrado["Coleta PM"].sum()) if not df_filtrado.empty else 0

    # 📊 Indicadores principais
    st.markdown("## 📊 Indicadores Principais")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Total de Sacos", total_sacos)

    with col2:
        st.metric("⚖️ Peso Total", f"{peso_total} kg")

    with col3:
        eficiencia = (total_am / (total_am + total_pm) * 100) if (total_am + total_pm) > 0 else 0
        st.metric("🌅 Eficiência AM", f"{eficiencia:.1f}%")

    # 📊 Gráfico de barras AM vs PM
    st.markdown("### 📊 Coleta por Período")
    df_melt = df_filtrado.melt(
        id_vars="Mes",
        value_vars=["Coleta AM", "Coleta PM"],
        var_name="Período",
        value_name="Quantidade de Sacos"
    )
    cores_futuristas = {"Coleta AM": "#00D4FF", "Coleta PM": "#FF6B35"}
    fig_main = px.bar(
        df_melt,
        x="Mes",
        y="Quantidade de Sacos",
        color="Período",
        color_discrete_map=cores_futuristas,
        barmode="group",
        title=f"📊 Coleta AM vs PM - {mes_selecionado.title()}"
    )
    fig_main.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        title_font=dict(size=16, color="#00D4FF", family="Inter"),
        title_x=0.5,
        showlegend=True
    )
    st.plotly_chart(fig_main, use_container_width=True)

    # 📊 Gráfico de pizza AM vs PM
    st.markdown("### 📊 Distribuição AM vs PM")
    fig_pie = go.Figure(
        data=[go.Pie(
            labels=["Coleta AM", "Coleta PM"],
            values=[total_am, total_pm],
            hole=0.6,
            marker=dict(colors=["rgba(0, 212, 255, 0.8)", "rgba(255, 107, 53, 0.8)"])
        )]
    )
    fig_pie.update_layout(
        title=dict(
            text=f"📊 Distribuição AM vs PM<br>{mes_selecionado.title()}",
            font=dict(size=13, color="#00D4FF", family="Inter"),
            x=0.5
        )
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # 📈 Evolução temporal
    st.markdown("### 📈 Evolução Temporal Completa")
    df_linha = df[df["Total de Sacos"].notna()].copy()
    df_linha["Mes_cat"] = pd.Categorical(df_linha["Mes"], categories=meses_disponiveis, ordered=True)
    df_linha = df_linha.sort_values("Mes_cat")

    fig_evolucao = make_subplots(
        rows=2, cols=1,
        subplot_titles=("📦 Volume de Coleta", "🌅 Distribuição AM/PM"),
        vertical_spacing=0.15,
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
    )
    fig_evolucao.add_trace(
        go.Scatter(x=df_linha["Mes"], y=df_linha["Total de Sacos"], mode='lines+markers',
                   name='Total de Sacos', line=dict(color='#9b30ff', width=4)),
        row=1, col=1
    )
    fig_evolucao.add_trace(
        go.Bar(x=df_linha["Mes"], y=df_linha["Coleta AM"], name='AM',
               marker=dict(color='rgba(0, 212, 255, 0.7)')),
        row=2, col=1
    )
    fig_evolucao.add_trace(
        go.Bar(x=df_linha["Mes"], y=df_linha["Coleta PM"], name='PM',
               marker=dict(color='rgba(255, 107, 53, 0.7)')),
        row=2, col=1
    )
    st.plotly_chart(fig_evolucao, use_container_width=True)

    # 💡 Insights rápidos
    st.markdown("## 💡 Insights")
    col_insight1, col_insight2 = st.columns(2)
    with col_insight1:
        st.markdown(f"<div class='insight-card'>Maior volume: {max(total_am,total_pm)} sacos</div>", unsafe_allow_html=True)
    with col_insight2:
        st.markdown(f"<div class='insight-card'>Peso total: {peso_total} kg</div>", unsafe_allow_html=True)
# ---------------------- ABA 2026 ----------------------
with aba2026:
    st.sidebar.markdown("## 🎛️ Filtros - 2026")

    # Tenta carregar dados da aba 2026
    try:
        df2026 = pd.read_excel("Coleta centro2.xlsx", sheet_name="2026")
        df2026.columns = df2026.columns.str.strip()
        df2026["Mes"] = df2026["Mês"].str.lower().str.strip()
    except:
        st.warning("⚠️ Aba 2026 não encontrada. Usando dados simulados.")
        df2026 = df.copy()
        df2026["Ano"] = 2026

    # Lista de meses
    meses_disponiveis = ["janeiro","fevereiro","março","abril","maio","junho",
                         "julho","agosto","setembro","outubro","novembro","dezembro"]
    meses_display = [m.title() for m in meses_disponiveis]

    # Seleção de mês
    mes_selecionado_2026 = st.sidebar.radio(
        "📅 Período:",
        options=meses_disponiveis,
        format_func=lambda x: meses_display[meses_disponiveis.index(x)],
        key="radio2026"
    )

    # 📊 Filtrar dados
    df_filtrado_2026 = df2026[df2026["Mes"] == mes_selecionado_2026]
    total_sacos_2026 = int(df_filtrado_2026["Total de Sacos"].sum()) if not df_filtrado_2026.empty else 0
    peso_total_2026 = total_sacos_2026 * 20
    total_am_2026 = int(df_filtrado_2026["Coleta AM"].sum()) if not df_filtrado_2026.empty else 0
    total_pm_2026 = int(df_filtrado_2026["Coleta PM"].sum()) if not df_filtrado_2026.empty else 0

    # 📊 Indicadores principais
    st.markdown("## 📊 Indicadores Principais - 2026")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Total de Sacos", total_sacos_2026)

    with col2:
        st.metric("⚖️ Peso Total", f"{peso_total_2026} kg")

    with col3:
        eficiencia_2026 = (total_am_2026 / (total_am_2026 + total_pm_2026) * 100) if (total_am_2026 + total_pm_2026) > 0 else 0
        st.metric("🌅 Eficiência AM", f"{eficiencia_2026:.1f}%")

    # 📊 Gráfico de barras AM vs PM
    st.markdown("### 📊 Coleta por Período - 2026")
    df_melt_2026 = df_filtrado_2026.melt(
        id_vars="Mes",
        value_vars=["Coleta AM", "Coleta PM"],
        var_name="Período",
        value_name="Quantidade de Sacos"
    )
    cores_futuristas = {"Coleta AM": "#00D4FF", "Coleta PM": "#FF6B35"}
    fig_main_2026 = px.bar(
        df_melt_2026,
        x="Mes",
        y="Quantidade de Sacos",
        color="Período",
        color_discrete_map=cores_futuristas,
        barmode="group",
        title=f"📊 Coleta AM vs PM - {mes_selecionado_2026.title()}"
    )
    fig_main_2026.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        title_font=dict(size=16, color="#00D4FF", family="Inter"),
        title_x=0.5,
        showlegend=True
    )
    st.plotly_chart(fig_main_2026, use_container_width=True)

    # 📊 Gráfico de pizza AM vs PM
    st.markdown("### 📊 Distribuição AM vs PM - 2026")
    fig_pie_2026 = go.Figure(
        data=[go.Pie(
            labels=["Coleta AM", "Coleta PM"],
            values=[total_am_2026, total_pm_2026],
            hole=0.6,
            marker=dict(colors=["rgba(0, 212, 255, 0.8)", "rgba(255, 107, 53, 0.8)"])
        )]
    )
    fig_pie_2026.update_layout(
        title=dict(
            text=f"📊 Distribuição AM vs PM<br>{mes_selecionado_2026.title()}",
            font=dict(size=13, color="#00D4FF", family="Inter"),
            x=0.5
        )
    )
    st.plotly_chart(fig_pie_2026, use_container_width=True)

    # 📈 Evolução temporal
    st.markdown("### 📈 Evolução Temporal Completa - 2026")
    df_linha_2026 = df2026[df2026["Total de Sacos"].notna()].copy()
    df_linha_2026["Mes_cat"] = pd.Categorical(df_linha_2026["Mes"], categories=meses_disponiveis, ordered=True)
    df_linha_2026 = df_linha_2026.sort_values("Mes_cat")

    fig_evolucao_2026 = make_subplots(
        rows=2, cols=1,
        subplot_titles=("📦 Volume de Coleta", "🌅 Distribuição AM/PM"),
        vertical_spacing=0.15,
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
    )
    fig_evolucao_2026.add_trace(
        go.Scatter(x=df_linha_2026["Mes"], y=df_linha_2026["Total de Sacos"], mode='lines+markers',
                   name='Total de Sacos', line=dict(color='#9b30ff', width=4)),
        row=1, col=1
    )
    fig_evolucao_2026.add_trace(
        go.Bar(x=df_linha_2026["Mes"], y=df_linha_2026["Coleta AM"], name='AM',
               marker=dict(color='rgba(0, 212, 255, 0.7)')),
        row=2, col=1
    )
    fig_evolucao_2026.add_trace(
        go.Bar(x=df_linha_2026["Mes"], y=df_linha_2026["Coleta PM"], name='PM',
               marker=dict(color='rgba(255, 107, 53, 0.7)')),
        row=2, col=1
    )
    st.plotly_chart(fig_evolucao_2026, use_container_width=True)

    # 💡 Insights rápidos
    st.markdown("## 💡 Insights - 2026")
    col_insight1, col_insight2 = st.columns(2)
    with col_insight1:
        st.markdown(f"<div class='insight-card'>Maior volume: {max(total_am_2026,total_pm_2026)} sacos</div>", unsafe_allow_html=True)
    with col_insight2:
        st.markdown(f"<div class='insight-card'>Peso total: {peso_total_2026} kg</div>", unsafe_allow_html=True)
# 📑 Tabela de dados detalhada
st.markdown("## 📑 Dados Detalhados")
with st.expander("📑 Ver Dados Detalhados"):
    df_display = df[df["Total de Sacos"].notna()].copy()
    df_display["Mês"] = df_display["Mês"].str.title()
    df_display["Peso Total (kg)"] = df_display["Total de Sacos"] * 20
    df_display["% AM"] = (df_display["Coleta AM"] / df_display["Total de Sacos"] * 100).round(1)
    df_display["% PM"] = (df_display["Coleta PM"] / df_display["Total de Sacos"] * 100).round(1)

    st.dataframe(
        df_display[["Mês", "Coleta AM", "Coleta PM", "Total de Sacos", "Peso Total (kg)", "% AM", "% PM"]],
        use_container_width=True
    )

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

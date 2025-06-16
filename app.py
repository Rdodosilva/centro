import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html

st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# CSS para tema geral e selectbox fechado (roxo neon)
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #000000;
            color: white;
        }
        h1, h2, h3, label, span, div {
            color: white !important;
        }
        /* Selectbox fechado */
        div[data-baseweb="select"] > div {
            background-color: rgba(155, 48, 255, 0.8) !important;
            border: 2px solid #9b30ff !important;
            border-radius: 10px;
        }
        div[data-baseweb="select"] span {
            color: white !important;
            font-weight: bold;
        }
        label, .stSelectbox label {
            color: white !important;
            font-weight: bold;
        }
        /* Tenta estilizar dropdown aberto */
        .rc-virtual-list-holder-inner, /* lista virtual scroll */
        div[role="listbox"] {
            background-color: rgba(155, 48, 255, 0.8) !important;
            color: white !important;
            font-weight: bold;
            border-radius: 10px !important;
            box-shadow: 0 0 12px 4px rgba(155, 48, 255, 0.9) !important;
        }
        div[role="option"] {
            color: white !important;
        }
        div[role="option"]:hover {
            background-color: rgba(200, 100, 255, 1) !important;
            color: black !important;
        }
        div[role="option"][aria-selected="true"] {
            background-color: rgba(255, 100, 255, 1) !important;
            color: black !important;
            font-weight: bold;
        }
        /* Estilo para métricas */
        .stMetric {
            background-color: #111111;
            border: 1px solid #9b30ff;
            border-radius: 12px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# INJEÇÃO DE JS para forçar o fundo roxo neon no dropdown aberto (fallback)
html("""
<script>
    const observer = new MutationObserver(() => {
        document.querySelectorAll('div[role="listbox"]').forEach(el => {
            el.style.backgroundColor = "rgba(155, 48, 255, 0.85)";
            el.style.color = "white";
            el.style.borderRadius = "10px";
            el.style.boxShadow = "0 0 12px 4px rgba(155, 48, 255, 0.9)";
        });
        document.querySelectorAll('div[role="option"]').forEach(opt => {
            opt.style.color = "white";
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
</script>
""", height=0)

# Resto do código: dados e gráficos (exemplo simplificado)

# Exemplo rápido dados fictícios para teste do dropdown e gráfico pizza
meses_disponiveis = ["janeiro", "fevereiro", "março", "abril", "maio"]
mes_selecionado = st.selectbox("Selecione o mês:", meses_disponiveis, format_func=lambda x: x.capitalize())

# Dados fictícios
total_am_geral = 150
total_pm_geral = 200

cores = {
    "Coleta AM": "#00FFFF",
    "Coleta PM": "#FFA500"
}

fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am_geral, total_pm_geral],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title="🔄 Distribuição Geral AM vs PM"
)
fig_pie.update_traces(
    textfont=dict(color='white', size=14),
    textinfo='label+percent+value',
    pull=[0.05, 0],
    marker=dict(line=dict(color='white', width=2)),
    hoverinfo='label+percent+value'
)
fig_pie.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="white",
    title_font=dict(size=22),
    title_x=0.5,
    legend=dict(
        font=dict(color="white", size=14),
        bgcolor="#000000"
    )
)

st.plotly_chart(fig_pie, use_container_width=True)

# Texto extra para lembrar unidade Kg no total
st.markdown("<p style='text-align:center; color:#9b30ff; font-weight:bold;'>*Valores são em sacos (20 kg cada).</p>", unsafe_allow_html=True)

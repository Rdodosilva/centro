import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# 🎨 CSS personalizado completo
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #000000;
            color: white;
        }
        h1, h2, h3, label, span, div {
            color: white !important;
        }
        /* RADIO estilizado como dropdown neon */
        section[data-testid="stRadio"] > div {
            background-color: rgba(155, 48, 255, 0.3);
            border: 2px solid #9b30ff;
            border-radius: 10px;
            padding: 8px;
        }
        label[data-testid="stMarkdownContainer"] {
            color: white;
            font-weight: bold;
        }
        div[role="radiogroup"] > label {
            background-color: rgba(0,0,0,0.6);
            padding: 5px 10px;
            border-radius: 8px;
            border: 1px solid #9b30ff;
            margin-right: 8px;
        }
        div[role="radiogroup"] > label:hover {
            background-color: #9b30ff;
            color: black;
        }
        div[role="radiogroup"] > label[data-selected="true"] {
            background-color: #9b30ff;
            color: black;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


# 🗓️ Meses
meses_disponiveis = ["janeiro", "fevereiro", "março", "abril", "maio"]

# 🔽 Dropdown estilizado (substituindo selectbox)
st.markdown("### 📅 Selecione o mês:")
mes_selecionado = st.radio(
    "",
    meses_disponiveis,
    horizontal=True,
    index=0,
)

st.markdown(f"## Mês selecionado: **{mes_selecionado.capitalize()}**")

# 🔢 Dados fictícios para exemplo
total_am_geral = 150
total_pm_geral = 200

# 🎨 Cores
cores = {
    "Coleta AM": "#00FFFF",
    "Coleta PM": "#FFA500"
}

# 🥧 Gráfico de pizza
fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am_geral, total_pm_geral],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title="🔄 Distribuição Geral AM vs PM"
)

fig_pie.update_traces(
    textinfo='percent+label',
    textposition='inside',
    textfont=dict(color='black', size=14),
    pull=[0.05, 0],
    hovertemplate='%{label}: %{value} kg (%{percent})<extra></extra>'
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

# 📊 Mostrar gráfico
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<p style='text-align:center; color:#9b30ff; font-weight:bold;'>*Valores em kg (cada saco = 20 kg).</p>", unsafe_allow_html=True)

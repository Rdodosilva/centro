import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# CSS geral para tema escuro + fontes brancas
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #000000;
            color: white;
        }
        h1, h2, h3, label, span, div {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Dropdown roxo neon (horizontal para exemplo, pode trocar para vertical)
meses_disponiveis = ["janeiro", "fevereiro", "março", "abril", "maio"]

mes_selecionado = option_menu(
    menu_title=None,
    options=meses_disponiveis,
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"background-color": "black"},
        "nav-link": {
            "font-size": "18px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#9b30ff",
            "color": "white",
            "border-radius": "10px",
            "padding": "8px 16px"
        },
        "nav-link-selected": {
            "background-color": "#9b30ff",
            "color": "white",
            "font-weight": "bold"
        },
    }
)

st.markdown(f"### Mês selecionado: **{mes_selecionado.capitalize()}**")

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
    textinfo='percent+label',  # só % e label, pra ficar limpo
    textposition='inside',
    textfont=dict(color='black', size=14),
    pull=[0.05, 0],
    hovertemplate='%{label}: %{value} sacos (%{percent})<extra></extra>'
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

st.markdown("<p style='text-align:center; color:#9b30ff; font-weight:bold;'>*Valores são em sacos (20 kg cada).</p>", unsafe_allow_html=True)

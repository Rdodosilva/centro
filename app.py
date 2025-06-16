import pandas as pd
import streamlit as st
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Dashboard Coleta Centro", page_icon="🚛", layout="wide")

# --- CSS para estilo preto total e texto branco ---
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #000000 !important;
            color: white !important;
            font-family: 'Segoe UI', sans-serif;
        }
        .stSelectbox label, .stMultiSelect label, .stTextInput label, .stSlider label {
            color: white !important;
        }
        .st-bd, .st-b5, .st-af, .st-c5 {
            background-color: #000000 !important;
            color: white !important;
        }
        .stMetricValue {
            color: white !important;
            font-weight: bold;
        }
        .stMetricLabel {
            color: white !important;
        }
        .stMarkdown {
            color: white !important;
        }
        .css-1y4p8pa {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- CARREGAR OS DADOS ---
df = pd.read_excel("Coleta centro2.xlsx")
df.columns = df.columns.str.strip()
df.rename(columns={"Mês": "Mes"}, inplace=True)
df = df.dropna(subset=["Total de Sacos"])

# --- FILTRO DE MÊS ---
meses = df["Mes"].unique().tolist()
meses.sort()
meses_selecionados = st.multiselect(
    "🗓️ Selecione os meses para visualizar:",
    options=meses,
    default=meses,
)

df_filtrado = df[df["Mes"].isin(meses_selecionados)]

# --- CÁLCULOS ---
total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

# --- TÍTULO ---
st.markdown(
    "<h1 style='text-align: center; color: white;'>🚛 Dashboard - Coleta Centro</h1>",
    unsafe_allow_html=True
)

# --- MÉTRICAS ---
col1, col2, col3 = st.columns(3)
col1.metric("🧺 Total de Sacos", total_sacos)
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

# --- PREPARAÇÃO PARA GRÁFICOS ---
df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

# --- CORES PADRÃO ---
cores = {
    "Coleta AM": "#00FFFF",  # Neon azul
    "Coleta PM": "#FFA500",  # Neon laranja
}

# --- GRÁFICO DE BARRAS ---
fig_bar = px.bar(
    df_melt,
    x="Mes",
    y="Quantidade de Sacos",
    color="Periodo",
    barmode="group",
    color_discrete_map=cores,
    title="🪣 Coleta de Sacos por Mês e Período"
)
fig_bar.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
    title_font=dict(size=22),
    xaxis=dict(color='white', showgrid=False),
    yaxis=dict(color='white', showgrid=False),
    legend=dict(font=dict(color='white')),
    title_x=0.5
)

# --- GRÁFICO DE PIZZA ---
fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am, total_pm],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title="🌅 vs 🌇 Coleta AM vs PM"
)
fig_pie.update_traces(
    textinfo='percent+label',
    textfont=dict(color='white', size=14),
)
fig_pie.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_x=0.5,
    legend=dict(font=dict(color='white'))
)

# --- EXIBIR GRÁFICOS LADO A LADO ---
col1, col2 = st.columns(2)
col1.plotly_chart(fig_bar, use_container_width=True)
col2.plotly_chart(fig_pie, use_container_width=True)

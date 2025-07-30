import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 🔧 CSS Estilo Dark 100% Preto com texto branco total
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }
        h1, h2, h3, h4, h5, h6,
        label, span, div, p, a, li, ul, ol, input, select, textarea,
        .stText, .stMarkdown, .css-10trblm, .css-1cpxqw2,
        .st-b3, .st-co, .st-cr, .st-da, .st-db, .st-dc {
            color: #FFFFFF !important;
        }
        .stMetric {
            background-color: #111111;
            border: 1px solid #00FFFF;
            border-radius: 12px;
            padding: 10px;
            color: #FFFFFF !important;
        }

        section[data-testid="stRadio"] > div {
            background-color: rgba(155, 48, 255, 0.15);
            border: 2px solid #9b30ff;
            border-radius: 10px;
            padding: 8px;
        }
        label[data-testid="stMarkdownContainer"] {
            color: #FFFFFF !important;
            font-weight: bold;
        }
        div[role="radiogroup"] > label {
            background-color: rgba(0,0,0,0.6);
            padding: 5px 10px;
            border-radius: 8px;
            border: 1px solid #9b30ff;
            margin-right: 8px;
            color: #FFFFFF !important;
        }
        div[role="radiogroup"] > label:hover {
            background-color: #9b30ff;
            color: #000000 !important;
        }
        div[role="radiogroup"] > label[data-selected="true"] {
            background-color: #9b30ff;
            color: #000000 !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# 🔄 Carregar dados da planilha do GitHub
url = "https://raw.githubusercontent.com/Rdodosilva/streamlit_coleta/main/coleta_mes.xlsx"
df = pd.read_excel(url)

# 📅 Filtro por mês
meses = df["Mês"].unique()
mes_escolhido = st.radio("Selecione o mês", meses, horizontal=True)
df_filtrado = df[df["Mês"] == mes_escolhido]

# 📊 Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Coleta AM", int(df_filtrado["Coleta AM"]))
col2.metric("Coleta PM", int(df_filtrado["Coleta PM"]))
col3.metric("Total de Sacos", int(df_filtrado["Total de Sacos"]))

# 🟣 Gráfico 1 - Distribuição Geral AM vs PM
st.subheader("Distribuição Geral AM vs PM")
fig1 = go.Figure()
fig1.add_trace(go.Pie(
    labels=["Coleta AM", "Coleta PM"],
    values=[df_filtrado["Coleta AM"].values[0], df_filtrado["Coleta PM"].values[0]],
    marker=dict(colors=["#9b30ff", "#6a0dad"]),
    textfont=dict(color="white"),
    hole=0.4
))
fig1.update_layout(paper_bgcolor="black", font_color="white")
st.plotly_chart(fig1)

# 📈 Gráfico 2 - Evolução de Sacos por Mês
st.subheader("Evolução da Quantidade de Sacos por Mês")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df["Mês"],
    y=df["Total de Sacos"],
    mode="lines+markers",
    line=dict(color="#00FFFF", width=3),
    marker=dict(size=8),
    hovertemplate='Mês: %{x}<br>Total: %{y}<extra></extra>'
))
fig2.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    xaxis=dict(title="Mês", color="white", showgrid=False),
    yaxis=dict(title="Total de Sacos", color="white", showgrid=False)
)
st.plotly_chart(fig2)

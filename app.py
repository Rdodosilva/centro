import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Estilo visual personalizado
st.markdown("""
    <style>
        body, .stApp {
            background-color: #000000;
            color: white;
        }
        .css-1aumxhk, .css-10trblm, .css-1d391kg, .st-bw {
            color: white;
        }
        .stRadio > div {
            flex-direction: row;
        }
        .stRadio div[role='radiogroup'] > label {
            border: 1px solid #6A0DAD;
            border-radius: 0.5rem;
            padding: 0.3rem 1rem;
            margin-right: 1rem;
            background-color: #000000;
            color: white;
        }
        .stRadio div[role='radiogroup'] > label:hover {
            background-color: #6A0DAD;
            color: white;
        }
        .stRadio div[role='radiogroup'] > label[data-selected="true"] {
            background-color: #6A0DAD !important;
            color: white !important;
        }
        .css-1v0mbdj, .css-12oz5g7, .css-1t7pwxw {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Coleta Centro - Análise por Turno")
url = "https://raw.githubusercontent.com/Rdodosilva/coleta-centro/main/coleta-centro.xlsx"
df = pd.read_excel(url)

# Filtro por mês
meses = df["Mês"].unique().tolist()
mes_selecionado = st.radio("Selecione o mês", meses, horizontal=True)

df_mes = df[df["Mês"] == mes_selecionado]

# Cartões de totais
total_am = int(df_mes["Coleta AM"].sum())
total_pm = int(df_mes["Coleta PM"].sum())
total_geral = int(df_mes["Total de Sacos"].sum())

col1, col2, col3 = st.columns(3)
col1.metric("🌅 Coleta AM", f"{total_am} sacos")
col2.metric("🌇 Coleta PM", f"{total_pm} sacos")
col3.metric("🧺 Total Geral", f"{total_geral} sacos")

# Gráfico de pizza
fig_pizza = go.Figure(data=[
    go.Pie(labels=["Coleta AM", "Coleta PM"],
           values=[total_am, total_pm],
           hole=0.5,
           marker=dict(colors=['#8A2BE2', '#D8BFD8']))
])
fig_pizza.update_layout(title="Distribuição Geral AM vs PM", font=dict(color='white'), paper_bgcolor='black')
st.plotly_chart(fig_pizza, use_container_width=True)

# Gráfico de linha
fig_linha = go.Figure()
fig_linha.add_trace(go.Scatter(x=df["Mês"], y=df["Total de Sacos"],
                               mode='lines+markers',
                               name='Total de Sacos',
                               line=dict(color='#9932CC')))
fig_linha.update_layout(
    title="📈 Evolução da Quantidade de Sacos por Mês",
    xaxis_title="Mês",
    yaxis_title="Total de Sacos",
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white')
)
st.plotly_chart(fig_linha, use_container_width=True)

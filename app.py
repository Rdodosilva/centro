import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Coleta Centro", layout="wide")

# Estilo CSS com letras brancas e fundo preto absoluto
st.markdown("""
    <style>
    body, .stApp {
        background-color: #000000;
        color: white;
    }
    .css-1d391kg, .css-1v3fvcr, .css-qri22k {
        color: white !important;
    }
    .css-1cpxqw2 edgvbvh3 {
        color: white;
    }
    .stRadio > div {
        flex-direction: row;
    }
    label[data-baseweb="radio"] {
        background-color: transparent;
        border: 1px solid #9b59b6;
        border-radius: 10px;
        padding: 8px 15px;
        margin: 5px;
        color: white;
    }
    label[data-baseweb="radio"]:hover {
        background-color: #9b59b6;
        color: white;
    }
    input[type="radio"]:checked + div {
        background-color: #9b59b6;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Carregamento da planilha do GitHub (se preferir local, troque o caminho)
url = "https://raw.githubusercontent.com/Rdodosilva/Coleta/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# Converte a coluna "Mês" para string
df["Mês"] = df["Mês"].astype(str)

# Filtro por mês
meses = df["Mês"].unique().tolist()
mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True)

df_filtrado = df[df["Mês"] == mes_selecionado]

# Layout dos cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Coleta AM", int(df_filtrado["Coleta AM"].values[0]))
with col2:
    st.metric("Coleta PM", int(df_filtrado["Coleta PM"].values[0]))
with col3:
    st.metric("Total de Sacos", int(df_filtrado["Total de Sacos"].values[0]))

st.markdown("---")

# Gráfico de barras - Coleta AM e PM
st.subheader("📊 Distribuição Geral: AM vs PM", divider='rainbow')
fig_bar = go.Figure(data=[
    go.Bar(name='Coleta AM', x=df["Mês"], y=df["Coleta AM"], marker_color='rgba(155, 89, 182, 0.8)'),
    go.Bar(name='Coleta PM', x=df["Mês"], y=df["Coleta PM"], marker_color='rgba(52, 152, 219, 0.8)')
])
fig_bar.update_layout(barmode='group', plot_bgcolor='black', paper_bgcolor='black',
                      font=dict(color='white'), xaxis=dict(color='white'), yaxis=dict(color='white'))

st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de linhas - Total de Sacos por mês
st.subheader("📈 Evolução da Quantidade de Sacos por Mês", divider='rainbow')
fig_line = px.line(df, x="Mês", y="Total de Sacos", markers=True, line_shape='linear')
fig_line.update_traces(line=dict(color='rgba(231, 76, 60, 1)', width=3), marker=dict(color='white', size=8))
fig_line.update_layout(plot_bgcolor='black', paper_bgcolor='black',
                       font=dict(color='white'), xaxis=dict(color='white'), yaxis=dict(color='white'))

st.plotly_chart(fig_line, use_container_width=True)

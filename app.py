import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Estilo customizado
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: white;
    }
    .main {
        background-color: #000000;
        color: white;
    }
    div[data-testid="metric-container"] {
        border: 1px solid #8A2BE2;
        border-radius: 12px;
        padding: 10px;
        background-color: #111111;
        color: white;
    }
    div[data-testid="metric-container"] > label {
        color: white;
    }
    [role="radiogroup"] > div {
        border: 1px solid #8A2BE2;
        border-radius: 10px;
        padding: 5px;
        margin-right: 8px;
        background-color: transparent;
        color: white;
    }
    [role="radiogroup"] > div:hover {
        background-color: #8A2BE233;
    }
    .stRadio label {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Carrega os dados
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# Filtro de mês
meses = df["Mês"].unique()
mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True)

# Filtra os dados
df_filtrado = df[df["Mês"] == mes_selecionado]

# Layout de métricas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Sacos", f"{int(df_filtrado['Total de Sacos'].sum())} sacos")
col2.metric("Coleta AM", f"{int(df_filtrado['Coleta Am'].sum())} sacos")
col3.metric("Coleta PM", f"{int(df_filtrado['Coleta PM'].sum())} sacos")

# Gráfico de barras: AM vs PM
fig1 = go.Figure(data=[
    go.Bar(name='Coleta AM', x=df_filtrado["Mês"], y=df_filtrado["Coleta Am"], marker_color='mediumpurple'),
    go.Bar(name='Coleta PM', x=df_filtrado["Mês"], y=df_filtrado["Coleta PM"], marker_color='purple')
])
fig1.update_layout(
    barmode='group',
    title='Distribuição Geral AM vs PM',
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    xaxis=dict(color='white'),
    yaxis=dict(color='white'),
    legend=dict(font=dict(color='white'))
)

# Gráfico de linha: evolução mensal
df_grouped = df.groupby("Mês")[["Coleta Am", "Coleta PM", "Total de Sacos"]].sum().reset_index()
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_grouped["Mês"], y=df_grouped["Total de Sacos"], mode='lines+markers', name='Total de Sacos', line=dict(color='violet')))
fig2.add_trace(go.Scatter(x=df_grouped["Mês"], y=df_grouped["Coleta Am"], mode='lines+markers', name='Coleta AM', line=dict(color='mediumpurple')))
fig2.add_trace(go.Scatter(x=df_grouped["Mês"], y=df_grouped["Coleta PM"], mode='lines+markers', name='Coleta PM', line=dict(color='purple')))
fig2.update_layout(
    title='Evolução da Coleta por Mês',
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    xaxis=dict(color='white'),
    yaxis=dict(color='white'),
    legend=dict(font=dict(color='white'))
)

# Exibição dos gráficos
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

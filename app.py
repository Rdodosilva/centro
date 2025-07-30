import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(layout="wide", page_title="Dashboard Coleta", page_icon="♻️")

# CSS customizado
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .css-18e3th9 {
            background-color: #000000;
        }
        .css-1d391kg {
            background-color: #000000;
        }
        .metric-container {
            transition: transform 0.3s ease;
        }
        .metric-container:hover {
            transform: scale(1.05);
        }
        .stRadio > div {
            background-color: transparent;
            border: 1px solid #8a2be2;
            border-radius: 10px;
            padding: 10px;
        }
        .stRadio label {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Carregar os dados do GitHub (formato .xlsx)
url = "https://raw.githubusercontent.com/Rdodosilva/dados/main/coleta_am_pm.xlsx"
df = pd.read_excel(url)

# Garantir que colunas estejam corretas
df.columns = [col.strip() for col in df.columns]

# Converter a coluna de data
df['Data'] = pd.to_datetime(df['Data'])

# Filtros
meses = df['Data'].dt.strftime('%B').unique()
mes_selecionado = st.radio("Selecione o mês", meses, horizontal=True)

df_filtrado = df[df['Data'].dt.strftime('%B') == mes_selecionado]

# Layout - Cards com animação
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Quantidade de Sacos", int(df_filtrado['Quantidade de Sacos'].sum()))
with col2:
    st.metric("Turno AM", int(df_filtrado[df_filtrado['Turno'] == 'AM']['Quantidade de Sacos'].sum()))
with col3:
    st.metric("Turno PM", int(df_filtrado[df_filtrado['Turno'] == 'PM']['Quantidade de Sacos'].sum()))

st.markdown("---")

# Distribuição geral AM vs PM
st.subheader("Distribuição Geral AM vs PM")
fig_turno = px.pie(df_filtrado, names='Turno', values='Quantidade de Sacos', color_discrete_sequence=px.colors.sequential.Purples)
fig_turno.update_layout(paper_bgcolor='black', font_color='white')
st.plotly_chart(fig_turno, use_container_width=True)

# Evolução mensal
st.subheader("Evolução da Quantidade de Sacos por Mês")
df_mes = df.copy()
df_mes['Mês'] = df_mes['Data'].dt.strftime('%B')
df_grouped = df_mes.groupby(['Mês', 'Turno'])['Quantidade de Sacos'].sum().reset_index()
fig_linha = px.line(df_grouped, x='Mês', y='Quantidade de Sacos', color='Turno', markers=True, line_shape='spline')
fig_linha.update_layout(paper_bgcolor='black', font_color='white', plot_bgcolor='black')
fig_linha.update_traces(line=dict(width=3), marker=dict(size=8))
st.plotly_chart(fig_linha, use_container_width=True)

# Rodapé
st.markdown("<hr style='border-color: #8a2be2;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;'>♻️ <b>Dashboard de Coleta | Atualizado automaticamente via GitHub</b></div>", unsafe_allow_html=True)

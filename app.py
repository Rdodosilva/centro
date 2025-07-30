import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Coleta", layout="wide", page_icon="🟣")

# --- Estilo visual ---
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: white;
    }
    .css-1v0mbdj, .css-10trblm {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Título ---
st.title("🚛 Dashboard de Coleta por Mês - Centro")

# --- Leitura do arquivo Excel ---
df = pd.read_excel("Coleta centro2.xlsx")
df.columns = df.columns.str.strip()

# --- Tratamento dos nomes de colunas ---
# Supondo que temos colunas: 'Mês', 'Coleta AM', 'Coleta PM' e 'Qtd Sacos'
colunas_esperadas = ['Mês', 'Coleta', 'Qtd Sacos']
for col in colunas_esperadas:
    if col not in df.columns:
        st.error(f"❌ Coluna esperada não encontrada: '{col}'")
        st.stop()

# --- Filtro de Turno ---
turnos = df['Turno'].dropna().unique()
turno_selecionado = st.radio("Selecione o turno:", options=turnos, horizontal=True)

df_filtrado = df[df['Turno'] == turno_selecionado]

# --- Agrupamento por Mês ---
df_grouped = df_filtrado.groupby('Mês')['Qtd Sacos'].sum().reset_index()

# Ordenar meses manualmente (ajustar caso esteja em ordem diferente)
ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
df_grouped['Mês'] = pd.Categorical(df_grouped['Mês'], categories=ordem_meses, ordered=True)
df_grouped = df_grouped.sort_values('Mês')

# --- Gráfico animado de evolução ---
fig = px.bar(df_grouped,
             x='Mês',
             y='Qtd Sacos',
             text='Qtd Sacos',
             title=f"Evolução da Coleta de Sacos por Mês ({turno_selecionado})",
             template='plotly_dark',
             labels={'Qtd Sacos': 'Quantidade de Sacos'})

fig.update_traces(textposition='outside')
fig.update_layout(xaxis_title="Mês", yaxis_title="Sacos Coletados", height=500)

st.plotly_chart(fig, use_container_width=True)

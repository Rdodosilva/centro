import streamlit as st
import pandas as pd
import plotly.express as px

# URL do ARQUIVO XLSX no GitHub
url = "https://raw.githubusercontent.com/seu-usuario/seu-repositorio/main/sua_planilha.xlsx"

@st.cache_data
def carregar_dados():
    df = pd.read_excel(url)
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
    df['Mês'] = df['Data'].dt.month_name().str.lower()
    return df

df = carregar_dados()

# Estilo visual preto, texto branco, botões roxos com contorno
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: white;
    }
    .stMetric {
        border: 2px solid #00FFFF;
        border-radius: 10px;
        padding: 12px;
        background-color: #111111;
    }
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
    }
    div[role='radiogroup'] > label {
        border: 2px solid #8a2be2;
        border-radius: 10px;
        padding: 8px 16px;
        margin: 5px;
        color: white !important;
        background-color: black;
        cursor: pointer;
    }
    div[role='radiogroup'] > label[data-selected="true"] {
        background-color: #8a2be2 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título e filtro por mês
st.markdown("<h1 style='text-align: center; color: white;'>🚛 Dashboard de Coleta</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Filtre por mês:</h3>", unsafe_allow_html=True)

# Mês em ordem correta
meses_ordenados = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
meses_disponiveis = sorted(df['Mês'].dropna().unique(), key=lambda x: meses_ordenados.index(x))
mes_escolhido = st.radio("", meses_disponiveis, horizontal=True)

# Filtra o mês escolhido
df_mes = df[df['Mês'] == mes_escolhido]

# Métricas
total_sacos = int(df_mes['Total de Sacos'].sum())
total_am = int(df_mes['Coleta AM'].sum())
total_pm = int(df_mes['Coleta PM'].sum())

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Sacos", total_sacos)
with col2:
    st.metric("Coleta AM", total_am)
with col3:
    st.metric("Coleta PM", total_pm)

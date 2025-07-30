import streamlit as st
import pandas as pd
import plotly.express as px

# Link do GitHub com a planilha
URL_PLANILHA = "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPOSITORIO/main/nome_da_planilha.csv"

# Carregando os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv(URL_PLANILHA, sep=';', encoding='utf-8')

df = carregar_dados()

# Convertendo coluna de data (caso necessário)
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)

# Extraindo o nome do mês
df['Mês'] = df['Data'].dt.month_name().str.lower()

# Estilo CSS para tema dark total e botões roxos
st.markdown("""
    <style>
    body, .stApp {
        background-color: #000000;
        color: white;
    }
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
    }
    div[role='radiogroup'] > label {
        border: 2px solid #8a2be2;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        color: white !important;
        background-color: #000000;
    }
    div[role='radiogroup'] > label[data-selected="true"] {
        background-color: #8a2be2 !important;
        color: white !important;
    }
    .stMetric {
        border: 2px solid #00ffff;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("<h1 style='text-align: center;'>🚛 Coleta Centro</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>📅 Selecione o mês:</h3>", unsafe_allow_html=True)

# Filtro de mês
meses_disponiveis = df['Mês'].dropna().unique().tolist()
meses_disponiveis = sorted(meses_disponiveis, key=lambda x: ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'].index(x))
mes_selecionado = st.radio("", meses_disponiveis, horizontal=True)

# Filtrando os dados
df_filtrado = df[df['Mês'] == mes_selecionado]

# Métricas principais
total_sacos = int(df_filtrado['Qtde Saco'].sum())
peso_total = int(df_filtrado['Peso'].sum())

col1, col2 = st.columns(2)
with col1:
    st.metric("🥔 Total de Sacos", total_sacos)
with col2:
    st.metric("⚖️ Peso Total", f"{peso_total} kg")

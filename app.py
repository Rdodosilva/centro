import streamlit as st
import pandas as pd
import os

@st.cache_data
def carregar_dados(uploaded_file=None):
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
    elif os.path.exists("dados_coleta.xlsx"):
        df = pd.read_excel("dados_coleta.xlsx")
    else:
        return None
    return df

# Upload manual caso o arquivo não esteja disponível
uploaded_file = st.file_uploader("⚠️ Arquivo 'dados_coleta.xlsx' não encontrado. Faça o upload abaixo", type=["xlsx"])
df = carregar_dados(uploaded_file)

if df is None:
    st.warning("📂 Por favor, envie o arquivo 'dados_coleta.xlsx' para continuar.")
    st.stop()

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Layout da página ---
st.set_page_config(layout="wide", page_title="Dashboard Coleta Centro", initial_sidebar_state="collapsed")

# --- Estilo personalizado ---
st.markdown("""
    <style>
        body, .stApp {
            background-color: #000000;
            color: white;
        }
        .stRadio > div {
            flex-direction: row;
            gap: 15px;
        }
        .stRadio label {
            background-color: transparent;
            border: 1px solid #8000ff;
            padding: 0.3em 1em;
            border-radius: 0.5em;
            color: white;
            cursor: pointer;
        }
        .stRadio input:checked + label {
            background-color: #8000ff;
        }
    </style>
""", unsafe_allow_html=True)

# --- Carregar dados ---
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Coleta centro2.xlsx")
    df["Mês"] = pd.Categorical(df["Mês"], ordered=True, categories=df["Mês"].unique())
    return df

df = carregar_dados()

# --- Filtro de mês ---
meses = df["Mês"].unique().tolist()
mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True, label_visibility="collapsed")

# --- Dados filtrados ---
df_filtrado = df[df["Mês"] == mes_selecionado]

# --- Cartões com totais ---
col1, col2, col3 = st.columns(3)
col1.metric("Coleta AM", int(df_filtrado["Coleta AM"].values[0]))
col2.metric("Coleta PM", int(df_filtrado["Coleta PM"].values[0]))
col3.metric("Total de Sacos", int(df_filtrado["Total de Sacos"].values[0]))

# --- Gráfico de linha com evolução ---
fig = px.line(
    df,
    x="Mês",
    y="Total de Sacos",
    markers=True,
    title="Evolução da Coleta de Sacos por Mês",
    template="plotly_dark"
)
fig.update_traces(line=dict(color="#8000ff", width=3))
fig.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black",
    font=dict(color="white"),
    title_font_size=20,
    hoverlabel=dict(bgcolor="black", font_size=14)
)

st.plotly_chart(fig, use_container_width=True)

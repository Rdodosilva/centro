import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Dashboard de Coleta", layout="wide", page_icon="♻️")

# Estilo global (dark, branco, roxo)
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .stApp {
            background-color: #000000;
        }
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
        .css-1aumxhk {
            background-color: #000000;
        }
        .stRadio > div {
            flex-direction: row;
        }
        .st-eb {
            color: white;
        }
        section[data-testid="stSidebar"] {
            background-color: #0f0f0f;
        }
        .element-container:has(.stRadio) label {
            background-color: #000;
            color: white;
            border: 1px solid #8000ff;
            border-radius: 10px;
            padding: 5px 10px;
            margin: 2px;
        }
        .element-container:has(.stRadio) label[data-selected="true"] {
            background-color: #8000ff;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def carregar_dados(uploaded_file=None):
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
    elif os.path.exists("Coleta centro2.xlsx"):
        df = pd.read_excel("Coleta centro2.xlsx")
    else:
        return None
    return df

st.title("♻️ Dashboard de Coleta - Turnos AM/PM")

uploaded_file = st.file_uploader("📂 Faça o upload da planilha de coleta (.xlsx)", type=["xlsx"])
df = carregar_dados(uploaded_file)

if df is None:
    st.warning("⚠️ Nenhuma planilha encontrada. Envie o arquivo 'Coleta centro2.xlsx' para continuar.")
    st.stop()

# Filtros
meses = sorted(df['MÊS'].unique())
mes_selecionado = st.radio("Selecione o Mês:", meses, index=len(meses)-1)

df_filtrado = df[df['MÊS'] == mes_selecionado]

# Layout 2 colunas
col1, col2 = st.columns(2)

with col1:
    total_turno_am = df_filtrado['TURNOS AM'].sum()
    total_turno_pm = df_filtrado['TURNOS PM'].sum()
    st.metric("Total Turno AM", f"{total_turno_am}")
    st.metric("Total Turno PM", f"{total_turno_pm}")

with col2:
    media_am = round(df_filtrado['TURNOS AM'].mean(), 2)
    media_pm = round(df_filtrado['TURNOS PM'].mean(), 2)
    st.metric("Média AM", media_am)
    st.metric("Média PM", media_pm)

# Gráfico de barras por bairro
fig_bar = px.bar(df_filtrado, x='BAIRRO', y=['TURNOS AM', 'TURNOS PM'],
                 barmode='group', title="Quantidade de Turnos por Bairro",
                 color_discrete_map={'TURNOS AM': '#8000ff', 'TURNOS PM': '#00ffff'})
fig_bar.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')

# Gráfico de pizza
soma_turnos = df_filtrado[['TURNOS AM', 'TURNOS PM']].sum()
fig_pie = px.pie(values=soma_turnos.values, names=soma_turnos.index,
                 title="Proporção AM vs PM", color_discrete_sequence=['#8000ff', '#00ffff'])
fig_pie.update_layout(paper_bgcolor='black', font_color='white')

# Gráfico de linha comparativo AM x PM
fig_linha = px.line(df_filtrado, x='BAIRRO', y=['TURNOS AM', 'TURNOS PM'],
                    markers=True, title="Comparativo AM x PM por Bairro",
                    color_discrete_map={'TURNOS AM': '#8000ff', 'TURNOS PM': '#00ffff'})
fig_linha.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')

# Mostrar gráficos
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_pie, use_container_width=True)
st.plotly_chart(fig_linha, use_container_width=True)

# Tabela expandida
with st.expander("📊 Ver dados detalhados"):
    st.dataframe(df_filtrado.style.set_properties(**{
        'background-color': '#000000',
        'color': 'white',
        'border-color': 'white'
    }))

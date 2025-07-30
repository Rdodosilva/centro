import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO DO DASHBOARD
st.set_page_config(page_title="Coleta Centro - Painel", layout="wide", page_icon="🗑️")

# ESTILO FUTURISTA ESCURO
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .stApp {
            background-color: #000000;
        }
        .titulo {
            color: white;
            font-size: 2em;
            font-weight: bold;
        }
        .valor {
            font-size: 2em;
            font-weight: bold;
            color: deepskyblue;
        }
        .stRadio > div {
            flex-direction: row;
        }
        .css-1n76uvr {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# TÍTULO
st.markdown("<div class='titulo'>📊 Dashboard de Coleta - Centro</div>", unsafe_allow_html=True)

# CARREGAR PLANILHA
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Coleta centro2.xlsx")
    df.columns = df.columns.str.strip().str.replace('\xa0', ' ').str.replace('\n', '').str.lower()
    df = df.rename(columns={
        'mês': 'Mes',
        'coleta am': 'Coleta_AM',
        'coleta pm': 'Coleta_PM',
        'total de sacos': 'Total_Sacos'
    })
    df['Mes'] = pd.Categorical(df['Mes'], categories=df['Mes'].unique(), ordered=True)
    return df

df = carregar_dados()

# FILTRO DE MÊS COM ESTILO ROXO
meses = df['Mes'].unique().tolist()
mes_selecionado = st.radio("🗓️ Selecione o Mês:", meses, horizontal=True)
df_filtrado = df[df['Mes'] == mes_selecionado]

# VALORES TOTAIS
total_am = int(df_filtrado['Coleta_AM'].sum())
total_pm = int(df_filtrado['Coleta_PM'].sum())
total_geral = int(df_filtrado['Total_Sacos'].sum())

col1, col2, col3 = st.columns(3)
col1.markdown("### 🌅 Coleta AM")
col1.markdown(f"<div class='valor'>{total_am}</div>", unsafe_allow_html=True)

col2.markdown("### 🌇 Coleta PM")
col2.markdown(f"<div class='valor'>{total_pm}</div>", unsafe_allow_html=True)

col3.markdown("### 🗑️ Total de Sacos")
col3.markdown(f"<div class='valor'>{total_geral}</div>", unsafe_allow_html=True)

st.markdown("---")

# GRÁFICO DE BARRAS - COLETA AM
fig_am = px.bar(
    df, x='Coleta_AM', y='Mes', orientation='h', title='Coleta AM por Mês',
    labels={'Coleta_AM': 'Quantidade', 'Mes': 'Mês'}, template='plotly_dark'
)
fig_am.update_traces(marker_color='mediumpurple')
st.plotly_chart(fig_am, use_container_width=True)

# GRÁFICO DE BARRAS - COLETA PM
fig_pm = px.bar(
    df, x='Coleta_PM', y='Mes', orientation='h', title='Coleta PM por Mês',
    labels={'Coleta_PM': 'Quantidade', 'Mes': 'Mês'}, template='plotly_dark'
)
fig_pm.update_traces(marker_color='orchid')
st.plotly_chart(fig_pm, use_container_width=True)

# NOVO GRÁFICO DE LINHA - EVOLUÇÃO DOS SACOS
fig_linha = px.line(
    df, x="Mes", y="Total_Sacos", markers=True,
    title="📈 Evolução da Quantidade de Sacos Coletados",
    labels={"Mes": "Mês", "Total_Sacos": "Total de Sacos"}, template="plotly_dark"
)
fig_linha.update_traces(line_color="deepskyblue", marker=dict(size=10, color='white'))
fig_linha.update_layout(font=dict(color='white', size=14), plot_bgcolor='black', paper_bgcolor='black')
st.plotly_chart(fig_linha, use_container_width=True)

# EXIBIR DADOS (OPCIONAL)
with st.expander("📄 Ver dados da planilha"):
    st.dataframe(df, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÕES DO APP
st.set_page_config(
    page_title="Dashboard de Coleta - Centro",
    layout="wide",
    page_icon="🗑️"
)

# ESTILO CUSTOMIZADO (Dark puro com branco)
st.markdown(
    """
    <style>
        body {
            background-color: #000000;
            color: #FFFFFF;
        }
        .stApp {
            background-color: #000000;
        }
        .stMarkdown, .stDataFrame, .stPlotlyChart {
            color: white;
        }
        .stRadio > div {
            flex-direction: row;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# TÍTULO
st.title("📊 Evolução da Coleta de Sacos - Centro")
st.markdown("Visualização interativa da quantidade de sacos coletados (AM + PM) por mês.")

# FUNÇÃO PARA CARREGAR E TRATAR OS DADOS
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Coleta centro2.xlsx")

    # Padroniza nomes das colunas
    df.columns = df.columns.str.strip().str.replace('\xa0', ' ').str.replace('\n', '').str.lower()

    df = df.rename(columns={
        'mês': 'Mes',
        'coleta am': 'Coleta_AM',
        'coleta pm': 'Coleta_PM',
        'total de sacos': 'Total_Sacos'
    })

    # Garante a ordem correta dos meses
    df['Mes'] = pd.Categorical(df['Mes'], categories=df['Mes'].unique(), ordered=True)

    return df

# CARREGA OS DADOS
df = carregar_dados()

# EXIBE A TABELA OPCIONALMENTE
with st.expander("📄 Ver dados da coleta"):
    st.dataframe(df, use_container_width=True)

# GRÁFICO DE LINHA (EVOLUÇÃO DOS SACOS)
fig = px.line(
    df,
    x="Mes",
    y="Total_Sacos",
    markers=True,
    title="Evolução Mensal da Quantidade de Sacos Coletados",
    labels={"Mes": "Mês", "Total_Sacos": "Total de Sacos"},
    template="plotly_dark"
)

fig.update_traces(line_color="deepskyblue", marker=dict(size=10, color='white'))
fig.update_layout(
    font=dict(color='white', size=14),
    plot_bgcolor='black',
    paper_bgcolor='black'
)

# MOSTRA O GRÁFICO
st.plotly_chart(fig, use_container_width=True)

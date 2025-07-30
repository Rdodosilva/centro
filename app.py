import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def carregar_dados():
    df = pd.read_excel("Coleta centro2.xlsx")

    # Corrigir nomes de colunas
    df.columns = df.columns.str.strip().str.replace('\xa0', ' ').str.replace('\n', '').str.lower()
    
    # Mostrar nomes de colunas lidos
    st.write("Colunas detectadas:", df.columns.tolist())

    # Renomear para padronizar
    df = df.rename(columns={
        'mês': 'Mes',
        'coleta am': 'Coleta_AM',
        'coleta pm': 'Coleta_PM',
        'total de sacos': 'Total_Sacos'
    })

    # Garantir que a coluna Mês está como categórica ordenada
    df['Mes'] = pd.Categorical(df['Mes'], ordered=True, categories=df['Mes'].unique())

    return df

df = carregar_dados()

# Gráfico de evolução da quantidade de sacos por mês
fig = px.line(df, x='Mes', y='Total_Sacos', markers=True,
              title='Evolução da Quantidade de Sacos por Mês',
              labels={'Mes': 'Mês', 'Total_Sacos': 'Total de Sacos'},
              template='plotly_dark')

fig.update_traces(line_color='cyan')
fig.update_layout(
    font=dict(color='white'),
    paper_bgcolor='black',
    plot_bgcolor='black'
)

st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO DO APP
st.set_page_config(
    page_title="Coleta de Sacos - Centro",
    layout="wide",
    page_icon="🗑️"
)

st.markdown(
    """
    <style>
        body {
            background-color: black;
            color: white;
        }
        .css-1d391kg {
            background-color: #0f0f0f !important;
        }
        .stRadio > div {
            flex-direction: row;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Evolução da Quantidade de Sacos por Mês")
st.markdown("Este painel apresenta a evolução mensal do total de sacos coletados (AM + PM) no centro da cidade.")

# FUNÇÃO PARA CARREGAR E TRATAR DADOS
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Coleta centro2.xlsx")

    # Normaliza os nomes das colunas
    df.columns = df.columns.str.strip().str.replace('\xa0', ' ').str.replace('\n', '').str.lower()

    # Renomeia colunas para padronização
    df = df.rename(columns={
        'mês': 'Mes',
        'coleta am': 'Coleta_AM',
        'coleta pm': 'Coleta_PM',
        'total de sacos': 'Total_Sacos'
    })

    # Garante que 'Mes' esteja em ordem correta
    df['Mes'] = pd.Categorical(df['Mes'], categories=df['Mes'].unique(), ordered=True)

    return df

# CARREGA OS DADOS
df = carregar_dados()

# EXIBE OS DADOS EM TABELA EXPANSÍVEL
with st.expander("📄 Ver dados"):
    st.dataframe(df, use_container_width=True)

# GRÁFICO DE LINHA INTERATIVO
fig = px.line(
    df,
    x="Mes",
    y="Total_Sacos",
    markers=True,
    title="Evolução da Quantidade de Sacos Coletados",
    labels={"Mes": "Mês", "Total_Sacos": "Total de Sacos"},
    template="plotly_dark"
)

fig.update_traces(line_color="cyan", marker=dict(size=10, color='white'))
fig.update_layout(
    font=dict(color='white'),
    plot_bgcolor='black',
    paper_bgcolor='black'
)

# EXIBE O GRÁFICO
st.plotly_chart(fig, use_container_width=True)

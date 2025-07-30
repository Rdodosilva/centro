import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide", page_title="Coleta Centro", initial_sidebar_state="collapsed")

# --- CSS CUSTOMIZADO ---
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .stApp {
            background-color: #000000;
        }
        .block-container {
            padding: 1rem 2rem 2rem 2rem;
        }
        .metric-card {
            background-color: #000000;
            border: 2px solid #7f00ff;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        .metric-card h1 {
            color: white;
            font-size: 32px;
        }
        .metric-card p {
            color: white;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# --- LEITURA DOS DADOS ---
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# Garantir nomes padronizados das colunas
df.columns = [col.strip() for col in df.columns]
df['Mês'] = df['Mês'].astype(str).str.upper()

# --- FILTRO POR MÊS ---
meses_disponiveis = df['Mês'].unique()
mes_escolhido = st.radio("Selecione o mês:", options=meses_disponiveis, horizontal=True,
                         label_visibility="collapsed")

df_filtrado = df[df['Mês'] == mes_escolhido]

# --- MÉTRICAS COM ANIMAÇÃO E CONTORNO ---
with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        total_sacos = int(df_filtrado['Total de Sacos'].sum())
        st.markdown(f"""
            <div class="metric-card">
                <p>Total de Sacos</p>
                <h1>{total_sacos}</h1>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        coleta_am = int(df_filtrado['Coleta Am'].sum())
        st.markdown(f"""
            <div class="metric-card">
                <p>Coleta AM</p>
                <h1>{coleta_am}</h1>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        coleta_pm = int(df_filtrado['Coleta PM'].sum())
        st.markdown(f"""
            <div class="metric-card">
                <p>Coleta PM</p>
                <h1>{coleta_pm}</h1>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# --- GRÁFICO DE BARRAS: Distribuição AM vs PM ---
fig_barras = go.Figure()
fig_barras.add_trace(go.Bar(
    x=["Coleta AM", "Coleta PM"],
    y=[coleta_am, coleta_pm],
    marker_color=['#9F00FF', '#7B68EE']
))
fig_barras.update_layout(
    title="Distribuição Geral: AM vs PM",
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(color='white')
)
st.plotly_chart(fig_barras, use_container_width=True)

# --- GRÁFICO DE LINHA: Evolução por Mês ---
df_mensal = df.groupby("Mês")[["Coleta Am", "Coleta PM", "Total de Sacos"]].sum().reset_index()

fig_linha = go.Figure()
fig_linha.add_trace(go.Scatter(
    x=df_mensal["Mês"], y=df_mensal["Coleta Am"], mode='lines+markers', name='Coleta AM',
    line=dict(color='#9F00FF')))
fig_linha.add_trace(go.Scatter(
    x=df_mensal["Mês"], y=df_mensal["Coleta PM"], mode='lines+markers', name='Coleta PM',
    line=dict(color='#7B68EE')))
fig_linha.update_layout(
    title="Evolução da Coleta por Mês",
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(color='white'),
    legend=dict(font=dict(color='white'))
)
st.plotly_chart(fig_linha, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.markdown("""
    <style>
        body { background-color: #000000; color: white; }
        .metric-card {
            border: 2px solid #8a2be2;
            border-radius: 12px;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.05);
            margin-bottom: 1rem;
            text-align: center;
        }
        .metric-card h2 {
            color: white;
        }
        .radio-button-group label {
            background-color: transparent !important;
            border: 2px solid #8a2be2;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            margin-right: 10px;
            cursor: pointer;
        }
        .radio-button-group input:checked + label {
            background-color: #8a2be2 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Carregar dados
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# Limpar e padronizar nomes de colunas
df.columns = df.columns.str.strip().str.lower()

# Garantir que coluna mês está como string para filtro
df['mês'] = df['mês'].astype(str).str.upper()

# Filtros
meses = df['mês'].unique().tolist()
mes_selecionado = st.radio("Selecione o mês:", meses, horizontal=True, key="mes_radio")

# Filtrar dados
df_filtrado = df[df['mês'] == mes_selecionado]

# Calcular métricas
total_am = int(df_filtrado['coleta am'].sum())
total_pm = int(df_filtrado['coleta pm'].sum())
total_geral = int(df_filtrado['total de sacos'].sum())

# Layout com 3 colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <h2>Coleta AM</h2>
            <h1>{total_am} sacos</h1>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <h2>Coleta PM</h2>
            <h1>{total_pm} sacos</h1>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <h2>Total de Sacos</h2>
            <h1>{total_geral} sacos</h1>
        </div>
    """, unsafe_allow_html=True)

# Gráfico interativo (linhas)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_filtrado['mês'], y=df_filtrado['coleta am'], mode='lines+markers', name='Coleta AM'))
fig.add_trace(go.Scatter(x=df_filtrado['mês'], y=df_filtrado['coleta pm'], mode='lines+markers', name='Coleta PM'))
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    title="Comparativo de Coletas",
    xaxis_title="Mês",
    yaxis_title="Quantidade de Sacos",
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

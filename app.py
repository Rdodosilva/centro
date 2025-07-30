import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

# 🎨 Estilo customizado com CSS
st.set_page_config(layout="wide", page_title="Dashboard de Coleta AM/PM", page_icon="♻️")

st.markdown("""
    <style>
        body {
            background-color: black;
            color: white;
        }
        .title {
            color: white !important;
            font-size: 40px;
            font-weight: bold;
        }
        .uploadbox .stButton>button {
            background-color: #6C63FF;
            color: white;
        }
        .css-1cpxqw2 edgvbvh3 {background-color: #000000;}
        .stRadio > div {
            background-color: transparent;
            color: white;
            border: 1px solid #6C63FF;
            border-radius: 0.5rem;
            padding: 0.3rem;
        }
    </style>
""", unsafe_allow_html=True)

# 📌 Título
st.markdown("<h1 class='title'>♻️ Dashboard de Coleta - Turnos AM/PM</h1>", unsafe_allow_html=True)

# 📂 Upload
arquivo = st.file_uploader("📂 Faça o upload da planilha de coleta (.xlsx)", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    # 🧹 Verifica colunas corretas
    colunas_esperadas = ["Mês", "Coleta AM", "Coleta PM", "Total de Sacos"]
    if not all(col in df.columns for col in colunas_esperadas):
        st.error("❌ Colunas inválidas. Esperado: Mês, Coleta AM, Coleta PM, Total de Sacos")
    else:
        # 🔄 Filtros
        meses = sorted(df["Mês"].unique())
        mes_selecionado = st.radio("🗓️ Selecione o mês:", meses, horizontal=True)

        df_filtrado = df[df["Mês"] == mes_selecionado]

        # 📊 Cards
        total_am = df_filtrado["Coleta AM"].sum()
        total_pm = df_filtrado["Coleta PM"].sum()
        total_sacos = df_filtrado["Total de Sacos"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("🌅 Total AM", f"{total_am} sacos")
        col2.metric("🌇 Total PM", f"{total_pm} sacos")
        col3.metric("🧮 Total Geral", f"{total_sacos} sacos")

        # 📈 Gráfico de barras por turno
        fig_turnos = go.Figure()
        fig_turnos.add_trace(go.Bar(
            x=df_filtrado["Mês"],
            y=df_filtrado["Coleta AM"],
            name='Coleta AM',
            marker_color='#636EFA'
        ))
        fig_turnos.add_trace(go.Bar(
            x=df_filtrado["Mês"],
            y=df_filtrado["Coleta PM"],
            name='Coleta PM',
            marker_color='#EF553B'
        ))
        fig_turnos.update_layout(
            title=dict(text='Distribuição AM x PM', font=dict(color='white')),
            xaxis_title='Mês',
            yaxis_title='Quantidade',
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            barmode='group'
        )
        st.plotly_chart(fig_turnos, use_container_width=True)

        # 📈 Gráfico de linhas (tendência)
        df_grouped = df.groupby("Mês")[["Coleta AM", "Coleta PM", "Total de Sacos"]].sum().reset_index()

        fig_linhas = go.Figure()
        fig_linhas.add_trace(go.Scatter(
            x=df_grouped["Mês"],
            y=df_grouped["Coleta AM"],
            name='Coleta AM',
            mode='lines+markers',
            line=dict(color='#00CC96')
        ))
        fig_linhas.add_trace(go.Scatter(
            x=df_grouped["Mês"],
            y=df_grouped["Coleta PM"],
            name='Coleta PM',
            mode='lines+markers',
            line=dict(color='#AB63FA')
        ))
        fig_linhas.add_trace(go.Scatter(
            x=df_grouped["Mês"],
            y=df_grouped["Total de Sacos"],
            name='Total',
            mode='lines+markers',
            line=dict(color='white')
        ))
        fig_linhas.update_layout(
            title=dict(text='Tendência de Coleta por Mês', font=dict(color='white')),
            xaxis_title='Mês',
            yaxis_title='Quantidade de Sacos',
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white')
        )
        st.plotly_chart(fig_linhas, use_container_width=True)

else:
    st.warning("⚠️ Arquivo não carregado. Faça o upload acima.")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard de Coleta",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="♻️"
)

# Estilo personalizado
st.markdown(
    """
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .main > div {
            padding: 1rem;
        }
        .css-1v0mbdj, .css-12ttj6m {
            color: white !important;
        }
        .stApp {
            background-color: #000000;
        }
        .st-bc {
            background-color: #000000;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stRadio > label {
            color: white !important;
        }
        .stRadio div[role="radiogroup"] > label {
            background-color: transparent;
            border: 1px solid #6A0DAD;
            color: white !important;
            border-radius: 5px;
            padding: 6px 12px;
        }
        .stRadio div[role="radiogroup"] > label[data-selected="true"] {
            background-color: #6A0DAD;
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("### ♻️ Dashboard de Coleta - Turnos AM/PM")

uploaded_file = st.file_uploader("Faça o upload da planilha de coleta (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Verificar se as colunas estão corretas
        colunas_esperadas = ["Mês", "Coleta AM", "Coleta PM", "Total de Sacos"]
        if not all(col in df.columns for col in colunas_esperadas):
            st.error("A planilha deve conter as colunas: Mês, Coleta AM, Coleta PM e Total de Sacos.")
        else:
            # Filtros de mês
            meses = df["Mês"].unique()
            mes_selecionado = st.radio("Selecione o mês", meses, horizontal=True)

            df_filtrado = df[df["Mês"] == mes_selecionado]

            # Cartões de resumo
            total_am = df_filtrado["Coleta AM"].sum()
            total_pm = df_filtrado["Coleta PM"].sum()
            total_geral = df_filtrado["Total de Sacos"].sum()

            col1, col2, col3 = st.columns(3)
            col1.metric("Total AM", int(total_am))
            col2.metric("Total PM", int(total_pm))
            col3.metric("Total Geral", int(total_geral))

            # Gráfico de barras por turno
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
                title='Distribuição AM x PM',
                title_font_color='white',
                xaxis_title='Mês',
                yaxis_title='Quantidade',
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white'),
                barmode='group'
            )
            st.plotly_chart(fig_turnos, use_container_width=True)

            # Gráfico de linhas de tendência
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
                title='Tendência de Coleta por Mês',
                title_font_color='white',
                xaxis_title='Mês',
                yaxis_title='Quantidade de Sacos',
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white')
            )
            st.plotly_chart(fig_linhas, use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
else:
    st.info("Aguardando o upload de uma planilha válida para visualizar o dashboard.")

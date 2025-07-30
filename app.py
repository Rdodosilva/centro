import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurações da página
st.set_page_config(page_title="Dashboard de Coleta AM/PM", layout="wide")

# Estilo CSS customizado (dark mode com elementos futuristas)
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: #000000;
            color: white;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            color: white;
        }
        .subtitle {
            font-size: 20px;
            color: white;
        }
        .upload-box {
            border: 2px dashed #7f5af0;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            background-color: #111;
        }
        .stButton>button {
            color: white;
            background-color: #7f5af0;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
        }
        .stRadio > div {
            flex-direction: row;
            justify-content: center;
        }
        .stRadio div[role="radiogroup"] > label {
            border: 2px solid #7f5af0;
            border-radius: 8px;
            padding: 6px 14px;
            margin: 5px;
            background-color: transparent;
            color: white;
            cursor: pointer;
        }
        .stRadio div[role="radiogroup"] > label[data-selected="true"] {
            background-color: #7f5af0;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("♻️ <span class='title'>Dashboard de Coleta - Turnos AM/PM</span>", unsafe_allow_html=True)
st.markdown("<span class='subtitle'>📂 Faça o upload da planilha de coleta (.xlsx)</span>", unsafe_allow_html=True)

# Upload do arquivo
arquivo = st.file_uploader("Selecione o arquivo", type="xlsx")

if arquivo is not None:
    try:
        df = pd.read_excel(arquivo)

        # Verifica se todas as colunas necessárias estão presentes
        colunas_esperadas = ['Mês', 'Coleta AM', 'Coleta PM', 'Total de Sacos']
        if all(col in df.columns for col in colunas_esperadas):
            df['Mês'] = df['Mês'].astype(str)

            meses = sorted(df['Mês'].unique())
            mes_selecionado = st.radio("📅 Selecione o mês:", meses, horizontal=True)

            df_filtrado = df[df['Mês'] == mes_selecionado]

            # Cartões de totais
            total_am = df_filtrado['Coleta AM'].sum()
            total_pm = df_filtrado['Coleta PM'].sum()
            total_geral = df_filtrado['Total de Sacos'].sum()

            col1, col2, col3 = st.columns(3)
            col1.metric("🕗 Coleta AM", f"{total_am} sacos")
            col2.metric("🌙 Coleta PM", f"{total_pm} sacos")
            col3.metric("📦 Total Geral", f"{total_geral} sacos")

            # Gráfico de barras
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df_filtrado['Mês'], y=df_filtrado['Coleta AM'], name='Coleta AM', marker_color='#7f5af0'))
            fig.add_trace(go.Bar(x=df_filtrado['Mês'], y=df_filtrado['Coleta PM'], name='Coleta PM', marker_color='#2cb67d'))

            fig.update_layout(
                barmode='group',
                plot_bgcolor='#000',
                paper_bgcolor='#000',
                font=dict(color='white'),
                title='Comparativo de Turnos - AM vs PM',
                title_font=dict(size=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

            # Gráfico de linhas (tendência por mês)
            df_total_por_mes = df.groupby('Mês')[['Coleta AM', 'Coleta PM']].sum().reset_index()

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df_total_por_mes['Mês'], y=df_total_por_mes['Coleta AM'],
                                      mode='lines+markers', name='Coleta AM', line=dict(color='#7f5af0')))
            fig2.add_trace(go.Scatter(x=df_total_por_mes['Mês'], y=df_total_por_mes['Coleta PM'],
                                      mode='lines+markers', name='Coleta PM', line=dict(color='#2cb67d')))

            fig2.update_layout(
                title='Tendência de Coleta AM/PM por Mês',
                plot_bgcolor='#000',
                paper_bgcolor='#000',
                font=dict(color='white')
            )
            st.plotly_chart(fig2, use_container_width=True)

        else:
            st.error("⚠️ A planilha deve conter as colunas: Mês, Coleta AM, Coleta PM e Total de Sacos.")

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
else:
    st.info("⏳ Aguarde o upload de uma planilha válida para visualizar o dashboard.")


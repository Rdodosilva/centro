import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Estilo CSS personalizado
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .main {
            background-color: #000000;
        }
        div[data-testid="stMetricValue"] {
            color: white;
        }
        div[data-testid="stMetricLabel"] {
            color: #aaaaaa;
        }
        div[data-testid="stMarkdownContainer"] > p {
            color: white;
        }
        .css-1cpxqw2.edgvbvh3 {
            background-color: #1c1c1c;
        }
        .css-1v3fvcr {
            background-color: #000000;
        }
        section[data-testid="stSidebar"] {
            background-color: #111111;
        }
        .stRadio > div {
            flex-direction: row;
        }
        label.css-yz1r0j.e16fv1kl3 {
            color: white;
            border: 1px solid #8000ff;
            border-radius: 0.5rem;
            padding: 0.25rem 0.75rem;
            margin-right: 0.5rem;
        }
        label.css-yz1r0j.e16fv1kl3:hover {
            background-color: #8000ff20;
        }
        input:checked + div[data-testid="stMarkdownContainer"] > p {
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard de Coleta - Centro da Cidade")

uploaded_file = st.file_uploader("Faça upload da planilha .xlsx", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Lê a planilha
        df = pd.read_excel(uploaded_file, sheet_name=0)
        df.columns = df.columns.str.strip()

        # Identifica automaticamente a coluna "Mês"
        nome_coluna_mes = None
        for col in df.columns:
            if col.lower().strip() in ['mês', 'mes', 'mÊs', 'mÉs']:
                nome_coluna_mes = col
                break

        if nome_coluna_mes is None:
            st.error("❌ A coluna 'Mês' não foi encontrada.")
        else:
            # Filtro de mês
            meses_disponiveis = df[nome_coluna_mes].dropna().unique().tolist()
            mes_selecionado = st.radio("Selecione o mês:", meses_disponiveis)

            df_filtrado = df[df[nome_coluna_mes] == mes_selecionado]

            # Métricas
            coleta_am = int(df_filtrado["Coleta AM"].values[0])
            coleta_pm = int(df_filtrado["Coleta PM"].values[0])
            total = int(df_filtrado["Total de Sacos"].values[0])

            col1, col2, col3 = st.columns(3)
            col1.metric("🌅 Coleta AM", f"{coleta_am}")
            col2.metric("🌇 Coleta PM", f"{coleta_pm}")
            col3.metric("🧮 Total de Sacos", f"{total}")

            # Gráfico de barras
            fig = go.Figure(data=[
                go.Bar(name='Coleta AM', x=[mes_selecionado], y=[coleta_am], marker_color='mediumpurple'),
                go.Bar(name='Coleta PM', x=[mes_selecionado], y=[coleta_pm], marker_color='indigo')
            ])
            fig.update_layout(
                barmode='group',
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white'),
                title=f'Comparativo AM x PM - {mes_selecionado}'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Gráfico de linha com todos os meses
            df_plot = df[df["Total de Sacos"] > 0]
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df_plot[nome_coluna_mes],
                y=df_plot["Total de Sacos"],
                mode='lines+markers',
                name='Total de Sacos',
                line=dict(color='violet')
            ))
            fig2.update_layout(
                title='📈 Evolução da Coleta Total (Meses)',
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white')
            )
            st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {str(e)}")

import streamlit as st
import pandas as pd
import plotly.express as px

# Estilo CSS
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .css-1offfwp {
            color: white;
        }
        .stRadio > div {
            flex-direction: row;
        }
        .stRadio div[role='radiogroup'] label {
            border: 2px solid #8000ff;
            border-radius: 10px;
            padding: 5px 10px;
            margin: 5px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚛 Dashboard de Coleta - Centro")

# Upload do CSV
arquivo = st.file_uploader("Faça o upload da planilha de coleta (CSV):", type="csv")

if arquivo is not None:
    df = pd.read_csv(arquivo)

    # Converter a coluna Mês para categoria
    df["Mês"] = pd.Categorical(df["Mês"], categories=[
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
        "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ], ordered=True)

    # Filtro de mês
    meses_disponiveis = df["Mês"].dropna().unique()
    mes_selecionado = st.radio("Selecione o mês:", meses_disponiveis)

    df_filtrado = df[df["Mês"] == mes_selecionado]

    # Métricas
    coleta_am = df_filtrado["Coleta AM"].sum()
    coleta_pm = df_filtrado["Coleta PM"].sum()
    total_sacos = df_filtrado["Total de Sacos"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("🕗 Coleta AM", f"{coleta_am}")
    col2.metric("🕓 Coleta PM", f"{coleta_pm}")
    col3.metric("🟣 Total de Sacos", f"{total_sacos}")

    # Gráfico de linhas
    fig = px.line(df_filtrado, x=df_filtrado.index, y=["Coleta AM", "Coleta PM"],
                  labels={"value": "Quantidade de Sacos", "index": "Dia"},
                  title=f"Evolução das Coletas - {mes_selecionado}",
                  markers=True)
    fig.update_layout(template="plotly_dark", title_font_size=20)
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de barras
    fig2 = px.bar(df_filtrado, x="Mês", y="Total de Sacos", color="Mês",
                  title="Total de Sacos por Mês")
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("⚠️ Faça o upload do arquivo CSV para visualizar o dashboard.")

import streamlit as st
import pandas as pd
import plotly.express as px

# Estilo visual escuro e moderno
st.set_page_config(page_title="Dashboard de Coleta - Centro", layout="wide")

# CSS personalizado para tema escuro e filtros com borda roxa
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: white;
    }
    .css-18e3th9 {
        background-color: #000000;
        color: white;
    }
    .css-1v3fvcr {
        background-color: #000000;
        color: white;
    }
    .css-1kyxreq {
        color: white;
    }
    .stRadio > div {
        flex-direction: row;
    }
    .stRadio div[role='radiogroup'] > label {
        border: 1px solid #7B68EE;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        margin-right: 0.5rem;
        color: white;
        background-color: #1c1c1c;
    }
    .stRadio div[role='radiogroup'] > label[data-selected="true"] {
        background-color: #7B68EE;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("<h1 style='color:white;'>🚛 Dashboard de Coleta - Centro</h1>", unsafe_allow_html=True)

# Upload do arquivo
uploaded_file = st.file_uploader("Faça o upload da planilha de coleta (CSV):", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Corrigir nomes de colunas para evitar erros
    df.columns = df.columns.str.strip().str.lower()

    # Renomear colunas esperadas para padrão conhecido
    rename_map = {
        "mês": "mes",
        "coleta am": "coleta_am",
        "coleta pm": "coleta_pm",
        "total de sacos": "total"
    }
    df.rename(columns=rename_map, inplace=True)

    # Verificar se as colunas necessárias estão no DataFrame
    expected_cols = {"mes", "coleta_am", "coleta_pm", "total"}
    if not expected_cols.issubset(set(df.columns)):
        st.error("❌ As colunas esperadas não foram encontradas. Verifique se o arquivo tem: 'Mês', 'Coleta AM', 'Coleta PM', 'Total de Sacos'.")
    else:
        # Remover linhas com "total" no mês
        df = df[~df["mes"].astype(str).str.lower().str.contains("total", na=False)]

        # Filtro de mês com botões roxos
        meses_unicos = df["mes"].dropna().unique()
        mes_selecionado = st.radio("Selecione o mês:", meses_unicos, horizontal=True)

        df_mes = df[df["mes"] == mes_selecionado]

        # Métricas
        total_am = int(df_mes["coleta_am"].sum())
        total_pm = int(df_mes["coleta_pm"].sum())
        total_geral = int(df_mes["total"].sum())

        col1, col2, col3 = st.columns(3)
        col1.metric("🕘 Coleta AM", f"{total_am} sacos")
        col2.metric("🌙 Coleta PM", f"{total_pm} sacos")
        col3.metric("📦 Total no Mês", f"{total_geral} sacos")

        # Gráfico de barras
        fig_bar = px.bar(df_mes, x="mes", y=["coleta_am", "coleta_pm"], 
                         labels={"value": "Quantidade", "mes": "Mês", "variable": "Turno"},
                         barmode="group", title="Comparativo de Coletas por Turno",
                         color_discrete_sequence=["#8A2BE2", "#00CED1"])
        fig_bar.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')

        st.plotly_chart(fig_bar, use_container_width=True)

        # Gráfico de linhas
        fig_line = px.line(df_mes, x="mes", y="total", title="Total de Sacos Coletados por Mês", markers=True,
                           line_shape="linear", color_discrete_sequence=["#7B68EE"])
        fig_line.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')

        st.plotly_chart(fig_line, use_container_width=True)
else:
    st.warning("⚠️ Faça o upload do arquivo CSV para visualizar o dashboard.")

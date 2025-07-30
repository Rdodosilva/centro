import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações da página
st.set_page_config(layout="wide", page_title="Dashboard Coleta AM/PM", page_icon="🧹")

# Estilo CSS personalizado
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: white;
    }
    .stApp {
        background-color: #000000;
        color: white;
    }
    .css-1v3fvcr, .css-10trblm, .stMarkdown, .css-1d391kg {
        color: white !important;
    }
    .css-1r6slb0 {
        background-color: #000000;
    }
    .css-1aumxhk, .css-1dp5vir {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("## ♻️ Dashboard de Coleta - Turnos AM/PM")
st.markdown("### Faça o upload da planilha de coleta (.xlsx)")

# Upload da planilha
uploaded_file = st.file_uploader("Selecione o arquivo", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Validação de colunas obrigatórias
    colunas_obrigatorias = ['TURNO', 'MÊS', 'BAIRRO', 'TOTAL COLETADO (kg)', 'DIA']
    for col in colunas_obrigatorias:
        if col not in df.columns:
            st.error(f"Coluna obrigatória ausente: {col}")
            st.stop()

    # Filtros
    col1, col2 = st.columns(2)

    with col1:
        meses = sorted(df['MÊS'].dropna().unique())
        mes = st.radio("📅 Selecione o mês:", meses, horizontal=True)

    with col2:
        turnos = df['TURNO'].dropna().unique()
        turno = st.radio("🕓 Selecione o turno:", turnos, horizontal=True)

    # Filtro aplicado
    df_filtrado = df[(df['MÊS'] == mes) & (df['TURNO'] == turno)]

    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
        st.stop()

    # Cartões principais
    total_kg = df_filtrado["TOTAL COLETADO (kg)"].sum()
    media_kg_dia = df_filtrado.groupby("DIA")["TOTAL COLETADO (kg)"].sum().mean()

    c1, c2 = st.columns(2)
    c1.metric("🔢 Total Coletado (kg)", f"{total_kg:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    c2.metric("📊 Média por Dia (kg)", f"{media_kg_dia:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.markdown("---")

    # Gráfico de linha (total por dia)
    linha = px.line(
        df_filtrado,
        x="DIA",
        y="TOTAL COLETADO (kg)",
        title=f"Evolução Diária da Coleta - {turno}",
        markers=True,
        template="plotly_dark",
        color_discrete_sequence=["#A020F0"]
    )
    linha.update_layout(title_font_color='white', font_color='white')
    st.plotly_chart(linha, use_container_width=True)

    # Gráfico de barras (por bairro)
    barras = px.bar(
        df_filtrado.groupby("BAIRRO")["TOTAL COLETADO (kg)"].sum().reset_index().sort_values(by="TOTAL COLETADO (kg)", ascending=False),
        x="TOTAL COLETADO (kg)",
        y="BAIRRO",
        orientation="h",
        title="Total Coletado por Bairro",
        template="plotly_dark",
        color_discrete_sequence=["#8000FF"]
    )
    barras.update_layout(title_font_color='white', font_color='white', yaxis=dict(autorange="reversed"))
    st.plotly_chart(barras, use_container_width=True)

    # Gráfico de pizza (por bairro)
    pizza = px.pie(
        df_filtrado,
        values="TOTAL COLETADO (kg)",
        names="BAIRRO",
        title="Distribuição da Coleta por Bairro",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Purples
    )
    pizza.update_layout(title_font_color='white', font_color='white')
    st.plotly_chart(pizza, use_container_width=True)

else:
    st.info("📥 Aguarde o upload de uma planilha válida para visualizar o dashboard.")

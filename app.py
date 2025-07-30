import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Coleta", layout="wide")

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel("dados_coleta.xlsx")
        df['Mês'] = pd.Categorical(df['Mês'], categories=df['Mês'], ordered=True)
        return df
    except FileNotFoundError:
        st.error("⚠️ Arquivo 'dados_coleta.xlsx' não encontrado. Certifique-se de que ele está na mesma pasta do app.")
        return pd.DataFrame()

df = carregar_dados()

if not df.empty:
    st.markdown("<h1 style='color:white;'>📊 Dashboard de Coleta - Visual Futurista</h1>", unsafe_allow_html=True)

    # Filtros
    meses = st.multiselect("Filtrar por mês:", df['Mês'].unique(), default=df['Mês'].unique())

    df_filtrado = df[df['Mês'].isin(meses)]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<h3 style='color:white;'>🌅 Coleta AM</h3>", unsafe_allow_html=True)
        st.metric("Total AM", int(df_filtrado["Coleta AM"].sum()))

    with col2:
        st.markdown("<h3 style='color:white;'>🌇 Coleta PM</h3>", unsafe_allow_html=True)
        st.metric("Total PM", int(df_filtrado["Coleta PM"].sum()))

    with col3:
        st.markdown("<h3 style='color:white;'>🧺 Total de Sacos</h3>", unsafe_allow_html=True)
        st.metric("Total Geral", int(df_filtrado["Total de Sacos"].sum()))

    st.divider()

    col4, col5 = st.columns(2)

    # Gráfico de barras
    with col4:
        fig_bar = px.bar(
            df_filtrado,
            x="Mês",
            y=["Coleta AM", "Coleta PM"],
            title="Quantidade de sacos por turno",
            barmode="group",
            template="plotly_dark",
            color_discrete_sequence=["#7F00FF", "#00BFFF"]
        )
        fig_bar.update_layout(title_font_color="white")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico de pizza
    with col5:
        total_am = df_filtrado["Coleta AM"].sum()
        total_pm = df_filtrado["Coleta PM"].sum()
        fig_pizza = px.pie(
            names=["Coleta AM", "Coleta PM"],
            values=[total_am, total_pm],
            title="Proporção AM vs PM",
            template="plotly_dark",
            color_discrete_sequence=["#7F00FF", "#00BFFF"]
        )
        fig_pizza.update_layout(title_font_color="white")
        st.plotly_chart(fig_pizza, use_container_width=True)

    st.divider()

    # Gráfico de linha: Evolução total de sacos por mês
    st.markdown("<h3 style='color:white;'>📈 Evolução da quantidade de sacos por mês</h3>", unsafe_allow_html=True)

    fig_linha = px.line(
        df_filtrado,
        x="Mês",
        y="Total de Sacos",
        title="Evolução mensal",
        markers=True,
        template="plotly_dark",
        line_shape="spline",
        color_discrete_sequence=["#00FFAA"]
    )
    fig_linha.update_traces(marker=dict(size=10, symbol="diamond", line=dict(width=2)))
    fig_linha.update_layout(title_font_color="white")
    st.plotly_chart(fig_linha, use_container_width=True)

else:
    st.warning("Não foi possível carregar os dados.")

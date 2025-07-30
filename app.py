import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# URL do GitHub (RAW)
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# Formatação de datas
df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")
df = df.dropna(subset=["DATA"])
df["MÊS"] = df["DATA"].dt.strftime("%m/%Y")

# Filtros únicos
df_meses = df["MÊS"].unique()
df_meses.sort()

# Estilo
st.set_page_config(layout="wide", page_title="Dashboard Coleta Centro")

# CSS customizado para visual futurista dark
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .metric {
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
        .css-1v0mbdj p {
            color: white !important;
        }
        .css-10trblm, .css-1d391kg {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Filtros
st.markdown("## Coleta Centro - Painel Futurista")
mes_escolhido = st.radio("Selecione o mês:", df_meses, horizontal=True, key="mes",
                          label_visibility="collapsed")
df_filtrado = df[df["MÊS"] == mes_escolhido]

# Métricas
col1, col2, col3 = st.columns(3)

col1.metric("🚮 Total Sacos AM", int(df_filtrado["QTD_SACOS_AM"].sum()))
col2.metric("🌙 Total Sacos PM", int(df_filtrado["QTD_SACOS_PM"].sum()))
col3.metric("📦 Total Geral", int(df_filtrado["QTD_SACOS_AM"].sum() + df_filtrado["QTD_SACOS_PM"].sum()))

# Gráfico de barras AM vs PM
st.markdown("### Distribuição Geral AM vs PM", unsafe_allow_html=True)
fig1 = px.bar(
    df_filtrado.melt(id_vars=["DATA"], value_vars=["QTD_SACOS_AM", "QTD_SACOS_PM"],
                     var_name="Turno", value_name="Quantidade"),
    x="DATA", y="Quantidade", color="Turno",
    color_discrete_map={"QTD_SACOS_AM": "#8e44ad", "QTD_SACOS_PM": "#9b59b6"},
    template="plotly_dark"
)
fig1.update_layout(xaxis_title="Data", yaxis_title="Quantidade de Sacos",
                   legend_title="Turno",
                   font=dict(color="white"))
st.plotly_chart(fig1, use_container_width=True)

# Evolução por mês
st.markdown("### Evolução da Quantidade de Sacos por Mês")
df_grouped = df.groupby("MÊS").agg({"QTD_SACOS_AM": "sum", "QTD_SACOS_PM": "sum"}).reset_index()
df_grouped["TOTAL"] = df_grouped["QTD_SACOS_AM"] + df_grouped["QTD_SACOS_PM"]
fig2 = px.line(df_grouped, x="MÊS", y="TOTAL", markers=True,
               labels={"TOTAL": "Quantidade Total", "MÊS": "Mês"},
               template="plotly_dark")
fig2.update_traces(line=dict(color="#bb86fc"))
fig2.update_layout(font=dict(color="white"))
st.plotly_chart(fig2, use_container_width=True)

# Mensagem final
st.markdown("---")
st.markdown("Criado por **@Rdodosilva** | Visual Futurista - Streamlit + Plotly", unsafe_allow_html=True)

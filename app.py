import streamlit as st
import pandas as pd
import plotly.express as px

# ===== Estilo futurista com fundo preto e texto branco =====
st.set_page_config(layout="wide")
with open("style.css", "w") as f:
    f.write("""
        body {
            background-color: #000000;
            color: white;
        }
        .css-1d391kg {
            color: white;
        }
        .css-1cpxqw2, .stRadio > div {
            background-color: transparent;
            color: white;
        }
        .st-bw {
            border-color: #8A2BE2 !important;
        }
        .st-emotion-cache-1kyxreq:hover {
            border: 2px solid #8A2BE2 !important;
        }
    """)
st.markdown('<style>' + open("style.css").read() + '</style>', unsafe_allow_html=True)

# ===== Carregar os dados do GitHub =====
url = "https://github.com/Rdodosilva/centro/raw/refs/heads/main/Coleta%20centro2.xlsx"
df = pd.read_excel(url)

# ===== Ajustar colunas e tipos =====
df.columns = df.columns.str.strip()  # Remover espaços extras nos nomes
df["MÊS"] = df["MÊS"].astype(str).str.upper()
df["TURNO"] = df["TURNO"].astype(str).str.upper()

# ===== Filtros de MÊS com botões roxos =====
meses_disponiveis = sorted(df["MÊS"].unique())
mes_escolhido = st.radio("Selecione o mês:", meses_disponiveis, horizontal=True)

df_filtrado = df[df["MÊS"] == mes_escolhido]

# ===== Títulos =====
st.markdown(f"<h2 style='color:white;'>📊 Dashboard de Coleta - {mes_escolhido}</h2>", unsafe_allow_html=True)

# ===== Cards Totais =====
col1, col2 = st.columns(2)
with col1:
    total_am = int(df_filtrado[df_filtrado["TURNO"] == "AM"]["TOTAL"].sum())
    st.markdown(f"<h3 style='color:white;'>☀️ Total AM: {total_am}</h3>", unsafe_allow_html=True)
with col2:
    total_pm = int(df_filtrado[df_filtrado["TURNO"] == "PM"]["TOTAL"].sum())
    st.markdown(f"<h3 style='color:white;'>🌙 Total PM: {total_pm}</h3>", unsafe_allow_html=True)

# ===== Gráfico de barras: Total por Rota =====
fig_bar = px.bar(
    df_filtrado,
    x="ROTA",
    y="TOTAL",
    color="TURNO",
    title="Total por Rota",
    template="plotly_dark",
    color_discrete_sequence=["#8A2BE2", "#00CED1"]
)
st.plotly_chart(fig_bar, use_container_width=True)

# ===== Gráfico de pizza: Proporção AM vs PM =====
turno_totais = df_filtrado.groupby("TURNO")["TOTAL"].sum().reset_index()
fig_pizza = px.pie(
    turno_totais,
    names="TURNO",
    values="TOTAL",
    title="Proporção de Coleta por Turno",
    template="plotly_dark",
    color_discrete_sequence=["#8A2BE2", "#00CED1"]
)
st.plotly_chart(fig_pizza, use_container_width=True)

# ===== Gráfico de linhas: Evolução por Rota =====
fig_linha = px.line(
    df_filtrado.sort_values("ROTA"),
    x="ROTA",
    y="TOTAL",
    color="TURNO",
    title="Evolução da Coleta por Rota",
    markers=True,
    template="plotly_dark",
    color_discrete_sequence=["#8A2BE2", "#00CED1"]
)
st.plotly_chart(fig_linha, use_container_width=True)

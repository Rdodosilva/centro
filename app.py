import streamlit as st
import pandas as pd
import plotly.express as px

# --- Estilo Futurista com CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');
    html, body, .stApp {
        background-color: #000000;
        color: white;
        font-family: 'Orbitron', sans-serif;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 10px;
    }
    div[data-testid="stMetricDelta"] {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Função para carregar e limpar os dados ---
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Coleta centro2.xlsx")
    df.columns = df.columns.str.strip()
    df["Mes"] = df["Mês"].str.lower().str.strip()
    return df

# --- Carregando dados ---
df = carregar_dados()
meses_disponiveis = df["Mes"].unique()

# --- Sidebar com filtros ---
st.sidebar.markdown("### 🔎 Filtros")
mes_selecionado = st.sidebar.selectbox("Selecione o mês", sorted(meses_disponiveis))
turno_selecionado = st.sidebar.selectbox("Selecione o turno", ["Todos", "Coleta AM", "Coleta PM"])

# --- Filtragem de dados ---
df_filtrado = df[df["Mes"] == mes_selecionado]
if turno_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Periodo"] == turno_selecionado]

# --- Título principal ---
st.markdown(f"<h2 style='text-align:center;'>📊 Dashboard de Coleta – <u>{mes_selecionado.capitalize()}</u></h2>", unsafe_allow_html=True)
st.markdown("")

# --- Métricas ---
total_sacos = df_filtrado["Total"].sum()
total_am = df_filtrado[df_filtrado["Periodo"] == "Coleta AM"]["Total"].sum()
total_pm = df_filtrado[df_filtrado["Periodo"] == "Coleta PM"]["Total"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("🧺 Total de Sacos", f"{total_sacos}")
col2.metric("🌅 Turno AM", f"{total_am}")
col3.metric("🌇 Turno PM", f"{total_pm}")

# --- Gráfico de Barras ---
fig_bar = px.bar(df_filtrado, x="Data", y="Total", color="Periodo",
                 title="Coleta por Dia",
                 labels={"Total": "Total de Sacos", "Data": "Data"},
                 template="plotly_dark")
fig_bar.update_layout(transition_duration=500)
st.plotly_chart(fig_bar, use_container_width=True)

# --- Gráfico de Pizza ---
fig_pie = px.pie(df_filtrado, values="Total", names="Periodo", hole=0.5,
                 title="Distribuição por Turno", template="plotly_dark")
fig_pie.update_layout(transition_duration=500)
st.plotly_chart(fig_pie, use_container_width=True)

# --- Exibir dados detalhados ---
with st.expander("📋 Ver dados detalhados"):
    st.dataframe(df_filtrado.style.set_properties(**{
        'background-color': 'black',
        'color': 'white',
        'border-color': 'white'
    }))

# --- Rodapé ---
st.markdown("---")
st.markdown("<p style='text-align:center; font-size:12px;'>Desenvolvido com ❤️ por Rodrigo | Streamlit + Plotly</p>", unsafe_allow_html=True)

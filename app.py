import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Coleta Centro - Dashboard Executivo", 
    page_icon="🚛", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# CSS
# ===============================
st.markdown("""
<style>
/* Força fundo escuro */
html, body, .stApp {
    background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    color:white;
}

/* HEADER SOME (para evitar sobrepor título) */
header[data-testid="stHeader"] {
    display: none !important;
}

/* Seletor de meses = botões */
.stRadio > div > div > div > label {
    background:#1a1a2e !important;
    border:1px solid #00FFFF !important;
    border-radius:6px !important;
    color:white !important;
    text-align:center !important;
    cursor:pointer !important;
    height:30px !important;
    font-size:0.8em !important;
    padding:5px !important;
}

/* HOVER = azul */
.stRadio > div > div > div > label:hover {
    background:rgba(0,255,255,0.15) !important;
}

/* SELECIONADO = VERMELHO TRANSLÚCIDO */
.stRadio > div > div > div > label[aria-checked="true"] {
    background:rgba(255,0,0,0.35) !important;
    border:2px solid rgba(255,0,0,0.7) !important;
    transform:scale(1.05) !important;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# DADOS (EXCEL)
# ===============================
excel_file_path = "Coleta centro2.xlsx"
xls = pd.ExcelFile(excel_file_path)
sheet_names = xls.sheet_names

with st.sidebar:
    st.markdown("## 🎛️ Filtros")
    ano_selecionado = st.selectbox("Ano:", sheet_names, index=0)

df = pd.read_excel(excel_file_path, sheet_name=ano_selecionado)
df.columns = df.columns.str.strip()
df["Mes"] = df["Mês"].str.lower().str.strip()

# ===============================
# TÍTULO QUE AGORA APARECE!
# ===============================
st.markdown(f"""
<div style='text-align:center;padding:10px 0;'>
    <div style='font-size:3rem;font-weight:700;'>
        🚛 <span style='background: linear-gradient(90deg, #00FFFF, #9b30ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;'>Coleta Centro</span> 🚛
    </div>
    <div style='font-size:1.3rem;color:#00FFFF;opacity:0.8;'>
        📊 Monitoramento de Crescimento de Resíduos | {ano_selecionado}
    </div>
</div>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR SELETOR DE MÊS
# ===============================
meses = ["janeiro","fevereiro","março","abril","maio","junho","julho",
         "agosto","setembro","outubro","novembro","dezembro"]

with st.sidebar:
    st.markdown("### 📅 Mês:")
    mes_selecionado = st.radio("", meses, index=0)

# ===============================
# FILTRAR
# ===============================
df_filtrado = df[df["Mes"] == mes_selecionado]

if df_filtrado.empty:
    total_sacos = 0
    total_am = 0
    total_pm = 0
else:
    total_sacos = int(df_filtrado["Total de Sacos"].sum())
    total_am = int(df_filtrado["Coleta AM"].sum())
    total_pm = int(df_filtrado["Coleta PM"].sum())

peso_total = total_sacos * 20
eficiencia = (total_am/(total_am+total_pm)*100) if (total_am+total_pm)>0 else 0

# ===============================
# INDICADORES
# ===============================
st.markdown("## 📈 Indicadores")

c1,c2,c3,c4 = st.columns(4)

with c1: st.metric("Total Sacos", total_sacos)
with c2: st.metric("Peso Total", f"{peso_total} kg")
with c3: st.metric("Eficiência AM", f"{eficiencia:.1f}%")
with c4: st.metric("Status", "Normal" if total_sacos<2000 else "Monitorar")

# ===============================
# GRÁFICO BARRAS
# ===============================
st.markdown(f"### 🚀 Coleta em {mes_selecionado.title()}")

df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade"
)

fig = px.bar(
    df_melt,
    x="Periodo",
    y="Quantidade",
    color="Periodo",
    color_discrete_map={
        "Coleta AM":"#00D4FF",
        "Coleta PM":"#FF6B35"
    }
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# EVOLUÇÃO ANUAL
# ===============================
st.markdown("### 📈 Evolução do Ano")

df_linha = df.copy()
fig2 = px.line(
    df_linha,
    x="Mes",
    y="Total de Sacos"
)

fig2.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

st.plotly_chart(fig2, use_container_width=True)


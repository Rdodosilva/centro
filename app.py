import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


# 🎯 Configuração da página
st.set_page_config(
    page_title="Coleta Centro - Dashboard Executivo",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
#  🔰  CSS (COM AJUSTE DO BOTÃO E DO TÍTULO)
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, .stApp {
    background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    color: white;
    font-family: 'Inter', sans-serif;
}

/* HEADER — agora permite ver o TÍTULO */
header[data-testid="stHeader"] {
    height: 2.875rem;
    background: transparent;
    z-index: -1 !important;
}

/* BOTÃO SELECIONADO — VERMELHO */
section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"] {
    background: linear-gradient(135deg, rgba(255,0,0,0.35), rgba(255,0,0,0.25)) !important;
    color: white !important;
    border: 2px solid rgba(255,0,0,0.55) !important;
    transform: scale(1.05) !important;
    font-weight: 700 !important;
}

/* resto do CSS permanece */    
</style>
""", unsafe_allow_html=True)


# =====================================================
#  📥 LEITURA DOS DADOS
# =====================================================
excel_file_path = "Coleta centro2.xlsx"

try:
    xls = pd.ExcelFile(excel_file_path)
    sheet_names = xls.sheet_names
    sheet_names_sorted = sorted(sheet_names)

    with st.sidebar:
        st.markdown("## 🎛️ Filtros")
        ano_selecionado = st.selectbox("Ano:", sheet_names_sorted, index=0)

    df = pd.read_excel(excel_file_path, sheet_name=ano_selecionado)
    df.columns = df.columns.str.strip()
    df["Mes"] = df["Mês"].str.lower().str.strip()

except:
    st.error("Erro ao abrir o Excel.")
    st.stop()



# =====================================================
#  🏷️ CABEÇALHO
# =====================================================
st.markdown(f"""
<div style='text-align:center; padding:18px 0;'>
    <div style='font-size:3.3em; font-weight:700;'>
        🚛 <span style='background: linear-gradient(90deg,#00FFFF,#9b30ff);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
        Coleta Centro </span> 🚛
    </div>
    <div style='font-size:1.25em; color:#00FFFF;'>
        📊 Monitoramento de Crescimento de Resíduos | {ano_selecionado}
    </div>
</div>
""", unsafe_allow_html=True)



# =====================================================
#  🖥️ SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("### 📅 Mês:")

    meses_disponiveis = ["janeiro","fevereiro","março","abril","maio","junho",
                         "julho","agosto","setembro","outubro","novembro","dezembro"]
    meses_display = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                     "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

    mes_selecionado = st.radio(
        "",
        options=meses_disponiveis,
        format_func=lambda x: meses_display[meses_disponiveis.index(x)],
        index=0
    )

    st.markdown("### 📊 Visualização")
    mostrar_comparativo = st.checkbox("Comparar com mês anterior", True)

    st.markdown("### 📤 Exportar (mantém igual)")


# =====================================================
#  🔢 CÁLCULOS
# =====================================================
df_filtrado = df[df["Mes"] == mes_selecionado]

total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

idx = meses_disponiveis.index(mes_selecionado)
if idx > 0:
    df_ant = df[df["Mes"] == meses_disponiveis[idx-1]]
    total_ant = int(df_ant["Total de Sacos"].sum())
    variacao = ((total_sacos-total_ant)/total_ant*100) if total_ant>0 else 0
else:
    variacao = 0


# =====================================================
#  📈 MÉTRICAS
# =====================================================
st.markdown("## 📈 Indicadores")
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("🧺 Total Sacos", f"{total_sacos:,}".replace(".", ","), f"{variacao:+.1f}%" if mostrar_comparativo else None)

with col2:
    st.metric("⚖️ Peso Total", f"{peso_total:,} kg".replace(".", ","))

with col3:
    eficiencia = total_am/(total_am+total_pm)*100 if (total_am+total_pm)>0 else 0
    st.metric("📊 Eficiência AM", f"{eficiencia:.1f}%")

with col4:
    st.metric("⚙️ Status", "Normal" if total_sacos<2500 else "Monitorar")


# =====================================================
#  📊 GRÁFICO BARRAS (mantém idêntico)
# =====================================================
df_melt = df_filtrado.melt(id_vars="Mes",
                           value_vars=["Coleta AM","Coleta PM"],
                           var_name="Periodo",
                           value_name="Quantidade")

cores = {"Coleta AM":"#00D4FF", "Coleta PM":"#FF6B35"}

fig_bar = px.bar(df_melt, x="Mes", y="Quantidade", color="Periodo",
                 color_discrete_map=cores)

st.plotly_chart(fig_bar, use_container_width=True)


# =====================================================
#  📊 GRÁFICO EVOLUÇÃO (mantém igual)
# =====================================================
st.markdown("### 📈 Evolução Anual")

df_ev = df.copy()
df_ev["Mes"] = pd.Categorical(df_ev["Mes"], categories=meses_disponiveis, ordered=True)
df_ev = df_ev.sort_values("Mes")

fig_line = px.line(df_ev, x="Mes", y="Total de Sacos")
st.plotly_chart(fig_line, use_container_width=True)



# =====================================================
#  📋 TABELA
# =====================================================
with st.expander("📋 Ver Dados"):
    st.dataframe(df, use_container_width=True)



# =====================================================
#  ⚡ FOOTER
# =====================================================
st.markdown(f"""
<div style='text-align:center;padding:18px;'>
    <span style='font-size:1.1em;color:#00FFFF;'>Sistema de Apoio | {ano_selecionado}</span>
</div>
""", unsafe_allow_html=True)

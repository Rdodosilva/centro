import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard Coleta Futurista")

@st.cache_data
def carregar_dados():
    df = pd.read_excel("dados_coleta.xlsx", header=0)
    
    # Normaliza nomes das colunas
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    
    # Debug: Mostra colunas disponíveis
    st.write("Colunas carregadas:", df.columns.tolist())

    # Organiza ordem dos meses
    df['mês'] = pd.Categorical(df['mês'], categories=df['mês'], ordered=True)
    return df

df = carregar_dados()

# Estilo
st.markdown("<h1 style='color:white;'>📦 Quantidade de Sacos por Período</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Gráfico de barras AM e PM
with col1:
    fig1 = px.bar(df, x="mês", y=["coleta_am", "coleta_pm"], barmode="group",
                  labels={"value": "Total de Sacos", "mês": "Mês"},
                  color_discrete_sequence=["#7E57C2", "#26C6DA"])
    fig1.update_layout(title="Distribuição Geral AM vs PM", title_font_color="white",
                       plot_bgcolor='black', paper_bgcolor='black',
                       font=dict(color="white"))
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico de pizza
with col2:
    totais = df[["coleta_am", "coleta_pm"]].sum()
    fig2 = px.pie(names=totais.index, values=totais.values,
                  color_discrete_sequence=["#7E57C2", "#26C6DA"])
    fig2.update_layout(title="Proporção Total AM vs PM", title_font_color="white",
                       plot_bgcolor='black', paper_bgcolor='black',
                       font=dict(color="white"))
    st.plotly_chart(fig2, use_container_width=True)

# Linha da evolução total
st.markdown("<h1 style='color:white;'>📈 Evolução da Coleta por Mês</h1>", unsafe_allow_html=True)
fig3 = px.line(df, x="mês", y="total_de_sacos", markers=True,
               labels={"total_de_sacos": "Total de Sacos", "mês": "Mês"},
               color_discrete_sequence=["#FFD54F"])
fig3.update_layout(title="Evolução da Quantidade de Sacos", title_font_color="white",
                   plot_bgcolor='black', paper_bgcolor='black',
                   font=dict(color="white"))
st.plotly_chart(fig3, use_container_width=True)

# Atualização automática ao modificar a planilha
st.caption("📌 Este dashboard será atualizado automaticamente ao carregar novos dados na planilha.")

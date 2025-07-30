import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Coleta Centro", layout="wide")

# Estilo visual
st.markdown("""
    <style>
        body { background-color: #000000; color: white; }
        .stRadio > div { flex-direction: row; }
        .css-1cpxqw2.edgvbvh3 { background-color: #000000; }
        .stRadio div[role=radiogroup] > label {
            border: 1px solid #9400d3;
            border-radius: 6px;
            padding: 6px 12px;
            margin-right: 10px;
            color: white;
        }
        .stRadio div[role=radiogroup] > label[data-selected="true"] {
            background-color: #9400d3;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Carregar dados
df = pd.read_excel("Coleta centro2.xlsx")

# Converter colunas de datas
df['Data'] = pd.to_datetime(df['Data'])
df['Mês'] = df['Data'].dt.month_name().str.capitalize()

# Filtros
meses_disponiveis = df['Mês'].unique().tolist()
mes = st.radio("📅 Selecione o mês:", meses_disponiveis, horizontal=True)

# Filtrar dados
df_filtrado = df[df['Mês'] == mes]

# Indicadores principais
total_sacos = df_filtrado['Qtde de sacos'].sum()
peso_total = df_filtrado['Peso'].sum()
am_total = df_filtrado[df_filtrado['Turno'] == 'AM']['Qtde de sacos'].sum()
pm_total = df_filtrado[df_filtrado['Turno'] == 'PM']['Qtde de sacos'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📦 Total de Sacos", total_sacos)
with col2:
    st.metric("⚖️ Peso Total", f"{peso_total} kg")
with col3:
    st.metric("🌅 AM / 🌆 PM", f"{am_total} AM / {pm_total} PM")

# 📈 Gráfico de Evolução de Sacos por Mês (gráfico de linhas)
df_linha = df.groupby('Mês')['Qtde de sacos'].sum().reset_index()
df_linha['Mês'] = pd.Categorical(df_linha['Mês'],
    categories=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
    ordered=True)
df_linha = df_linha.sort_values('Mês')

fig_linha = px.line(df_linha, x='Mês', y='Qtde de sacos', markers=True,
    title="📈 Evolução da Quantidade de Sacos por Mês",
    line_shape="linear",
    template="plotly_dark")

fig_linha.update_traces(line=dict(color="#9400d3", width=3))
fig_linha.update_layout(title_font_size=20)

st.plotly_chart(fig_linha, use_container_width=True)

# (Coloque aqui seus gráficos de barras e pizza já existentes)

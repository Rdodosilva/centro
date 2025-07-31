import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# === URL da planilha hospedada no GitHub ===
url = "https://raw.githubusercontent.com/Rdodosilva/dash_coleta/main/dados/dados_coleta.csv"
df = pd.read_csv(url)

# === Tratamento dos dados ===
df['Mês'] = pd.Categorical(df['Mês'], categories=[
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho'
], ordered=True)
df = df.sort_values('Mês')

# === CSS Customizado para tema escuro e visual futurista ===
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .main {
            background-color: #000000;
        }
        h1, h2, h3, h4, h5, h6, p, .stText, .stMarkdown {
            color: white !important;
        }
        .stButton>button, .stRadio>div>label {
            background-color: transparent;
            color: white;
            border: 1px solid #9b59b6;
            border-radius: 10px;
            padding: 0.3em 1em;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #9b59b6;
            color: black;
        }
        .stRadio>div>label:hover {
            color: #9b59b6;
        }
    </style>
""", unsafe_allow_html=True)

# === Título ===
st.markdown("<h1 style='text-align: center; color: white;'>📊 Dashboard de Coleta - Centro da Cidade</h1>", unsafe_allow_html=True)

# === Filtros ===
meses = df['Mês'].unique()
mes_selecionado = st.radio("Selecione o mês:", options=meses, horizontal=True)

df_filtrado = df[df['Mês'] == mes_selecionado]

# === KPIs ===
total_sacos = int(df_filtrado['Total de Sacos'].sum())
total_am = int(df_filtrado['Coleta AM'].sum())
total_pm = int(df_filtrado['Coleta PM'].sum())

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📦 Total de Sacos", total_sacos)
with col2:
    st.metric("🌅 Coleta AM", total_am)
with col3:
    st.metric("🌇 Coleta PM", total_pm)

# === Gráfico de Barras (AM vs PM por mês) ===
df_barras = df[['Mês', 'Coleta AM', 'Coleta PM']].melt(id_vars='Mês', var_name='Turno', value_name='Quantidade')
fig_bar = px.bar(df_barras, x='Mês', y='Quantidade', color='Turno',
                 color_discrete_map={'Coleta AM': '#8e44ad', 'Coleta PM': '#00cfff'},
                 barmode='group', title='📊 Coleta AM vs PM por Mês')
fig_bar.update_layout(
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font_color='white',
    title_font_color='white',
    legend_font_color='white'
)
st.plotly_chart(fig_bar, use_container_width=True)

# === Gráfico de Pizza (Proporção AM/PM no mês selecionado) ===
df_pizza = pd.DataFrame({
    'Turno': ['Coleta AM', 'Coleta PM'],
    'Quantidade': [total_am, total_pm]
})
fig_pie = px.pie(df_pizza, names='Turno', values='Quantidade',
                 color='Turno',
                 color_discrete_map={'Coleta AM': '#8e44ad', 'Coleta PM': '#00cfff'},
                 title=f'🍕 Proporção de Coleta no mês de {mes_selecionado}')
fig_pie.update_layout(
    paper_bgcolor='#000000',
    font_color='white',
    title_font_color='white',
    legend_font_color='white'
)
st.plotly_chart(fig_pie, use_container_width=True)

# === Rodapé ===
st.markdown("<p style='text-align:center;color:gray;'>© 2025 - Dashboard criado por Rodrigo Silva</p>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# Estilo customizado para deixar tudo branco no fundo preto
st.markdown("""
    <style>
        body, .stApp {
            background-color: #000000;
            color: white;
        }
        .css-1cpxqw2, .stRadio label, .stRadio div {
            color: white !important;
        }
        .st-bx, .st-co, .st-dj, .st-dk {
            color: white !important;
        }
        h1, h2, h3, h4, h5, h6, p, span, div {
            color: white !important;
        }
        .css-q8sbsg {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Leitura da planilha do GitHub
url = "https://raw.githubusercontent.com/Rdodosilva/streamlit_coleta/main/base_coleta.xlsx"
df = pd.read_excel(url)

# Conversão de data
df['Data'] = pd.to_datetime(df['Data'])
df['Mês'] = df['Data'].dt.strftime('%b/%Y')

# Filtro por mês
meses = df['Mês'].unique().tolist()
mes_selecionado = st.radio("Selecione o mês", meses, horizontal=True)

df_filtrado = df[df['Mês'] == mes_selecionado]

# Título
st.title("Dashboard de Coleta (AM/PM)")

# Cartão de total de sacos
total_sacos = int(df_filtrado['Qtd_Sacos'].sum())
st.markdown(f"## Quantidade total de sacos: {total_sacos}", unsafe_allow_html=True)

# Gráfico de barras AM vs PM
sacos_turno = df_filtrado.groupby('Turno')['Qtd_Sacos'].sum().reset_index()
fig_bar = px.bar(
    sacos_turno,
    x='Turno',
    y='Qtd_Sacos',
    title='Distribuição Geral AM vs PM',
    color='Turno',
    color_discrete_map={'AM': 'mediumpurple', 'PM': 'orchid'}
)
fig_bar.update_layout(
    paper_bgcolor='black',
    plot_bgcolor='black',
    font_color='white',
    title_font_color='white',
    xaxis=dict(color='white'),
    yaxis=dict(color='white'),
    legend=dict(font=dict(color='white'))
)
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de linha - evolução por mês
sacos_mes = df.groupby('Mês')['Qtd_Sacos'].sum().reset_index()
fig_linha = px.line(
    sacos_mes,
    x='Mês',
    y='Qtd_Sacos',
    title='Evolução da quantidade de sacos por mês',
    markers=True
)
fig_linha.update_traces(line_color='violet', marker_color='white')
fig_linha.update_layout(
    paper_bgcolor='black',
    plot_bgcolor='black',
    font_color='white',
    title_font_color='white',
    xaxis=dict(color='white'),
    yaxis=dict(color='white'),
    legend=dict(font=dict(color='white'))
)
st.plotly_chart(fig_linha, use_container_width=True)

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# CSS total para fundo preto puro e texto branco puro, filtro totalmente preto com letras brancas
st.markdown("""
<style>
    /* Fundo geral preto sólido */
    html, body, .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    /* Textos e títulos brancos puros */
    h1, h2, h3, label, span, div, p {
        color: #FFFFFF !important;
    }
    /* Estilo do selectbox (filtro) */
    div.stSelectbox > div[role="combobox"] {
        background-color: #000000 !important;
        border: 2px solid #00FFFF !important; /* azul neon */
        border-radius: 8px !important;
        padding: 6px 12px !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    div.stSelectbox > div[role="combobox"] > div {
        color: #FFFFFF !important;
    }
    div[role="listbox"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    div[role="option"]:hover {
        background-color: #00FFFF !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }
    div[role="option"][aria-selected="true"] {
        background-color: #00FFFF !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }
    /* Métricas fundo escuro com borda azul neon */
    div[data-testid="metric-container"] {
        background-color: #111111 !important;
        border: 2px solid #00FFFF !important;
        border-radius: 12px !important;
        padding: 15px !important;
        color: #FFFFFF !important;
    }
    /* Ajusta cor de textos dentro das métricas */
    div[data-testid="metric-container"] > div > div {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")
df.columns = df.columns.str.strip()
df["Mes"] = df["Mês"].str.lower()

# Meses fixos para filtro
meses_filtro = ["janeiro", "fevereiro", "março", "abril", "maio"]

# Título principal
st.markdown("<h1 style='text-align:center; font-size: 3em;'>🚛 Coleta Centro</h1>", unsafe_allow_html=True)

# Filtro centralizado e estilizado
st.markdown("<h2 style='text-align:center;'>📅 Selecione o mês:</h2>", unsafe_allow_html=True)
mes_selecionado = st.selectbox(
    "",
    meses_filtro,
    index=0,
    format_func=lambda x: x.capitalize()
)

# Filtra dados do mês selecionado
df_filtrado = df[(df["Mes"] == mes_selecionado) & (df["Total de Sacos"].notna())]

# Métricas
total_sacos = int(df_filtrado["Total de Sacos"].sum())
peso_total = total_sacos * 20
total_am = int(df_filtrado["Coleta AM"].sum())
total_pm = int(df_filtrado["Coleta PM"].sum())

# Totais gerais para gráfico pizza
total_am_geral = int(df["Coleta AM"].sum())
total_pm_geral = int(df["Coleta PM"].sum())

# Métricas alinhadas
col1, col2, col3 = st.columns(3)
col1.metric("🧺 Total de Sacos", f"{total_sacos}")
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

# Preparar dados para gráfico de barras
df_melt = df_filtrado.melt(
    id_vars="Mes",
    value_vars=["Coleta AM", "Coleta PM"],
    var_name="Periodo",
    value_name="Quantidade de Sacos"
)

cores = {
    "Coleta AM": "#00FFFF",  # azul neon
    "Coleta PM": "#FFA500"   # laranja neon
}

# Gráfico de barras
fig_bar = px.bar(
    df_melt,
    x="Mes",
    y="Quantidade de Sacos",
    color="Periodo",
    color_discrete_map=cores,
    barmode="group",
    title="📦 Quantidade de Sacos por Período"
)
fig_bar.update_traces(
    hovertemplate='%{y} sacos - %{color}',
    marker_line_color='white',
    marker_line_width=1.5,
    opacity=0.9
)
fig_bar.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="#FFFFFF",
    title_font=dict(size=22),
    title_x=0.5,
    xaxis=dict(title="Mês", color="#FFFFFF", showgrid=False, tickfont=dict(color="#FFFFFF")),
    yaxis=dict(title="Quantidade de Sacos", color="#FFFFFF", showgrid=False, tickfont=dict(color="#FFFFFF")),
    legend=dict(
        title="Período",
        font=dict(color="#FFFFFF", size=14),
        bgcolor="#000000"
    ),
    bargap=0.2,
    bargroupgap=0.1
)

# Gráfico de pizza AM vs PM geral
fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am_geral, total_pm_geral],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title="🔄 Distribuição Geral AM vs PM"
)
fig_pie.update_traces(
    textfont=dict(color='#FFFFFF', size=14),
    textinfo='label+percent+value',
    pull=[0.05, 0],
    marker=dict(line=dict(color='#FFFFFF', width=2)),
    hoverinfo='label+percent+value'
)
fig_pie.update_layout(
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font_color="#FFFFFF",
    title_font=dict(size=22),
    title_x=0.5,
    legend=dict(
        font=dict(color="#FFFFFF", size=14),
        bgcolor="#000000"
    )
)

# Mostrar gráficos lado a lado
col4, col5 = st.columns(2)
col4.plotly_chart(fig_bar, use_container_width=True)
col5.plotly_chart(fig_pie, use_container_width=True)
import pandas as pd
import streamlit as st
import plotly.express as px

# Configurações de página
st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# CSS customizado para tema escuro e filtro com fundo roxo neon transparente e texto preto
st.markdown("""
<style>
/* Fundo geral preto e texto branco */
body, .block-container {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Métricas: texto branco */
[data-testid="metric-container"] {
    color: #FFFFFF !important;
}

/* Título centralizado e branco */
h1 {
    color: #FFFFFF !important;
    text-align: center;
    font-weight: 800;
}

/* Estilo filtro meses: fundo roxo neon transparente e texto preto */
div.stSelectbox > div[role="combobox"] {
    background-color: rgba(128, 0, 128, 0.7) !important; /* roxo neon transparente */
    color: black !important; /* texto do mês escrito em preto */
    border: 2px solid #8A2BE2 !important; /* borda roxa neon */
    border-radius: 8px !important;
    padding: 6px 12px !important;
    font-weight: 600 !important;
    width: 250px !important;
    margin: auto;
}

/* Texto dentro do filtro */
div.stSelectbox > div[role="combobox"] > div {
    color: black !important;
}

/* Fundo e texto na lista suspensa */
div[role="listbox"] {
    background-color: rgba(128, 0, 128, 0.7) !important; /* mesma cor roxa transparente */
    color: black !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}

/* Hover roxo neon com texto branco */
div[role="option"]:hover {
    background-color: #8A2BE2 !important; /* roxo neon sólido */
    color: white !important;
    font-weight: 700 !important;
}

/* Seleção roxo neon com texto branco */
div[role="option"][aria-selected="true"] {
    background-color: #8A2BE2 !important;
    color: white !important;
    font-weight: 700 !important;
}

/* Legendas do gráfico - texto branco */
.legendtext, .legendtitle {
    color: #FFFFFF !important;
}

/* Tooltip texto branco */
[role="tooltip"] {
    color: #FFFFFF !important;
    background-color: #222222 !important;
    border: 1px solid #8A2BE2 !important;
}

/* Scrollbar para o filtro */
div[role="listbox"]::-webkit-scrollbar {
    width: 8px;
}
div[role="listbox"]::-webkit-scrollbar-thumb {
    background-color: #8A2BE2;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# Carregar os dados
df = pd.read_excel("Coleta centro2.xlsx")

# Ajuste o nome da coluna de meses conforme seu arquivo
col_mes = "Mês"

# Remover linhas sem dados em "Total de Sacos"
df = df.dropna(subset=["Total de Sacos"])

# Título do app
st.markdown("<h1>Coleta Centro 🚛</h1>", unsafe_allow_html=True)

# Meses fixos e só os que tem dados no DF
meses_possiveis = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"]
meses_com_dados = [mes for mes in meses_possiveis if mes in df[col_mes].dropna().unique()]

# Filtro de meses centralizado e estilizado
mes_selecionado = st.selectbox(
    "Selecione o mês",
    options=meses_com_dados,
    index=0
)

# Filtrar dados pelo mês selecionado
df_mes = df[df[col_mes] == mes_selecionado]

# Cálculos métricas
total_sacos = int(df_mes["Total de Sacos"].sum())
peso_total = total_sacos * 20  # Cada saco 20kg
total_am = int(df_mes["Coleta AM"].sum())
total_pm = int(df_mes["Coleta PM"].sum())

# Exibir métricas em 3 colunas
col1, col2, col3 = st.columns(3)
col1.metric("🧺 Total de Sacos", f"{total_sacos}")
col2.metric("⚖️ Peso Total (kg)", f"{peso_total}")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} / {total_pm}")

# Preparar dados para gráfico de barras
df_melt = df_mes.melt(id_vars=col_mes, value_vars=["Coleta AM", "Coleta PM"],
                      var_name="Período", value_name="Quantidade de Sacos")

cores = {
    "Coleta AM": "#00BFFF",  # Azul neon
    "Coleta PM": "#FFA500",  # Laranja neon
}

# Gráfico de barras interativo
fig_bar = px.bar(
    df_melt,
    x=col_mes,
    y="Quantidade de Sacos",
    color="Período",
    barmode="group",
    color_discrete_map=cores,
    title=f"🪣 Coleta de Sacos - {mes_selecionado}"
)

fig_bar.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
    title_x=0.5,
    legend_title_font_color="white",
    legend_font_color="white",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de pizza AM vs PM no mês selecionado
fig_pie = px.pie(
    names=["Coleta AM", "Coleta PM"],
    values=[total_am, total_pm],
    color=["Coleta AM", "Coleta PM"],
    color_discrete_map=cores,
    title=f"🌅 vs 🌇 Distribuição - {mes_selecionado}",
    hole=0.4
)

fig_pie.update_traces(textinfo='percent+label', textfont_color='white')
fig_pie.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
    title_x=0.5,
    legend_title_font_color="white",
    legend_font_color="white",
)

st.plotly_chart(fig_pie, use_container_width=True)

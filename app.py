# 🔧 Pegando os meses que têm dados
meses_disponiveis = df["Mês"].dropna().unique().tolist()

# 🔥 Aplicando CSS no filtro (apenas visual)
st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        background-color: rgba(128, 0, 128, 0.4);
        border-radius: 10px;
    }
    div[data-baseweb="select"] span {
        color: black !important;
        font-weight: bold;
    }
    label, .stSelectbox label {
        color: white !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 🎯 Filtro centralizado
filtro_col1, filtro_col2, filtro_col3 = st.columns([1, 2, 1])
with filtro_col2:
    mes_selecionado = st.selectbox(
        "Selecione o mês",
        sorted(meses_disponiveis)
    )

# 🔍 Filtrar o DataFrame
df_filtrado = df[df["Mês"] == mes_selecionado]

st.markdown("""
<style>
/* Fundo roxo neon transparente no filtro */
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
</style>
""", unsafe_allow_html=True)

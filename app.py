import streamlit as st
import os
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Mapa das Lojas",
    page_icon="🏪",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    
    .mapa-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin: 20px 0;
    }
    
    .foto-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin-top: 20px;
        background: white;
        padding: 20px;
    }
    
    .store-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        text-align: center;
    }
    
    .store-name-big {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    
    .instructions {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Mapeamento: Nome no mapa -> Nome do arquivo
mapeamento_imagens = {
    # Rua Trajano - Esquerda
    "Magazine Luiza": "Magazine Luiza.jpeg",
    "Cia. do Homem": "Cia do Homem.jpeg",
    "Damiller": "Damyller.jpeg",
    "Pop Dente": "Pop dente - Lupo.jpeg",
    "Lupo": "Pop dente - Lupo.jpeg",
    "ViVo": "Lojas Vivo.jpeg",
    "Bazar das chaves": "Bazar das chave - Panvel.jpeg",
    "Panvel": "Bazar das chave - Panvel.jpeg",
    
    # Rua Trajano - Direita Superior
    "Nfuzzi": "Nluzzi.jpeg",
    "Para Alugar IBAGY": "Aluga Ibagy.jpeg",
    "Botton Utilidades": "Botton Utilidades.jpeg",
    "bob's": "Bob's.jpeg",
    "Artigos Religiosos": "Itens Religiosos.jpeg",
    "Caixa": "images/caixa.jpeg",
    "Achadinhos": "Achadinhos.jpeg",
    "U Mi Acessórios": "U mi Acessorios.jpeg",
    "Vonny cosmeticos": "Vonny cosmeticos.jpeg",
    
    # Rua Trajano - Direita Inferior
    "Museu": "images/museu.jpeg",
    "Café do Frank": "Café do Frank.jpeg",
    "Massa Viva": "Massa Viva.jpeg",
    "Floripa Implante": "Foripa Implantes.jpeg",
    "Preço Popular": "Preço popular.jpeg",
    "Brasil Cacau": "Brasil cacau.jpeg",
    "Cia. do Homem": "Cia do Homem 1.jpeg",
    "Da Praça": "Da Praça.jpeg",
    
    # Rua Felipe Schmidt - Esquerda
    "Mil Bijus": "Mil Bijus.jpeg",
    "Colombo": "Colombo.jpeg",
    "top1 Company": "Top 1 Company.jpeg",
    "Tim": "Tim.jpeg",
    "Corner bem": "Restauante Comer bem.jpeg",
    "Storil": "Estoril.jpeg",
    "Mercadão": "Mercadão dos Ocúlos.jpeg",
    "Restaurante Magnolia": "Restaurante Magnolia.jpeg",
    "Carioca calçados": "carioca calçados.jpeg",
    "Kotzias": "Kotzias.jpeg",
    "Floripa Store": "Floripa store.jpeg",
    "JS Store": "JS Store.jpeg",
    "Fuccs": "Fucci's.jpeg",
    "Vila Sucos": "Vita sucos.jpeg",
    "Carioca cosmeticos": "Carioca cosmeticos.jpeg",
    "Irmãos": "Irmãos.jpeg",
    "Fasbindrt": "Fasbinder.jpeg",
    "Top1 Calçados": "Top 1 calçados.jpeg",
    "Sabor do Tempero": "Restaurante sabor de tempero.jpeg",
    "Procon": "Procon.jpeg",
    
    # Rua Felipe Schmidt - Direita
    "Loja de Acessórios": "Loja de acessorios.jpeg",
    "Ótica Catarinense": "Otica catarinense.jpeg",
    "BMG": "Banco BMG.jpeg",
    "Trid": "Trid.jpeg",
    "Claro": "Claro.jpeg",
    "Preço Unico": "Preço Unico 80,00.jpeg",
    "Amo Biju": "Amo bijuterias.jpeg",
    "AgiBank": "Agibank.jpeg",
    "Cheirln Bão": "Cheirin bão.jpeg",
    "Oboticário": "Oboticario.jpeg",
    "Crefisa": "Crefisa.jpeg",
    "Ótica Rosangela": "Ótica Rosangela.jpeg",
    "MC Donalds": "MC Donald.jpeg",
    "Para Alugar": "Para Alugar.jpeg",
    "Outlet Brás": "Outlet Brás.jpeg",
    "Suiê": "Suiê.jpeg",
    "Tim revenda de chip": "Tim revenda de chip.jpeg",
    "Tudo Dez": "Tudo dez.jpeg"
}

# Lista única de lojas
todas_lojas = sorted(mapeamento_imagens.keys())

# Inicializar session state
if 'loja_selecionada' not in st.session_state:
    st.session_state.loja_selecionada = None

# Header
st.title("🗺️ Mapa das Lojas")

# Layout principal
col_mapa, col_foto = st.columns([1.2, 1])

with col_mapa:

    # Exibir o mapa
    if os.path.exists("mapa.jpg"):
        st.markdown('<div class="mapa-container">', unsafe_allow_html=True)
        st.image("mapa.jpg", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ Arquivo 'mapa.jpg' não encontrado na raiz do projeto")
    
    st.markdown(
        '<div class="instructions">💡 <b>Dica:</b> Selecione uma loja ao lado para ver sua fachada.</div>',
        unsafe_allow_html=True
    )

with col_foto:
    st.markdown("### 🏪 Selecione uma Loja")
    
    loja_selecionada = st.selectbox(
        "Escolha a loja:",
        ["Selecione uma loja..."] + todas_lojas,
        key="loja_selector"
    )
    
    if loja_selecionada and loja_selecionada != "Selecione uma loja...":
        st.session_state.loja_selecionada = loja_selecionada
        
        st.markdown(
            f'<div class="store-info"><div class="store-name-big">📍 {loja_selecionada}</div></div>',
            unsafe_allow_html=True
        )
        
        nome_arquivo = mapeamento_imagens.get(loja_selecionada)
        
        if nome_arquivo:
            caminhos_possiveis = [
                nome_arquivo,
                f"images/{nome_arquivo}",
                nome_arquivo.replace("images/", "")
            ]
            
            imagem_encontrada = False
            for caminho in caminhos_possiveis:
                if os.path.exists(caminho):
                    st.markdown('<div class="foto-container">', unsafe_allow_html=True)
                    st.image(caminho, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    imagem_encontrada = True
                    break
            
            if not imagem_encontrada:
                st.warning(f"⚠️ Foto não encontrada: `{nome_arquivo}`")
                st.info("Verifique se a imagem está na raiz ou em `images/`")
        else:
            st.error("❌ Loja não mapeada.")
    else:
        st.info("👈 Veja o mapa ao lado e selecione uma loja acima.")
        
        st.markdown("---")
        st.markdown("**📊 Estatísticas do Mapa:**")
        st.metric("Total de Lojas", len(todas_lojas))
        st.metric("Imagens Mapeadas", len([x for x in mapeamento_imagens.values()]))

# Footer
st.markdown("---")
st.caption("🏢 Mapa das lojas do centro | Desenvolvido para apresentação executiva")

# Botão reset
if st.session_state.loja_selecionada:
    if st.button("🔄 Resetar Seleção", use_container_width=True):
        st.session_state.loja_selecionada = None
        st.rerun()

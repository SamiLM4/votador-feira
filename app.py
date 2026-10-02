import streamlit as st
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import time

st.set_page_config(
    page_title="🗳️ Votador Feira",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# CSS customizado
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
    }

    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
    }

    .stSelectbox, .stSlider {
        margin: 1rem 0;
    }

    .titulo-principal {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    .card-projeto {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .card-projeto:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .estrelas-container {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin: 2rem 0;
    }

    .estrela-btn {
        font-size: 3rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .resumo-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    .info-item {
        margin: 0.5rem 0;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

URL_BASE = "https://cti.colegios.fve.edu.br/feira/index.html"

# Emojis das estrelas
ESTRELAS = {
    1: "⭐",
    2: "⭐⭐",
    3: "⭐⭐⭐",
    4: "⭐⭐⭐⭐",
    5: "⭐⭐⭐⭐⭐"
}

@st.cache_resource
def extrair_projetos():
    """Extrai títulos e links dos projetos usando Playwright."""
    with sync_playwright() as p:
        context = p.firefox.launch_persistent_context(
            user_data_dir=None,
            headless=True
        )
        page = context.new_page()

        try:
            page.goto(URL_BASE, wait_until="networkidle")
            page.wait_for_selector("section#grade article.card-projeto", timeout=15000)
            time.sleep(2)

            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            grade = soup.find('section', id='grade')

            if not grade:
                return []

            cards = grade.find_all('article', class_='card-projeto')

            projetos = []
            for idx, card in enumerate(cards):
                try:
                    titulo_elem = card.find('strong')
                    if not titulo_elem:
                        continue
                    titulo = titulo_elem.text.strip()

                    link_elem = card.find('a', class_='botao')
                    if not link_elem:
                        continue
                    link = link_elem.get('href', '')

                    match = re.search(r'id=([a-zA-Z0-9]+)', link)
                    if match:
                        projeto_id = match.group(1)
                        projetos.append({
                            "id": idx,
                            "titulo": titulo,
                            "link": link,
                            "projeto_id": projeto_id
                        })
                except:
                    continue

            return projetos

        finally:
            page.close()
            context.close()

def votar_projeto(projeto_id, numero_votos, estrelas, progress_bar, status_text):
    """Realiza votação com número de estrelas específico."""

    votos_sucesso = 0

    for voto_num in range(1, numero_votos + 1):
        with sync_playwright() as p:
            context = p.firefox.launch_persistent_context(
                user_data_dir=None,
                headless=True
            )
            page = context.new_page()

            try:
                url_projeto = f"https://cti.colegios.fve.edu.br/feira/projeto.html?id={projeto_id}"
                page.goto(url_projeto, wait_until="networkidle")

                # Seleciona a estrela específica
                page.wait_for_selector("span:has-text('5')", timeout=10000)
                page.click(f"span:has-text('{estrelas} ')")

                time.sleep(0.5)
                page.click("button[type='submit']")

                votos_sucesso += 1

            except Exception as e:
                pass

            finally:
                page.close()
                context.close()

        # Atualiza progresso
        progress = voto_num / numero_votos
        progress_bar.progress(progress)
        status_text.info(f"⏳ Progresso: {voto_num}/{numero_votos} votos | ⭐ {estrelas} estrelas")

        if voto_num < numero_votos:
            time.sleep(2)

    return votos_sucesso

# Interface Principal
st.markdown("""
    <div class="titulo-principal">
        <h1>🗳️ Votador - Feira de Ciência e Tecnologia</h1>
        <p>Vote nos melhores projetos da Univap Centro 2026</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🔍 Selecione um Projeto")

with col2:
    if st.button("🔄 Recarregar", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()

# Carrega projetos
with st.spinner("⏳ Carregando projetos..."):
    projetos = extrair_projetos()

if not projetos:
    st.error("❌ Nenhum projeto encontrado!")
    st.stop()

st.success(f"✅ {len(projetos)} projetos disponíveis")

# Cria lista de opções
opcoes = [f"{p['titulo'][:75]}" for p in projetos]

# Selectbox para escolher projeto
projeto_selecionado_idx = st.selectbox(
    "Escolha um projeto para votar:",
    range(len(projetos)),
    format_func=lambda i: f"[{i+1}] {opcoes[i]}"
)

projeto = projetos[projeto_selecionado_idx]

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Quantas Estrelas?")

    # Seleção de estrelas com botões
    st.write("Clique para selecionar:")

    cols = st.columns(5)
    estrelas_selecionadas = 5  # padrão

    for i in range(5):
        with cols[i]:
            if st.button(ESTRELAS[i+1], key=f"star_{i+1}", use_container_width=True):
                estrelas_selecionadas = i + 1

    # Exibe seleção atual
    st.markdown(f"""
        <div style='text-align: center; margin-top: 1rem; font-size: 2rem;'>
        {ESTRELAS[estrelas_selecionadas]}
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("🔢 Quantos Votos?")

    num_votos = st.slider(
        "Número de vezes que deseja votar:",
        min_value=1,
        max_value=500,
        value=10,
        step=1,
        label_visibility="collapsed"
    )

st.markdown("---")

st.markdown(f"""
    <div class="resumo-box">
        <h3>📋 Resumo da Votação</h3>
        <div class="info-item">📌 <strong>Projeto:</strong> {projeto['titulo'][:80]}</div>
        <div class="info-item">🆔 <strong>ID:</strong> {projeto['projeto_id']}</div>
        <div class="info-item">⭐ <strong>Estrelas:</strong> {ESTRELAS[estrelas_selecionadas]}</div>
        <div class="info-item">🔢 <strong>Total de Votos:</strong> {num_votos}x</div>
    </div>
""", unsafe_allow_html=True)

# Botão para votar
if st.button("🚀 INICIAR VOTAÇÃO", use_container_width=True, type="primary"):
    st.warning("⚠️ Não feche esta aba! O processo está em andamento...")

    progress_bar = st.progress(0)
    status_text = st.empty()

    votos_sucesso = votar_projeto(projeto['projeto_id'], num_votos, estrelas_selecionadas, progress_bar, status_text)

    st.markdown("---")

    if votos_sucesso == num_votos:
        st.balloons()
        st.success(f"""
            ✅ **VOTAÇÃO CONCLUÍDA COM SUCESSO!**

            📊 {votos_sucesso}/{num_votos} votos realizados

            ⭐ {ESTRELAS[estrelas_selecionadas]} para "{projeto['titulo'][:60]}"
        """)
    else:
        st.warning(f"""
            ⚠️ Votação parcialmente concluída

            📊 {votos_sucesso}/{num_votos} votos realizados
        """)

st.markdown("---")

st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>💡 Made with ❤️ for Univap Centro</p>
        <p>🔐 Cada voto usa uma sessão privada diferente</p>
    </div>
""", unsafe_allow_html=True)

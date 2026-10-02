import streamlit as st
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import time

st.set_page_config(page_title="🗳️ Votador Feira", layout="wide")

URL_BASE = "https://cti.colegios.fve.edu.br/feira/index.html"

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

def votar_projeto(projeto_id, numero_votos, progress_bar, status_text):
    """Realiza votação abrindo nova sessão privada para cada voto."""

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

                page.wait_for_selector("span:has-text('5')", timeout=10000)
                page.click("span:has-text('5')")

                time.sleep(0.5)
                page.click("button[type='submit']")

                votos_sucesso += 1

            except Exception as e:
                status_text.warning(f"Erro no voto {voto_num}: {str(e)}")

            finally:
                page.close()
                context.close()

        # Atualiza progresso
        progress = voto_num / numero_votos
        progress_bar.progress(progress)
        status_text.info(f"Progresso: {voto_num}/{numero_votos} votos")

        if voto_num < numero_votos:
            time.sleep(2)

    return votos_sucesso

# Interface
st.title("🗳️ Sistema de Votação - Feira de Ciência e Tecnologia")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Selecione um projeto")

with col2:
    if st.button("🔄 Recarregar Projetos", key="reload"):
        st.cache_resource.clear()
        st.rerun()

# Carrega projetos
with st.spinner("⏳ Carregando projetos..."):
    projetos = extrair_projetos()

if not projetos:
    st.error("❌ Nenhum projeto encontrado!")
    st.stop()

st.success(f"✅ {len(projetos)} projetos disponíveis")

# Cria lista de opções para o selectbox
opcoes = [f"{p['titulo'][:80]}" for p in projetos]

# Selectbox para escolher projeto
projeto_selecionado_idx = st.selectbox(
    "Escolha um projeto:",
    range(len(projetos)),
    format_func=lambda i: opcoes[i]
)

projeto = projetos[projeto_selecionado_idx]

st.markdown("---")
st.subheader("Configurar votação")

# Slider para número de votos
num_votos = st.slider(
    "Quantas vezes deseja votar?",
    min_value=1,
    max_value=500,
    value=10,
    step=1
)

st.markdown("---")
st.subheader("Resumo")

col1, col2 = st.columns(2)
with col1:
    st.write("**Projeto selecionado:**")
    st.write(projeto['titulo'])
with col2:
    st.write("**ID do projeto:**")
    st.write(projeto['projeto_id'])

st.write("**Quantidade de votos:**")
st.write(f"{num_votos}x")

st.markdown("---")

# Botão para votar
if st.button("🚀 INICIAR VOTAÇÃO", type="primary", use_container_width=True):
    st.warning("⚠️ Não feche esta aba! O processo está em andamento...")

    progress_bar = st.progress(0)
    status_text = st.empty()

    votos_sucesso = votar_projeto(projeto['projeto_id'], num_votos, progress_bar, status_text)

    st.balloons()
    st.success(f"✅ VOTAÇÃO CONCLUÍDA!\n\n{votos_sucesso}/{num_votos} votos realizados com sucesso!")

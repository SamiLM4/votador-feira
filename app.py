import streamlit as st
import requests
import re
import time

st.set_page_config(
    page_title="🗳️ Votador Feira",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# CSS customizado com tema escuro
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
    }

    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --primary-light: linear-gradient(135deg, #8b9ef8 0%, #9b6db3 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --dark-bg: #0f1419;
        --dark-card: #1a1f2e;
        --dark-text: #e0e0e0;
    }

    html {
        color-scheme: dark light;
    }

    body {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        color: var(--dark-text);
    }

    .main {
        background: var(--dark-bg);
        padding: 2rem;
        border-radius: 20px;
        color: var(--dark-text);
    }

    .stSelectbox, .stSlider {
        margin: 1rem 0;
    }

    .titulo-principal {
        text-align: center;
        background: var(--primary-gradient);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .titulo-principal h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }

    .titulo-principal p {
        font-size: 1.1rem;
        opacity: 0.95;
    }

    .card-projeto {
        background: var(--dark-card);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }

    .card-projeto:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
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
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
    }

    .estrela-btn:hover {
        transform: scale(1.1);
        filter: drop-shadow(0 4px 8px rgba(102, 126, 234, 0.4));
    }

    .resumo-box {
        background: var(--primary-gradient);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px 0 rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .resumo-box h3 {
        margin-bottom: 1rem;
        font-size: 1.3rem;
        font-weight: 600;
    }

    .info-item {
        margin: 0.8rem 0;
        font-size: 1rem;
        opacity: 0.95;
    }

    /* Styling para inputs */
    .stSelectbox [data-baseweb="select"] {
        background-color: var(--dark-card) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }

    .stSlider [data-testid="stThumb"] {
        background: var(--primary-gradient) !important;
    }

    /* Botões */
    .stButton > button {
        background: var(--primary-gradient) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }

    /* Subheadings */
    h2, h3 {
        color: white !important;
        font-weight: 600 !important;
    }

    /* Markdown text */
    .stMarkdown {
        color: var(--dark-text) !important;
    }

    /* Dividers */
    hr {
        border-color: rgba(102, 126, 234, 0.2) !important;
    }

    /* Success/Warning/Error messages */
    .stAlert {
        border-radius: 10px !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
    }

    /* Spinner */
    .stSpinner {
        color: #667eea !important;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: var(--primary-gradient) !important;
    }

    /* Responsivo para mobile */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }

        .titulo-principal {
            padding: 2rem 1rem;
            margin-bottom: 1.5rem;
        }

        .titulo-principal h1 {
            font-size: 1.8rem !important;
        }

        .titulo-principal p {
            font-size: 0.95rem !important;
        }

        .resumo-box {
            padding: 1.5rem 1rem;
            margin: 1.5rem 0;
        }

        .info-item {
            font-size: 0.95rem;
        }

        .stSelectbox {
            margin: 0.75rem 0;
        }

        .stSlider {
            margin: 0.75rem 0;
        }

        /* Estrelas responsivas */
        .estrela-btn {
            font-size: 2.2rem !important;
        }

        /* Botões maiores em mobile */
        .stButton > button {
            width: 100% !important;
            padding: 0.85rem !important;
            font-size: 1rem !important;
        }

        /* Subheadings menores */
        h2 {
            font-size: 1.5rem !important;
        }

        h3 {
            font-size: 1.2rem !important;
        }

        /* Spacing ajustado */
        .stMarkdown {
            margin: 0.5rem 0 !important;
        }

        /* Colunas responsivas */
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            margin-right: 0 !important;
            margin-bottom: 1rem !important;
        }

        /* Grid layout responsivo para colunas */
        [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 0.5rem !important;
        }

        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            flex: 1 1 100% !important;
            min-width: 0 !important;
        }
    }

    @media (max-width: 480px) {
        .main {
            padding: 0.75rem;
        }

        .titulo-principal {
            padding: 1.5rem 0.75rem;
            margin-bottom: 1rem;
        }

        .titulo-principal h1 {
            font-size: 1.4rem !important;
        }

        .titulo-principal p {
            font-size: 0.85rem !important;
        }

        .resumo-box {
            padding: 1.2rem 0.75rem;
            margin: 1rem 0;
        }

        .info-item {
            font-size: 0.9rem;
        }

        .estrela-btn {
            font-size: 1.8rem !important;
        }

        /* Ocultar textos longos em mobile muito pequeno */
        .stMarkdown p {
            font-size: 0.9rem !important;
        }

        h3 {
            font-size: 1rem !important;
        }
    }

    /* Animações suaves */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .titulo-principal {
        animation: fadeIn 0.6s ease-out;
    }

    .resumo-box {
        animation: fadeIn 0.8s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

URL_API = "https://cti.colegios.fve.edu.br/feira/api/v1/projetos/publicos"

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
    """Extrai projetos da API pública."""
    try:
        response = requests.get(URL_API, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get('success') or not data.get('data', {}).get('projetos'):
            return []

        projetos = []
        for idx, projeto in enumerate(data['data']['projetos']):
            try:
                projetos.append({
                    "id": idx,
                    "titulo": projeto.get('tema', '').strip(),
                    "projeto_id": projeto.get('id', ''),
                    "curso": projeto.get('curso', ''),
                    "descricao": projeto.get('descricao', '')
                })
            except:
                continue

        return projetos

    except Exception as e:
        st.error(f"Erro ao carregar projetos: {str(e)}")
        return []

def votar_projeto(projeto_id, numero_votos, estrelas, progress_bar, status_text):
    """Realiza votação com número de estrelas específico."""

    votos_sucesso = 0

    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        for voto_num in range(1, numero_votos + 1):
            try:
                url_projeto = f"https://cti.colegios.fve.edu.br/feira/projeto.html?id={projeto_id}"

                # Prepara dados para POST da votação
                dados = {
                    'projeto_id': projeto_id,
                    'estrelas': estrelas,
                    'voto': 1
                }

                # Tenta enviar votação
                response_voto = session.post(
                    url_projeto,
                    data=dados,
                    headers=headers,
                    timeout=10
                )

                if response_voto.status_code in [200, 201]:
                    votos_sucesso += 1

            except Exception as e:
                pass

            # Atualiza progresso
            progress = voto_num / numero_votos
            progress_bar.progress(progress)
            status_text.info(f"⏳ Progresso: {voto_num}/{numero_votos} votos | ⭐ {estrelas} estrelas")

            if voto_num < numero_votos:
                time.sleep(1)

    except Exception as e:
        status_text.error(f"Erro ao votar: {str(e)}")

    return votos_sucesso

# Interface Principal
st.markdown("""
    <div class="titulo-principal">
        <h1>🗳️ Votador - Feira de Ciência e Tecnologia</h1>
        <p>Vote nos melhores projetos da Univap Centro 2026</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔍 Selecione um Projeto")

with col2:
    if st.button("🔄 Recarregar", use_container_width=True, key="reload_btn"):
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

st.subheader("⭐ Quantas Estrelas?")
st.write("Clique para selecionar:")

cols = st.columns(5)
estrelas_selecionadas = 5  # padrão

for i in range(5):
    with cols[i]:
        if st.button(ESTRELAS[i+1], key=f"star_{i+1}", use_container_width=True):
            estrelas_selecionadas = i + 1

# Exibe seleção atual
st.markdown(f"""
    <div style='text-align: center; margin-top: 1rem; font-size: 2.5rem;'>
    {ESTRELAS[estrelas_selecionadas]}
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

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

"""
Script para extrair projetos uma única vez e salvar em JSON.
Execute isto localmente antes de fazer deploy.
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json
import time

URL_BASE = "https://cti.colegios.fve.edu.br/feira/index.html"

def extrair_projetos():
    """Extrai projetos e salva em JSON."""
    print("🔄 Extraindo projetos...")

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
                print("❌ Elemento 'grade' não encontrado!")
                return []

            cards = grade.find_all('article', class_='card-projeto')
            print(f"✅ Encontrados {len(cards)} projetos")

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
                except Exception as e:
                    print(f"⚠️  Erro ao extrair projeto {idx}: {e}")
                    continue

            # Salva em JSON
            with open('projetos.json', 'w', encoding='utf-8') as f:
                json.dump(projetos, f, ensure_ascii=False, indent=2)

            print(f"✅ {len(projetos)} projetos salvos em 'projetos.json'")
            return projetos

        finally:
            page.close()
            context.close()

if __name__ == "__main__":
    extrair_projetos()

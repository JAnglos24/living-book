import os
import time
import json
import re
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load credentials from symbios
load_dotenv(r"D:\symbios_seed\.env")
USER = os.getenv("LINKEDIN_USER")
PWD = os.getenv("LINKEDIN_PASS")

def extract_articles():
    with sync_playwright() as p:
        print("Iniciando Playwright...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()

        print("Navegando a LinkedIn Login...")
        page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
        page.fill("#username", USER)
        page.fill("#password", PWD)
        page.click('[type="submit"]')
        page.wait_for_url("**/feed/**", timeout=30000)
        
        print("Login exitoso. Navegando a artículos...")
        page.goto("https://www.linkedin.com/in/josé-angel-sosa-lópez-2568683a/recent-activity/articles/", wait_until="networkidle")
        
        try:
            page.wait_for_selector('.profile-creator-shared-feed-update__container', timeout=15000)
        except:
            print("No se encontraron articulos o cargó lento.")
        
        for i in range(3):
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(2)
            
        articles = []
        items = page.query_selector_all('.profile-creator-shared-feed-update__container')
        
        for item in items:
            title_el = item.query_selector('.break-words.update-components-article__title')
            link_el = item.query_selector('a.app-aware-link')
            date_el = item.query_selector('.visually-hidden')
            desc_el = item.query_selector('.update-components-article__description')
            
            if title_el and link_el:
                title = title_el.inner_text().strip()
                link = link_el.get_attribute("href").split('?')[0]
                date = date_el.inner_text().strip() if date_el else "Reciente"
                desc = desc_el.inner_text().strip() if desc_el else ""
                
                articles.append({
                    "title": title,
                    "link": link,
                    "date": date,
                    "desc": desc
                })
                
        print(f"Se extrajeron {len(articles)} articulos.")
        browser.close()
        return articles

def update_astro_files(articles):
    if not articles:
        return
        
    html_content = ""
    for art in articles:
        html_content += f"""
    <article class="article">
      <span class="date">{art['date']}</span>
      <div>
        <h2><a href="{art['link']}">{art['title']}</a></h2>
        <p>{art['desc']}</p>
      </div>
      <a class="go" href="{art['link']}">Read on LinkedIn ↗</a>
    </article>
"""
    
    def replace_file(filepath, lang):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            replaced_html = html_content
            if lang == 'es':
                replaced_html = replaced_html.replace('Read on LinkedIn ↗', 'Leer en LinkedIn ↗')
                
            pattern = re.compile(r'<section class="list">\s*<div class="wrap">[\s\S]*?</div>\s*</section>')
            new_content = pattern.sub(f'<section class="list">\n  <div class="wrap">\n{replaced_html}  </div>\n</section>', content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[{lang.upper()}] Archivo actualizado: {filepath}")
        except Exception as e:
            print(f"Error actualizando {filepath}: {e}")
            
    replace_file(r"D:\Proyectos personales\personal branding\living_book_astro\src\pages\articles.astro", "en")
    replace_file(r"D:\Proyectos personales\personal branding\living_book_astro\src\pages\es\articles.astro", "es")

if __name__ == "__main__":
    arts = extract_articles()
    update_astro_files(arts)

import os
import re

EN_SRC = r"D:\Proyectos personales\personal branding\Living book\Chapter6\ebook-chapter-06.html"
ES_SRC = r"D:\Proyectos personales\personal branding\Living book\Chapter6\es-ebook-chapter-06.html"

EN_DEST = r"D:\Proyectos personales\personal branding\living_book_astro\src\content\ebook\06-designing-for-maintenance-not-just-launch.mdx"
ES_DEST_DIR = r"D:\Proyectos personales\personal branding\living_book_astro\src\pages\es\ebook\06-designing-for-maintenance-not-just-launch"
ES_DEST = os.path.join(ES_DEST_DIR, "index.astro")

os.makedirs(ES_DEST_DIR, exist_ok=True)

# Helper to read with encoding fallback
def read_html(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Test if invalid characters were read
            if '\ufffd' not in content:
                return content
    except UnicodeDecodeError:
        pass
    with open(path, 'r', encoding='windows-1252') as f:
        return f.read()

en_raw = read_html(EN_SRC)
es_raw = read_html(ES_SRC)

def clean_svgs(content):
    # Convert SVG classes and var(--line) to presentation attributes
    replacements = [
        ('fill="var(--line)"', 'fill="#C9D0D8"'),
        ('class="dbox strong"', 'fill="#0057D9" stroke="#0057D9" stroke-width="1.5"'),
        ('class="dbox"', 'fill="#FFFFFF" stroke="#C9D0D8" stroke-width="1.5"'),
        ('class="dtext on"', 'font-family="Archivo,sans-serif" font-weight="700" fill="#ffffff"'),
        ('class="dtext"', 'font-family="Archivo,sans-serif" font-weight="700" fill="#111418"'),
        ('class="dsub on"', 'font-family="Archivo,sans-serif" font-weight="500" fill="rgba(255,255,255,.85)"'),
        ('class="dsub"', 'font-family="Archivo,sans-serif" font-weight="500" fill="#5C6673"'),
        ('class="darrow blue"', 'stroke="#2E7CFF" stroke-width="1.5" fill="none"'),
        ('class="darrow"', 'stroke="#C9D0D8" stroke-width="1.5" fill="none"'),
    ]
    for old, new in replacements:
        content = content.replace(old, new)
    return content

def remove_colophon(content):
    # Remove <section class="colophon">...</section>
    pattern = r'<section class="colophon">.*?</section>'
    return re.sub(pattern, '', content, flags=re.DOTALL)

def extract_body(content):
    # Extract between <body> and </body>, removing script tag before </body>
    m = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
    if not m:
        raise ValueError("Could not find body tag")
    body = m.group(1).strip()
    # Remove script tag at end of body if present
    body = re.sub(r'<script.*?</script>', '', body, flags=re.DOTALL).strip()
    return body

# Process EN
en_body = extract_body(en_raw)
en_body = remove_colophon(en_body)
en_body = clean_svgs(en_body)

# In EN body, convert topbar
en_topbar_old = re.search(r'<div class="topbar">.*?</div>\s*</div>', en_body, re.DOTALL)
en_topbar_new = """<div class="topbar">
  <div class="wrap row">
    <a class="home" href="/">JAS</a>
    <div class="chapmeta"><b>Chapter 06</b><span>Designing for Maintenance, Not Just Launch</span></div>
    <nav aria-label="Book">
      <a href="/ebook/">Contents</a>
      <a href="/author/">Author</a>
    </nav>
    <div class="lang" role="group" aria-label="Language"><a href="/ebook/06-designing-for-maintenance-not-just-launch/" aria-current="page">EN</a><span aria-hidden="true">/</span><a href="/es/ebook/06-designing-for-maintenance-not-just-launch/" hreflang="es">ES</a></div>
    <button class="toc-btn" id="tocBtn" aria-haspopup="dialog" aria-controls="tocPanel">Contents</button>
  </div>
  <div class="progress" aria-hidden="true"><i id="progressBar"></i></div>
</div>"""

en_body = re.sub(r'<div class="topbar">.*?<div class="progress".*?</div>\s*</div>', en_topbar_new, en_body, count=1, flags=re.DOTALL)

# In EN body, update chapternav prev link to Astro route
en_body = en_body.replace('href="ebook-chapter-05.html"', 'href="/ebook/05-digital-materials-apis-data-and-constraints/"')

# In EN body, update footer links
en_body = en_body.replace('href="ebook.html"', 'href="/ebook/"')
en_body = en_body.replace('href="author.html"', 'href="/author/"')

# In MDX, convert HTML comments <!-- ... --> to {/* ... */}
en_body = re.sub(r'<!--(.*?)-->', r'{/*\1*/}', en_body)

# Assemble MDX
en_mdx = f"""---
chapter: 6
title: "Designing for Maintenance, Not Just Launch"
status: "published"
published_at: 2026-10-12
summary: "A product has to keep being useful after its debut. Designing its maintenance means anticipating wear, growth, costs and conditions of use that launch barely lets us see."
---

{en_body}
"""

with open(EN_DEST, 'w', encoding='utf-8') as f:
    f.write(en_mdx)

print(f"Wrote EN MDX: {EN_DEST}")

# Process ES
es_body = extract_body(es_raw)
es_body = remove_colophon(es_body)
es_body = clean_svgs(es_body)

es_topbar_new = """<div class="topbar">
  <div class="wrap row">
    <a class="home" href="/es/">JAS</a>
    <div class="chapmeta"><b>Capítulo 06</b><span>Diseñar para el mantenimiento, no solo para el lanzamiento</span></div>
    <nav aria-label="Libro">
      <a href="/es/ebook/">Contenido</a>
      <a href="/es/author/">Autor</a>
    </nav>
    <div class="lang" role="group" aria-label="Idioma"><a href="/ebook/06-designing-for-maintenance-not-just-launch/" hreflang="en">EN</a><span aria-hidden="true">/</span><a href="/es/ebook/06-designing-for-maintenance-not-just-launch/" aria-current="page">ES</a></div>
    <button class="toc-btn" id="tocBtn" aria-haspopup="dialog" aria-controls="tocPanel">Contenido</button>
  </div>
  <div class="progress" aria-hidden="true"><i id="progressBar"></i></div>
</div>"""

es_body = re.sub(r'<div class="topbar">.*?<div class="progress".*?</div>\s*</div>', es_topbar_new, es_body, count=1, flags=re.DOTALL)

# In ES body, update chapternav prev link to Astro route
es_body = es_body.replace('href="es-ebook-chapter-05.html"', 'href="/es/ebook/05-digital-materials-apis-data-and-constraints/"')

# In ES body, update footer links
es_body = es_body.replace('href="es-ebook.html"', 'href="/es/ebook/"')
es_body = es_body.replace('href="es-author.html"', 'href="/es/author/"')
es_body = es_body.replace('href="#privacy"', 'href="/es/privacidad/"')

es_astro = f"""---
import Layout from '../../../../layouts/Layout.astro';
import editorialCss from '../../../../styles/chapter-editorial.css?raw';
const title = "Capítulo 6 — Diseñar para el mantenimiento, no solo para el lanzamiento · Pensar en Productos, Construir Sistemas";
const summary = "Capítulo 6 del Libro Vivo: por qué el mantenimiento forma parte de la visión de producto — dos especificaciones físicas, la economía del mantenimiento, SSDLC y SSDF, volumen y margen, el día de la emergencia, un mapa a tres años y cómo medir lo que envejece.";
---
<Layout
  title={{title}}
  description={{summary}}
  ogImage="/assets/ebook-hero.png"
  ogType="article"
  ogUrl="https://www.jasosal.com/es/ebook/06-designing-for-maintenance-not-just-launch/"
>
<Fragment set:html={{`<style>${{editorialCss}}</style>`}} />

{es_body}

<script is:inline>
(function(){{
  var bar=document.getElementById('progressBar');
  function onScroll(){{
    var h=document.documentElement, p=(h.scrollTop)/(h.scrollHeight-h.clientHeight)*100;
    if(bar) bar.style.setProperty('--p', p+'%');
  }}
  document.addEventListener('scroll', onScroll, {{passive:true}}); onScroll();
  var tocBtn=document.getElementById('tocBtn');
  if(tocBtn){{ tocBtn.addEventListener('click', function(){{ window.location.href='/es/ebook/#toc'; }}); }}
}})();
</script>
</Layout>
"""

with open(ES_DEST, 'w', encoding='utf-8') as f:
    f.write(es_astro)

print(f"Wrote ES Astro: {ES_DEST}")

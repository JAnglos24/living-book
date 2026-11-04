import os
import re
import xml.dom.minidom
from PIL import Image

ROOT = r"D:\Proyectos personales\personal branding"
SRC = os.path.join(ROOT, "Living book", "Chapter 9")
SITE = os.path.join(ROOT, "living_book_astro")
ASSETS = os.path.join(SITE, "public", "assets")

EN_SRC = os.path.join(SRC, "ebook-chapter-09.html")
ES_SRC = os.path.join(SRC, "es-ebook-chapter-09.html")
SLUG = "09-engineering-excellence-as-a-product-decision"
EN_DEST = os.path.join(SITE, "src", "content", "ebook", SLUG + ".mdx")
ES_DEST_DIR = os.path.join(SITE, "src", "pages", "es", "ebook", SLUG)
ES_DEST = os.path.join(ES_DEST_DIR, "index.astro")
os.makedirs(ES_DEST_DIR, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

# 1. Measure dimensions of all images in public/assets
DIMS = {}
for fn in os.listdir(ASSETS):
    if fn.startswith("chapter-09-"):
        fp = os.path.join(ASSETS, fn)
        if fn.endswith((".jpg", ".png")):
            try:
                im = Image.open(fp)
                DIMS[fn] = im.size
            except Exception as e:
                print("Error reading", fn, e)

print(f"Loaded {len(DIMS)} image dimensions from public/assets")

# 2. Extract standalone SVGs
def extract_standalone_svgs(html_content, lang):
    svgs = re.findall(r'<svg[^>]*>[\s\S]*?</svg>', html_content)
    names = ['chapter-09-mean-median', 'chapter-09-benefit-journey', 'chapter-09-two-evidence-loops']
    assert len(svgs) == 3, f"Expected 3 SVGs, found {len(svgs)}"
    for i, name in enumerate(names):
        s = svgs[i]
        if 'xmlns="http://www.w3.org/2000/svg"' not in s:
            s = s.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        # Validate XML
        xml.dom.minidom.parseString(s.encode("utf-8"))
        fn = f"{name}-{lang}.svg"
        with open(os.path.join(ASSETS, fn), "w", encoding="utf-8") as f:
            f.write(s)
        print(f"Saved standalone SVG: {fn}")

# 3. HTML processing helpers
def read_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_body(content):
    m = re.search(r"<body[^>]*>(.*)</body>", content, re.DOTALL)
    body = m.group(1).strip()
    return re.sub(r"<script.*?</script>", "", body, flags=re.DOTALL).strip()

def remove_unwanted(content):
    # Remove preview-note
    content = re.sub(r'<div class="preview-note">.*?</div>', "", content, flags=re.DOTALL)
    # Remove colophon (editorial history - not published in chapter page)
    content = re.sub(r'<section class="colophon">.*?</section>', "", content, flags=re.DOTALL)
    return content.strip()

def fix_images(body):
    def repl(m):
        tag = m.group(0)
        src = re.search(r'src="/assets/([^"]+)"', tag).group(1)
        if src in DIMS:
            w, h = DIMS[src]
            tag = re.sub(r'width="\d+"', f'width="{w}"', tag)
            tag = re.sub(r'height="\d+"', f'height="{h}"', tag)
        return tag

    return re.sub(r'<img [^>]*src="/assets/chapter-09-[^>]*>', repl, body)

def fix_links(body, lang):
    es = lang == "es"
    pre = "/es" if es else ""
    ebook_file = "es-ebook-chapter-" if es else "ebook-chapter-"
    slugs = {
        "01": "01-what-can-industrial-design-teach",
        "02": "02-product-strategy-materials-cost-of-a-decision",
        "03": "03-what-a-production-line-teaches-about-architecture",
        "04": "04-the-product-is-never-just-the-object",
        "05": "05-digital-materials-apis-data-and-constraints",
        "06": "06-designing-for-maintenance-not-just-launch",
        "07": "07-interfaces-as-tolerances",
        "08": "08-what-breaks-when-you-scale-a-product",
        "09": SLUG,
    }
    for n, s in slugs.items():
        body = body.replace(f'href="{ebook_file}{n}.html"', f'href="{pre}/ebook/{s}/"')
        body = body.replace(f'href="ebook-chapter-{n}.html"', f'href="/ebook/{s}/"')
        body = body.replace(f'href="es-ebook-chapter-{n}.html"', f'href="/es/ebook/{s}/"')
    body = body.replace('href="es-ebook.html"', 'href="/es/ebook/"').replace('href="ebook.html"', 'href="/ebook/"')
    body = body.replace('href="es-author.html"', 'href="/es/author/"').replace('href="author.html"', 'href="/author/"')
    body = body.replace('href="es-contact.html"', 'href="/es/contacto/"').replace('href="contact.html"', 'href="/contact/"')
    return body

def topbar(lang):
    if lang == "en":
        return f"""<div class="topbar">
  <div class="wrap row">
    <a class="home" href="/">JAS</a>
    <div class="chapmeta"><b>Chapter 09</b><span>Engineering Excellence as a Product Decision</span></div>
    <nav aria-label="Book">
      <a href="/ebook/">Contents</a>
      <a href="/author/">Author</a>
    </nav>
    <div class="lang" role="group" aria-label="Language"><a href="/ebook/{SLUG}/" aria-current="page">EN</a><span aria-hidden="true">/</span><a href="/es/ebook/{SLUG}/" hreflang="es">ES</a></div>
    <button class="toc-btn" id="tocBtn" aria-haspopup="dialog" aria-controls="tocPanel">Contents</button>
  </div>
  <div class="progress" aria-hidden="true"><i id="progressBar"></i></div>
</div>"""
    return f"""<div class="topbar">
  <div class="wrap row">
    <a class="home" href="/es/">JAS</a>
    <div class="chapmeta"><b>Capítulo 09</b><span>La excelencia en ingeniería como decisión de producto</span></div>
    <nav aria-label="Libro">
      <a href="/es/ebook/">Contenido</a>
      <a href="/es/author/">Autor</a>
    </nav>
    <div class="lang" role="group" aria-label="Idioma"><a href="/ebook/{SLUG}/" hreflang="en">EN</a><span aria-hidden="true">/</span><a href="/es/ebook/{SLUG}/" aria-current="page">ES</a></div>
    <button class="toc-btn" id="tocBtn" aria-haspopup="dialog" aria-controls="tocPanel">Contenido</button>
  </div>
  <div class="progress" aria-hidden="true"><i id="progressBar"></i></div>
</div>"""

def build_body(path, lang):
    raw = read_html(path)
    extract_standalone_svgs(raw, lang)
    body = remove_unwanted(extract_body(raw))
    body = re.sub(r'<div class="topbar">.*?<div class="progress".*?</div>\s*</div>', topbar(lang), body, count=1, flags=re.DOTALL)
    body = fix_images(body)
    body = fix_links(body, lang)
    return body

SUMMARY_EN = "How to turn a population's expectations into engineering decisions, experiment with rigor and use evidence to improve physical products, digital products and services."
SUMMARY_ES = "Cómo convertir las expectativas de una población en decisiones de ingeniería, experimentar con rigor y usar la evidencia para mejorar productos físicos, digitales y servicios."

# ---- EN (MDX)
en_body = build_body(EN_SRC, "en")
en_body = re.sub(r"<br(?!\s*/)>", "<br />", en_body)
en_body = re.sub(r"<!--(.*?)-->", r"{/*\1*/}", en_body, flags=re.DOTALL)
en_mdx = f"""---
chapter: 9
title: "Engineering Excellence as a Product Decision"
status: "published"
published_at: 2026-11-03
summary: "{SUMMARY_EN}"
og_image: "/assets/chapter-09-expectation-workshop.jpg"
hero_image: "/assets/chapter-09-expectation-workshop.jpg"
keywords: "product engineering, quality, applied statistics, experimentation, continuous improvement, product decisions, ergonomics"
---

{en_body}
"""
with open(EN_DEST, "w", encoding="utf-8") as f:
    f.write(en_mdx)
print("EN ->", EN_DEST)

# ---- ES (Astro)
es_body = build_body(ES_SRC, "es")
es_astro = f"""---
import Layout from '../../../../layouts/Layout.astro';
import editorialCss from '../../../../styles/chapter-editorial.css?raw';
const title = "Capítulo 9 — La excelencia en ingeniería como decisión de producto · Pensar en Productos, Construir Sistemas";
const summary = "{SUMMARY_ES}";
---
<Layout
  title={{title}}
  description={{summary}}
  ogImage="/assets/chapter-09-expectation-workshop.jpg"
  ogType="article"
  ogUrl="https://www.jasosal.com/es/ebook/{SLUG}/"
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
with open(ES_DEST, "w", encoding="utf-8") as f:
    f.write(es_astro)
print("ES ->", ES_DEST)

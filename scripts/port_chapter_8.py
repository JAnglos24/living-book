import os
import re
import xml.dom.minidom
from PIL import Image

ROOT = r"D:\Proyectos personales\personal branding"
SRC = os.path.join(ROOT, "Living book", "Chapter 8")
SITE = os.path.join(ROOT, "living_book_astro")
ASSETS = os.path.join(SITE, "public", "assets")

EN_SRC = os.path.join(SRC, "ebook-chapter-08.html")
ES_SRC = os.path.join(SRC, "es-ebook-chapter-08.html")
SLUG = "08-what-breaks-when-you-scale-a-product"
EN_DEST = os.path.join(SITE, "src", "content", "ebook", SLUG + ".mdx")
ES_DEST_DIR = os.path.join(SITE, "src", "pages", "es", "ebook", SLUG)
ES_DEST = os.path.join(ES_DEST_DIR, "index.astro")
os.makedirs(ES_DEST_DIR, exist_ok=True)

# --- imagenes: PNG de origen -> JPG optimizado (el objeto transparente queda PNG con alfa) ---
PHOTOS = {
    "chapter-08-workshop-bottleneck": "Unfired Vessels Await the Kiln-3.png",
    "chapter-08-promise-handmade": "Hands shaping a clay vessel-1.png",
    "chapter-08-promise-short-series": "Seven Stoneware Vessels, One Cobalt Accent-5.png",
    "chapter-08-promise-volume-line": "Ceramic Rows Along a Blue Line-7.png",
    "chapter-08-pressure-casting-mold": "Porcelain bowl beside casting mold-2.png",
    "chapter-08-hand-finishing": "Cobalt rim on handmade porcelain-4.png",
    "chapter-08-exceptions-bench": "Nueve formas, un hilo azul-1.png",
    "chapter-08-inspection-bench": "Medición de precisión en cerámica-2.png",
    "chapter-08-shadow-board": "Dos ausencias azules en el tablero-3.png",
    "chapter-08-packing-returns": "Plato blanco y cerámica rota-4.png",
    "chapter-08-two-benches": "Dos mesas, dos momentos-5.png",
    "chapter-08-robot-arm-demold": "Robot y manos en el taller cerámico-6.png",
}
DIMS = {}
for name, fn in PHOTOS.items():
    im = Image.open(os.path.join(SRC, "Assets", fn)).convert("RGB")
    im.save(os.path.join(ASSETS, name + ".jpg"), "JPEG", quality=86, optimize=True, progressive=True)
    DIMS[name + ".jpg"] = im.size
kim = Image.open(os.path.join(SRC, "Assets", "Kintsugi cobalt stoneware bowl-6.png"))
assert kim.mode == "RGBA" and kim.getchannel("A").getextrema()[0] < 255, "el objeto kintsugi debe tener alfa real"
kim.save(os.path.join(ASSETS, "chapter-08-kintsugi-bowl-transparent.png"), optimize=True)
DIMS["chapter-08-kintsugi-bowl-transparent.png"] = kim.size


def read_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_body(content):
    m = re.search(r"<body[^>]*>(.*)</body>", content, re.DOTALL)
    body = m.group(1).strip()
    return re.sub(r"<script.*?</script>", "", body, flags=re.DOTALL).strip()


def remove_colophon(content):
    return re.sub(r'<section class="colophon">.*?</section>', "", content, flags=re.DOTALL)


FIGS = ["chapter-08-adoption-curve", "chapter-08-support-bells", "chapter-08-performance-dip"]


def externalize_svgs(body, lang):
    """Los 3 diagramas grandes usan <style>+clases (la CSP los dejaria negros): van como archivos .svg
    y la pagina los referencia con <image> dentro de un <svg> (el CSS existente de .diagram svg los dimensiona)."""
    out, idx = [], [0]

    def repl(m):
        svg = m.group(0)
        if len(svg) < 5000:
            return svg
        name = FIGS[idx[0]]
        idx[0] += 1
        label = re.search(r'aria-label="([^"]*)"', svg).group(1)
        vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
        w, h = vb.group(1), vb.group(2)
        standalone = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1) if 'xmlns="' not in svg.split(">")[0] else svg
        standalone = re.sub(r'\srole="img"|\saria-label="[^"]*"', "", standalone, count=2)
        xml.dom.minidom.parseString(standalone.encode("utf-8"))  # debe ser XML valido
        fn = f"{name}-{lang}.svg"
        with open(os.path.join(ASSETS, fn), "w", encoding="utf-8") as f:
            f.write(standalone)
        out.append(fn)
        return (f'<svg role="img" aria-label="{label}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
                f'<image href="/assets/{fn}" x="0" y="0" width="{w}" height="{h}"/></svg>')

    body = re.sub(r"<svg.*?</svg>", repl, body, flags=re.DOTALL)
    assert len(out) == 3, out
    return body


def fix_images(body):
    def repl(m):
        tag = m.group(0)
        src = re.search(r'src="/assets/([^"]+)"', tag).group(1)
        base = src.rsplit(".", 1)[0]
        real = base + (".png" if "transparent" in base else ".jpg")
        w, h = DIMS[real]
        tag = tag.replace(src, real)
        return re.sub(r'width="\d+"', f'width="{w}" height="{h}"', tag, count=1)

    return re.sub(r'<img [^>]*src="/assets/chapter-08-[^>]*>', repl, body)


def fix_common(body, lang):
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
        "08": SLUG,
    }
    for n, s in slugs.items():
        body = body.replace(f'href="{ebook_file}{n}.html"', f'href="{pre}/ebook/{s}/"')
    body = body.replace('href="es-ebook.html"', 'href="/es/ebook/"').replace('href="ebook.html"', 'href="/ebook/"')
    body = body.replace('href="es-author.html"', 'href="/es/author/"').replace('href="author.html"', 'href="/author/"')
    body = body.replace('href="../downloads/thinking-in-products-building-systems-current.pdf"',
                        'href="/downloads/thinking-in-products-building-systems-current.pdf"')
    return body


def topbar(lang):
    if lang == "en":
        return f"""<div class="topbar">
  <div class="wrap row">
    <a class="home" href="/">JAS</a>
    <div class="chapmeta"><b>Chapter 08</b><span>What Breaks When You Scale a Product</span></div>
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
    <div class="chapmeta"><b>Capítulo 08</b><span>Qué se rompe al escalar un producto</span></div>
    <nav aria-label="Libro">
      <a href="/es/ebook/">Contenido</a>
      <a href="/es/author/">Autor</a>
    </nav>
    <div class="lang" role="group" aria-label="Idioma"><a href="/ebook/{SLUG}/" hreflang="en">EN</a><span aria-hidden="true">/</span><a href="/es/ebook/{SLUG}/" aria-current="page">ES</a></div>
    <button class="toc-btn" id="tocBtn" aria-haspopup="dialog" aria-controls="tocPanel">Contenido</button>
  </div>
  <div class="progress" aria-hidden="true"><i id="progressBar"></i></div>
</div>"""


def build(path, lang):
    body = remove_colophon(extract_body(read_html(path)))
    body = re.sub(r'<div class="topbar">.*?<div class="progress".*?</div>\s*</div>', topbar(lang), body, count=1, flags=re.DOTALL)
    body = externalize_svgs(body, lang)
    body = fix_images(body)
    body = fix_common(body, lang)
    return body


SUMMARY_EN = "Growth changes the conditions under which a product creates value. The product owner's job is to recognize what must be transformed and what deserves to remain."
SUMMARY_ES = "Crecer cambia las condiciones bajo las que un producto crea valor. La tarea del dueño de producto consiste en reconocer qué debe transformarse y qué merece permanecer."

# ---- EN (MDX)
en_body = build(EN_SRC, "en")
en_body = re.sub(r"<br(?!\s*/)>", "<br />", en_body)
en_body = re.sub(r"<!--(.*?)-->", r"{/*\1*/}", en_body, flags=re.DOTALL)
en_mdx = f"""---
chapter: 8
title: "What Breaks When You Scale a Product"
status: "published"
published_at: 2026-10-27
summary: "{SUMMARY_EN}"
og_image: "/assets/chapter-08-promise-short-series.jpg"
hero_image: "/assets/chapter-08-promise-short-series.jpg"
keywords: "scaling products, product management, industrial design, production, adoption, change management, product operations"
---

{en_body}
"""
with open(EN_DEST, "w", encoding="utf-8") as f:
    f.write(en_mdx)
print("EN ->", EN_DEST)

# ---- ES (Astro)
es_body = build(ES_SRC, "es")
es_astro = f"""---
import Layout from '../../../../layouts/Layout.astro';
import editorialCss from '../../../../styles/chapter-editorial.css?raw';
const title = "Capítulo 8 — Qué se rompe al escalar un producto · Pensar en Productos, Construir Sistemas";
const summary = "{SUMMARY_ES}";
---
<Layout
  title={{title}}
  description={{summary}}
  ogImage="/assets/chapter-08-promise-short-series.jpg"
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

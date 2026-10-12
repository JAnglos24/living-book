import os
import re

EN_SRC = r"D:\Proyectos personales\personal branding\Living book\Chapter6\ebook-chapter-06.html"
ES_SRC = r"D:\Proyectos personales\personal branding\Living book\Chapter6\es-ebook-chapter-06.html"

EN_DEST = r"D:\Proyectos personales\personal branding\living_book_astro\src\content\ebook\06-designing-for-maintenance-not-just-launch.mdx"
ES_DEST_DIR = r"D:\Proyectos personales\personal branding\living_book_astro\src\pages\es\ebook\06-designing-for-maintenance-not-just-launch"
ES_DEST = os.path.join(ES_DEST_DIR, "index.astro")

os.makedirs(ES_DEST_DIR, exist_ok=True)

def read_html(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '\ufffd' not in content:
                return content
    except UnicodeDecodeError:
        pass
    with open(path, 'r', encoding='windows-1252') as f:
        return f.read()

en_raw = read_html(EN_SRC)
es_raw = read_html(ES_SRC)

def clean_svgs(content):
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
    pattern = r'<section class="colophon">.*?</section>'
    return re.sub(pattern, '', content, flags=re.DOTALL)

def extract_body(content):
    m = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
    if not m:
        raise ValueError("Could not find body tag")
    body = m.group(1).strip()
    body = re.sub(r'<script.*?</script>', '', body, flags=re.DOTALL).strip()
    return body

IMAGES_DATA = [
    {
        "file": "chapter-06-launch-and-year-three.jpg",
        "w": 2400, "h": 3000,
        "alt_es": "Dos objetos idénticos sin marca, uno nuevo y otro con años de uso, sobre una superficie neutra",
        "alt_en": "Two identical unbranded objects, one new and one with years of use, on a neutral surface",
        "span_es": "[ retrato 4:5 — dos objetos idénticos lado a lado: uno nuevo y otro con tres años de uso, con una pieza reemplazada en cobalto ]",
        "span_en": "[ 4:5 portrait — two identical objects side by side: one new and one with three years of use, with one replaced part in cobalt ]"
    },
    {
        "file": "chapter-06-playground-repaint.jpg",
        "w": 3200, "h": 1800,
        "alt_es": "Estructura metálica de un juego infantil en un parque durante un repintado",
        "alt_en": "Metal play structure in a park during a repaint",
        "span_es": "[ lámina 16:9 — un juego infantil de acero en un parque durante un repintado, con una franja cobalto a medio aplicar ]",
        "span_en": "[ 16:9 plate — a steel children's play structure in a park during a repaint, with a cobalt stripe half applied ]"
    },
    {
        "file": "chapter-06-spare-parts-workbench.jpg",
        "w": 2400, "h": 3000,
        "alt_es": "Mesa de trabajo con carcasas de repuesto, piezas pequeñas ordenadas y herramientas de precisión",
        "alt_en": "Workbench with spare casings, small organized parts and precision tools",
        "span_es": "[ retrato 4:5 — mesa de trabajo con carcasas de repuesto, piezas pequeñas ordenadas y herramientas de precisión bajo una lámpara ]",
        "span_en": "[ 4:5 portrait — a workbench with spare casings, small organized parts and precision tools under a lamp ]"
    },
    {
        "file": "chapter-06-repairable-object-transparent.png",
        "w": 2400, "h": 2400,
        "alt_es": "Vista despiezada de un objeto con tapa, empaque, cuerpo y base, con las piezas reemplazables resaltadas en cobalto",
        "alt_en": "Exploded view of an object with lid, gasket, body and base, with replaceable parts highlighted in cobalt",
        "span_es": "[ objeto transparente — vista despiezada de un objeto con tapa, empaque, cuerpo y base; las piezas de desgaste resaltadas en cobalto ]",
        "span_en": "[ transparent object — exploded view of an object with lid, gasket, body and base; the wear parts highlighted in cobalt ]"
    },
    {
        "file": "chapter-06-filter-shelf.jpg",
        "w": 2400, "h": 3000,
        "alt_es": "Estante de taller con cartuchos de filtro sin marca",
        "alt_en": "Workshop shelf with unbranded filter cartridges",
        "span_es": "[ retrato 4:5 — estante de taller con cartuchos de filtro sin marca y una etiqueta cobalto ]",
        "span_en": "[ 4:5 portrait — a workshop shelf with unbranded filter cartridges and a cobalt tag ]"
    },
    {
        "file": "chapter-06-handover-binder.jpg",
        "w": 2400, "h": 3000,
        "alt_es": "Un manual cerrado junto a una bitácora abierta con anotaciones",
        "alt_en": "A closed manual next to an open logbook with notes",
        "span_es": "[ retrato 4:5 — un manual cerrado junto a una bitácora abierta con anotaciones borrosas y un marcador cobalto ]",
        "span_en": "[ 4:5 portrait — a closed manual beside an open logbook with blurred notes and a cobalt bookmark ]"
    },
    {
        "file": "chapter-06-worn-handrail.jpg",
        "w": 2400, "h": 3000,
        "alt_es": "Primer plano de un pasamanos metálico con la pintura desgastada donde se agarra",
        "alt_en": "Close-up of a metal handrail with paint worn away where it is gripped",
        "span_es": "[ retrato 4:5 — primer plano de un pasamanos metálico con la pintura desgastada justo donde se agarra, y un detalle cobalto fuera de foco ]",
        "span_en": "[ 4:5 portrait — close-up of a metal handrail with paint worn away exactly where it is gripped, with an out-of-focus cobalt detail ]"
    },
    {
        "file": "chapter-06-emergency-phone.jpg",
        "w": 2400, "h": 3000,
        "alt_es": "Una mano sostiene un teléfono con pantalla tenue en una calle lluviosa",
        "alt_en": "A hand holding a phone with a dim screen on a rainy street",
        "span_es": "[ retrato 4:5 — una mano sostiene un teléfono con pantalla tenue y poca batería en una calle lluviosa, desenfocada, con un reflejo cobalto ]",
        "span_en": "[ 4:5 portrait — a hand holding a phone with a dim screen and low battery on a rainy, out-of-focus street, with a cobalt reflection ]"
    },
    {
        "file": "chapter-06-three-year-wall.jpg",
        "w": 2400, "h": 3000,
        "alt_es": "Pared de planeación con tres hileras de tarjetas en blanco unidas por un hilo azul",
        "alt_en": "Planning wall with three rows of blank cards joined by a blue thread",
        "span_es": "[ retrato 4:5 — pared de planeación con tres hileras de tarjetas en blanco y un hilo cobalto que las une ]",
        "span_en": "[ 4:5 portrait — a planning wall with three rows of blank cards joined by a cobalt thread ]"
    },
    {
        "file": "chapter-06-calipers-and-gauge.jpg",
        "w": 2400, "h": 3000,
        "alt_es": "Calibre, medidor de espesor y balanza junto a un componente desgastado y una libreta de campo",
        "alt_en": "Calipers, a thickness gauge and a scale next to a worn component and a field notebook",
        "span_es": "[ retrato 4:5 — calibre, medidor de espesor de recubrimiento y balanza sobre un componente desgastado, con una libreta de campo y un lápiz cobalto ]",
        "span_en": "[ 4:5 portrait — calipers, a coating-thickness gauge and a scale next to a worn component, with a field notebook and a cobalt pencil ]"
    },
    {
        "file": "chapter-06-weathering-rack.jpg",
        "w": 2400, "h": 3000,
        "alt_es": "Bastidor exterior con muestras idénticas etiquetadas, expuestas a la intemperie",
        "alt_en": "Outdoor rack with identical tagged samples exposed to the weather",
        "span_es": "[ retrato 4:5 — bastidor exterior con muestras idénticas etiquetadas con tarjetas cobalto, expuestas a la intemperie ]",
        "span_en": "[ 4:5 portrait — an outdoor rack with identical samples tagged with cobalt cards, exposed to the weather ]"
    },
    {
        "file": "chapter-06-second-life-product.jpg",
        "w": 2400, "h": 3000,
        "alt_es": "Un objeto reparado sobre una mesa de servicio junto a una bandeja de piezas de repuesto",
        "alt_en": "A repaired object on a service table next to a tray of spare parts",
        "span_es": "[ retrato 4:5 — un objeto reparado sobre una mesa de servicio, con una bandeja de piezas de repuesto y un empaque nuevo en cobalto ]",
        "span_en": "[ 4:5 portrait — a repaired object on a service table, with a tray of spare parts and a new cobalt gasket ]"
    }
]

def inject_images(content, is_es=True):
    for img in IMAGES_DATA:
        span_text = img["span_es"] if is_es else img["span_en"]
        alt_text = img["alt_es"] if is_es else img["alt_en"]
        src = f"/assets/{img['file']}"
        w, h = img["w"], img["h"]
        
        # Replace <span>...</span> with <img ... />
        pattern = re.escape(f"<span>{span_text}</span>")
        replacement = f'<img src="{src}" alt="{alt_text}" width="{w}" height="{h}" loading="lazy" />'
        content = re.sub(pattern, replacement, content)
    return content

# Process EN
en_body = extract_body(en_raw)
en_body = remove_colophon(en_body)
en_body = clean_svgs(en_body)
en_body = inject_images(en_body, is_es=False)

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
en_body = en_body.replace('href="ebook-chapter-05.html"', 'href="/ebook/05-digital-materials-apis-data-and-constraints/"')
en_body = en_body.replace('href="ebook.html"', 'href="/ebook/"')
en_body = en_body.replace('href="author.html"', 'href="/author/"')
en_body = en_body.replace('<span>Living edition 0.1</span>', '<span>Living edition 0.6</span>')

# Fix void tags in MDX
en_body = re.sub(r'<br(?!\s*/)>', r'<br />', en_body)
en_body = re.sub(r'<!--(.*?)-->', r'{/*\1*/}', en_body)

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
es_body = inject_images(es_body, is_es=True)

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
es_body = es_body.replace('href="es-ebook-chapter-05.html"', 'href="/es/ebook/05-digital-materials-apis-data-and-constraints/"')
es_body = es_body.replace('href="es-ebook.html"', 'href="/es/ebook/"')
es_body = es_body.replace('href="es-author.html"', 'href="/es/author/"')
es_body = es_body.replace('href="#privacy"', 'href="/es/privacidad/"')
es_body = es_body.replace('<span>Edición viva 0.1</span>', '<span>Edición viva 0.6</span>')

es_astro = f"""---
import Layout from '../../../../layouts/Layout.astro';
import editorialCss from '../../../../styles/chapter-editorial.css?raw';
const title = "Capítulo 6 — Diseñar para el mantenimiento, no solo para el lanzamiento · Pensar en Productos, Construir Sistemas";
const summary = "Capítulo 6 del Libro Vivo: por qué el mantenimiento forma parte de la visión de producto — dos especificaciones físicas, la economía del mantenimiento, SSDLC y SSDF, volumen y margen, el día de la emergencia, un mapa a tres años y cómo medir lo que envejece.";
---
<Layout
  title={{title}}
  description={{summary}}
  ogImage="/assets/chapter-06-launch-and-year-three.jpg"
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

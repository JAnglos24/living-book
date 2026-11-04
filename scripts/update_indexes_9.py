import os

B = r"D:\Proyectos personales\personal branding\living_book_astro"
S9 = "09-engineering-excellence-as-a-product-decision"
S8 = "08-what-breaks-when-you-scale-a-product"

DEK_EN = "How to turn a population&#x27;s expectations into engineering decisions, experiment with rigor and use evidence to improve physical products, digital products and services."
DEK_ES = "Cómo convertir las expectativas de una población en decisiones de ingeniería, experimentar con rigor y usar la evidencia para mejorar productos físicos, digitales y servicios."

def edit(path, pairs):
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    for old, new in pairs:
        assert s.count(old) == 1, f"Pattern count != 1 ({s.count(old)}) in {path}:\n{old[:120]}"
        s = s.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("ok", path)

# 1. chapter-editorial.css
css_path = os.path.join(B, "src", "styles", "chapter-editorial.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()
if ".figure.r916" not in css:
    css_addition = """
/* retratos más altos para acompañar columnas de texto largas (cap. 9) */
.longform .figure.r916{aspect-ratio:9/16}
.longform .figure.r23{aspect-ratio:2/3}
"""
    with open(css_path, "a", encoding="utf-8") as f:
        f.write(css_addition)
    print("ok chapter-editorial.css updated with r916 and r23")

# 2. Unlock Chapter 8 -> 9
edit(os.path.join(B, "src", "content", "ebook", f"{S8}.mdx"), [
    ('<div class="side next"><span class="lbl">NEXT →</span><span class="title" aria-disabled="true" style="opacity:.5">Next chapter — in development</span></div>',
     f'<div class="side next"><span class="lbl">NEXT →</span><a href="/ebook/{S9}/"><span class="title">Engineering Excellence as a Product Decision</span></a></div>')
])

edit(os.path.join(B, "src", "pages", "es", "ebook", S8, "index.astro"), [
    ('<div class="side next"><span class="lbl">SIGUIENTE →</span><span class="title" aria-disabled="true" style="opacity:.5">Siguiente capítulo — en desarrollo</span></div>',
     f'<div class="side next"><span class="lbl">SIGUIENTE →</span><a href="/es/ebook/{S9}/"><span class="title">La excelencia en ingeniería como decisión de producto</span></a></div>')
])

# 3. EN Index
card_8_en = '''    <article class="chapcard">
      <img class="bg-img" src="/assets/chapter-08-promise-short-series.jpg" alt="Chapter 8 hero">
      <span class="ch-num" aria-hidden="true">08</span>
      <div class="body">
        <p class="kicker">Part II &middot; From Physical to Digital &mdash; Chapter 8</p>
        <h3><a href="/ebook/08-what-breaks-when-you-scale-a-product/">What Breaks When You Scale a Product</a></h3>
        <p class="dek">Growth changes the conditions under which a product creates value. The product owner&#x27;s job is to recognize what must be transformed and what deserves to remain.</p>
        <a class="link" href="/ebook/08-what-breaks-when-you-scale-a-product/">Read chapter 8 &rarr;</a>
      </div>
    </article>'''

card_9_en = f'''    <article class="chapcard">
      <img class="bg-img" src="/assets/chapter-09-expectation-workshop.jpg" alt="Chapter 9 hero">
      <span class="ch-num" aria-hidden="true">09</span>
      <div class="body">
        <p class="kicker">Part III &middot; Building Digital Products &mdash; Chapter 9</p>
        <h3><a href="/ebook/{S9}/">Engineering Excellence as a Product Decision</a></h3>
        <p class="dek">{DEK_EN}</p>
        <a class="link" href="/ebook/{S9}/">Read chapter 9 &rarr;</a>
      </div>
    </article>'''

edit(os.path.join(B, "src", "pages", "ebook", "index.astro"), [
    ('<span class="num" aria-hidden="true">0.8</span>', '<span class="num" aria-hidden="true">0.9</span>'),
    ('Living edition 0.8 — 8 of ~20 chapters published — updated weekly', 'Living edition 0.9 — 9 of ~20 chapters published — updated weekly'),
    ('<div><b>8</b><span>CHAPTERS PUBLISHED<br>AS OF THIS EDITION</span></div>', '<div><b>9</b><span>CHAPTERS PUBLISHED<br>AS OF THIS EDITION</span></div>'),
    (f'<a href="/ebook/{S8}/">Chapter 8 of 20 (planned) &rarr;</a>', f'<a href="/ebook/{S9}/">Chapter 9 of 20 (planned) &rarr;</a>'),
    (card_8_en, card_9_en),
    ('<div class="partmeta"><b>Part III — Building Digital Products</b><span>0 of 4 published</span></div>',
     '<div class="partmeta"><b>Part III — Building Digital Products</b><span>1 of 4 published</span></div>'),
    ('<li><span class="n">09</span><span class="t locked">Engineering Excellence as a Product Decision</span><span class="st">Upcoming</span></li>',
     f'<li class="published"><a href="/ebook/{S9}/"><span class="n">09</span><span class="t">Engineering Excellence as a Product Decision</span><span class="st">Published</span></a></li>'),
    ('<li><b>Edition 0.8</b> Chapter 8 published — 27 Oct 2026</li>',
     '<li><b>Edition 0.9</b> Chapter 9 published — 03 Nov 2026</li>\n        <li><b>Edition 0.8</b> Chapter 8 published — 27 Oct 2026</li>'),
    ('Download PDF &mdash; Edition 0.8', 'Download PDF &mdash; Edition 0.9'),
    ('<li><a href="#toc"><span class="n">III</span><span class="t">Building Digital Products</span><span class="st">0/4</span></a></li>',
     '<li><a href="#toc"><span class="n">III</span><span class="t">Building Digital Products</span><span class="st">1/4</span></a></li>'),
])

# 4. ES Index
card_8_es = '''    <article class="chapcard">
      <img class="bg-img" src="/assets/chapter-08-promise-short-series.jpg" alt="Capítulo 8 hero">
      <span class="ch-num" aria-hidden="true">08</span>
      <div class="body">
        <p class="kicker">Parte II &middot; De lo Físico a lo Digital &mdash; Capítulo 8</p>
        <h3><a href="/es/ebook/08-what-breaks-when-you-scale-a-product/">Qué se rompe al escalar un producto</a></h3>
        <p class="dek">Crecer cambia las condiciones bajo las que un producto crea valor. La tarea del dueño de producto consiste en reconocer qué debe transformarse y qué merece permanecer.</p>
        <a class="link" href="/es/ebook/08-what-breaks-when-you-scale-a-product/">Leer el capítulo 8 &rarr;</a>
      </div>
    </article>'''

card_9_es = f'''    <article class="chapcard">
      <img class="bg-img" src="/assets/chapter-09-expectation-workshop.jpg" alt="Capítulo 9 hero">
      <span class="ch-num" aria-hidden="true">09</span>
      <div class="body">
        <p class="kicker">Parte III &middot; Construir Productos Digitales &mdash; Capítulo 9</p>
        <h3><a href="/es/ebook/{S9}/">La excelencia en ingeniería como decisión de producto</a></h3>
        <p class="dek">{DEK_ES}</p>
        <a class="link" href="/es/ebook/{S9}/">Leer el capítulo 9 &rarr;</a>
      </div>
    </article>'''

edit(os.path.join(B, "src", "pages", "es", "ebook", "index.astro"), [
    ('<span class="num" aria-hidden="true">0.8</span>', '<span class="num" aria-hidden="true">0.9</span>'),
    ('Edición viva 0.8 — 8 de ~20 capítulos publicados — se actualiza cada semana', 'Edición viva 0.9 — 9 de ~20 capítulos publicados — se actualiza cada semana'),
    ('<div><b>8</b><span>CAPÍTULOS PUBLICADOS<br>EN ESTA EDICIÓN</span></div>', '<div><b>9</b><span>CAPÍTULOS PUBLICADOS<br>EN ESTA EDICIÓN</span></div>'),
    (f'<a href="/es/ebook/{S8}/">Capítulo 8 de 20 (planeados) &rarr;</a>', f'<a href="/es/ebook/{S9}/">Capítulo 9 de 20 (planeados) &rarr;</a>'),
    (card_8_es, card_9_es),
    ('<div class="partmeta"><b>Parte III — Construir Productos Digitales</b><span>0 de 4 publicados</span></div>',
     '<div class="partmeta"><b>Parte III — Construir Productos Digitales</b><span>1 de 4 publicados</span></div>'),
    ('<li><span class="n">09</span><span class="t locked">La excelencia en ingeniería como decisión de producto</span><span class="st">Próximamente</span></li>',
     f'<li class="published"><a href="/es/ebook/{S9}/"><span class="n">09</span><span class="t">La excelencia en ingeniería como decisión de producto</span><span class="st">Publicado</span></a></li>'),
    ('<li><b>Edición 0.8</b> Capítulo 8 publicado — 27 oct 2026</li>',
     '<li><b>Edición 0.9</b> Capítulo 9 publicado — 03 nov 2026</li>\n        <li><b>Edición 0.8</b> Capítulo 8 publicado — 27 oct 2026</li>'),
    ('Descargar PDF &mdash; Edición 0.8', 'Descargar PDF &mdash; Edición 0.9'),
    ('<li><a href="#toc"><span class="n">III</span><span class="t">Construir Productos Digitales</span><span class="st">0/4</span></a></li>',
     '<li><a href="#toc"><span class="n">III</span><span class="t">Construir Productos Digitales</span><span class="st">1/4</span></a></li>'),
])

# 5. Home EN
edit(os.path.join(B, "src", "pages", "index.astro"), [
    (f'<a class="cta ghost" href="/ebook/{S8}/">Read the latest chapter',
     f'<a class="cta ghost" href="/ebook/{S9}/">Read the latest chapter')
])

# 6. Home ES
edit(os.path.join(B, "src", "pages", "es", "index.astro"), [
    (f'<a class="cta ghost" href="/es/ebook/{S8}/">Leer el último capítulo',
     f'<a class="cta ghost" href="/es/ebook/{S9}/">Leer el último capítulo')
])

# 7. scripts/generate-pdf.mjs
edit(os.path.join(B, "scripts", "generate-pdf.mjs"), [
    (f"'/ebook/{S8}/'],", f"'/ebook/{S8}/', '/ebook/{S9}/'],"),
    (f"'/es/ebook/{S8}/'],", f"'/es/ebook/{S8}/', '/es/ebook/{S9}/'],"),
])

print("ALL INDEXES, NAVIGATION, HOME AND PDF ROUTES SUCCESSFULLY UPDATED!")

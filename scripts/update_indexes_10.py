import os

B = r"D:\Proyectos personales\personal branding\living_book_astro"
S10 = "10-from-factory-floor-to-code"
S9 = "09-engineering-excellence-as-a-product-decision"

DEK_EN = "How work gets organized to produce with quality, how it adapts when we don&#x27;t yet know the solution, and how we know the result serves the customer once it arrives."
DEK_ES = "Cómo se organiza el trabajo para producir con calidad, cómo se adapta cuando todavía no conocemos la solución, y cómo sabemos que el resultado sirve una vez que llega al cliente."

def edit(path, pairs):
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    for old, new in pairs:
        assert s.count(old) == 1, f"Pattern count != 1 ({s.count(old)}) in {path}:\n{old[:120]}"
        s = s.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("ok", path)

# 1. Unlock Chapter 9 -> 10
edit(os.path.join(B, "src", "content", "ebook", f"{S9}.mdx"), [
    ('<div class="next locked" aria-disabled="true"><div class="dir">Next chapter &rarr;</div><div class="ctitle">10 — Agents, Automation and the New Production Line &mdash; in development</div></div>',
     f'<a class="next" href="/ebook/{S10}/"><div class="dir">Next chapter &rarr;</div><div class="ctitle">10 — From the Factory Floor to Code</div></a>')
])

edit(os.path.join(B, "src", "pages", "es", "ebook", S9, "index.astro"), [
    ('<div class="next locked" aria-disabled="true"><div class="dir">Siguiente capítulo &rarr;</div><div class="ctitle">10 — Agentes, automatización y la nueva línea de producción &mdash; en desarrollo</div></div>',
     f'<a class="next" href="/es/ebook/{S10}/"><div class="dir">Siguiente capítulo &rarr;</div><div class="ctitle">10 — De la fábrica al código</div></a>')
])

# 2. EN Index
card_9_en = f'''<article class="chapcard">
      <img class="bg-img" src="/assets/chapter-09-expectation-workshop.jpg" alt="Chapter 9 hero">
      <span class="ch-num" aria-hidden="true">09</span>
      <div class="body">
        <p class="kicker">Part III &middot; Building Digital Products &mdash; Chapter 9</p>
        <h3><a href="/ebook/{S9}/">Engineering Excellence as a Product Decision</a></h3>
        <p class="dek">How to turn a population&#x27;s expectations into engineering decisions, experiment with rigor and use evidence to improve physical products, digital products and services.</p>
        <a class="link" href="/ebook/{S9}/">Read chapter 9 &rarr;</a>
      </div>
    </article>'''

card_10_en = f'''<article class="chapcard">
      <img class="bg-img" src="/assets/chapter-10-bottle-cap-lineup.jpg" alt="Chapter 10 hero">
      <span class="ch-num" aria-hidden="true">10</span>
      <div class="body">
        <p class="kicker">Part III &middot; Building Digital Products &mdash; Chapter 10</p>
        <h3><a href="/ebook/{S10}/">From the Factory Floor to Code</a></h3>
        <p class="dek">{DEK_EN}</p>
        <a class="link" href="/ebook/{S10}/">Read chapter 10 &rarr;</a>
      </div>
    </article>'''

edit(os.path.join(B, "src", "pages", "ebook", "index.astro"), [
    ('<span class="num" aria-hidden="true">0.9</span>', '<span class="num" aria-hidden="true">0.10</span>'),
    ('Living edition 0.9 — 9 of ~20 chapters published — updated weekly', 'Living edition 0.10 — 10 of ~20 chapters published — updated weekly'),
    ('<div><b>9</b><span>CHAPTERS PUBLISHED<br>AS OF THIS EDITION</span></div>', '<div><b>10</b><span>CHAPTERS PUBLISHED<br>AS OF THIS EDITION</span></div>'),
    (f'<a href="/ebook/{S9}/">Chapter 9 of 20 (planned) &rarr;</a>', f'<a href="/ebook/{S10}/">Chapter 10 of 20 (planned) &rarr;</a>'),
    (card_9_en, card_10_en),
    ('<div class="partmeta"><b>Part III — Building Digital Products</b><span>1 of 4 published</span></div>',
     '<div class="partmeta"><b>Part III — Building Digital Products</b><span>2 of 4 published</span></div>'),
    ('<li><span class="n">10</span><span class="t locked">Agents, Automation and the New Production Line</span><span class="st">Upcoming</span></li>',
     f'<li class="published"><a href="/ebook/{S10}/"><span class="n">10</span><span class="t">From the Factory Floor to Code</span><span class="st">Published</span></a></li>'),
    ('<li><b>Edition 0.9</b> Chapter 9 published — 03 Nov 2026</li>',
     '<li><b>Edition 0.10</b> Chapter 10 published — 11 Nov 2026</li>\n        <li><b>Edition 0.9</b> Chapter 9 published — 03 Nov 2026</li>'),
    ('Download PDF &mdash; Edition 0.9', 'Download PDF &mdash; Edition 0.10'),
    ('<li><a href="#toc"><span class="n">III</span><span class="t">Building Digital Products</span><span class="st">1/4</span></a></li>',
     '<li><a href="#toc"><span class="n">III</span><span class="t">Building Digital Products</span><span class="st">2/4</span></a></li>'),
])

# 3. ES Index
card_9_es = f'''<article class="chapcard">
      <img class="bg-img" src="/assets/chapter-09-expectation-workshop.jpg" alt="Capítulo 9 hero">
      <span class="ch-num" aria-hidden="true">09</span>
      <div class="body">
        <p class="kicker">Parte III &middot; Construir Productos Digitales &mdash; Capítulo 9</p>
        <h3><a href="/es/ebook/{S9}/">La excelencia en ingeniería como decisión de producto</a></h3>
        <p class="dek">Cómo convertir las expectativas de una población en decisiones de ingeniería, experimentar con rigor y usar la evidencia para mejorar productos físicos, digitales y servicios.</p>
        <a class="link" href="/es/ebook/{S9}/">Leer el capítulo 9 &rarr;</a>
      </div>
    </article>'''

card_10_es = f'''<article class="chapcard">
      <img class="bg-img" src="/assets/chapter-10-bottle-cap-lineup.jpg" alt="Capítulo 10 hero">
      <span class="ch-num" aria-hidden="true">10</span>
      <div class="body">
        <p class="kicker">Parte III &middot; Construir Productos Digitales &mdash; Capítulo 10</p>
        <h3><a href="/es/ebook/{S10}/">De la fábrica al código</a></h3>
        <p class="dek">{DEK_ES}</p>
        <a class="link" href="/es/ebook/{S10}/">Leer el capítulo 10 &rarr;</a>
      </div>
    </article>'''

edit(os.path.join(B, "src", "pages", "es", "ebook", "index.astro"), [
    ('<span class="num" aria-hidden="true">0.9</span>', '<span class="num" aria-hidden="true">0.10</span>'),
    ('Edición viva 0.9 — 9 de ~20 capítulos publicados — se actualiza cada semana', 'Edición viva 0.10 — 10 de ~20 capítulos publicados — se actualiza cada semana'),
    ('<div><b>9</b><span>CAPÍTULOS PUBLICADOS<br>EN ESTA EDICIÓN</span></div>', '<div><b>10</b><span>CAPÍTULOS PUBLICADOS<br>EN ESTA EDICIÓN</span></div>'),
    (f'<a href="/es/ebook/{S9}/">Capítulo 9 de 20 (planeados) &rarr;</a>', f'<a href="/es/ebook/{S10}/">Capítulo 10 de 20 (planeados) &rarr;</a>'),
    (card_9_es, card_10_es),
    ('<div class="partmeta"><b>Parte III — Construir Productos Digitales</b><span>1 de 4 publicados</span></div>',
     '<div class="partmeta"><b>Parte III — Construir Productos Digitales</b><span>2 de 4 publicados</span></div>'),
    ('<li><span class="n">10</span><span class="t locked">Agentes, automatización y la nueva línea de producción</span><span class="st">Próximamente</span></li>',
     f'<li class="published"><a href="/es/ebook/{S10}/"><span class="n">10</span><span class="t">De la fábrica al código</span><span class="st">Publicado</span></a></li>'),
    ('<li><b>Edición 0.9</b> Capítulo 9 publicado — 03 nov 2026</li>',
     '<li><b>Edición 0.10</b> Capítulo 10 publicado — 11 nov 2026</li>\n        <li><b>Edición 0.9</b> Capítulo 9 publicado — 03 nov 2026</li>'),
    ('Descargar PDF &mdash; Edición 0.9', 'Descargar PDF &mdash; Edición 0.10'),
    ('<li><a href="#toc"><span class="n">III</span><span class="t">Construir Productos Digitales</span><span class="st">1/4</span></a></li>',
     '<li><a href="#toc"><span class="n">III</span><span class="t">Construir Productos Digitales</span><span class="st">2/4</span></a></li>'),
])

# 4. Home EN
edit(os.path.join(B, "src", "pages", "index.astro"), [
    (f'<a class="cta ghost" href="/ebook/{S9}/">Read the latest chapter',
     f'<a class="cta ghost" href="/ebook/{S10}/">Read the latest chapter')
])

# 5. Home ES
edit(os.path.join(B, "src", "pages", "es", "index.astro"), [
    (f'<a class="cta ghost" href="/es/ebook/{S9}/">Leer el último capítulo',
     f'<a class="cta ghost" href="/es/ebook/{S10}/">Leer el último capítulo')
])

# 6. scripts/generate-pdf.mjs
edit(os.path.join(B, "scripts", "generate-pdf.mjs"), [
    (f"'/ebook/{S9}/'],", f"'/ebook/{S9}/', '/ebook/{S10}/'],"),
    (f"'/es/ebook/{S9}/'],", f"'/es/ebook/{S9}/', '/es/ebook/{S10}/'],"),
])

print("ALL INDEXES, NAVIGATION, HOME AND PDF ROUTES SUCCESSFULLY UPDATED FOR CHAPTER 10!")

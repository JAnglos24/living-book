import re

B = r"D:\Proyectos personales\personal branding\living_book_astro\src\\"
S8 = "08-what-breaks-when-you-scale-a-product"
S7 = "07-interfaces-as-tolerances"
DEK_EN = "Growth changes the conditions under which a product creates value. The product owner&#x27;s job is to recognize what must be transformed and what deserves to remain."
DEK_ES = "Crecer cambia las condiciones bajo las que un producto crea valor. La tarea del dueño de producto consiste en reconocer qué debe transformarse y qué merece permanecer."


def edit(path, pairs):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:80], s.count(old))
        s = s.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("ok", path.split("src")[-1])


def card(lang):
    en = lang == "en"
    p = "" if en else "/es"
    return f'''    <article class="chapcard">
      <img class="bg-img" src="/assets/chapter-08-promise-short-series.jpg" alt="{'Chapter 8 hero' if en else 'Capítulo 8 hero'}">
      <span class="ch-num" aria-hidden="true">08</span>
      <div class="body">
        <p class="kicker">{'Part II &middot; From Physical to Digital &mdash; Chapter 8' if en else 'Parte II &middot; De lo Físico a lo Digital &mdash; Capítulo 8'}</p>
        <h3><a href="{p}/ebook/{S8}/">{'What Breaks When You Scale a Product' if en else 'Qué se rompe al escalar un producto'}</a></h3>
        <p class="dek">{DEK_EN if en else DEK_ES}</p>
        <a class="link" href="{p}/ebook/{S8}/">{'Read chapter 8' if en else 'Leer el capítulo 8'} &rarr;</a>
      </div>
    </article>'''


def old_card(lang):
    en = lang == "en"
    p = "" if en else "/es"
    dek7 = ("An interface takes shape within the limits of materials, processes, device, context, business and person. Designing means recognizing those limits, measuring them, and deciding who absorbs the effort when we exceed them."
            if en else "La interfaz toma forma dentro de lo que permiten materiales, procesos, dispositivo, contexto, negocio y persona. Diseñar exige reconocer esos límites, medirlos y decidir quién absorbe el esfuerzo cuando los sobrepasamos.")
    return f'''    <article class="chapcard">
      <img class="bg-img" src="/assets/chapter-07-hero.jpg" alt="{'Chapter 7 hero' if en else 'Capítulo 7 hero'}">
      <span class="ch-num" aria-hidden="true">07</span>
      <div class="body">
        <p class="kicker">{'Part II &middot; From Physical to Digital &mdash; Chapter 7' if en else 'Parte II &middot; De lo Físico a lo Digital &mdash; Capítulo 7'}</p>
        <h3><a href="{p}/ebook/{S7}/">{'Interfaces as Tolerances' if en else 'Interfaces como tolerancias'}</a></h3>
        <p class="dek">{dek7}</p>
        <a class="link" href="{p}/ebook/{S7}/">{'Read chapter 7' if en else 'Leer el capítulo 7'} &rarr;</a>
      </div>
    </article>'''


# ---- EN index
edit(B + r"pages\ebook\index.astro", [
    ('<span class="num" aria-hidden="true">0.7</span>', '<span class="num" aria-hidden="true">0.8</span>'),
    ("Living edition 0.7 — 7 of ~20 chapters published", "Living edition 0.8 — 8 of ~20 chapters published"),
    (f'<a href="/ebook/{S7}/">Chapter 7 of 20 (planned) &rarr;</a>', f'<a href="/ebook/{S8}/">Chapter 8 of 20 (planned) &rarr;</a>'),
    (old_card("en"), card("en")),
    ("<span>3 of 4 published</span>", "<span>4 of 4 published</span>"),
    ('<li><span class="n">08</span><span class="t locked">What Breaks When You Scale a Product</span><span class="st">Upcoming</span></li>',
     f'<li class="published"><a href="/ebook/{S8}/"><span class="n">08</span><span class="t">What Breaks When You Scale a Product</span><span class="st">Published</span></a></li>'),
    ("<li><b>Edition 0.7</b> Chapter 7 published — 19 Oct 2026</li>",
     "<li><b>Edition 0.8</b> Chapter 8 published — 27 Oct 2026</li>\n        <li><b>Edition 0.7</b> Chapter 7 published — 19 Oct 2026</li>"),
    ("Download PDF &mdash; Edition 0.7", "Download PDF &mdash; Edition 0.8"),
])

# ---- ES index (ademas corrige el cap. 7, que aparecia como "Proximamente" estando publicado)
edit(B + r"pages\es\ebook\index.astro", [
    ('<span class="num" aria-hidden="true">0.7</span>', '<span class="num" aria-hidden="true">0.8</span>'),
    ("Edición viva 0.7 — 7 de ~20 capítulos publicados", "Edición viva 0.8 — 8 de ~20 capítulos publicados"),
    (f'<a href="/es/ebook/{S7}/">Capítulo 7 de 20 (planeados) &rarr;</a>', f'<a href="/es/ebook/{S8}/">Capítulo 8 de 20 (planeados) &rarr;</a>'),
    (old_card("es"), card("es")),
    ("<span>3 de 4 publicados</span>", "<span>4 de 4 publicados</span>"),
    ('<li><span class="n">07</span><span class="t locked">Las interfaces como tolerancias</span><span class="st">Próximamente</span></li>',
     f'<li class="published"><a href="/es/ebook/{S7}/"><span class="n">07</span><span class="t">Interfaces como tolerancias</span><span class="st">Publicado</span></a></li>'),
    ('<li><span class="n">08</span><span class="t locked">Qué se rompe al escalar un producto</span><span class="st">Próximamente</span></li>',
     f'<li class="published"><a href="/es/ebook/{S8}/"><span class="n">08</span><span class="t">Qué se rompe al escalar un producto</span><span class="st">Publicado</span></a></li>'),
    ("<li><b>Edición 0.7</b> Capítulo 7 publicado — 19 oct 2026</li>",
     "<li><b>Edición 0.8</b> Capítulo 8 publicado — 27 oct 2026</li>\n        <li><b>Edición 0.7</b> Capítulo 7 publicado — 19 oct 2026</li>"),
    ("Descargar PDF &mdash; Edición 0.7", "Descargar PDF &mdash; Edición 0.8"),
])

# ---- navegacion del cap. 7 -> 8
edit(B + r"content\ebook\07-interfaces-as-tolerances.mdx", [(
    '''    <div class="next locked" aria-disabled="true">
      <div class="dir">Next chapter &rarr;</div>
      <div class="ctitle">08 — What Breaks When You Scale a Product &mdash; in development</div>
    </div>''',
    f'''    <a class="next" href="/ebook/{S8}/">
      <div class="dir">Next chapter &rarr;</div>
      <div class="ctitle">08 — What Breaks When You Scale a Product</div>
    </a>''')])
edit(B + r"pages\es\ebook\07-interfaces-as-tolerances\index.astro", [(
    '''      <div class="next locked" aria-disabled="true">
        <div class="dir">Siguiente capítulo &rarr;</div>
        <div class="ctitle">08 — Qué se rompe cuando escalas un producto &mdash; en desarrollo</div>
      </div>''',
    f'''      <a class="next" href="/es/ebook/{S8}/">
        <div class="dir">Siguiente capítulo &rarr;</div>
        <div class="ctitle">08 — Qué se rompe al escalar un producto</div>
      </a>''')])

# ---- PDF
edit(r"D:\Proyectos personales\personal branding\living_book_astro\scripts\generate-pdf.mjs", [
    (f"'/ebook/{S7}/'],", f"'/ebook/{S7}/', '/ebook/{S8}/'],"),
    (f"'/es/ebook/{S7}/'],", f"'/es/ebook/{S7}/', '/es/ebook/{S8}/'],"),
])

# ---- EN home: "ultimo capitulo"
edit(B + r"pages\index.astro", [(f'/ebook/{S7}/', f'/ebook/{S8}/')])

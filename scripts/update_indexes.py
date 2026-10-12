import os

EN_INDEX = r"D:\Proyectos personales\personal branding\living_book_astro\src\pages\ebook\index.astro"
ES_INDEX = r"D:\Proyectos personales\personal branding\living_book_astro\src\pages\es\ebook\index.astro"

# Update EN
with open(EN_INDEX, 'r', encoding='utf-8') as f:
    en = f.read()

en = en.replace(
    'Living edition 0.5 — 5 of ~20 chapters published',
    'Living edition 0.6 — 6 of ~20 chapters published'
)
en = en.replace(
    '<div><b>5</b><span>CHAPTERS PUBLISHED<br>AS OF THIS EDITION</span></div>',
    '<div><b>6</b><span>CHAPTERS PUBLISHED<br>AS OF THIS EDITION</span></div>'
)
en = en.replace(
    '<a href="/ebook/05-digital-materials-apis-data-and-constraints/">Chapter 5 of 20 (planned) &rarr;</a>',
    '<a href="/ebook/06-designing-for-maintenance-not-just-launch/">Chapter 6 of 20 (planned) &rarr;</a>'
)
en = en.replace(
    '''    <article class="chapcard">
      <img class="bg-img" src="/assets/chapter-05-cobalt-flask-table.jpg" alt="Chapter 5 hero - Cobalt flask">
      <span class="ch-num" aria-hidden="true">05</span>
      <div class="body">
        <p class="kicker">Part II &middot; From Physical to Digital &mdash; Chapter 5</p>
        <h3><a href="/ebook/05-digital-materials-apis-data-and-constraints/">Digital Materials: APIs, Data and Constraints</a></h3>
        <p class="dek">A vacuum flask reveals how materials shape a product. A marketplace hides decisions of the same kind. Behind a product page sit inventory feeds, payment services, and data copied from one system to the next.</p>
        <a class="link" href="/ebook/05-digital-materials-apis-data-and-constraints/">Read chapter 5 &rarr;</a>
      </div>
    </article>''',
    '''    <article class="chapcard">
      <img class="bg-img" src="/assets/chapter-05-cobalt-flask-table.jpg" alt="Chapter 6 hero">
      <span class="ch-num" aria-hidden="true">06</span>
      <div class="body">
        <p class="kicker">Part II &middot; From Physical to Digital &mdash; Chapter 6</p>
        <h3><a href="/ebook/06-designing-for-maintenance-not-just-launch/">Designing for Maintenance, Not Just Launch</a></h3>
        <p class="dek">A product has to keep being useful after its debut. Designing its maintenance means anticipating wear, growth, costs and conditions of use that launch barely lets us see.</p>
        <a class="link" href="/ebook/06-designing-for-maintenance-not-just-launch/">Read chapter 6 &rarr;</a>
      </div>
    </article>'''
)
# Fix 04 typo in Part I
en = en.replace(
    '<li class="published"><a href="/ebook/05-digital-materials-apis-data-and-constraints/"><span class="n">05</span><span class="t">The Product Is Never Just the Object</span><span class="st">Published</span></a></li>',
    '<li class="published"><a href="/ebook/04-the-product-is-never-just-the-object/"><span class="n">04</span><span class="t">The Product Is Never Just the Object</span><span class="st">Published</span></a></li>'
)
# Part II 2 of 4
en = en.replace(
    '<div class="partmeta"><b>Part II — From Physical to Digital</b><span>1 of 4 published</span></div>',
    '<div class="partmeta"><b>Part II — From Physical to Digital</b><span>2 of 4 published</span></div>',
    1
)
en = en.replace(
    '<li><span class="n">06</span><span class="t locked">Designing for Maintenance, Not Just Launch</span><span class="st">Upcoming</span></li>',
    '<li class="published"><a href="/ebook/06-designing-for-maintenance-not-just-launch/"><span class="n">06</span><span class="t">Designing for Maintenance, Not Just Launch</span><span class="st">Published</span></a></li>'
)
en = en.replace(
    '<ul>\n        <li><b>Edition 0.4</b>',
    '<ul>\n        <li><b>Edition 0.6</b> Chapter 6 published — 12 Oct 2026</li>\n        <li><b>Edition 0.5</b> Chapter 5 published — 05 Oct 2026</li>\n        <li><b>Edition 0.4</b>'
)
en = en.replace(
    'Download PDF &mdash; Edition 0.4',
    'Download PDF &mdash; Edition 0.6'
)

with open(EN_INDEX, 'w', encoding='utf-8') as f:
    f.write(en)
print("Updated EN index.astro")


# Update ES
with open(ES_INDEX, 'r', encoding='utf-8') as f:
    es = f.read()

es = es.replace(
    'Edición viva 0.5 — 5 de ~20 capítulos publicados',
    'Edición viva 0.6 — 6 de ~20 capítulos publicados'
)
es = es.replace(
    '<div><b>5</b><span>CAPÍTULOS PUBLICADOS<br>EN ESTA EDICIÓN</span></div>',
    '<div><b>6</b><span>CAPÍTULOS PUBLICADOS<br>EN ESTA EDICIÓN</span></div>'
)
es = es.replace(
    '<a href="/es/ebook/05-digital-materials-apis-data-and-constraints/">Capítulo 5 de 20 (planeados) &rarr;</a>',
    '<a href="/es/ebook/06-designing-for-maintenance-not-just-launch/">Capítulo 6 de 20 (planeados) &rarr;</a>'
)
es = es.replace(
    '''    <article class="chapcard">
      <img class="bg-img" src="/assets/chapter-05-cobalt-flask-table.jpg" alt="Capítulo 5 - termo cobalto">
      <span class="ch-num" aria-hidden="true">05</span>
      <div class="body">
        <p class="kicker">Parte II &middot; De lo Físico a lo Digital &mdash; Capítulo 5</p>
        <h3><a href="/es/ebook/05-digital-materials-apis-data-and-constraints/">Materiales digitales: APIs, datos y restricciones</a></h3>
        <p class="dek">Un termo revela cómo los materiales dan forma a un producto. Un marketplace esconde decisiones similares. Detrás de una página de producto hay inventarios, pagos y datos copiados de un sistema a otro.</p>
        <a class="link" href="/es/ebook/05-digital-materials-apis-data-and-constraints/">Leer el capítulo 5 &rarr;</a>
      </div>
    </article>''',
    '''    <article class="chapcard">
      <img class="bg-img" src="/assets/chapter-05-cobalt-flask-table.jpg" alt="Capítulo 6 hero">
      <span class="ch-num" aria-hidden="true">06</span>
      <div class="body">
        <p class="kicker">Parte II &middot; De lo Físico a lo Digital &mdash; Capítulo 5</p>
        <h3><a href="/es/ebook/06-designing-for-maintenance-not-just-launch/">Diseñar para el mantenimiento, no solo para el lanzamiento</a></h3>
        <p class="dek">Un producto necesita seguir siendo útil después de estrenarse. Diseñar su mantenimiento exige anticipar desgaste, crecimiento, costos y condiciones de uso que el lanzamiento apenas deja ver.</p>
        <a class="link" href="/es/ebook/06-designing-for-maintenance-not-just-launch/">Leer el capítulo 6 &rarr;</a>
      </div>
    </article>'''
)
es = es.replace(
    '<div class="partmeta"><b>Parte II — De lo Físico a lo Digital</b><span>1 de 4 publicados</span></div>',
    '<div class="partmeta"><b>Parte II — De lo Físico a lo Digital</b><span>2 de 4 publicados</span></div>',
    1
)
es = es.replace(
    '<li><span class="n">06</span><span class="t locked">Diseñar para el mantenimiento, no solo para el lanzamiento</span><span class="st">Próximamente</span></li>',
    '<li class="published"><a href="/es/ebook/06-designing-for-maintenance-not-just-launch/"><span class="n">06</span><span class="t">Diseñar para el mantenimiento, no solo para el lanzamiento</span><span class="st">Publicado</span></a></li>'
)
es = es.replace(
    '<ul>\n        <li><b>Edición 0.4</b>',
    '<ul>\n        <li><b>Edición 0.6</b> Capítulo 6 publicado — 12 oct 2026</li>\n        <li><b>Edición 0.5</b> Capítulo 5 publicado — 05 oct 2026</li>\n        <li><b>Edición 0.4</b>'
)
es = es.replace(
    'Descargar PDF &mdash; Edición 0.4',
    'Descargar PDF &mdash; Edición 0.6'
)

with open(ES_INDEX, 'w', encoding='utf-8') as f:
    f.write(es)
print("Updated ES index.astro")

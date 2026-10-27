"""Home EN = home EN anterior + lo nuevo de la v4. Las lineas 'equal' entre la home ES anterior y la v4 se toman de la EN
(ambas homes son paralelas linea a linea); las insertadas por la v4 se traducen con TR."""
import difflib
import re

ROOT = r"D:\Proyectos personales\personal branding"
OLD_ES = ROOT + r"\es_index_pre_v4.astro.bak"
OLD_EN = ROOT + r"\index_en_pre_v4.astro.bak"
V4_ES = ROOT + r"\living_book_astro\src\pages\es\index.astro"
DEST = ROOT + r"\living_book_astro\src\pages\index.astro"


def rd(p):
    return open(p, encoding="utf-8", newline=None).read().split("\n")


a, en, b = rd(OLD_ES), rd(OLD_EN), rd(V4_ES)
assert len(a) == len(en), (len(a), len(en))

# (ES, EN) — solo texto visible/aria de lo que agrego la v4
TR = [
    ("Conoce +", "Discover +"),
    ("↻ Ver el film", "↻ Watch the film"),
    ("Activar el sonido del film", "Turn the film sound on"),
    ("Sonido: apagado", "Sound: off"),
    ("Sonido: activo", "Sound: on"),
    ("Silenciar el film", "Mute the film"),
    ("Saltar la animación de apertura", "Skip the opening animation"),
    ("Saltar ▸", "Skip ▸"),
    ("<!-- ========== 02 LO QUE HAGO ========== -->", "<!-- ========== 02 WHAT I DO ========== -->"),
    ("<!-- ========== 03 CARTA DEL AUTOR ========== -->", "<!-- ========== 03 AUTHOR'S LETTER ========== -->"),
    ('>Lo que hago<', '>What I do<'),
    ("Cuatro formas de hacer que algo importe.", "Four ways to make something matter."),
    ("Dirijo portafolios y diseño producto con una sola pregunta: ¿qué siente la persona del otro lado?",
     "I lead portfolios and design product around one question: what does the person on the other side feel?"),
    (">Portafolio<", ">Portfolio<"),
    ("Dirigir portafolios", "Leading portfolios"),
    ("Convierto una lista de iniciativas en un portafolio que se entiende, se prioriza y se defiende ante cualquier comité.",
     "I turn a list of initiatives into a portfolio that can be understood, prioritized and defended before any committee."),
    ("Leer el capítulo 3", "Read chapter 3"),
    (">Producto<", ">Product<"),
    ("Diseñar producto", "Designing product"),
    ("Acompaño una idea desde el primer boceto hasta que escala, con la disciplina del diseño industrial aplicada a lo digital.",
     "I accompany an idea from the first sketch until it scales, with the discipline of industrial design applied to the digital."),
    ("Leer el capítulo 1", "Read chapter 1"),
    (">Sentir<", ">Feel<"),
    ("Hacer que se sienta", "Making it felt"),
    ("Marca, experiencia de uso y marketing al servicio de lo que nadie ve en una hoja de especificaciones: lo que se siente al tocarlo.",
     "Brand, user experience and marketing in service of what nobody sees on a spec sheet: what it feels like to touch it."),
    ("Leer el capítulo 4", "Read chapter 4"),
    (">Influir<", ">Influence<"),
    ("Liderar sin imponer", "Leading without imposing"),
    ("Equipos en árbol horizontal con cruces de matriz: cada rama tiene dueño y lo mejor ocurre donde se encuentran.",
     "Horizontal tree teams with matrix crossings: every branch has an owner and the best happens where they meet."),
    ("Conocer mi trayectoria", "Learn about my path"),
    ("Priorizar<br>Equilibrar<br>Defender", "Prioritize<br>Balance<br>Defend"),
    ("Idea<br>Diseño<br>Desarrollo<br>Escala", "Idea<br>Design<br>Development<br>Scale"),
    ("“Loewy no vendía acero, vidrio ni papel.”", "“Loewy wasn't selling steel, glass, or paper.”"),
    ("Capítulo 4 · El libro vivo", "Chapter 4 · The living book"),
    ("Marca<br>Experiencia<br>Marketing", "Brand<br>Experience<br>Marketing"),
    (">Diseño</text>", ">Design</text>"),
    (">Personas</text>", ">People</text>"),
    ("Persuadir<br>Invitar<br>Cuidar", "Persuade<br>Invite<br>Care"),
    ("Carta del autor", "Author's letter"),
    ("México<br>Octubre 2026", "Mexico<br>October 2026"),
    ("Mi cargo dice que administro. Lo que me mueve es otra cosa: el diseño, la experiencia de quien usa lo que hacemos, la forma en que una idea bien contada cambia a una persona. No mando: invito. Si algo se hace bien, <em>se siente</em>.",
     "My title says I administer. What moves me is something else: design, the experience of whoever uses what we make, the way a well-told idea changes a person. I don't command: I invite. If something is done well, <em>it is felt</em>."),
    ("Director de Gestión de Producto · Senior Portfolio Manager", "Senior Portfolio Manager · Product Management Director"),
    ('href="/es/ebook/03-', 'href="/ebook/03-'),
    ('href="/es/ebook/01-', 'href="/ebook/01-'),
    ('href="/es/ebook/04-', 'href="/ebook/04-'),
    ('href="/es/author/"', 'href="/author/"'),
]


def tr(line):
    for es, e in TR:
        line = line.replace(es, e)
    return line


out = []
for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if t == "equal":
        out += en[i1:i2]
    elif t == "insert":
        out += [tr(x) for x in b[j1:j2]]
    elif t == "replace" and (i2 - i1) == 1 and (j2 - j1) == 1:
        out += en[i1:i2]  # p.ej. el enlace "ultimo capitulo": la EN ya apunta al cap. 8
    elif t == "replace":  # <script> -> bloque del film + <script is:inline>
        out += [tr(x) for x in b[j1:j2]]
    else:
        raise SystemExit(f"opcode inesperado {t} {i1}-{i2}")

s = "\n".join(out)
# lo que quede en espanol dentro de lo insertado delata una traduccion faltante
ins_es = [l for l in s.split("\n") if re.search(r"Lo que hago|Carta del autor|Saltar|Sonido|Conoce|Ver el film|Dirigir|Portafolio", l)]
assert not ins_es, ins_es[:3]
open(DEST, "w", encoding="utf-8").write(s)
print("home EN v4 ->", DEST, len(s))

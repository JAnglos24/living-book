import os
import re
import shutil

ROOT = r"D:\Proyectos personales\personal branding"
V4 = os.path.join(ROOT, "propuesta_v4_revista")
SITE = os.path.join(ROOT, "living_book_astro")
DEST = os.path.join(SITE, "src", "pages", "es", "index.astro")
FILM_DIR = os.path.join(SITE, "public", "assets", "film")
os.makedirs(FILM_DIR, exist_ok=True)

# respaldo de la home aprobada anterior (una sola vez)
bak = os.path.join(ROOT, "es_index_pre_v4.astro.bak")
if not os.path.exists(bak):
    shutil.copy(DEST, bak)

for fn in ("film.css", "film.js", "gsap.min.js", "film_audio.m4a"):
    shutil.copy(os.path.join(V4, "assets", fn), os.path.join(FILM_DIR, fn))

with open(os.path.join(V4, "index.html"), encoding="utf-8") as f:
    s = f.read()
with open(bak, encoding="utf-8") as f:
    old = f.read()

# --- cabecera: se conserva la de la home aprobada (title, description, SeoHead)
old_title = re.search(r"<title>.*?</title>", old, re.S).group(0)
s = re.sub(r"<title>.*?</title>", lambda m: old_title, s, count=1, flags=re.S)
s = s.replace('<link rel="preload" as="image" href="assets/jas-warm.webp" type="image/webp">\n<link rel="stylesheet" href="fonts/fonts.css">',
              '<link rel="preload" as="image" href="/assets/jas-warm.webp" type="image/webp">\n<link rel="preload" href="/fonts/Archivo-normal.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="stylesheet" href="/fonts/fonts.css">')
s = s.replace('<link rel="stylesheet" href="assets/film.css">\n<meta name="robots" content="noindex">',
              '<link rel="stylesheet" href="/assets/film/film.css">\n<SeoHead />')

# --- rutas
s = s.replace('src="assets/film_audio.m4a"', 'src="/assets/film/film_audio.m4a"')
s = s.replace('<script src="assets/gsap.min.js"></script>', '<script is:inline src="/assets/film/gsap.min.js"></script>')
s = s.replace('<script src="assets/film.js"></script>', '<script is:inline src="/assets/film/film.js"></script>')
s = re.sub(r'(src|href)="assets/', r'\1="/assets/', s)
s = s.replace("https://www.jasosal.com/", "/")
s = s.replace("/es/ebook/07-interfaces-as-tolerances/", "/es/ebook/08-what-breaks-when-you-scale-a-product/")
# scripts inline restantes: se mantienen tal cual (clasicos, sin bundling)
s = re.sub(r"<script>", "<script is:inline>", s)

# --- frontmatter de Astro
s = "---\nimport SeoHead from '../../components/SeoHead.astro';\n---\n" + s
assert "noindex" not in s and "Propuesta v4" not in s and "assets/film.js" not in s
with open(DEST, "w", encoding="utf-8") as f:
    f.write(s)
print("home ES v4 ->", DEST, len(s))

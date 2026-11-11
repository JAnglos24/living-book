import os
import re
from PIL import Image

SRC_DIR = r"D:\Proyectos personales\personal branding\Living book\Chapter10\Assets"
SITE_DIR = r"D:\Proyectos personales\personal branding\living_book_astro"
PUB_DIR = os.path.join(SITE_DIR, "public", "assets")
EN_MDX = os.path.join(SITE_DIR, "src", "content", "ebook", "10-from-factory-floor-to-code.mdx")
ES_ASTRO = os.path.join(SITE_DIR, "src", "pages", "es", "ebook", "10-from-factory-floor-to-code", "index.astro")

mapping = {
    'fig10_1.jpg': 'chapter-10-bottle-cap-lineup.jpg',
    'fig10_2.jpg': 'chapter-10-leak-test-stopwatch.jpg',
    'fig10_3.png': 'chapter-10-caps-corridor.jpg',
    'fig10_4.jpg': 'chapter-10-gauge-gasket.jpg',
    'fig10_5.png': 'chapter-10-cap-mechanism-transparent.png',
    'fig10_6.jpg': 'chapter-10-sprint-board.jpg',
    'fig10_7.jpg': 'chapter-10-pilot-packaging.jpg',
    'fig10_8.jpg': 'chapter-10-branch-string-board.jpg',
    'fig10_9.jpg': 'chapter-10-pass-fail-lamp.jpg',
    'fig10_10.jpg': 'chapter-10-bottle-queue-adapter.jpg',
    'fig10_11.jpg': 'chapter-10-duplicate-receipts.jpg',
    'fig10_13.png': 'chapter-10-focus-group-table.jpg',
    'fig10_15.jpg': 'chapter-10-budget-ledger.jpg',
    'fig10_16.jpg': 'chapter-10-cap-mockup-row.jpg',
    'fig10_18.jpg': 'chapter-10-hand-on-mold.jpg',
}

dimensions = {}

print("=== Sincronizando Assets Curados desde Chapter10/Assets a public/assets ===")
for src_fn, pub_fn in mapping.items():
    src_fp = os.path.join(SRC_DIR, src_fn)
    pub_fp = os.path.join(PUB_DIR, pub_fn)
    
    if not os.path.exists(src_fp):
        raise FileNotFoundError(f"Missing source asset: {src_fp}")
        
    im = Image.open(src_fp)
    w, h = im.size
    dimensions[pub_fn] = (w, h)
    
    if pub_fn.endswith(".png"):
        im.save(pub_fp, "PNG", optimize=True)
    else:
        im = im.convert("RGB")
        im.save(pub_fp, "JPEG", quality=88, progressive=True)
        
    print(f"-> {pub_fn}: {w}x{h} ({os.path.getsize(pub_fp):,} bytes)")

print("\n=== Actualizando dimensiones en EN MDX y ES Astro ===")
def update_file_dims(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    def repl(m):
        tag = m.group(0)
        src_m = re.search(r'src="/assets/([^"]+)"', tag)
        if src_m:
            fn = src_m.group(1)
            if fn in dimensions:
                w, h = dimensions[fn]
                tag = re.sub(r'width="\d+"', f'width="{w}"', tag)
                tag = re.sub(r'height="\d+"', f'height="{h}"', tag)
        return tag

    new_content = re.sub(r'<img [^>]*src="/assets/chapter-10-[^>]*>', repl, content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated image tags in {os.path.basename(file_path)}")

update_file_dims(EN_MDX)
update_file_dims(ES_ASTRO)
print("\nSincronización completa con éxito.")

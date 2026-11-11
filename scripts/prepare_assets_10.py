import os
import shutil
from PIL import Image

BRAIN_SCRATCH = r"C:\Users\jasos\.gemini\antigravity\brain\7d9db109-fc2c-4b01-8d4b-6067e3a94280"
CHAPTER10_ASSETS = r"D:\Proyectos personales\personal branding\Living book\Chapter10\Assets"
PUBLIC_ASSETS = r"D:\Proyectos personales\personal branding\living_book_astro\public\assets"

os.makedirs(PUBLIC_ASSETS, exist_ok=True)

# Sources
sources = {
    "chapter-10-bottle-cap-lineup.jpg": os.path.join(CHAPTER10_ASSETS, "fig10_1.png"),
    "chapter-10-leak-test-stopwatch.jpg": os.path.join(CHAPTER10_ASSETS, "fig10_2.png"),
    "chapter-10-caps-corridor.jpg": os.path.join(CHAPTER10_ASSETS, "fig10_3.png"),
    "chapter-10-gauge-gasket.jpg": os.path.join(BRAIN_SCRATCH, "control_calidad_junta_silicon_1794415108752.jpg"),
    "chapter-10-cap-mechanism-transparent.png": os.path.join(BRAIN_SCRATCH, "scratch", "test_cap_alpha.png"),
    "chapter-10-sprint-board.jpg": os.path.join(CHAPTER10_ASSETS, "fig10_6.png"),
    "chapter-10-pilot-packaging.jpg": os.path.join(BRAIN_SCRATCH, "cajas_taller_editorial_1794415131730.jpg"),
    "chapter-10-branch-string-board.jpg": os.path.join(BRAIN_SCRATCH, "corkboard_thread_branch_loop_1794415149045.jpg"),
    "chapter-10-pass-fail-lamp.jpg": os.path.join(CHAPTER10_ASSETS, "fig10_9.png"),
    "chapter-10-bottle-queue-adapter.jpg": os.path.join(CHAPTER10_ASSETS, "fig10_10.png"),
    "chapter-10-duplicate-receipts.jpg": os.path.join(BRAIN_SCRATCH, "silent_error_editorial_desk_1794415133542.jpg"),
    "chapter-10-focus-group-table.jpg": os.path.join(CHAPTER10_ASSETS, "fig10_13.png"),
    "chapter-10-budget-ledger.jpg": os.path.join(CHAPTER10_ASSETS, "fig10_15.png"),
    "chapter-10-cap-mockup-row.jpg": os.path.join(CHAPTER10_ASSETS, "fig10_16.png"),
    "chapter-10-hand-on-mold.jpg": os.path.join(CHAPTER10_ASSETS, "fig10_18.png"),
}

# Also save missing into Chapter10 Assets as backups
shutil.copy2(sources["chapter-10-gauge-gasket.jpg"], os.path.join(CHAPTER10_ASSETS, "fig10_4.jpg"))
shutil.copy2(sources["chapter-10-pilot-packaging.jpg"], os.path.join(CHAPTER10_ASSETS, "fig10_7.jpg"))
shutil.copy2(sources["chapter-10-branch-string-board.jpg"], os.path.join(CHAPTER10_ASSETS, "fig10_8.jpg"))
shutil.copy2(sources["chapter-10-duplicate-receipts.jpg"], os.path.join(CHAPTER10_ASSETS, "fig10_11.jpg"))

for dst_name, src_file in sources.items():
    dst_path = os.path.join(PUBLIC_ASSETS, dst_name)
    im = Image.open(src_file)
    if dst_name.endswith(".png"):
        im.save(dst_path, "PNG", optimize=True)
    else:
        im = im.convert("RGB")
        im.save(dst_path, "JPEG", quality=86, progressive=True)
    print(f"Saved {dst_name}: {im.size}")

print("All 15 images processed successfully!")


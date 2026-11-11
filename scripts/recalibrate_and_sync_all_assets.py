import os
import cv2
import numpy as np
from PIL import Image

CHAPTER10_ASSETS = r"D:\Proyectos personales\personal branding\Living book\Chapter10\Assets"
SITE_ASSETS = r"D:\Proyectos personales\personal branding\living_book_astro\public\assets"
SITE_DIR = r"D:\Proyectos personales\personal branding\living_book_astro"
EN_MDX = os.path.join(SITE_DIR, "src", "content", "ebook", "10-from-factory-floor-to-code.mdx")
ES_ASTRO = os.path.join(SITE_DIR, "src", "pages", "es", "ebook", "10-from-factory-floor-to-code", "index.astro")
EN_HTML = r"D:\Proyectos personales\personal branding\Living book\Chapter10\ebook-chapter-10.html"
ES_HTML = r"D:\Proyectos personales\personal branding\Living book\Chapter10\es-ebook-chapter-10.html"

# Mapping between Chapter10/Assets and public/assets
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

# 5-Stop Cobalt LUT matching #0057D9 (Symbios Braun/Rams Cobalt Blue)
def get_cobalt_lut():
    stops_l = np.array([0.00, 0.30, 0.60, 0.85, 1.00])
    stops_bgr = np.array([
        [70.0,  20.0,   0.0],  # L=0.00: Oclusión profunda (#001446)
        [140.0, 50.0,   0.0],  # L=0.30: Terminador profundo (#00328C)
        [217.0, 87.0,   0.0],  # L=0.60: Cobalto puro oficial (#0057D9)
        [245.0, 160.0, 70.0],  # L=0.85: Cobalto iluminado (#46A0F5)
        [255.0, 248.0, 238.0], # L=1.00: Reflejo especular (#EEF8FF)
    ])
    lut = np.zeros((256, 3), dtype=np.float32)
    for i in range(256):
        l = i / 255.0
        idx = np.searchsorted(stops_l, l)
        if idx == 0:
            lut[i] = stops_bgr[0]
        elif idx >= len(stops_l):
            lut[i] = stops_bgr[-1]
        else:
            t = (l - stops_l[idx-1]) / (stops_l[idx] - stops_l[idx-1])
            lut[i] = (1 - t) * stops_bgr[idx-1] + t * stops_bgr[idx]
    return lut

COBALT_LUT = get_cobalt_lut()

def calibrate_image(src_fp, pub_fn):
    has_alpha = False
    alpha_channel = None

    if src_fp.endswith(".png"):
        im = Image.open(src_fp)
        if im.mode == "RGBA":
            has_alpha = True
            arr = np.array(im)
            alpha_channel = arr[:, :, 3]
            img_bgr = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2BGR)
        else:
            img_bgr = cv2.imread(src_fp)
    else:
        img_bgr = cv2.imread(src_fp)

    if img_bgr is None:
        raise ValueError(f"Could not read {src_fp}")

    is_receipts = "fig10_11" in src_fp or "duplicate-receipts" in pub_fn
    is_gasket = "fig10_4" in src_fp or "gauge-gasket" in pub_fn
    
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]

    # Blue range in OpenCV HSV: hue around 108 (216 degrees)
    hue_dist = np.abs(h - 108.0)
    hue_dist = np.minimum(hue_dist, 180.0 - hue_dist)
    hue_weight = np.clip(1.0 - hue_dist / 28.0, 0.0, 1.0)

    if is_receipts:
        sat_weight = np.clip((s - 95.0) / 50.0, 0.0, 1.0)
    elif is_gasket:
        sat_weight = np.clip((s - 50.0) / 35.0, 0.0, 1.0)
    else:
        sat_weight = np.clip((s - 25.0) / 40.0, 0.0, 1.0)

    val_weight = np.clip((v - 20.0) / 30.0, 0.0, 1.0)
    mask = hue_weight * sat_weight * val_weight
    area_pct = np.mean(mask > 0.15) * 100

    if area_pct > 0.05:
        l_idx = np.clip(np.max(img_bgr, axis=-1), 0, 255).astype(np.uint8)
        cobalt_bgr = COBALT_LUT[l_idx]

        if is_receipts:
            desk_blue = (hue_weight > 0.1) & (s < 95.0)
            s[desk_blue] *= 0.15
            hsv[:,:,1] = s
            neutral_bgr = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
        else:
            neutral_bgr = img_bgr.astype(np.float32)

        smooth_mask = cv2.GaussianBlur(mask, (3, 3), 0.5)
        mask_3d = np.dstack([smooth_mask, smooth_mask, smooth_mask])

        result_bgr = neutral_bgr * (1.0 - mask_3d) + cobalt_bgr * mask_3d
        result_bgr = np.clip(result_bgr, 0, 255).astype(np.uint8)

        accent_pix = result_bgr[mask > 0.3]
        if len(accent_pix) > 0:
            avg_b = np.mean(accent_pix[:, 0])
            avg_g = np.mean(accent_pix[:, 1])
            avg_r = np.mean(accent_pix[:, 2])
            hex_col = f"#{int(avg_r):02X}{int(avg_g):02X}{int(avg_b):02X}"
        else:
            hex_col = "N/A"
    else:
        result_bgr = img_bgr
        hex_col = "Neutral"

    return result_bgr, has_alpha, alpha_channel, area_pct, hex_col

print("=== RECALIBRANDO TODAS LAS IMÁGENES AL COBALTO #0057D9 ===")
final_dims = {}

for src_fn, pub_fn in mapping.items():
    src_fp = os.path.join(CHAPTER10_ASSETS, src_fn)
    pub_fp = os.path.join(SITE_ASSETS, pub_fn)

    res_bgr, has_alpha, alpha_ch, area_pct, hex_col = calibrate_image(src_fp, pub_fn)
    h, w = res_bgr.shape[:2]
    final_dims[pub_fn] = (w, h)

    # Save to public/assets
    if pub_fn.endswith(".png") and has_alpha:
        res_rgb = cv2.cvtColor(res_bgr, cv2.COLOR_BGR2RGB)
        out_arr = np.dstack([res_rgb, alpha_ch])
        Image.fromarray(out_arr).save(pub_fp, "PNG", optimize=True)
    elif pub_fn.endswith(".png"):
        res_rgb = cv2.cvtColor(res_bgr, cv2.COLOR_BGR2RGB)
        Image.fromarray(res_rgb).save(pub_fp, "PNG", optimize=True)
    else:
        res_rgb = cv2.cvtColor(res_bgr, cv2.COLOR_BGR2RGB)
        Image.fromarray(res_rgb).save(pub_fp, "JPEG", quality=90, progressive=True)

    # ALSO save to Chapter10/Assets so the local folder is 100% updated!
    if src_fn.endswith(".png") and has_alpha:
        res_rgb = cv2.cvtColor(res_bgr, cv2.COLOR_BGR2RGB)
        out_arr = np.dstack([res_rgb, alpha_ch])
        Image.fromarray(out_arr).save(src_fp, "PNG", optimize=True)
    elif src_fn.endswith(".png"):
        res_rgb = cv2.cvtColor(res_bgr, cv2.COLOR_BGR2RGB)
        Image.fromarray(res_rgb).save(src_fp, "PNG", optimize=True)
    else:
        res_rgb = cv2.cvtColor(res_bgr, cv2.COLOR_BGR2RGB)
        Image.fromarray(res_rgb).save(src_fp, "JPEG", quality=90, progressive=True)

    print(f"[{src_fn} -> {pub_fn}] Blue area: {area_pct:5.2f}% | Hex: {hex_col} | Size: {w}x{h}")

print("\n=== ACTUALIZANDO MDX, ASTRO Y HTML CON CACHE-BUSTER ?v=cobalt ===")
import re

def update_tags(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    def repl(m):
        tag = m.group(0)
        src_m = re.search(r'src="(/assets/[^"?]+)(?:\?[^"]*)?"', tag)
        if src_m:
            base_url = src_m.group(1)
            fn = os.path.basename(base_url)
            # Add or update ?v=cobalt
            new_src = f'{base_url}?v=cobalt'
            tag = re.sub(r'src="[^"]+"', f'src="{new_src}"', tag)
            if fn in final_dims:
                w, h = final_dims[fn]
                tag = re.sub(r'width="\d+"', f'width="{w}"', tag)
                tag = re.sub(r'height="\d+"', f'height="{h}"', tag)
        return tag

    new_content = re.sub(r'<img [^>]*src="(/assets/chapter-10-[^">]+)"[^>]*>', repl, content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated {os.path.basename(file_path)}")

update_tags(EN_MDX)
update_tags(ES_ASTRO)
update_tags(EN_HTML)
update_tags(ES_HTML)

print("\n¡Calibración cromática y sincronización completa!")

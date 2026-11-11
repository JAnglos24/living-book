import os
import shutil
import cv2
import numpy as np
from PIL import Image

SITE_ASSETS = r"D:\Proyectos personales\personal branding\living_book_astro\public\assets"
BACKUP_DIR = os.path.join(SITE_ASSETS, "backup_pre_cobalt")
os.makedirs(BACKUP_DIR, exist_ok=True)

# 5-Stop Cobalt LUT matching #0057D9 (Braun/Rams Cobalt Blue)
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

def process_image(fp, fn):
    # Backup original first if not already backed up
    backup_path = os.path.join(BACKUP_DIR, fn)
    if not os.path.exists(backup_path):
        shutil.copy2(fp, backup_path)
    read_path = backup_path

    has_alpha = False
    alpha_channel = None

    if fn.endswith(".png"):
        im = Image.open(read_path)
        if im.mode == "RGBA":
            has_alpha = True
            arr = np.array(im)
            alpha_channel = arr[:, :, 3]
            img_bgr = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2BGR)
        else:
            img_bgr = cv2.imread(read_path)
    else:
        img_bgr = cv2.imread(read_path)

    if img_bgr is None:
        print(f"Skipping unreadable {fn}")
        return

    is_receipts = "duplicate-receipts" in fn
    is_gasket = "gauge-gasket" in fn
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]

    # Blue range in OpenCV HSV: hue around 108 (216 degrees)
    hue_dist = np.abs(h - 108.0)
    # Circular hue wrap around 180
    hue_dist = np.minimum(hue_dist, 180.0 - hue_dist)
    hue_weight = np.clip(1.0 - hue_dist / 28.0, 0.0, 1.0)

    if is_receipts:
        # High saturation threshold to select ONLY the severed cable, not the slate desk
        sat_weight = np.clip((s - 95.0) / 50.0, 0.0, 1.0)
    elif is_gasket:
        # Focus on the gauge sleeve and isolate from steel bench reflection
        sat_weight = np.clip((s - 50.0) / 35.0, 0.0, 1.0)
    else:
        sat_weight = np.clip((s - 25.0) / 40.0, 0.0, 1.0)

    val_weight = np.clip((v - 20.0) / 30.0, 0.0, 1.0)
    mask = hue_weight * sat_weight * val_weight

    # Total area with blue
    area_pct = np.mean(mask > 0.15) * 100

    # If image has significant blue accent (> 0.05% area)
    if area_pct > 0.05:
        # Calculate intrinsic luminance
        l_idx = np.clip(np.max(img_bgr, axis=-1), 0, 255).astype(np.uint8)
        cobalt_bgr = COBALT_LUT[l_idx]

        # In receipts, desaturate the cold blue cast on the desk
        if is_receipts:
            desk_blue = (hue_weight > 0.1) & (s < 95.0)
            s[desk_blue] *= 0.15
            hsv[:,:,1] = s
            neutral_bgr = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
        else:
            neutral_bgr = img_bgr.astype(np.float32)

        # Smooth mask blur
        smooth_mask = cv2.GaussianBlur(mask, (3, 3), 0.5)
        mask_3d = np.dstack([smooth_mask, smooth_mask, smooth_mask])

        result_bgr = neutral_bgr * (1.0 - mask_3d) + cobalt_bgr * mask_3d
        result_bgr = np.clip(result_bgr, 0, 255).astype(np.uint8)

        # Measure new average color in accent
        accent_pix = result_bgr[mask > 0.3]
        if len(accent_pix) > 0:
            avg_b = np.mean(accent_pix[:, 0])
            avg_g = np.mean(accent_pix[:, 1])
            avg_r = np.mean(accent_pix[:, 2])
            hex_col = f"#{int(avg_r):02X}{int(avg_g):02X}{int(avg_b):02X}"
        else:
            hex_col = "N/A"

        # Save back
        if has_alpha:
            res_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)
            out_arr = np.dstack([res_rgb, alpha_channel])
            Image.fromarray(out_arr).save(fp, "PNG", optimize=True)
        else:
            res_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)
            Image.fromarray(res_rgb).save(fp, "JPEG", quality=86, progressive=True)

        print(f"CALIBRATED: {fn:40s} | Area: {area_pct:5.2f}% (<=8% rule: {area_pct<=8.0}) | New Avg Accent: {hex_col}")
    else:
        print(f"NEUTRAL:    {fn:40s} | Area: {area_pct:5.2f}% (pure atelier neutral palette)")

images = [f for f in sorted(os.listdir(SITE_ASSETS)) if f.startswith("chapter-10-") and f.endswith((".jpg", ".png"))]
for fn in images:
    fp = os.path.join(SITE_ASSETS, fn)
    process_image(fp, fn)

print("\nAll Chapter 10 images recalibrated to Symbios #0057D9 Cobalt specifications!")

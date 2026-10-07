#!/usr/bin/env python3
import os
import subprocess
import tempfile
from PIL import Image, ImageDraw

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PATH = os.path.join(PROJECT_DIR, "Screenshot 2026-10-07 at 10.59.45 AM.png")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
RES_DIR = os.path.join(PROJECT_DIR, "android", "app", "src", "main", "res")

def main():
    print("Loading image:", IMAGE_PATH)
    orig = Image.open(IMAGE_PATH).convert("RGBA")
    w, h = orig.size
    src = orig.load()

    # Isolate logo with clean anti-aliasing
    rgba = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dest = rgba.load()

    for y in range(h):
        for x in range(w):
            if 180 <= x <= 400 and 105 <= y <= 380:
                r, g, b, a = src[x, y]
                m = max(r, g, b)
                if m <= 20:
                    dest[x, y] = (0, 0, 0, 0)
                elif m >= 50:
                    dest[x, y] = (r, g, b, 255)
                else:
                    alpha = int(255 * (m - 20) / (50 - 20))
                    dest[x, y] = (r, g, b, alpha)

    bbox = rgba.getbbox()
    print("Cropped logo bbox:", bbox)
    logo_crop = rgba.crop(bbox)
    logo_w, logo_h = logo_crop.size

    def create_canvas_icon(canvas_size, logo_target_h, bg_color=None, circular=False):
        aspect = logo_w / logo_h
        target_w = int(logo_target_h * aspect)
        target_h = int(logo_target_h)
        scaled_logo = logo_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)

        if bg_color is not None:
            canvas = Image.new("RGBA", (canvas_size, canvas_size), bg_color)
        else:
            canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))

        offset_x = (canvas_size - target_w) // 2
        offset_y = (canvas_size - target_h) // 2
        canvas.alpha_composite(scaled_logo, (offset_x, offset_y))

        if circular:
            mask = Image.new("L", (canvas_size, canvas_size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, canvas_size, canvas_size), fill=255)
            final_canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
            final_canvas.paste(canvas, (0, 0), mask=mask)
            return final_canvas

        return canvas

    # 1. Generate Expo Assets
    os.makedirs(ASSETS_DIR, exist_ok=True)

    # 1024x1024 standard app icon (black background, safe zone height 512px)
    icon_1024 = create_canvas_icon(1024, 512, bg_color=(0, 0, 0, 255))
    icon_1024.save(os.path.join(ASSETS_DIR, "icon.png"), "PNG")

    # 1024x1024 adaptive icon foreground (transparent background, safe zone height 512px)
    adaptive_fg = create_canvas_icon(1024, 512, bg_color=None)
    adaptive_fg.save(os.path.join(ASSETS_DIR, "adaptive-icon.png"), "PNG")

    # 192x192 favicon
    favicon = create_canvas_icon(192, 120, bg_color=(0, 0, 0, 255), circular=True)
    favicon.save(os.path.join(ASSETS_DIR, "favicon.png"), "PNG")

    # 512x512 splash icon
    splash_icon = create_canvas_icon(512, 340, bg_color=None)
    splash_icon.save(os.path.join(ASSETS_DIR, "splash-icon.png"), "PNG")

    print("Expo assets generated in:", ASSETS_DIR)

    # 2. Generate Android native mipmap icons
    # Densities:
    # mdpi: 48x48 (logo ~34px), adaptive fg: 108x108 (logo ~54px)
    # hdpi: 72x72 (logo ~51px), adaptive fg: 162x162 (logo ~81px)
    # xhdpi: 96x96 (logo ~68px), adaptive fg: 216x216 (logo ~108px)
    # xxhdpi: 144x144 (logo ~102px), adaptive fg: 324x324 (logo ~162px)
    # xxxhdpi: 192x192 (logo ~136px), adaptive fg: 432x432 (logo ~216px)

    densities = {
        "mipmap-mdpi": {"legacy_size": 48, "legacy_logo": 34, "fg_size": 108, "fg_logo": 54},
        "mipmap-hdpi": {"legacy_size": 72, "legacy_logo": 51, "fg_size": 162, "fg_logo": 81},
        "mipmap-xhdpi": {"legacy_size": 96, "legacy_logo": 68, "fg_size": 216, "fg_logo": 108},
        "mipmap-xxhdpi": {"legacy_size": 144, "legacy_logo": 102, "fg_size": 324, "fg_logo": 162},
        "mipmap-xxxhdpi": {"legacy_size": 192, "legacy_logo": 136, "fg_size": 432, "fg_logo": 216},
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        for folder, config in densities.items():
            dest_folder = os.path.join(RES_DIR, folder)
            os.makedirs(dest_folder, exist_ok=True)

            # A. ic_launcher.webp (Square with rounded corners or full black square)
            # Full black square with centered logo
            ic_launcher = create_canvas_icon(config["legacy_size"], config["legacy_logo"], bg_color=(0, 0, 0, 255))
            tmp_png = os.path.join(tmpdir, f"{folder}_launcher.png")
            ic_launcher.save(tmp_png, "PNG")
            out_webp = os.path.join(dest_folder, "ic_launcher.webp")
            subprocess.run(["cwebp", "-lossless", tmp_png, "-o", out_webp], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # B. ic_launcher_round.webp (Circular icon)
            ic_launcher_round = create_canvas_icon(config["legacy_size"], config["legacy_logo"], bg_color=(0, 0, 0, 255), circular=True)
            tmp_round_png = os.path.join(tmpdir, f"{folder}_round.png")
            ic_launcher_round.save(tmp_round_png, "PNG")
            out_round_webp = os.path.join(dest_folder, "ic_launcher_round.webp")
            subprocess.run(["cwebp", "-lossless", tmp_round_png, "-o", out_round_webp], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # C. ic_launcher_foreground.webp (Transparent adaptive foreground)
            ic_launcher_fg = create_canvas_icon(config["fg_size"], config["fg_logo"], bg_color=None)
            tmp_fg_png = os.path.join(tmpdir, f"{folder}_fg.png")
            ic_launcher_fg.save(tmp_fg_png, "PNG")
            out_fg_webp = os.path.join(dest_folder, "ic_launcher_foreground.webp")
            subprocess.run(["cwebp", "-lossless", tmp_fg_png, "-o", out_fg_webp], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            print(f"Generated icons for {folder}: legacy={config['legacy_size']}x{config['legacy_size']}, foreground={config['fg_size']}x{config['fg_size']}")

    print("All icons successfully generated!")

if __name__ == "__main__":
    main()

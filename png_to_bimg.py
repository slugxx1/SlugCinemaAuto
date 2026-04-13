from pathlib import Path
from PIL import Image

# CC color palette
CC_COLORS = [
    ("0", (240, 240, 240)),  # white
    ("1", (242, 178, 51)),   # orange
    ("2", (229, 127, 216)),  # magenta
    ("3", (153, 178, 242)),  # light blue
    ("4", (222, 222, 108)),  # yellow
    ("5", (127, 204, 25)),   # lime
    ("6", (242, 178, 204)),  # pink
    ("7", (76, 76, 76)),     # gray
    ("8", (153, 153, 153)),  # light gray
    ("9", (76, 153, 178)),   # cyan
    ("a", (178, 102, 229)),  # purple
    ("b", (51, 102, 204)),   # blue
    ("c", (127, 102, 76)),   # brown
    ("d", (87, 166, 78)),    # green
    ("e", (204, 76, 76)),    # red
    ("f", (25, 25, 25)),     # black
]

FRAME_DIR = Path("frames")
OUT_DIR = Path("bimg")
OUT_DIR.mkdir(exist_ok=True)

def nearest_cc_color(rgb):
    r, g, b = rgb
    best_code = "f"
    best_dist = None
    for code, (cr, cg, cb) in CC_COLORS:
        dist = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2
        if best_dist is None or dist < best_dist:
            best_dist = dist
            best_code = code
    return best_code

def image_to_bimg(path: Path, out_path: Path):
    img = Image.open(path).convert("RGB")
    width, height = img.size

    rows = []
    for y in range(height):
        text = []
        fg = []
        bg = []

        for x in range(width):
            code = nearest_cc_color(img.getpixel((x, y)))
            text.append(" ")
            fg.append(code)
            bg.append(code)

        rows.append(( "".join(text), "".join(fg), "".join(bg) ))

    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("return {\n")
        for text, fg, bg in rows:
            escaped_text = text.replace("\\", "\\\\").replace('"', '\\"')
            escaped_fg = fg.replace("\\", "\\\\").replace('"', '\\"')
            escaped_bg = bg.replace("\\", "\\\\").replace('"', '\\"')
            f.write(f'    {{"{escaped_text}", "{escaped_fg}", "{escaped_bg}"}},\n')
        f.write("}\n")

def main():
    files = sorted(FRAME_DIR.glob("*.png"))
    if not files:
        raise SystemExit("No PNG frames found in ./frames")

    for file in files:
        out_file = OUT_DIR / (file.stem + ".bimg")
        image_to_bimg(file, out_file)
        print(f"Converted {file.name} -> {out_file.name}")

if __name__ == "__main__":
    main()

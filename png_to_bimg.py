from PIL import Image
import os

PALETTE = {
    "0": (240, 240, 240),
    "1": (242, 178, 51),
    "2": (229, 127, 216),
    "3": (153, 178, 242),
    "4": (222, 222, 108),
    "5": (127, 204, 25),
    "6": (242, 178, 204),
    "7": (76, 76, 76),
    "8": (153, 153, 153),
    "9": (76, 153, 178),
    "a": (178, 102, 229),
    "b": (51, 102, 204),
    "c": (127, 102, 76),
    "d": (87, 166, 78),
    "e": (204, 76, 76),
    "f": (25, 25, 25),
}

palette_items = list(PALETTE.items())

def nearest_color(rgb):
    r, g, b = rgb
    best_code = "f"
    best_dist = float("inf")
    for code, (pr, pg, pb) in palette_items:
        dist = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if dist < best_dist:
            best_dist = dist
            best_code = code
    return best_code

def lua_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

input_dir = "frames"
output_dir = "bimg"

os.makedirs(output_dir, exist_ok=True)

files = sorted(f for f in os.listdir(input_dir) if f.lower().endswith(".png"))

for filename in files:
    path = os.path.join(input_dir, filename)
    img = Image.open(path).convert("RGB")
    w, h = img.size

    rows = []
    for y in range(h):
        text = " " * w
        fg = "0" * w
        bg = "".join(nearest_color(img.getpixel((x, y))) for x in range(w))
        rows.append((text, fg, bg))

    out_name = os.path.splitext(filename)[0] + ".bimg"
    out_path = os.path.join(output_dir, out_name)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("return {\n")
        for i, (text, fg, bg) in enumerate(rows):
            comma = "," if i < len(rows) - 1 else ""
            f.write(f'  {{"{lua_escape(text)}", "{lua_escape(fg)}", "{lua_escape(bg)}"}}{comma}\n')
        f.write("}\n")

print(f"Converted {len(files)} frames.")

"""Builds the scene assets from the hill photo and the cow cut-outs.   Run: python3 src/make_wallpaper.py

    assets/hill.jpg          the clean hill (no cows): the page background
    assets/sprites/*.webp    one transparent image per cow, so the page can animate each one
    assets/sky-mask.png      sky-only mask, so the page can recolour just the sky for sunset and night
    assets/cows.json         where each cow sits, as % of the scene (used for sprites, shadows and click targets)

Hill photo: Unsplash, by Zongnan Bao. Cow photos: Wikimedia Commons (see README credits).
"""
import json, os, statistics
from PIL import Image, ImageDraw, ImageFilter
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))   # run from the repo root, wherever this is called from
os.makedirs("assets/sprites", exist_ok=True)
W, H = 2000, 1333                                   # cow positions below are in these pixels

base = Image.open("assets/hill-base.jpg").convert("RGB")
if base.size != (W, H): base = base.resize((W, H), Image.LANCZOS)
base.resize((1600, 1067), Image.LANCZOS).save("assets/hill.jpg", quality=58, optimize=True)

# ---- sky mask: everything above the hill's crest line ----
small = base.resize((800, 533), Image.LANCZOS); px = small.load(); w, h = small.size
def is_grass(p): return p[1] > p[2] + 12 and p[1] > p[0] + 8
crest = []
for x in range(w):
    y = 0
    while y < h - 6 and not (is_grass(px[x, y]) and all(is_grass(px[x, y + k]) for k in range(1, 5))): y += 1
    crest.append(y)
crest = [int(statistics.median(crest[max(0, i - 6):i + 7])) for i in range(w)]   # ignore stray bushes and specks
mask = Image.new("L", (w, h), 0); d = ImageDraw.Draw(mask)
for x, yc in enumerate(crest): d.line([(x, 0), (x, max(0, yc - 1))], fill=255)
sky = Image.new("RGBA", (w, h), (255, 255, 255, 0)); sky.putalpha(mask.filter(ImageFilter.GaussianBlur(1.2)))
sky.save("assets/sky-mask.png", optimize=True)

# ---- cows ----
def load(name, trim=None):
    im = Image.open(name).convert("RGBA")
    if trim:                                        # erase a stray second cow behind the main one
        x0, y0, x1, y1 = [int(v * s) for v, s in zip(trim, (im.width, im.height, im.width, im.height))]
        a = im.getchannel("A"); ImageDraw.Draw(a).rectangle([x0, y0, x1, y1], fill=0); im.putalpha(a)
    return im.crop(im.getchannel("A").getbbox())

def feather(im, bottom, left):                      # melt the cow's feet (and a cropped-off edge) into the grass
    a = im.getchannel("A"); px = a.load()
    for x in range(int(im.width * left)):
        k = x / (im.width * left)
        for y in range(im.height): px[x, y] = int(px[x, y] * k)
    for y in range(int(im.height * (1 - bottom)), im.height):
        k = (im.height - 1 - y) / (im.height * bottom)
        for x in range(im.width): px[x, y] = int(px[x, y] * k)
    im.putalpha(a); return im

# name: (cut-out, height, left x, y of the feet, trim, bottom feather, left feather)   -- pixels in the 2000x1333 scene
# Spread across the field: near cow on the left, far cows in the middle, a nearer one on the right.
COWS = {
    "A": ("cutA.png", 340, 125, 1262, None, .06, 0),                 # big front-on cow, nearest (About)
    "E": ("cutE.png", 100, 690, 1040, None, .14, .32),               # resting brown/white cow (Personal Project)
    "B": ("cutB.png", 108, 1200, 950, (0, .43, .36, 1), .08, 0),     # small standing cow, far (Now)
    "D": ("cutD.png", 140, 1693, 1150, None, .14, .55),              # resting black/white cow (Say hi)
}
# Portrait (phone) arrangement: a phone shows only ~600px of the 2000px-wide scene, centred on x=1000, so the cows are
# bunched into that strip and staggered by depth: name: (left x, y of the feet).
MOBILE = {"A": (1000, 1290), "E": (800, 900), "B": (1130, 850), "D": (760, 1080)}
boxes = {}
for name, (file, height, x, feet, trim, fb, fl) in COWS.items():
    im = load(f"assets/cows/{file}", trim)
    im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    feather(im, fb, fl).save(f"assets/sprites/{name}.webp", "WEBP", quality=86, method=6)
    boxes[name] = dict(l=round(x / 20, 3), t=round((feet - height) / 13.33, 3), w=round(im.width / 20, 3), h=round(height / 13.33, 3))
for name, (x, feet) in MOBILE.items():
    boxes[name]["ml"] = round(x / 20, 3); boxes[name]["mt"] = round((feet - COWS[name][1]) / 13.33, 3)
json.dump(boxes, open("assets/cows.json", "w"), indent=1)
print("ok", boxes)

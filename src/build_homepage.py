"""Builds dist/index.html, a single self-contained page (images embedded).

    python3 src/make_wallpaper.py     # hill, cow sprites, sky mask -> assets/
    python3 src/build_homepage.py     # fill src/template.html -> dist/index.html
"""
import base64, io, json, os
from PIL import Image
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))   # run from the repo root, wherever this is called from

def file_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()

def img_uri(img, quality):
    buf = io.BytesIO(); img.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def li(items, cls=""):
    return "".join(f'<li class="{cls}">{i}</li>' if cls else f"<li>{i}</li>" for i in items)

# ---- content (edit these) ----
BIO = ("I'm Melodie. I love spending time outdoors, cooking, and running medium distances very slowly. I also enjoy working with data - check out this <a href=\"#work\" class=\"cowlink\" data-go=\"work\">Custom Fitness Tracking App</a> I built to model and analyze my personal health and activity data!")
DESC = ("Apple's Health and Activity apps don't show the stats I want to see, so I built my own custom app. "
        "I exported 5.6 million lines of raw XML Health data, parsed it into Parquet, and charted things like heatmaps of "
        "workout volume/type, pace on repeat routes, pace by heart-rate zone, workout type distribution with custom categories, "
        "gym PRs, and other stats exactly how I want to see them!")
NOW = ["Studying cake decorating techniques and whipped cream stabilization methods",
       "Conducting fun analyses of my health and fitness data",
       "Learning to play tennis with no coach but big dreams"]
EMAIL = "melodie4052@gmail.com"
PROFILE = "https://github.com/melodiehsieh"
REPO = "https://github.com/melodiehsieh/apple-health-dashboard"
LINKEDIN = "https://linkedin.com/in/melodiehsieh"
RESUME = "Hsieh_Melodie.pdf"      # the PDF in dist/, served next to index.html
PROJECT = "https://melodiehsieh.com/health/"

# Which cow opens which card: (cow letter in src/make_wallpaper.py, card key, label above the cow,
#   mouth position as (x, y) fractions of the cow image, and which way the cow faces: "r" or "l")
COWS = [("A", "about", "About", (.51, .54), "r"),
        ("B", "now", "Lately...", (.07, .41), "l"),
        ("E", "work", "Personal Project:\nCustom Fitness Tracking", (.80, .48), "r"),
        ("D", "hi", "Say hi", (.84, .42), "r")]
boxes = json.load(open("assets/cows.json"))
def place(c):
    b = boxes[c]
    # --l/--t place the cow on wide screens, --ml/--mt on portrait (phone) screens; see the CSS
    return (f'--l:{b["l"]:.2f}%;--t:{b["t"]:.2f}%;--ml:{b["ml"]:.2f}%;--mt:{b["mt"]:.2f}%;'
            f'width:{b["w"]:.2f}%;height:{b["h"]:.2f}%')
pens = "".join(
    f'<div class="pen" data-k="{k}" style="{place(c)}"><i class="shadow"></i>'
    f'<img class="sprite" alt="" src="{file_uri(f"assets/sprites/{c}.webp", "image/webp")}"></div>' for c, k, label, mouth, face in COWS)
hot = "".join(
    f'<button class="cow" data-k="{k}" data-face="{face}" aria-label="{label.replace(chr(10), " ")}" style="{place(c)};--mx:{mouth[0]*100:.0f}%;--my:{mouth[1]*100:.0f}%">'
    f'<span class="tag">{label.replace(chr(10), "<br>")}</span></button>' for c, k, label, mouth, face in COWS)
# one moo per cow (assets/sounds/<cow letter>.m4a), played when that cow is clicked
sounds = {k: file_uri(f"assets/sounds/{c}.m4a", "audio/mp4") for c, k, label, mouth, face in COWS}

shot = img_uri(Image.open("assets/activity.jpg").convert("RGB").crop((0, 0, 800, 450)).resize((640, 360), Image.LANCZOS), 75)

fills = {
    "%%WALL%%": file_uri("assets/hill.jpg", "image/jpeg"),
    "%%SKYMASK%%": file_uri("assets/sky-mask.png", "image/png"),
    "%%PENS%%": pens,
    "%%ME%%": file_uri("assets/me.jpg", "image/jpeg"),
    "%%SHOT%%": shot,
    "%%HOT%%": hot,
    "%%SOUNDS%%": json.dumps(sounds),
    "%%BIO%%": BIO, "%%DESC%%": DESC, "%%EMAIL%%": EMAIL,
    "%%NOW%%": li(NOW),
    # order: R&eacute;sum&eacute;, LinkedIn, GitHub; every external link opens in a new tab
    "%%LINKS%%": (f'<a class="pill" href="{RESUME}" target="_blank" rel="noopener">R&eacute;sum&eacute;</a>'
                  f'<a class="pill l" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>'
                  f'<a class="pill l" href="{PROFILE}" target="_blank" rel="noopener">GitHub</a>'),
    "%%PROJ%%": (f'<a class="pill" href="{PROJECT}" target="_blank" rel="noopener">Open the project</a>'
                 f'<a class="pill l" href="{REPO}" target="_blank" rel="noopener">Source</a>'),
}
# The hill's ridge line, read from the sky mask, so the moon can rise from behind it (40 samples across the scene)
mask = Image.open("assets/sky-mask.png").split()[3]
crest = []
for i in range(40):
    x = int((i + .5) / 40 * mask.width)
    y = next((y for y in range(mask.height) if mask.getpixel((x, y)) < 128), mask.height)
    crest.append(round(y / mask.height, 3))
fills["%%CREST%%"] = json.dumps(crest)

html = open("src/template.html").read()
for k, v in fills.items():
    html = html.replace(k, v)
assert "%%" not in html, "unfilled placeholder left in template"
os.makedirs("dist", exist_ok=True)
open("dist/index.html", "w").write(html)
print("dist/index.html", len(html) // 1024, "KB")

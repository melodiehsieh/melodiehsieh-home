"""Builds dist/index.html, a single self-contained page (images embedded).

    python3 make_wallpaper.py     # composite the cows onto the hill photo -> assets/hill-cows.jpg
    python3 build_homepage.py     # fill template.html -> dist/index.html
"""
import base64

def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()

def li(items, cls=""):
    return "".join(f"<li class={cls}>{i}</li>" if cls else f"<li>{i}</li>" for i in items)

# ---- content (edit these) ----
BIO = "Hi, I'm Melodie. I like working with data, and I build small projects to see what it says. This site collects the ones I'm happy to share."
DESC = ("Apple's Health and Activity apps don't show the stats I am curious about, so I built my own. "
        "I exported 5.6 million lines of raw XML Health data, parsed it into Parquet, and charted pace on repeat routes, "
        "pace by heart-rate zone, workout type distribution with custom categories, and gym PRs.")
TAGS = ["Python", "DuckDB", "Parquet", "TypeScript", "Observable Plot"]
NOW = ["Training for the next race and watching zone 2 pace drop.",
       "Learning more about DuckDB-WASM and static data sites.",
       "Reading about how to present health data without overselling it."]
SKILLS = ["Data analysis", "SQL", "Python", "Data visualization", "Customer success", "Automation"]
PROFILE = "https://github.com/melodiehsieh"
REPO = "https://github.com/melodiehsieh/apple-health-dashboard"

thumb = ('<div class="shot"><img class="thumb" src="' + b64("assets/activity.jpg", "image/jpeg") +
         '" alt="Activity Tracking dashboard showing the September 2026 workout calendar"></div>')

fills = {
    "%%WALLPAPER%%": b64("assets/hill-cows.jpg", "image/jpeg"),
    "%%AVATAR%%": b64("assets/cow-avatar.jpg", "image/jpeg"),
    "%%ME%%": b64("assets/me.jpg", "image/jpeg"),
    "%%PCOW%%": b64("assets/cow-inline.png", "image/png"),
    "%%THUMB%%": thumb,
    "%%BIO%%": BIO, "%%DESC%%": DESC,
    "%%TAGS%%": li(TAGS, "tag"), "%%SKILLS%%": li(SKILLS, "sk"), "%%NOW%%": li(NOW),
    "%%GH%%": REPO, "%%PROFILE%%": PROFILE,
}
html = open("template.html").read()
for k, v in fills.items():
    html = html.replace(k, v)
assert "%%" not in html, "unfilled placeholder left in template"
import os; os.makedirs("dist", exist_ok=True)
open("dist/index.html", "w").write(html)
print("dist/index.html", len(html) // 1024, "KB")

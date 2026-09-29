# Composite cut-out cow photos onto the hill wallpaper (hill-base.jpg, Unsplash photo by Zongnan Bao). Run: python3 make_wallpaper.py
from PIL import Image, ImageFilter, ImageDraw
bliss = Image.open('assets/hill-base.jpg').convert('RGBA')
if bliss.size != (2000,1333): bliss = bliss.resize((2000,1333), Image.LANCZOS)   # keep the cow coordinates below valid
ORIG = bliss.copy()                                             # untouched field, used to put grass back over the cows' feet
def load(name, trim=None):
    im = Image.open(name).convert('RGBA')
    if trim:                                                     # erase a stray second cow behind the main one
        x0,y0,x1,y1 = [int(v*s) for v,s in zip(trim,(im.width,im.height,im.width,im.height))]
        a = im.getchannel('A'); ImageDraw.Draw(a).rectangle([x0,y0,x1,y1], fill=0); im.putalpha(a)
    return im.crop(im.getchannel('A').getbbox())
def feather_bottom(im, frac=.12, left=.0):
    a = im.getchannel('A'); h = im.height; px = a.load()
    if left:                                                     # fade the photo's hard left crop edge too
        for x in range(int(im.width*left)):
            k = x/(im.width*left)
            for y in range(h): px[x,y] = int(px[x,y]*k)
    for y in range(int(h*(1-frac)), h):
        k = (h-1-y)/(h*frac)
        for x in range(im.width): px[x,y] = int(px[x,y]*k)
    im.putalpha(a); return im
def place(base, cow, height, x, feet_y):
    c = cow.resize((round(cow.width*height/cow.height), height), Image.LANCZOS)
    # soft contact shadow on the grass
    sh = Image.new('RGBA', base.size, (0,0,0,0)); d = ImageDraw.Draw(sh)
    w = c.width; d.ellipse([x-w*.05, feet_y-height*.05, x+w*1.05, feet_y+height*.07], fill=(10,40,0,120))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(height*.03)))
    base.alpha_composite(c, (x, feet_y-height))
    # tall grass in front: fade the untouched field photo back in over the lowest ~22% of the cow
    m = Image.new('L', base.size, 0); md = ImageDraw.Draw(m); top = int(feet_y-height*.22)
    for yy in range(top, feet_y+int(height*.04)):
        md.line([(x-4, yy), (x+w+4, yy)], fill=int(235*min(1,(yy-top)/(feet_y-top+1))**1.4))
    base.paste(ORIG, (0,0), m.filter(ImageFilter.GaussianBlur(2)))
D = feather_bottom(load('assets/cows/cutD.png'), .14, .16); E = feather_bottom(load('assets/cows/cutE.png'), .14, .16)
A = load('assets/cows/cutA.png'); B = load('assets/cows/cutB.png', trim=(0,.43,.36,1)); C = load('assets/cows/cutC.png')
cw = C.resize((round(C.width*96/C.height), 96), Image.LANCZOS)   # 96px tall = 2x for a 48px display size
cw.save('assets/cow-inline.png', optimize=True)
out = bliss.copy()
# far to near so nearer cows overlap farther ones; positions are in 2000x1333 image pixels
place(out, B, 120, 200, 865)     # small, far, left of the About window
# (the standing brown/white cow C now lives inside the Dashboard window, next to the 'Personal project' pill)
place(out, E, 92, 800, 1050)     # resting brown/white cow, further up the slope, above the standing one
place(out, D, 104, 1872, 1015)   # resting black/white cow, in the grass to the right of the Dashboard window
place(out, A, 340, 30, 1262)     # big front-on cow, bottom-left, nearest
out.convert('RGB').resize((1600,1067), Image.LANCZOS).save('assets/hill-cows.jpg', quality=52, optimize=True)
print(out.size)

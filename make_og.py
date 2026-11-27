#!/usr/bin/env python3
"""make_og.py — og.png 1200x630 for Platform 3 Furniture demo host (t_f9208927).
Lane painter pattern (v2 discipline from marisols run 11-26): hard text column —
every measured line must end <= TEXT_RIGHT; all art geometry >= ART_LEFT; asserted
before save."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "public", "og.png")
W, H = 1200, 630
TEXT_RIGHT = 742
ART_LEFT = 792
fails = []

INK   = (20, 33, 48)
INK2  = (34, 51, 67)
CREAM = (245, 239, 225)
BRASS = (201, 153, 62)
BRASSLT = (233, 200, 120)
WOOD  = (124, 82, 48)
SLATE = (93, 111, 127)

def F(size, bold=False):
    cands = (["/System/Library/Fonts/Supplemental/Iowan Old Style Bold.ttf",
              "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"] if bold else
             ["/System/Library/Fonts/Supplemental/Iowan Old Style Roman.ttf",
              "/System/Library/Fonts/Supplemental/Times New Roman.ttf"])
    for c in cands:
        if os.path.exists(c):
            try: return ImageFont.truetype(c, size)
            except OSError: pass
    return ImageFont.load_default()

def SANS(size, bold=False):
    cands = (["/System/Library/Fonts/Supplemental/Futura Bold.ttc", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else
             ["/System/Library/Fonts/Supplemental/Futura.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"])
    for c in cands:
        if os.path.exists(c):
            try: return ImageFont.truetype(c, size)
            except OSError: pass
    return ImageFont.load_default()

im = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(im)

# subtle rail rules bottom + arch hint on the right
for y in (H-58, H-44):
    d.line([(0, y), (W, y)], fill=INK2, width=4)
for x in range(30, W, 84):
    d.line([(x, H-66), (x, H-36)], fill=INK2, width=4)

# ---- text column ----
MARGIN = 64
lines = []
def put_kicker(y):
    f = SANS(21, bold=True)
    txt = "NOW OPEN · OAKLAND, MARYLAND"
    tw = d.textlength(txt, font=f)
    d.rounded_rectangle((MARGIN, y, MARGIN + tw + 44, y + 44), 22, outline=BRASS, width=2)
    d.text((MARGIN + 22, y + 11), txt, font=f, fill=BRASSLT)
    lines.append(("kicker", MARGIN + 22 + tw, y + 44))
    return y + 66

def put_heading(y):
    f = F(58, bold=True)
    for row in ("Furniture & mattresses,", "arriving at Platform 3."):
        tw = d.textlength(row, font=f)
        d.text((MARGIN, y), row, font=f, fill=CREAM)
        lines.append((row[:18], MARGIN + tw, y + 72))
        y += 74
    return y + 10

def put_body(y):
    f = SANS(25)
    rows = ["Furniture and mattresses in Oakland's former",
            "Grand Central Station building — new inventory",
            "arriving on an ongoing basis."]
    for row in rows:
        tw = d.textlength(row, font=f)
        d.text((MARGIN, y), row, font=f, fill=(210, 220, 228))
        lines.append((row[:16], MARGIN + tw, y + 34))
        y += 40
    return y + 22

def put_addr(y):
    f = SANS(23, bold=True)
    row = "312 S. Third Street · Garrett County · MD 21554"
    tw = d.textlength(row, font=f)
    d.text((MARGIN, y), row, font=f, fill=BRASS)
    lines.append(("addr", MARGIN + tw, y + 30))
    return y

put_kicker(56)
y = put_heading(124)
y = put_body(y)
put_addr(y)

# ---- art: station plate + clock ----
ax0 = ART_LEFT
# nameplate
pw, ph = 358, 108
px, py = ax0 + 4, 118
d.rounded_rectangle((px, py, px + pw, py + ph), 12, fill=INK2, outline=BRASS, width=3)
for rx, ry in ((px + 16, py + 15), (px + pw - 16, py + 15), (px + 16, py + ph - 15), (px + pw - 16, py + ph - 15)):
    d.ellipse((rx - 5, ry - 5, rx + 5, ry + 5), fill=BRASS)
ft = F(38, bold=True)
txt = "PLATFORM 3"
tw = d.textlength(txt, font=ft)
d.text((px + (pw - tw) / 2, py + 22), txt, font=ft, fill=CREAM)
fs = SANS(13, bold=True)
sub = "FURNITURE & MATTRESSES · OAKLAND MD"
tw2 = d.textlength(sub, font=fs)
d.text((px + (pw - tw2) / 2, py + 66), sub, font=fs, fill=BRASSLT)
d.line([(px + 30, py + ph - 26), (px + pw - 30, py + ph - 26)], fill=BRASS, width=2)

# clock below-right of plate
cx, cy, r = ax0 + 192, 350, 118
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=INK2, outline=BRASS, width=6)
d.ellipse((cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16), fill=CREAM)
import math
for ang in range(0, 360, 30):
    x1 = cx + (r - 24) * math.cos(math.radians(ang)); y1 = cy + (r - 24) * math.sin(math.radians(ang))
    x2 = cx + (r - 34) * math.cos(math.radians(ang)); y2 = cy + (r - 34) * math.sin(math.radians(ang))
    d.line([(x1, y1), (x2, y2)], fill=INK, width=4)
d.line([(cx, cy), (cx + 24, cy - 42)], fill=INK, width=7)
d.line([(cx, cy), (cx + 52, cy + 26)], fill=WOOD, width=5)
d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=BRASS)

# armchair glyph bottom-right
ox, oy = ax0 + 34, 486
d.rounded_rectangle((ox, oy + 34, ox + 96, oy + 66), 10, fill=WOOD)
d.rounded_rectangle((ox - 14, oy + 60, ox + 110, oy + 88), 12, fill=(138, 90, 51))
d.rounded_rectangle((ox + 4, oy - 8, ox + 92, oy + 40), 18, fill=(164, 105, 58))

# ---- asserts ----
for name, right, bot in lines:
    if right > TEXT_RIGHT: fails.append(f'text line "{name}" ends at x={right:.0f} > TEXT_RIGHT={TEXT_RIGHT}')
art_min_x = min(px, cx - r, ox - 14)
if art_min_x < ART_LEFT: fails.append(f'art geometry x={art_min_x} < ART_LEFT={ART_LEFT}')
if fails:
    print("OG FAILS:\n  " + "\n  ".join(fails)); sys.exit(1)

im.save(OUT, "PNG")
print(f"og.png saved {W}x{H}; text right-most = {max(l[1] for l in lines):.0f}; art left-most = {art_min_x}")

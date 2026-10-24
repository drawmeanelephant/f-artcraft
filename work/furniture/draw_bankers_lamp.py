#!/usr/bin/env python3
"""Banker's lamp — field plate V1R00. Emeralite type: a stepped brass
foot, a straight stem, and the pulled half-shell of green cased glass
tilted forward on its pivot, warm light spilling out of the mouth onto
the desk. Pull chain with a ball weight off the right end.
Brass plate, quiet-library mood. 1000x1000, drawn in screen space.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Banker's Lamp — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E140C"   # warm dark, not black
EXTENT = []


def ext(x, y):
    EXTENT.append((x, y))
    return (x, y)


def stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(a, b, *pairs):
    return {"gradient": {"kind": "linear", "start": [round(a[0], 1), round(a[1], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)], "stops": stops(*pairs)}}


def rad(*pairs):
    return {"gradient": {"kind": "radial", "stops": stops(*pairs)}}


BR_D, BR_L = "#4A3010", "#D8A94E"       # brass ramp
BR_HI = "#F0D08A"
GR_D, GR_L = "#0C3520", "#2E8A54"       # bottle green glass ramp
GR_HI = "#7AD8A2"


def ellipse(name, cx, cy, w, h, fill, stroke=NONE, sw=1.5, opacity=None):
    kw = {}
    if opacity is not None:
        kw["opacity"] = opacity
    d.shape("ellipse", name, x=round(cx - w / 2), y=round(cy - h / 2),
            width=round(w), height=round(h), fill=fill, stroke=stroke,
            strokeWidth=sw, **kw)
    ext(cx - w / 2, cy - h / 2)
    ext(cx + w / 2, cy + h / 2)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#141A10"), (1, "#070905")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A7440", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5E4E2E"), (0.6, "#3A301C"), (1, "#1C160C")),
        stroke="#100C06", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2D2A8", strokeWidth=3, opacity=24)
# warm light the lamp throws on the plate itself
d.shape("ellipse", "Lamp aura", x=200, y=150, width=600, height=560,
        fill=rad((0, "#EFC27A", 15), (0.55, "#9A7A44", 5), (1, "#6A5426", 0)),
        stroke=NONE)

FY = 662
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#5A4E32", 34), (1, "#14100A", 72)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E0D4AE", strokeWidth=2, opacity=18)

# pool of light on the desk under the lamp
ellipse("Light pool", 500, 700, 400, 96,
        rad((0, "#F2C878", 38), (0.6, "#B08A48", 14), (1, "#7A5E28", 0)))
# base shadow
ellipse("Base shadow", 500, 688, 300, 42,
        rad((0, "#040302", 62), (0.6, "#040302", 24), (1, "#040302", 0)))

# --- brass foot: stacked steps -------------------------------------------------------
ellipse("Foot bottom", 500, 678, 252, 30,
        lin((370, 660), (630, 700), (0, BR_L), (0.45, BR_D), (1, "#2E1E08")),
        stroke=INK, sw=2.0)
ellipse("Foot top", 500, 668, 252, 30,
        lin((370, 652), (630, 684), (0, BR_HI), (0.5, BR_L), (1, BR_D)),
        stroke=INK, sw=2.0)
ellipse("Foot step", 500, 652, 158, 22,
        lin((420, 640), (580, 664), (0, BR_L), (1, BR_D)), stroke=INK, sw=1.8)
ellipse("Stem socket", 500, 644, 96, 16,
        lin((450, 636), (550, 652), (0, BR_HI), (1, BR_D)), stroke=INK, sw=1.6)

# --- stem ----------------------------------------------------------------------------
d.path("M491,648 L491,352 L509,352 L509,648 Z", "Stem",
       fill=lin((491, 0), (509, 0), (0, BR_D), (0.45, BR_HI), (0.75, BR_L), (1, BR_D)),
       stroke=INK, strokeWidth=2.0, join="round")
ext(491, 352); ext(509, 648)
d.path("M495.5,640 L495.5,360", "Stem highlight", fill=NONE,
       stroke=BR_HI, strokeWidth=2.2, opacity=55)
# stem collars
for i, cy in enumerate((402, 620)):
    ellipse(f"Stem collar {i+1}", 500, cy, 34, 11,
            lin((483, 0), (517, 0), (0, BR_D), (0.5, BR_HI), (1, BR_D)),
            stroke=INK, sw=1.5)

# --- the green glass shade ------------------------------------------------------------
# silhouette: a pulled half-shell — domed top, ends curling under, front lip
# bowed down so the warm mouth reads beneath it
SHELL = ("M352,338 "
         "C338,328 336,302 348,290 "
         "C382,262 618,262 652,290 "
         "C664,302 662,328 648,338 "
         "C560,364 440,364 352,338 Z")
LIP = ("M352,338 "
       "C440,364 560,364 648,338")

# mouth interior: cased-glass underside, drawn before the lip stroke
d.path("M368,341 C440,362 560,362 632,341 C624,374 376,374 368,341 Z",
       "Shade mouth", fill=lin((0, 336), (0, 376),
       (0, "#F8E4B0", 92), (0.7, "#D8A860", 80), (1, "#8A5E28", 60)),
       stroke=NONE)
ext(368, 341); ext(632, 376)

# the shell itself
d.path(SHELL, "Glass shell",
       fill=lin((500, 262), (500, 366),
                (0, GR_HI), (0.28, GR_L), (0.72, GR_D), (1, "#062114")),
       stroke=INK, strokeWidth=2.4, join="round")
# two bulbs tucked inside the mouth; the lip stroke covers their tops
for i, bx in enumerate((428, 572)):
    ellipse(f"Bulb {i+1}", bx, 360, 22, 16,
            rad((0, "#FFF2CC"), (0.7, "#F2C878"), (1, "#C89040", 0)),
            stroke=NONE)
# rolled rim: redraw the front lip as a highlight edge over the mouth
d.path(LIP, "Front lip", fill=NONE, stroke="#0A2A18", strokeWidth=4.5, cap="round")
d.path(LIP, "Lip edge light", fill=NONE, stroke=GR_HI, strokeWidth=1.8,
       opacity=60, cap="round")
# specular streak along the dome
d.path("M392,286 C440,272 560,272 608,286", "Dome streak", fill=NONE,
       stroke="#BEF2D4", strokeWidth=7, opacity=30, cap="round")
d.path("M404,290 C450,279 550,279 596,290", "Dome streak core", fill=NONE,
       stroke="#E2F8EA", strokeWidth=3, opacity=45, cap="round")
# right end: a sliver of cased interior inside the curl
d.path("M648,296 C660,306 658,326 646,336 C652,322 652,308 648,296 Z",
       "End interior", fill="#F4E0AC", opacity=85, stroke=NONE)

# pivot knuckle where the stem meets the shell
ellipse("Pivot knuckle", 500, 346, 26, 18,
        rad((0, BR_HI), (0.6, BR_L), (1, BR_D)), stroke=INK, sw=1.6)

# --- pull chain + ball off the right end ----------------------------------------------
for i in range(7):
    ellipse(f"Chain bead {i+1}", 622 + (i % 2) * 1.5, 352 + i * 8, 4.5, 4.5,
            rad((0, BR_HI), (1, BR_D)), stroke=NONE)
ellipse("Chain pull", 623, 412, 11, 11, rad((0, BR_HI), (1, BR_D)),
        stroke=INK, sw=1.2)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("lamp extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


# --- caption ----------------------------------------------------------------------------------
def find(node, oid):
    if isinstance(node, dict):
        if node.get("id") == oid and "bounds" in node:
            return node["bounds"]
        for v in node.values():
            r = find(v, oid)
            if r:
                return r
    elif isinstance(node, list):
        for v in node:
            r = find(v, oid)
            if r:
                return r
    return None


def caption(name, mats):
    n = d.text(name, "Name", x=500, y=934, size=56, font="Virelai Sans",
               color="#F2E8D0", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C4B28A", justify="center")
    d.cmd("text.setStyle", "Name tracking", id=n["id"], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", id=m["id"], tracking=260)
    doc = d.m.call("inspect_document", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" %
              (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]


caption("BANKERS LAMP", "BRASS · GREEN GLASS")
d.finish("bankers-lamp-V1R00")

#!/usr/bin/env python3
"""Koala — field-guide plate V1R00. Asleep in the fork of a gum tree where the
light is greenest: a grey ball of fur wedged into the crook of a smooth-barked
limb, chin dropped, lids shut, one paw slack on the bark. Luminous eucalyptus
plate with mist bands, dappled light and hanging gum sprays. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Koala — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1C1A14"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def quad(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
            u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1])

def ribbon(p0, p1, p2, w0, w1, label, n=20, **kw):
    """Tapered strip along a quadratic; w0/w1 are full widths at root/tip."""
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y = quad(p0, p1, p2, t)
        x0, y0 = quad(p0, p1, p2, max(0, t - 0.01))
        x1, y1 = quad(p0, p1, p2, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        Rr.append((x + dy/ln * w, y - dx/ln * w))
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    return d.path(s, label, **kw)

def leaf(cx, cy, ln, deg, w=0.34, label="Leaf", **kw):
    """Sickle-shaped gum leaf pointing along deg (down = 90)."""
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tip = (cx + ux * ln, cy + uy * ln)
    s = ("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z" % (
        cx, cy,
        cx + ux * ln * 0.45 + nx * ln * w, cy + uy * ln * 0.45 + ny * ln * w,
        tip[0], tip[1],
        cx + ux * ln * 0.55 - nx * ln * w * 0.8, cy + uy * ln * 0.55 - ny * ln * w * 0.8,
        cx, cy))
    return d.path(s, label, **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#12201A"), (1, "#040A07"))
PLATE_GRAD = rad((0, "#D6E4C8"), (0.55, "#A2BE94"), (1, "#5E8060"))
FUR = lin(470, 300, 470, 690, (0, "#C4C0B6"), (0.5, "#9C988E"), (1, "#746F66"))
BARK = lin(500, 560, 500, 720, (0, "#9C8B72"), (1, "#5A4A34"))

# --- backdrop + eucalyptus plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#A2BE94", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E5638", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EAF2DC", strokeWidth=3, opacity=45)

# deep foliage shadows at the rim's edge
d.shape("ellipse", "Foliage L", x=80, y=300, width=190, height=320,
        fill="#3E5638", opacity=30, stroke=NONE)
d.shape("ellipse", "Foliage R", x=760, y=380, width=160, height=280,
        fill="#3E5638", opacity=28, stroke=NONE)
# the green pool of light the sleeper is soaking in
d.shape("ellipse", "Light pool", x=230, y=140, width=540, height=460,
        fill=rad((0, "#EDF5DE"), (1, "#EDF5DE")), opacity=45, stroke=NONE)
# drifting mist bands
d.shape("ellipse", "Mist 1", x=170, y=430, width=660, height=90,
        fill="#F0F6E4", opacity=22, stroke=NONE)
d.shape("ellipse", "Mist 2", x=240, y=520, width=520, height=60,
        fill="#F0F6E4", opacity=16, stroke=NONE)

# --- hanging gum sprays ------------------------------------------------------------
def spray(x0, y0, x1, y1, n, label, side=1):
    d.path(f"M{x0},{y0} Q{(x0+x1)/2},{(y0+y1)/2 + 18} {x1},{y1}", f"{label} stem",
           fill=NONE, stroke="#5C7E62", strokeWidth=4, cap="round")
    for k in range(n):
        t = (k + 1) / (n + 1)
        x, y = quad((x0, y0), ((x0+x1)/2, (y0+y1)/2 + 18), (x1, y1), t)
        leaf(x, y, 58 - 14 * abs(0.5 - t), 95 + side * (38 - 26 * t),
             w=0.30, label=f"{label} leaf {k+1}",
             fill="#7FA088" if k % 2 else "#8FAE92", opacity=88, stroke=NONE)
spray(770, 142, 645, 305, 6, "Spray top-right", side=-1)
spray(235, 118, 350, 282, 5, "Spray top-left", side=1)
# one leaf letting go — the doze mood in a single object
leaf(610, 360, 46, 148, w=0.30, label="Falling leaf", fill="#9CBC9E", opacity=80, stroke=NONE)

# dapples of light among the green
for i, (x, y, w) in enumerate([(300,260,26),(420,210,18),(560,180,22),(680,330,16),
                               (250,420,14),(740,470,18),(350,560,12),(620,590,10)]):
    assert on_disc(x, y, 14), (x, y)
    d.shape("ellipse", f"Dapple {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4F9E4", opacity=30, stroke=NONE)

# --- the gum limb and its fork ------------------------------------------------------
# fork tine first (the upright arm of the V), behind everything
ribbon((398, 632), (346, 548), (298, 462), 58, 26, "Fork tine",
       fill=BARK, stroke=INK, strokeWidth=5)
# main limb crossing the plate, bowed and tapered, ends exiting under the rim
ribbon((140, 700), (505, 645), (905, 568), 90, 52, "Limb",
       fill=BARK, stroke=INK, strokeWidth=5)
# smooth-bark peeling strips + grain
d.path("M200,680 C330,650 520,624 700,600", "Bark grain 1", fill=NONE,
       stroke="#6E5C42", strokeWidth=4, opacity=50, cap="round")
d.path("M240,698 C420,668 620,640 840,596", "Bark grain 2", fill=NONE,
       stroke="#6E5C42", strokeWidth=3, opacity=40, cap="round")
d.path("M320,660 C420,645 520,630 600,616", "Bark peel", fill=NONE,
       stroke="#C4B394", strokeWidth=6, opacity=55, cap="round")
d.path("M340,600 C360,570 378,540 390,512", "Tine grain", fill=NONE,
       stroke="#6E5C42", strokeWidth=3, opacity=45, cap="round")
# shadow the koala throws onto the bark
d.shape("ellipse", "Sitter's shadow", x=370, y=600, width=210, height=44,
        fill="#3E3020", opacity=30, stroke=NONE)

# === the koala, wedged asleep in the fork ============================================
# --- body: an egg of grey, leaning back into the crook -------------------------------
d.path("M470,418 C525,418 565,453 578,508 C590,563 585,618 555,652 "
       "C525,682 450,687 415,662 C380,638 362,588 368,533 "
       "C374,478 415,418 470,418 Z", "Body", fill=FUR, stroke=INK, strokeWidth=5)
# big pale chest patch — koala's soft front
d.path("M472,508 C518,508 546,538 550,578 C554,620 532,650 490,656 "
       "C452,660 420,644 410,612 C400,582 408,550 430,530 "
       "C442,519 456,510 472,508 Z", "Chest cream",
       fill=rad((0, "#EDEAE0"), (1, "#C9C4B6")), opacity=72, stroke=NONE)
# flank shade where the body curves away
d.path("M400,540 C400,585 415,625 445,650 C415,645 392,612 386,575 "
       "C382,548 388,528 400,540 Z", "Flank shade", fill="#55514A", opacity=30, stroke=NONE)

# --- arms: stubby limbs tucked against the body's edges -----------------------------
ribbon((402, 512), (388, 575), (380, 634), 40, 26, "Arm L",
       fill=lin(402, 512, 380, 634, (0, "#8E8A80"), (1, "#6A655C")),
       stroke=INK, strokeWidth=4)
ribbon((550, 508), (568, 570), (578, 628), 38, 25, "Arm R",
       fill=lin(550, 508, 578, 628, (0, "#8E8A80"), (1, "#6A655C")),
       stroke=INK, strokeWidth=4)
# paws gripping: toe nubs on the bark
for i, (x, y) in enumerate([(354, 642), (368, 648), (382, 644)]):
    d.shape("ellipse", f"Toe L {i+1}", x=x-8, y=y-7, width=16, height=14,
            fill="#5E5A52", stroke=INK, strokeWidth=2.5)
for i, (x, y) in enumerate([(572, 636), (586, 640), (599, 634)]):
    d.shape("ellipse", f"Toe R {i+1}", x=x-8, y=y-7, width=16, height=14,
            fill="#5E5A52", stroke=INK, strokeWidth=2.5)

# --- head: broad, sunk low on the shoulders, drooped -----------------------------------
d.path("M475,302 C530,302 566,330 570,376 C574,422 543,458 494,466 "
       "C446,472 402,454 390,412 C380,374 392,336 426,316 "
       "C440,308 458,302 475,302 Z", "Head",
       fill=lin(475, 300, 470, 470, (0, "#B8B4AA"), (1, "#86827A")),
       stroke=INK, strokeWidth=5)
# crown highlight — the green light on the fur
d.shape("ellipse", "Crown light", x=415, y=305, width=130, height=55,
        fill="#F0EFE4", opacity=30, stroke=NONE)

# --- ears: two ragged clouds of fluff ---------------------------------------------------
def fluffy_ear(cx, cy, r, label, odeg, droop=0):
    # rounded wedge of fluff; bumps crowd the outer rim, smooth toward the head
    d.shape("ellipse", f"{label} base", x=cx - r, y=cy - r + droop,
            width=r * 2, height=r * 2, fill="#8E8A80", stroke=INK, strokeWidth=4)
    for k, off in enumerate([-75, -45, -15, 15, 45, 75, 105]):
        a = math.radians(odeg + off)
        bx = cx + math.cos(a) * r * 0.96
        by = cy + droop + math.sin(a) * r * 0.96
        s = r * (0.42 if k % 2 else 0.55)
        d.shape("ellipse", f"{label} tuft {k+1}", x=bx - s / 2, y=by - s / 2,
                width=s, height=s, fill="#8E8A80", stroke=NONE)
    # soft pale core, not spokes — the inner ear's warm fur
    d.shape("ellipse", f"{label} inner", x=cx - r * 0.58, y=cy + droop - r * 0.52,
            width=r * 1.16, height=r * 1.04, fill="#CFC9BB", opacity=72, stroke=NONE)
    for k, off in enumerate([-40, -8, 25, 55]):
        a = math.radians(odeg + off)
        x0 = cx + math.cos(a) * r * 0.55
        y0 = cy + droop + math.sin(a) * r * 0.55
        x1 = cx + math.cos(a) * r * 0.95
        y1 = cy + droop + math.sin(a) * r * 0.95
        d.path(f"M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}", f"{label} fringe {k+1}",
               fill=NONE, stroke="#E8E4D8", strokeWidth=5, opacity=55, cap="round")
fluffy_ear(362, 312, 60, "Ear L", 185, droop=6)
fluffy_ear(590, 308, 60, "Ear R", -5, droop=14)

# --- sleeping face ----------------------------------------------------------------------
# closed lids: two soft arcs, lashes hinting down
for label, (x0, y0, x1, y1) in [("Lid L", (428, 392, 468, 396)),
                                ("Lid R", (510, 396, 550, 400))]:
    d.path(f"M{x0},{y0} Q{(x0+x1)/2},{y0 + 12} {x1},{y1}", label, fill=NONE,
           stroke=INK, strokeWidth=5, cap="round")
for i, (x, y) in enumerate([(436, 398), (446, 401), (520, 402), (530, 405)]):
    d.path(f"M{x},{y} l-3,5", f"Lash {i+1}", fill=NONE, stroke=INK,
           strokeWidth=2.5, opacity=65, cap="round")
# brow peace-lines
d.path("M428,368 C442,360 458,358 472,362", "Brow L", fill=NONE,
       stroke="#6E6A60", strokeWidth=4, opacity=45, cap="round")
d.path("M508,362 C522,358 538,360 550,368", "Brow R", fill=NONE,
       stroke="#6E6A60", strokeWidth=4, opacity=45, cap="round")
# the great leathery nose — the koala signature
d.path("M490,404 C516,404 529,422 527,447 C525,470 511,484 491,484 "
       "C471,484 457,470 455,447 C453,422 465,404 490,404 Z",
       "Nose", fill=lin(490, 404, 490, 484, (0, "#3E352C"), (1, "#171310")),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nose sheen", x=468, y=412, width=22, height=14,
        fill="#8A8074", opacity=55, stroke=NONE)
d.path("M491,442 L491,470", "Nose crease", fill=NONE, stroke="#0E0B08",
       strokeWidth=3, opacity=50, cap="round")
# tiny mouth, chin tucked
d.path("M478,500 Q491,506 504,500", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
# pale cheek ruffs
d.path("M402,420 C398,445 408,465 425,475", "Cheek ruff L", fill=NONE,
       stroke="#D8D4C8", strokeWidth=8, opacity=55, cap="round")
d.path("M556,425 C558,448 550,467 535,477", "Cheek ruff R", fill=NONE,
       stroke="#D8D4C8", strokeWidth=8, opacity=55, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#22301E", strokeWidth=6)

# --- caption ---------------------------------------------------------------------
d.text("KOALA", "Name", x=500, y=940, size=60, font="Virelai Sans",
       color="#E8F0DC", justify="center")
LINE2, SZ2, TRK = "PHASCOLARCTOS CINEREUS", 20, 240
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#A8C09A", justify="center")
if r and "id" in r:
    d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
if r and "id" in r:
    b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
    print("second line bounds", {k: round(v) for k, v in b2.items()})
    assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("koala-V1R00")

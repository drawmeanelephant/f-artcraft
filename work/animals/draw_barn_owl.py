#!/usr/bin/env python3
"""Barn owl — field plate V1R00. Face-on bust in the dark of the rafters:
the heart-shaped ivory facial dish, two deep black eyes, the small pale
down-turned beak; tawny crown and speckled shoulders settling onto the disc's
own arc. Behind: a moonbeam shafting down through the roof beams, dust in the
light. Rafter plate, hush mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Barn Owl — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#26180E"   # warm dark umber, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def linO(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def radO(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

def smooth(pts, closed=True):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

def mirrored(pts):
    """close a right-half outline through the vertical centreline"""
    return pts + [(2 * PCX - x, y) for x, y in reversed(pts[1:-1])]

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#1A120C"), (1, "#070402"))
PLATE_GRAD = rad((0, "#4A3E30"), (0.55, "#2E241B"), (1, "#16100B"))
RUFF_GRAD  = rad((0, "#8A6234"), (0.7, "#6B4826"), (1, "#4A3016"))
DISH_GRAD  = rad((0, "#FDF9EE"), (0.55, "#EFE2C4"), (1, "#C9AE82"))
CROWN_GRAD = rad((0, "#C89858"), (0.6, "#A07438"), (1, "#6E4A20"))
BODY_GRAD  = lin(0, 500, 0, 880, (0, "#9A7240"), (0.55, "#7A562C"), (1, "#4A3018"))
BEAM_GRAD  = lin(0, 90, 0, 230, (0, "#3E2C1A"), (1, "#221610"))

# --- backdrop + night-barn plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#6B5A42", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)

# moonbeam: a tall soft column of light — radial alpha fades to 0 in every
# direction, so no hard edge anywhere; a second narrower ellipse is its hot core
d.shape("ellipse", "Moonbeam", x=330, y=80, width=340, height=580,
        fill=radO((0, "#BFD0E8", 14), (0.6, "#BFD0E8", 7), (1, "#BFD0E8", 0)), stroke=NONE)
d.shape("ellipse", "Moonbeam core", x=405, y=90, width=180, height=540,
        fill=radO((0, "#D4E0F0", 12), (0.55, "#D4E0F0", 6), (1, "#D4E0F0", 0)), stroke=NONE)
# hayloft glow tucked inside the rafter apex where the beam enters — alpha fades to 0
d.shape("ellipse", "Loft glow", x=400, y=62, width=200, height=90,
        fill=radO((0, "#D8E4F4", 30), (1, "#D8E4F4", 0)), stroke=NONE)

# rafters: the barn apex — two slopes meeting above the disc + a collar tie
RAFTER_L = "M178,214 L196,196 L474,52 L506,64 L238,226 Z"
RAFTER_R = "M822,214 L804,196 L526,52 L494,64 L762,226 Z"
d.path(RAFTER_L, "Rafter L", fill=BEAM_GRAD, stroke=NONE)
d.path(RAFTER_R, "Rafter R", fill=BEAM_GRAD, stroke=NONE)
d.path("M188,196 L812,196 L800,158 L200,158 Z", "Collar tie", fill=BEAM_GRAD, stroke=NONE)
for i, dd in enumerate(["M210,205 L470,72", "M790,205 L530,72",
                        "M215,178 L790,178", "M222,168 L778,168"]):
    d.path(dd, f"Beam grain {i+1}", fill=NONE, stroke="#5A4226", strokeWidth=3, opacity=45, cap="round")
# pegs where the collar tie meets the rafters
d.shape("ellipse", "Peg L", x=208, y=182, width=14, height=14, fill="#16100A", stroke=NONE)
d.shape("ellipse", "Peg R", x=778, y=182, width=14, height=14, fill="#16100A", stroke=NONE)

# dust motes hanging in the beam
for i, (x, y, w) in enumerate([(430,150,4),(505,210,3),(560,290,5),(470,330,3),
                               (600,380,4),(520,430,3),(640,470,4),(450,240,3),(580,540,3)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8DCC0", opacity=45, stroke=NONE)
# a few stray strands of hay hanging from the collar tie
for i, (x, y, ln_, bend) in enumerate([(330,196,58,-14),(360,196,40,10),(660,196,64,16)]):
    d.path(f"M{x},{y} Q{x+bend},{y+ln_*0.6} {x+bend*1.4},{y+ln_}",
           f"Hay strand {i+1}", fill=NONE, stroke="#8A6E3C", strokeWidth=3, opacity=40, cap="round")

# --- shoulders: barred buff mass settling onto the disc arc ------------------------
sy = 700
sl, sr = disc_x(sy, -1), disc_x(sy, 1)
BODY = [(sl, sy), (238, 664), (262, 596), (312, 548), (352, 522),
        (388, 512), (436, 516), (500, 522), (564, 516), (612, 512),
        (648, 522), (688, 548), (738, 596), (762, 664), (sr, sy)]
d.path(smooth(BODY, closed=False) + f" A{PR},{PR} 0 0 1 {sl:.1f},{sy} Z",
       "Shoulders", fill=BODY_GRAD, stroke=NONE)
# soft breast light where the moonbeam lands
d.shape("ellipse", "Breast light", x=400, y=560, width=200, height=140,
        fill="#D8C09A", opacity=16, stroke=NONE)
# barred scallops across the chest — rows of shallow arcs
for j, (y, w_, op) in enumerate([(592, 7, 42), (634, 7, 38), (676, 7, 34), (716, 6, 30)]):
    d.path(f"M{300+j*10},{y} C380,{y+22} 620,{y+22} {700-j*10},{y}",
           f"Breast bar {j+1}", fill=NONE, stroke="#3A2410", strokeWidth=w_, opacity=op, cap="round")
# the owl's fine speckle field over the shoulders
for i, (x, y) in enumerate([(330,600),(392,578),(448,560),(560,560),(622,580),(680,604),
                            (360,646),(430,630),(500,624),(575,632),(646,652),
                            (392,692),(472,686),(552,690),(630,694),(500,742),(420,736),(584,738)]):
    d.shape("ellipse", f"Breast speckle {i+1}", x=x - 4, y=y - 3, width=8, height=6,
            fill="#2E1C0C", opacity=50, stroke=NONE)

# --- crown: tawny dome behind the heart ---------------------------------------------
d.path(smooth(mirrored([(500, 262), (580, 276), (646, 318), (668, 380),
                        (640, 430), (560, 420), (500, 400)])),
       "Crown", fill=CROWN_GRAD, stroke=NONE)
# crown speckles
for i, (x, y) in enumerate([(420,286),(470,272),(540,274),(600,292),(380,320),
                            (632,330),(452,316),(560,320)]):
    d.shape("ellipse", f"Crown speckle {i+1}", x=x - 4, y=y - 3, width=8, height=6,
            fill="#3A2410", opacity=55, stroke=NONE)
# pale brow line over the crown front edge
d.path("M392,330 C440,296 560,296 608,330", "Crown light", fill=NONE,
       stroke="#D8B478", strokeWidth=6, opacity=35, cap="round")

# --- the heart: darker ruff ring first, ivory dish inside -----------------------------
HEART = [(500, 356), (570, 330), (648, 346), (686, 406), (674, 478),
         (626, 552), (564, 608), (500, 650)]
d.path(smooth(mirrored([((x - PCX) * 1.10 + PCX, (y - 470) * 1.08 + 470) for x, y in HEART])),
       "Facial ruff", fill=RUFF_GRAD, stroke=NONE)
d.path(smooth(mirrored(HEART)), "Facial dish", fill=DISH_GRAD,
       stroke="#8A6234", strokeWidth=3)
# the dish's faint radial rings — the ear's parabola made visible
for i, (sc, op) in enumerate([(0.86, 22), (0.68, 16)]):
    d.path(smooth(mirrored([(PCX + (x - PCX) * sc, 430 + (y - 430) * sc) for x, y in HEART])),
           f"Dish ring {i+1}", fill=NONE, stroke="#B89468", strokeWidth=3, opacity=op)
# shadow pooling at the heart's lower V
d.path("M430,560 C460,600 540,600 570,560 C560,616 440,616 430,560 Z",
       "Chin shadow", fill="#A8845A", opacity=35, stroke=NONE)

# --- eyes: deep black wells, slight tear-streak toward the beak ------------------------
for side in (-1, 1):
    ex = PCX + side * 88
    nm = "L" if side < 0 else "R"
    d.path(f"M{ex - 26},424 C{ex - 20},402 {ex + 20},402 {ex + 26},424 "
           f"C{ex + 22},446 {ex - 22},446 {ex - 26},424 Z",
           f"Eye socket {nm}", fill="#1A0F08", stroke=NONE)
    d.shape("ellipse", f"Eye {nm}", x=ex - 17, y=410, width=34, height=34,
            fill=rad((0, "#3A2410"), (0.45, "#160C06"), (1, "#0A0503")), stroke=NONE)
    d.shape("ellipse", f"Eye glint {nm}", x=ex - 7 + side * -3, y=415, width=7, height=7,
            fill="#FFF6E0", opacity=80, stroke=NONE)
    # the faint dark streak running from the inner eye corner down toward the beak
    d.path(f"M{ex - side * 20},440 C{ex - side * 34},470 {PCX + side * 30},500 {PCX + side * 22},524",
           f"Eye streak {nm}", fill=NONE, stroke="#6B4826", strokeWidth=4, opacity=45, cap="round")

# --- beak: small pale horn, down-curved, hiding in the dish's lower third --------------
d.path("M478,442 C486,434 514,434 522,442 C528,470 520,506 500,528 C480,506 472,470 478,442 Z",
       "Beak", fill=lin(0, 440, 0, 528, (0, "#E4D4B4"), (1, "#9A7C54")),
       stroke="#6B4826", strokeWidth=3)
d.shape("ellipse", "Nostril L", x=486, y=456, width=9, height=6, fill="#4A3016", opacity=70, stroke=NONE)
d.shape("ellipse", "Nostril R", x=505, y=456, width=9, height=6, fill="#4A3016", opacity=70, stroke=NONE)
d.path("M500,528 C494,540 488,548 480,554", "Beak tip shade", fill=NONE,
       stroke="#6B4826", strokeWidth=4, opacity=50, cap="round")
# sparse downy feathers lifting off the chin
for i, (x, bend) in enumerate([(470, -16), (500, 0), (530, 16)]):
    d.path(f"M{x},648 Q{x + bend},664 {x + bend * 1.3},678",
           f"Chin down {i+1}", fill=NONE, stroke="#C9AE82", strokeWidth=3, opacity=50, cap="round")

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#0E0A06", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9B48E", strokeWidth=3, opacity=28)

# --- name + second line ---------------------------------------------------------------
d.text("BARN OWL", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#EBDCC0", justify="center")
LINE2, SZ2, TRK = "TYTO ALBA", 22, 340
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#A88E66", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("barn-owl-V1R00")

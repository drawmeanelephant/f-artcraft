#!/usr/bin/env python3
"""Common raven — field plate V1R00. A steep banking soar off a winter cliff:
wide fingered wings in a hard V, wedge tail fanned, heavy bristled bill,
shaggy throat hackles, the dashed corkscrew trail of the barrel roll it just
flew still hanging off the cliff brow. Cliff plate, winter-timber mood —
grey snowfield with bare snags below, drifting specks. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Common Raven — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#16181D"   # cold dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def rim_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0C1218"), (1, "#04070A"))
PLATE_GRAD = rad((0, "#9EACBA"), (0.55, "#556472"), (1, "#202A33"))
LAND_GRAD  = lin(90, 470, 800, 880, (0, "#5E5248"), (0.55, "#383028"), (1, "#1E1810"))
BODY_GRAD  = lin(660, 370, 400, 500, (0, "#3A4148"), (0.5, "#22262D"), (1, "#101318"))
WING_GRAD  = lin(560, 400, 800, 200, (0, "#2E353D"), (0.6, "#1B2026"), (1, "#0C0F13"))
WING2_GRAD = lin(480, 390, 230, 215, (0, "#262B32"), (0.6, "#171B20"), (1, "#0B0E12"))

# --- backdrop + winter plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7E8C9A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#141C24", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6E0E8", strokeWidth=3, opacity=35)

# low winter light pooling upper right, where the bird is headed
d.shape("ellipse", "Pale sun", x=560, y=130, width=340, height=230,
        fill=rad((0, "#E6ECF0", 30), (0.6, "#E6ECF0", 12), (1, "#E6ECF0", 0)), stroke=NONE)

# drifting snow specks
for i, (x, y, w) in enumerate([(240, 170, 5), (390, 120, 4), (560, 105, 5), (720, 140, 4),
                               (810, 300, 5), (160, 340, 5), (300, 300, 4), (660, 520, 4),
                               (840, 440, 5), (480, 210, 4)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Speck {i+1}", x=x, y=y, width=w, height=w,
            fill="#EAF2F8", opacity=55, stroke=NONE)

# --- the cliff + snowfield: one landmass closing on the disc's own arc ------------
xl, xr = rim_x(470, -1), rim_x(760, 1)
d.path(f"M{xl:.1f},470 C150,478 200,502 250,542 C330,600 420,662 520,702 "
       f"C620,737 700,757 {xr:.1f},760 A{PR},{PR} 0 0 1 {xl:.1f},470 Z",
       "Cliff snowfield", fill=LAND_GRAD, stroke=NONE)
# broken snag at the brow — the launch post
d.path("M118,478 C124,458 136,446 152,444 M136,470 L152,450 M130,466 L120,452",
       "Brow snag", fill=NONE, stroke="#241E14", strokeWidth=4, opacity=80, cap="round")
# strata + cracks on the cliff face (upper left of the landmass)
for i, dd in enumerate(["M95,545 C160,552 230,578 285,612",
                        "M112,605 C180,618 250,642 302,666",
                        "M140,668 C210,682 290,700 355,714"]):
    d.path(dd, f"Stratum {i+1}", fill=NONE, stroke="#241C12",
           strokeWidth=5, opacity=45, cap="round")
for i, dd in enumerate(["M175,505 L160,555", "M240,555 L222,608"]):
    d.path(dd, f"Crack {i+1}", fill=NONE, stroke="#241C12",
           strokeWidth=3.5, opacity=40, cap="round")
# snow sheet lying along the slope's top edge, right half
d.path("M330,640 C430,690 570,738 790,758", "Snow line", fill=NONE,
       stroke="#DCE6EE", strokeWidth=20, opacity=50, cap="round")
d.path("M300,618 C420,672 560,720 700,745", "Snow line 2", fill=NONE,
       stroke="#C4D2DE", strokeWidth=8, opacity=35, cap="round")
# bare winter timber on the snow slope
for i, (x0, y0, x1, y1) in enumerate([(622, 758, 610, 655), (700, 763, 692, 690),
                                      (545, 738, 538, 672), (762, 768, 756, 716)]):
    d.path(f"M{x0},{y0} C{x0 - 4},{(y0 + y1) / 2:.0f} {x1 + 4},{(y0 + y1) / 2:.0f} {x1},{y1}",
           f"Trunk {i+1}", fill=NONE, stroke="#2E2620", strokeWidth=4.5, cap="round")
    for k, (dx, dy) in enumerate([(-16, -22), (14, -30)]):
        bx, by = x1 + (x0 - x1) * 0.3, y1 + (y0 - y1) * 0.3 + k * 14
        d.path(f"M{bx:.0f},{by:.0f} l{dx},{dy}", f"Trunk {i+1} branch {k+1}",
               fill=NONE, stroke="#2E2620", strokeWidth=3, cap="round")

# the corkscrew trail of the roll it just flew, hanging off the brow
d.path("M148,462 C205,412 262,392 300,402 C338,412 356,446 344,474 "
       "C334,496 308,504 292,492 C278,482 280,460 294,452 "
       "C306,446 318,452 322,464 C328,478 340,488 356,494",
       "Roll trail", fill=NONE, stroke="#C8D6E2", strokeWidth=3.5,
       opacity=45, dash=[5, 10], cap="round")

# === the raven =====================================================================
# far wing — up-left over the cliff top, slightly darker, scalloped primaries
d.path("M475,388 C432,338 398,295 372,264 Q320,228 240,208 "
       "Q278,230 282,252 Q252,246 238,254 Q275,264 288,278 "
       "Q260,278 250,290 Q282,298 296,308 "
       "C355,340 405,390 430,432 C448,415 465,400 475,388 Z",
       "Far wing", fill=WING2_GRAD, stroke=INK, strokeWidth=4)
# wedge tail fanning left, centre feathers longest
d.path("M418,438 C382,448 348,468 320,494 L312,508 "
       "C350,512 388,504 420,488 C426,470 424,452 418,438 Z",
       "Tail", fill=lin(415, 440, 315, 505, (0, "#262C33"), (1, "#14181D")),
       stroke=INK, strokeWidth=4.5)
for i, (tx, ty) in enumerate([(330, 496), (345, 505), (358, 492)]):
    d.path(f"M415,462 L{tx},{ty}", f"Tail feather {i+1}", fill=NONE,
           stroke="#0C0F13", strokeWidth=3, opacity=60, cap="round")

# body — plump torpedo, head running into the shoulders
d.path("M648,366 C612,352 555,352 515,368 C470,385 430,412 408,442 "
       "C400,455 402,468 415,478 C450,496 515,500 565,488 "
       "C615,476 648,448 660,415 C668,396 662,378 648,366 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=5.5)
# steel sheen along the back
d.path("M640,368 C600,356 550,358 512,372", "Back sheen", fill=NONE,
       stroke="#5E7086", strokeWidth=8, opacity=35, cap="round")
# belly shade
d.path("M440,470 C490,492 560,492 610,466", "Belly shade", fill=NONE,
       stroke="#05070A", strokeWidth=14, opacity=30, cap="round")

# shaggy throat hackles — the raven's beard, a pointed tuft under the chin
d.path("M598,414 C616,426 638,434 660,436 L652,450 L642,440 L634,456 "
       "L624,442 L612,452 L604,434 Z",
       "Hackles", fill="#101318", stroke=INK, strokeWidth=3)
for i, (x0, x1) in enumerate([(612, 630), (622, 646), (632, 656)]):
    d.path(f"M{x0},426 C{x0 + 4},432 {x1 - 6},434 {x1},440",
           f"Hackle split {i+1}", fill=NONE, stroke="#3E4854",
           strokeWidth=2, opacity=55, cap="round")

# near wing — up-right into the light, broad blade with scalloped primaries
d.path("M548,398 C600,345 640,305 672,272 Q730,225 795,200 "
       "Q750,224 744,244 Q778,238 790,246 Q748,252 736,268 "
       "Q764,268 770,278 Q730,274 716,284 Q734,292 726,302 "
       "C668,332 615,385 588,430 C575,416 560,406 548,398 Z",
       "Near wing", fill=WING_GRAD, stroke=INK, strokeWidth=5)
# iridescent wash along the near wing's leading edge
d.path("M556,390 C605,342 645,298 670,268 C705,240 748,218 782,206",
       "Wing sheen", fill=NONE, stroke="#6E84A0", strokeWidth=9, opacity=30, cap="round")
# faint separations between the primaries
for i, (x0, y0, x1, y1) in enumerate([(744, 242, 714, 268), (734, 268, 706, 292)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Primary slit {i+1}", fill=NONE,
           stroke="#05070A", strokeWidth=3, opacity=60, cap="round")

# head + bill — one silhouette: low crown running down the arched culmen
# to the hooked tip, bristles shading the bill base
d.path("M600,366 C606,354 618,348 632,350 C660,352 700,360 728,378 "
       "C742,388 750,398 744,406 C730,412 700,414 676,410 "
       "C668,420 656,424 644,422 C624,420 608,408 602,392 "
       "C598,382 598,374 600,366 Z",
       "Head and bill", fill=lin(640, 350, 730, 415, (0, "#2C323A"), (1, "#121519")),
       stroke=INK, strokeWidth=4.5)
# gape line + the pale culmen sheen
d.path("M664,400 C692,408 720,408 742,400", "Gape", fill=NONE,
       stroke="#05070A", strokeWidth=3, opacity=60, cap="round")
d.path("M656,360 C685,356 714,366 734,384", "Culmen sheen", fill=NONE,
       stroke="#6E7E92", strokeWidth=3, opacity=45, cap="round")
# nasal bristles — short strokes lying forward over the bill base
for i, (x0, y0) in enumerate([(676, 368), (684, 372), (692, 376), (700, 380)]):
    d.path(f"M{x0},{y0} L{x0 + 20},{y0 + 8}",
           f"Bristle {i+1}", fill=NONE, stroke="#0A0D11", strokeWidth=3, cap="round")
# nostril dot
d.shape("ellipse", "Nostril", x=694, y=384, width=7, height=5,
        fill="#05070A", opacity=80, stroke=NONE)

# the eye — dark amber bead under a low brow
d.shape("ellipse", "Eye", x=626, y=372, width=17, height=17,
        fill="#4A3016", stroke="#0C0E12", strokeWidth=2.5)
d.shape("ellipse", "Eye pupil", x=631, y=377, width=7, height=7,
        fill="#0A0806", stroke=NONE)
d.shape("ellipse", "Eye glint", x=629, y=375, width=4, height=4,
        fill="#F0E8D0", opacity=85, stroke=NONE)
d.path("M616,368 C628,362 642,362 652,368", "Brow shade", fill=NONE,
       stroke="#0C0F13", strokeWidth=6, opacity=55, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#10161C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6E0E8", strokeWidth=3, opacity=28)

# --- name -------------------------------------------------------------------------
r1 = d.text("COMMON RAVEN", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#DCE6EE", justify="center")

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
b = find(layers, r1["id"])["bounds"]
print("name bounds", {k: round(v) for k, v in b.items()})
assert b["width"] <= 800 and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("common-raven-V1R00")

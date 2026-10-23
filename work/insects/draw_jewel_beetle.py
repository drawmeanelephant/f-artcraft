#!/usr/bin/env python3
"""Jewel beetle — field plate V1R00. Three-quarter dorsal view, the beetle
drawn upright then tilted so the near flank shows; elytra run
green -> gold -> copper in one gradient with a hard specular streak,
antennae kept fine; near-black plate so the sheen does the work. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jewel Beetle — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#160E08"

def lin(angle, *stops):
    return {"gradient": {"kind": "linear", "angle": angle, "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def linp(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1], "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def disc_pt(deg, r=R):
    a = math.radians(deg)
    return (CX + r * math.cos(a), CY + r * math.sin(a))

def cubic(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    mt = 1 - t
    x = mt**3*x0 + 3*mt*mt*t*x1 + 3*mt*t*t*x2 + t**3*x3
    y = mt**3*y0 + 3*mt*mt*t*y1 + 3*mt*t*t*y2 + t**3*y3
    tx = 3*mt*mt*(x1-x0) + 6*mt*t*(x2-x1) + 3*t*t*(x3-x2)
    ty = 3*mt*mt*(y1-y0) + 6*mt*t*(y2-y1) + 3*t*t*(y3-y2)
    return x, y, tx, ty

def frame(p, t):
    x, y, tx, ty = cubic(p, t)
    ln = math.hypot(tx, ty) or 1
    return x, y, tx / ln, ty / ln, -ty / ln, tx / ln

def ribbon(p, widths, n=32):
    left, right = [], []
    k = len(widths) - 1
    for i in range(n + 1):
        t = i / n
        x, y, ux, uy, nx, ny = frame(p, t)
        s = t * k; j = min(int(s), k - 1); f = s - j
        w = (widths[j] * (1 - f) + widths[j + 1] * f) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    pts = left + right[::-1]
    return f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(
        f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"

# --- backdrop + near-black plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#0C0C12"), (1, "#030304")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#26242E"), (0.6, "#17161E"), (1, "#0B0B10")),
        stroke="#2E2C38", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#44424F", strokeWidth=3, opacity=45)
# faint concentric lathe rings on the dark plate
for i, (w, op) in enumerate([(640, 12), (500, 10), (360, 10), (230, 8)]):
    d.shape("ellipse", f"Lathe ring {i+1}", x=500 - w / 2, y=460 - w / 2,
            width=w, height=w, fill=NONE, stroke="#3C3A46", strokeWidth=3, opacity=op)
# scattered gold dust — the only sparkle the plate is allowed
for i, (x, y, w) in enumerate([(190, 220, 5), (788, 196, 6), (838, 430, 4), (168, 560, 5),
                               (268, 762, 6), (720, 742, 5), (360, 150, 4), (640, 158, 5),
                               (222, 402, 4), (790, 600, 6), (500, 122, 4), (336, 668, 4)]):
    d.shape("ellipse", f"Gold dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8A44E", opacity=40, stroke=NONE)
# soft sheen sweeping the upper-left of the disc
d.shape("ellipse", "Plate sheen", x=190, y=110, width=420, height=260,
        fill="#5E5C6E", opacity=14, stroke=NONE)

# soft shadow the beetle casts on the plate
d.shape("ellipse", "Beetle shadow", x=370, y=640, width=300, height=44,
        fill="#000000", opacity=40, stroke=NONE)

# everything drawn from here on is the beetle; collect it so it can be tilted
BEETLE = []
_call = d.call
def _capture(tool, args, label):
    r = _call(tool, args, label)
    if tool in ("draw_path", "draw_shape") and isinstance(r, dict) and "id" in r:
        BEETLE.append(r["id"])
    return r
d.call = _capture

BRONZE = "#2A1A10"
ELY_GRAD = linp(500, 320, 500, 700,
                (0, "#3ECF8E"), (0.38, "#8FCC3E"), (0.62, "#E8BE3E"),
                (0.85, "#C06E2A"), (1, "#7E3E1C"))

# --- antennae: fine, short, faintly serrated -------------------------------------
def antenna(name, base, ctrl, tip, serr_side):
    bx, by = base
    d.path(f"M{bx},{by} Q{ctrl[0]},{ctrl[1]} {tip[0]},{tip[1]}", f"{name} shaft",
           fill=NONE, stroke=BRONZE, strokeWidth=3.5, cap="round")
    # tiny serration ticks along the outer edge of the curve
    for j, t in enumerate([0.35, 0.55, 0.75, 0.9]):
        x = (1-t)**2*bx + 2*(1-t)*t*ctrl[0] + t*t*tip[0]
        y = (1-t)**2*by + 2*(1-t)*t*ctrl[1] + t*t*tip[1]
        d.path(f"M{x:.0f},{y:.0f} L{x + serr_side*9:.0f},{y - 5:.0f}", f"{name} tooth {j+1}",
               fill=NONE, stroke=BRONZE, strokeWidth=3, cap="round")
    d.shape("ellipse", f"{name} tip", x=tip[0]-3, y=tip[1]-3, width=6, height=6,
            fill="#5E3A1E", stroke=NONE)

antenna("Far antenna", (466, 236), (438, 196), (418, 170), -1)
antenna("Near antenna", (534, 236), (562, 196), (582, 170), 1)

# --- legs: short stubs just showing past the body edge ----------------------------
def leg(name, hip, foot, side):
    hx, hy = hip; fx, fy = foot
    mx = hx + side * 30; my = (hy + fy) / 2 - 12
    d.path(f"M{hx},{hy} Q{mx},{my} {fx},{fy}", f"{name} ink",
           fill=NONE, stroke=INK, strokeWidth=8, cap="round")
    d.path(f"M{hx},{hy} Q{mx},{my} {fx},{fy}", name,
           fill=NONE, stroke="#4A2E18", strokeWidth=5, cap="round")
    d.path(f"M{fx},{fy} L{fx + side*10},{fy + 8}", f"{name} tarsus",
           fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")

leg("Far fore leg", (445, 320), (420, 352), -1)
leg("Far mid leg", (428, 440), (402, 470), -1)
leg("Far hind leg", (434, 560), (414, 592), -1)
leg("Near fore leg", (555, 320), (582, 352), 1)
leg("Near mid leg", (572, 440), (600, 472), 1)
leg("Near hind leg", (566, 560), (590, 592), 1)

# --- elytra ----------------------------------------------------------------------
# far (left) elytron
d.path("M500,332 C446,340 416,404 420,490 C424,576 458,648 500,688 "
       "L500,332 Z", "Far elytron", fill=ELY_GRAD, stroke=INK, strokeWidth=5)
# near (right) elytron — a shade wider so the tilt reads as three-quarter
d.path("M500,332 C560,340 592,404 587,490 C582,576 546,648 500,688 "
       "L500,332 Z", "Near elytron", fill=ELY_GRAD, stroke=INK, strokeWidth=5)
# suture line
d.path("M500,336 L500,684", "Elytra suture", fill=NONE,
       stroke="#0E0806", strokeWidth=3, opacity=80)

# engraved striae curving with each elytron
for name, xoff in [("Far", -38), ("Far", -64), ("Near", 40), ("Near", 66)]:
    sgn = 1 if xoff > 0 else -1
    d.path(f"M{500 + xoff*0.4:.0f},348 C{500 + xoff*1.35:.0f},420 "
           f"{500 + xoff*1.45:.0f},540 {500 + xoff*0.55:.0f},652",
           f"{name} stria {abs(xoff)}", fill=NONE, stroke="#3A2410",
           strokeWidth=3, opacity=38, cap="round")
# puncture rows between the striae
for j, (x, y) in enumerate([(474, 420), (468, 500), (476, 580), (452, 460), (458, 545),
                            (530, 420), (536, 500), (528, 580), (552, 460), (548, 545)]):
    d.shape("ellipse", f"Puncture {j+1}", x=x, y=y, width=5, height=7,
            fill="#241608", opacity=40, stroke=NONE)

# near-side flank (epipleuron): dark copper band visible along the right edge
d.path("M584,420 C592,480 586,560 556,624 C574,560 578,480 570,424 Z",
       "Near flank band", fill="#5E2E14", opacity=75, stroke=NONE)
d.path("M584,414 C592,470 588,540 566,608", "Near flank edge light",
       fill=NONE, stroke="#E8A04E", strokeWidth=3, opacity=55, cap="round")

# speculars: a hard streak on the near elytron, a soft one on the far
d.path("M542,352 C566,412 570,500 556,590 C560,500 556,416 534,356 Z",
       "Near specular band", fill="#FFF4D0", opacity=80, stroke=NONE)
d.path("M548,360 C566,420 568,500 558,576", "Near specular core",
       fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=85, cap="round")
d.path("M452,360 C432,420 430,500 444,584 C434,500 438,420 458,362 Z",
       "Far specular band", fill="#D8F0C8", opacity=34, stroke=NONE)
d.shape("ellipse", "Elytra broad gloss", x=470, y=350, width=130, height=90,
        fill="#EAFFD8", opacity=18, stroke=NONE)
# rim light along the top of the elytra base
d.path("M428,380 C452,344 548,344 578,382", "Elytra rim light",
       fill=NONE, stroke="#F2E8B0", strokeWidth=4, opacity=60, cap="round")
# tip shadow at the apex
d.path("M486,664 C494,676 506,676 514,664 C508,678 492,678 486,664 Z",
       "Apex shadow", fill="#2E1408", opacity=60, stroke=NONE)

# scutellum: small triangle tucked between the elytra bases
d.path("M500,336 L514,362 L486,362 Z", "Scutellum",
       fill=rad((0, "#C89A3A"), (1, "#6E4418")), stroke=INK, strokeWidth=3)

# --- pronotum: wide, flattened trapezoid the head sinks into ------------------------
d.path("M424,354 C422,318 442,292 500,288 C558,292 578,318 576,354 "
       "C544,370 456,370 424,354 Z", "Pronotum",
       fill=rad((0, "#E8C85A"), (0.55, "#B07C2E"), (1, "#5E3814")),
       stroke=INK, strokeWidth=5)
d.path("M444,308 C464,294 536,294 556,310", "Pronotum rim light",
       fill=NONE, stroke="#FFF0B8", strokeWidth=4, opacity=70, cap="round")
d.path("M458,302 C476,294 514,293 534,301", "Pronotum specular",
       fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=70, cap="round")
d.path("M436,340 C466,356 534,356 564,340", "Pronotum base shadow",
       fill=NONE, stroke="#3A2008", strokeWidth=6, opacity=40, cap="round")

# --- head: a low wedge, mostly sunk under the pronotum's front edge ------------------
d.path("M460,266 C460,242 478,226 500,226 C522,226 540,242 540,266 "
       "C540,282 522,292 500,292 C478,292 460,282 460,266 Z", "Head",
       fill=rad((0, "#6E4A22"), (0.6, "#38200E"), (1, "#160A04")),
       stroke=INK, strokeWidth=4)
d.path("M472,240 C486,232 514,232 528,240", "Head rim light",
       fill=NONE, stroke="#E8B060", strokeWidth=3.5, opacity=60, cap="round")
# large compound eyes hugging the head's flanks
d.shape("ellipse", "Far eye", x=446, y=250, width=28, height=36,
        fill=rad((0, "#5E4A30"), (1, "#140C06")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Near eye", x=526, y=250, width=28, height=36,
        fill=rad((0, "#5E4A30"), (1, "#140C06")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Far eye glint", x=453, y=256, width=6, height=6,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Near eye glint", x=533, y=256, width=6, height=6,
        fill="#FFFFFF", opacity=80, stroke=NONE)

d.call = _call
# tilt the whole beetle a touch so the near flank reads as three-quarter dorsal
d.call("transform", {"ids": BEETLE, "rotate": 9, "scale": 112, "origin": [500, 450]},
       "tilt beetle")

# --- caption --------------------------------------------------------------------------
d.text("JEWEL BEETLE", "Name", x=500, y=940, size=56, font="Virelai Sans",
       color="#EEDFB8", justify="center")
o = d.text("COLEOPTERA", "Order", x=500, y=975, size=22, font="Virelai Sans",
           color="#A89478", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Order tracking", ids=[o["id"]], tracking=400)

d.finish("jewel-beetle-V1R00")

#!/usr/bin/env python3
"""Galapagos tortoise — field plate V1R00. An island's memory walking on four
columns: the dome carapace in profile, elephantine legs, the long neck
reaching ahead and up. Highlands plate, century mood — cool mist on the
grass, a small finch riding the shell's shoulder. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Galapagos Tortoise — Field Plate", 1000, 1000)
rng = random.Random(7)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#14100A"                    # warm dark ink, never pure black

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

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0B100C"), (1, "#030504"))
PLATE_GRAD = rad((0, "#96A88E"), (0.55, "#546A56"), (1, "#1E2A20"))
SHELL_GRAD = rad((0, "#7A643E"), (0.5, "#54452C"), (1, "#2A2014"))
SKIN_GRAD  = lin(0, 420, 0, 800, (0, "#6E6250"), (0.55, "#4C4234"), (1, "#282216"))
FLOOR_GRAD = lin(0, 770, 0, 890, (0, "#4E6244"), (1, "#1A2416"))

# --- backdrop + highland plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#96A88E", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#22301F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4DEC4", strokeWidth=3, opacity=30)

# highland light, cool and diffuse
d.shape("ellipse", "Highland light", x=300, y=130, width=400, height=260,
        fill=rad((0, "#E4EAD2", 16), (0.6, "#E4EAD2", 7), (1, "#E4EAD2", 0)), stroke=NONE)
# mist bands drifting behind the subject
for i, (x, y, w, h, op) in enumerate([(500, 330, 620, 60, 12), (430, 405, 560, 44, 10),
                                      (560, 500, 640, 52, 9)]):
    d.shape("ellipse", f"Mist {i+1}", x=x - w/2, y=y - h/2, width=w, height=h,
            fill="#DCE6CE", opacity=op, stroke=NONE)
# seed-head motes
for i in range(22):
    a = rng.uniform(0, math.tau); rr = math.sqrt(rng.uniform(0, 1)) * 380
    x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
    w = rng.uniform(2.5, 6)
    d.shape("ellipse", f"Mote {i+1}", x=x - w/2, y=y - w/2, width=w, height=w,
            fill="#C4D2AA", opacity=rng.uniform(12, 26), stroke=NONE)

# --- far-side legs first: darker, half-hidden behind the shell ------------------
def leg(cxp, top, foot_y, w_, label, grad, dark=False):
    op = 90 if not dark else 100
    d.path(f"M{cxp - w_/2},{top} C{cxp - w_/2 - 4},{top + 50} {cxp - w_/2 + 6},{foot_y - 40} "
           f"{cxp - w_/2 - 10},{foot_y} C{cxp - 10},{foot_y + 14} {cxp + 10},{foot_y + 14} "
           f"{cxp + w_/2 + 10},{foot_y} C{cxp + w_/2 - 6},{foot_y - 40} {cxp + w_/2 + 4},{top + 50} "
           f"{cxp + w_/2},{top} Z",
           label, fill=grad, stroke=INK, strokeWidth=3)
    # wrinkle rings + toe claws on the foot pad
    for j in range(2):
        wy_ = top + 44 + j * 38
        d.path(f"M{cxp - w_/2 + 4},{wy_} C{cxp - 10},{wy_ + 10} {cxp + 10},{wy_ + 10} {cxp + w_/2 - 4},{wy_}",
               f"{label} wrinkle {j+1}", fill=NONE, stroke="#241C10",
               strokeWidth=3, opacity=45, cap="round")
    for j in range(3):
        cx_ = cxp - w_/2 + 10 + j * (w_ - 14) / 2
        d.path(f"M{cx_ - 7},{foot_y + 2} L{cx_},{foot_y + 15} L{cx_ + 8},{foot_y + 2} Z",
               f"{label} claw {j+1}", fill="#C9BC98", stroke=INK, strokeWidth=2)

leg(415, 640, 788, 62, "Hind leg far", lin(0, 640, 0, 800, (0, "#443A2C"), (1, "#1E180E")))
leg(600, 648, 794, 66, "Fore leg far", lin(0, 640, 0, 800, (0, "#443A2C"), (1, "#1E180E")))

# --- neck + head: drawn before the shell so the shell lip overlaps the base ----
d.path("M676,608 C690,560 706,520 726,488 C738,468 748,452 756,436 "
       "C772,448 780,462 778,478 C770,514 754,556 736,608 Z",
       "Neck", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M694,560 C712,556 730,548 744,536",
                        "M706,522 C722,516 736,506 746,494",
                        "M720,478 C732,472 742,464 750,454"]):
    d.path(dd, f"Neck wrinkle {i+1}", fill=NONE, stroke="#2A2216",
           strokeWidth=3.5, opacity=55, cap="round")
# head: low wedge, blunt snout reaching ahead, worn patient eye
d.path("M742,444 C742,422 754,406 776,402 C796,398 816,408 824,426 "
       "C828,438 824,452 812,460 C798,470 778,474 762,470 "
       "C750,466 742,456 742,444 Z",
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Eye", x=776, y=426, width=14, height=15, fill="#141008", stroke=NONE)
d.shape("ellipse", "Eye glint", x=779, y=428, width=4, height=4, fill="#E4DCC0", opacity=85, stroke=NONE)
d.shape("ellipse", "Nostril", x=812, y=424, width=5, height=4, fill="#1E180E", stroke=NONE)
d.path("M784,458 C792,462 802,462 810,458", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
d.shape("ellipse", "Head shine", x=760, y=410, width=26, height=10,
        fill="#C9C0A0", opacity=22, stroke=NONE)

# --- the carapace: dome profile with scute seams ------------------------------
d.path("M284,664 C280,548 348,436 486,412 "
       "C598,394 704,452 726,552 C734,592 732,628 722,654 "
       "C682,670 622,678 560,678 L420,678 C360,676 306,670 284,664 Z",
       "Carapace", fill=SHELL_GRAD, stroke=INK, strokeWidth=5)
# plastron lip: a lighter rim along the bottom edge
d.path("M300,652 C360,664 440,670 520,670 C600,670 674,662 716,646",
       "Plastron lip", fill=NONE, stroke="#9A8658", strokeWidth=5, opacity=55, cap="round")
# marginal ticks along the rim
for i in range(16):
    t = i / 15
    x = 304 + t * 404
    y = 656 + 8 * math.sin(t * math.pi)
    d.path(f"M{x:.0f},{y - 8:.0f} L{x:.0f},{y + 4:.0f}",
           f"Marginal {i+1}", fill=NONE, stroke="#2A2014", strokeWidth=2.5,
           opacity=55, cap="round")
# costal scute seams: curves following the dome's fall
for i, (x0, y0, c1x, c1y, x1, y1) in enumerate([
        (372, 470, 352, 540, 344, 640),
        (462, 428, 440, 520, 430, 650),
        (562, 420, 560, 510, 552, 655),
        (654, 452, 664, 540, 646, 650)]):
    d.path(f"M{x0},{y0} C{c1x},{c1y} {c1x},{c1y + 40} {x1},{y1}",
           f"Costal seam {i+1}", fill=NONE, stroke="#241C10",
           strokeWidth=4, opacity=60, cap="round")
# growth lines inside each costal plate — faint arcs echoing the dome
for i, (x, y, w, h) in enumerate([(410, 540, 100, 120), (505, 520, 110, 130),
                                  (605, 535, 96, 115), (340, 555, 60, 90)]):
    d.path(f"M{x - w/2},{y} C{x - w/4},{y + h*0.35} {x + w/4},{y + h*0.35} {x + w/2},{y}",
           f"Growth {i+1}", fill=NONE, stroke="#8A7648", strokeWidth=2.5,
           opacity=30, cap="round")
# weathering: crown highlight + a few pale scuffs on the dome
d.path("M400,452 C470,424 570,422 640,452", "Crown light", fill=NONE,
       stroke="#C4B284", strokeWidth=10, opacity=25, cap="round")
for i, (x, y, w) in enumerate([(520, 470, 26), (620, 500, 20), (450, 500, 16)]):
    d.path(f"M{x},{y} L{x + w},{y + w*0.3:.0f}", f"Scuff {i+1}", fill=NONE,
           stroke="#B8A674", strokeWidth=3, opacity=30, cap="round")

# --- near legs: front column stepping, rear column planted ----------------------
leg(360, 655, 806, 74, "Hind leg", lin(0, 640, 0, 820, (0, "#5E5240"), (1, "#262012")))
leg(652, 660, 800, 78, "Fore leg", lin(0, 640, 0, 820, (0, "#5E5240"), (1, "#262012")))

# --- grass floor: crest at y812, bottom closes on the disc arc -------------------
fy = 812
fdx = math.sqrt(R * R - (fy - CY) ** 2)
d.path(f"M{CX-fdx:.1f},{fy} C320,798 420,806 540,800 C640,796 720,804 {CX+fdx:.1f},{fy} "
       f"A{R},{R} 0 0 1 {CX-fdx:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{CX-fdx+8:.1f},{fy-2} C330,796 430,802 540,796 C640,792 720,800 {CX+fdx-8:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#D4DEC4", strokeWidth=4, opacity=35, cap="round")
# grass blades pricking up off the crest
for i, (x, y, dx, h) in enumerate([(250, 812, -14, 44), (290, 814, 8, 52), (340, 816, -6, 38),
                                   (420, 816, 10, 46), (560, 812, -8, 40), (620, 814, 12, 50),
                                   (700, 810, -10, 42), (740, 806, 6, 36), (480, 818, 4, 34)]):
    assert on_disc(x + dx, y - h, 8), (x, y)
    d.path(f"M{x},{y + 4} C{x + dx*0.4},{y - h*0.5} {x + dx},{y - h} {x + dx + 4},{y - h + 6}",
           f"Blade {i+1}", fill=NONE, stroke="#3E5234", strokeWidth=4, cap="round")
# low mist wisp lying on the grass, kept inside the disc's lower arc
my = 800
mdx = math.sqrt(R * R - (my - CY) ** 2) - 20
d.path(f"M{CX-mdx:.0f},{my} C{CX-mdx*0.4:.0f},{my-14} {CX+mdx*0.4:.0f},{my-14} {CX+mdx:.0f},{my}",
       "Ground mist", fill=NONE, stroke="#DCE6CE", strokeWidth=12, opacity=8, cap="round")

# --- the finch: a small dark passenger on the shell's shoulder -------------------
d.path("M396,414 C390,398 398,384 414,382 C430,380 442,390 442,404 "
       "C442,416 432,424 418,424 C406,424 398,420 396,414 Z",
       "Finch body", fill="#26231C", stroke=INK, strokeWidth=2)
d.path("M398,410 L372,404 L378,416 L396,418 Z", "Finch tail",
       fill="#26231C", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Finch head", x=436, y=382, width=18, height=18,
        fill="#26231C", stroke=INK, strokeWidth=2)
d.path("M452,388 L466,392 L452,396 Z", "Finch beak", fill="#3A3428", stroke=INK, strokeWidth=1.5)
d.shape("ellipse", "Finch eye", x=443, y=387, width=4, height=4, fill="#C9C0A0", opacity=90, stroke=NONE)
for i in range(2):
    d.path(f"M{418 + i*8},424 L{416 + i*8},434", f"Finch leg {i+1}", fill=NONE,
           stroke=INK, strokeWidth=2, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0C120A", strokeWidth=6)

# --- name ----------------------------------------------------------------------
r1 = d.text("GALAPAGOS TORTOISE", "Name", x=500, y=962, size=50, font="Virelai Sans",
            color="#D8DEC2", justify="center")

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

d.finish("galapagos-tortoise-V1R00")

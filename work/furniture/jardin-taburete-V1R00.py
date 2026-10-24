#!/usr/bin/env python3
"""Jardín taburete — field plate V1R00. A construction study of the armless
wood-and-hide chair made in Jardín, Antioquia: four splayed posts, a hide
seat stretched over the rails and laced beneath, carrying a slight sag,
and a wide hide band for a backrest between the two rear posts. Near-side
three-quarter view on a cool indigo disc; warm hide, no painted ornament —
the joinery is the drawing. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Jardín Taburete — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241610"


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def rim_x(y, side=-1):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)


def quad(pts):
    return ("M%.1f,%.1f " % pts[0] +
            " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z")


def beam(top, bot, wt, wb):
    """tapered post quad: (x,y) endpoints, half-widths wt/wb along normal."""
    tx, ty = top; bx, by = bot
    dx, dy = bx - tx, by - ty
    ln = math.hypot(dx, dy); nx, ny = -dy / ln, dx / ln
    return [(tx + nx * wt, ty + ny * wt), (tx - nx * wt, ty - ny * wt),
            (bx - nx * wb, by - ny * wb), (bx + nx * wb, by + ny * wb)]


# --- palette ---------------------------------------------------------------------
BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C1226"), (1, "#04060F"))
PLATE_GRAD = rad((0, "#4E639E"), (0.6, "#31427A"), (1, "#151E42"))
WOOD = lin(500, 280, 500, 750, (0, "#7A5230"), (0.6, "#5A3820"), (1, "#38200F"))
WOOD_DIM = lin(500, 280, 500, 750, (0, "#5C3E24"), (1, "#2A180B"))
HIDE = lin(430, 510, 640, 620, (0, "#D9A868"), (0.55, "#A8743C"), (1, "#7A4A22"))
HIDE_BACK = lin(450, 280, 670, 380, (0, "#BE8C52"), (0.6, "#96622F"), (1, "#6E4120"))
RAWHIDE = "#EFDDB8"
FLOOR = lin(0, 770, 0, 880, (0, "#2E3D72"), (0.6, "#1B2750"), (1, "#0D1430"))

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=58, y=18, width=884, height=884, fill="#8FA4E0", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0E1530", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8B6E0", strokeWidth=3, opacity=40)

# cool moonlit pool upper-left, a few drifting motes
d.shape("ellipse", "Light pool", x=270, y=160, width=340, height=200,
        fill="#B8C6F0", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(310, 270, 18), (440, 210, 14), (600, 220, 18),
                               (720, 320, 14), (250, 430, 16), (540, 300, 12)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mote {i+1}", x=x - w / 2, y=y - w / 3, width=w, height=w * 0.66,
            fill="#C4D0F4", opacity=13, stroke=NONE)

# --- floor, closing on the disc arc ----------------------------------------------------
fy = 772
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C340,758 420,782 500,774 C580,766 670,770 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C340,758 420,782 500,774 C580,766 670,770 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#8FA0DC", strokeWidth=4, opacity=38, cap="round")
d.shape("ellipse", "Chair shadow", x=360, y=756, width=330, height=26,
        fill="#05070F", opacity=38, stroke=NONE)

# --- far legs + rear posts (behind the seat plane) --------------------------------------
def post(top, bot, wt, wb, label, fill):
    d.path(quad(beam(top, bot, wt, wb)), label, fill=fill, stroke=INK, strokeWidth=4)

# back-left post runs foot -> backrest top in one line (seat covers the joint)
post((452, 296), (448, 706), 11, 9, "Post BL", WOOD_DIM)
post((650, 278), (664, 712), 12, 10, "Post BR", WOOD)
# far stretchers between the back legs, low
d.path(quad(beam((450, 660), (662, 646), 8, 8)), "Stretcher back", fill=WOOD_DIM,
       stroke=INK, strokeWidth=3.5)

# --- hide backrest band laced between the rear posts ------------------------------------
d.path("M452,306 Q556,288 660,290 L658,366 Q556,378 454,374 Z",
       "Back band", fill=HIDE_BACK, stroke=INK, strokeWidth=4)
# slight sag shading across the band's belly
d.path("M462,330 Q556,318 650,318 L650,344 Q556,334 462,348 Z",
       "Band shade", fill="#5E3A1C", opacity=35, stroke=NONE)
# lacing: X-stitches where the hide wraps each post
for i in range(4):
    y = 314 + i * 14
    for x0, sgn in ((449, 1), (663, -1)):
        d.path(f"M{x0},{y} l{sgn * 8},6 M{x0},{y + 6} l{sgn * 8},-6",
               f"Back lace {'L' if sgn > 0 else 'R'}{i+1}", fill=NONE,
               stroke=RAWHIDE, strokeWidth=2.6, cap="round")
# post caps
d.path("M446,298 Q452,288 458,298", "Cap L", fill=NONE, stroke="#8A6238", strokeWidth=5, cap="round")
d.path("M644,280 Q650,270 656,280", "Cap R", fill=NONE, stroke="#8A6238", strokeWidth=5, cap="round")

# --- seat: wood rails under a stretched hide panel --------------------------------------
# rails (wood) peeking under the hide edges
d.path(quad([(368, 592), (580, 572), (580, 596), (368, 616)]), "Rail front",
       fill=WOOD, stroke=INK, strokeWidth=4)
d.path(quad([(580, 572), (654, 518), (654, 542), (580, 596)]), "Rail right",
       fill=WOOD, stroke=INK, strokeWidth=4)
# shadow under the seat plane so gaps read as shade, not sky
d.path(quad([(382, 586), (576, 566), (648, 516), (454, 536)]),
       "Under-seat shade", fill="#140C06", opacity=55, stroke=NONE)
# hide panel: front edge bows down a touch — the sag
d.path("M372,582 Q474,602 578,562 L652,508 L448,530 Q410,556 372,582 Z",
       "Seat hide", fill=HIDE, stroke=INK, strokeWidth=4.5)
# sag shading pooled at centre-front of the panel
d.shape("ellipse", "Seat sag", x=440, y=556, width=150, height=26,
        fill="#5E3A1C", opacity=30, stroke=NONE)
# drop edge: the hide rolled over the front rail
d.path("M372,582 Q474,602 578,562 L578,574 Q474,612 372,594 Z",
       "Seat drop edge", fill="#8A5A2C", stroke=INK, strokeWidth=3)
# rawhide lacing — V-loops over the front and right edges
for i in range(10):
    t = i / 9
    x = 380 + (572 - 380) * t
    y = 584 + (566 - 584) * t + 6 * math.sin(math.pi * t)
    d.path(f"M{x:.0f},{y:.0f} q2,10 8,12", f"Lace F{i+1}", fill=NONE,
           stroke=RAWHIDE, strokeWidth=2.6, opacity=90, cap="round")
for i in range(5):
    t = i / 4
    x = 582 + (648 - 582) * t
    y = 566 + (512 - 566) * t
    d.path(f"M{x:.0f},{y:.0f} q8,6 10,12", f"Lace R{i+1}", fill=NONE,
           stroke=RAWHIDE, strokeWidth=2.6, opacity=90, cap="round")

# --- near legs + near stretchers (in front of the seat plane) ----------------------------
post((384, 604), (356, 746), 13, 10, "Leg FL", WOOD)
post((572, 588), (588, 742), 13, 10, "Leg FR", WOOD)
# front + side stretchers, ≥3pt — the essential thin geometry kept fat
d.path(quad(beam((366, 668), (584, 660), 8, 8)), "Stretcher front", fill=WOOD,
       stroke=INK, strokeWidth=3.5)
d.path(quad(beam((586, 656), (660, 634), 7, 7)), "Stretcher right", fill=WOOD,
       stroke=INK, strokeWidth=3.5)
d.path(quad(beam((362, 672), (446, 650), 7, 7)), "Stretcher left", fill=WOOD_DIM,
       stroke=INK, strokeWidth=3.5)
# pegged joinery: peg head at each stretcher socket
for i, (x, y) in enumerate([(368, 668), (582, 660), (588, 654), (366, 670)]):
    d.shape("ellipse", f"Peg {i+1}", x=x - 4, y=y - 4, width=9, height=9,
            fill="#2A180B", stroke=NONE)
    d.shape("ellipse", f"Peg dot {i+1}", x=x - 1, y=y - 2, width=3, height=3,
            fill="#9A7448", stroke=NONE)
# feet pads
for i, (x, y) in enumerate([(356, 746), (588, 742), (448, 706), (664, 712)]):
    d.shape("ellipse", f"Foot {i+1}", x=x - 12, y=y - 4, width=24, height=9,
            fill="#2A180B", stroke=NONE)
# contact shade under the back feet on the receding floor
d.shape("ellipse", "Foot shade BL", x=426, y=704, width=48, height=12,
        fill="#05070F", opacity=30, stroke=NONE)
d.shape("ellipse", "Foot shade BR", x=640, y=710, width=52, height=12,
        fill="#05070F", opacity=30, stroke=NONE)

# seat grain — two faint strokes following the hide's give
d.path("M400,568 Q480,584 560,556", "Seat grain 1", fill=NONE,
       stroke="#6E4522", strokeWidth=3, opacity=45, cap="round")
d.path("M420,540 Q490,552 560,534", "Seat grain 2", fill=NONE,
       stroke="#6E4522", strokeWidth=3, opacity=35, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0E1530", strokeWidth=6)

# --- caption -----------------------------------------------------------------------------
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
    n = d.text(name, "Name", x=500, y=930, size=56, font="Virelai Sans",
               color="#E8D9BC", justify="center")
    m = d.text(mats, "Materials", x=500, y=966, size=23, font="Virelai Sans",
               color="#9AA6D0", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=50)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=280)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" % (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]


caption("JARDÍN TABURETE", "WOOD · HIDE")
d.finish("jardin-taburete-V1R00")

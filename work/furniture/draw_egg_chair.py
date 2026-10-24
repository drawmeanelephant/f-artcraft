#!/usr/bin/env python3
"""Egg chair — furniture field plate V1R00. Front near-three-quarter of a
swivel pod chair: a tall upholstered shell tilting back, its inner facing
visible inside the opening, wing lobes curling in at mid-height, a plump
seat cushion at the bowl, riding a cast-aluminium column and four-star
base. Wool plate, cocoon mood — the chair turns away from the room.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Egg Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A120A"   # warm dark, not black
EXTENT = []


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


def smooth(pts, closed=False, move=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#15161A"), (1, "#08090B")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#66685C", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#585A50"), (0.6, "#3C3E38"), (1, "#20221E")),
        stroke="#0F100D", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D2D4C4", strokeWidth=3, opacity=25)
d.shape("ellipse", "Back glow", x=210, y=150, width=540, height=540,
        fill=rad((0, "#F0A868", 17), (0.6, "#A86840", 5), (1, "#6E4A32", 0)), stroke=NONE)

FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#5E6054", 34), (1, "#141510", 72)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E0E2D0", strokeWidth=2, opacity=18)

# --- shadow ---------------------------------------------------------------------
d.shape("ellipse", "Chair shadow", x=300, y=664, width=420, height=54,
        fill=rad((0, "#050604", 64), (0.6, "#050604", 28), (1, "#050604", 0)), stroke=NONE)

# --- swivel base: far spokes, column, near spokes ------------------------------------
ALU = ((0, "#7E868C"), (0.3, "#D6DADE"), (0.5, "#5A6166"), (0.75, "#9AA2A8"), (1, "#2E3336"))


def spoke(name, cx, cy, ex, ey, w, dark=False):
    """One star foot: a tapered arm from the column hub out to a small pad."""
    dx, dy = ex - cx, ey - cy
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    pts = [(cx + nx * w, cy + ny * w), (ex + nx * w * 0.45, ey + ny * w * 0.45 - 4),
           (ex, ey - 6), (ex - nx * w * 0.45, ey - ny * w * 0.45 - 4),
           (cx - nx * w, cy - ny * w)]
    d.path(smooth(pts, closed=True), name,
           fill=lin((cx, cy), (ex, ey), *ALU), stroke=INK, strokeWidth=2.5,
           join="round", opacity=60 if dark else 100)
    EXTENT.append((ex, ey))
    # pad foot
    d.shape("ellipse", f"{name} pad", x=round(ex - 9), y=round(ey - 8), width=18, height=10,
            fill=rad((0, "#3A3E42"), (1, "#141618")), stroke=INK, strokeWidth=1.6,
            opacity=60 if dark else 100)


HUB = (508, 664)
# far pair first
spoke("Spoke far L", HUB[0], HUB[1], 416, 692, 9, dark=True)
spoke("Spoke far R", HUB[0], HUB[1], 596, 690, 9, dark=True)
# column: slightly tapered, leaning with the shell
col = [(492, 560), (528, 558), (522, 660), (496, 662)]
d.path(smooth(col, closed=True), "Column",
       fill=lin((492, 0), (528, 0), *ALU), stroke=INK, strokeWidth=3, join="round")
EXTENT += col
d.path("M497,575 L502,650", "Column light", fill=NONE, stroke="#E8ECEF",
       strokeWidth=3, cap="round", opacity=45)
# hub cap where spokes meet the column
d.shape("ellipse", "Hub", x=486, y=650, width=46, height=26,
        fill=rad((0, "#B8BEC4"), (0.6, "#6E757C"), (1, "#2E3336")),
        stroke=INK, strokeWidth=2.5)
# near pair of spokes over the hub
spoke("Spoke near L", HUB[0], HUB[1] + 6, 388, 700, 10)
spoke("Spoke near R", HUB[0], HUB[1] + 6, 622, 698, 10)

# --- shell ---------------------------------------------------------------------------
# ovoid outline, top domed, tucked under at the bowl; slight lean back
SHELL = [(500, 176), (560, 182), (616, 214), (652, 272), (664, 344),
         (660, 420), (646, 492), (614, 556), (576, 606), (546, 636),
         (500, 646), (452, 640), (410, 614), (376, 566), (352, 500),
         (338, 420), (334, 344), (344, 266), (378, 214), (436, 184)]
shell_pts = SHELL + []  # closed loop, no long jump
d.path(smooth(SHELL, closed=True), "Shell",
       fill=lin((0, 176), (0, 646), (0, "#D8784A"), (0.35, "#B85C34"),
                (0.7, "#8A3E20"), (1, "#542412")),
       stroke=INK, strokeWidth=5, join="round")
EXTENT += SHELL

# shell rim light along the upper-left silhouette
d.path(smooth([(500, 176), (436, 184), (378, 214), (344, 266), (334, 344)]),
       "Shell rim light", fill=NONE, stroke="#F4AE80", strokeWidth=4,
       cap="round", opacity=55)

# --- inner facing: the padded opening inside the shell ---------------------------------
# the opening sits inside the outline, biased up-left as the pod tips back
IN = [(478, 240), (528, 246), (574, 272), (606, 320), (620, 382),
      (620, 446), (606, 512), (576, 566), (544, 602), (508, 620),
      (468, 616), (430, 596), (400, 556), (380, 500), (370, 438),
      (372, 368), (384, 306), (416, 266), (448, 246)]
d.path(smooth(IN, closed=True), "Inner facing",
       fill=lin((0, 240), (0, 620), (0, "#B85C34"), (0.4, "#96471F"),
                (0.8, "#6A2F14"), (1, "#421C0C")),
       stroke="#3A1808", strokeWidth=3.5, join="round")
EXTENT += IN

# cove shadow under the dome — the deepest shade of the cocoon
d.path(smooth([(478, 240), (528, 246), (574, 272), (606, 320), (620, 382),
               (596, 372), (560, 326), (510, 300), (464, 296)]),
       "Cove shadow", fill=rad((0, "#2A0F04", 55), (1, "#2A0F04", 0)), stroke=NONE)
# shell lip: outer fabric rolling over the inner edge, upper-right
d.path(smooth([(560, 182), (616, 214), (652, 272), (664, 344), (660, 420),
               (640, 414), (636, 340), (620, 268), (586, 226), (540, 196)]),
       "Shell lip", fill=lin((0, 182), (0, 420), (0, "#E8905E"), (1, "#A04A24", 0)),
       stroke=NONE)

# wing lobes curling in at mid-height
for side, pts in (("L", [(372, 420), (398, 428), (424, 452), (438, 490),
                         (436, 528), (414, 552), (388, 556), (368, 532),
                         (360, 492), (360, 452)]),
                  ("R", [(620, 392), (648, 402), (662, 436), (664, 478),
                         (654, 516), (630, 542), (600, 548), (580, 528),
                         (574, 490), (578, 444), (596, 414)])):
    d.path(smooth(pts, closed=True), f"Wing {side}",
           fill=lin((pts[0][0], 390), (pts[0][0], 560),
                    (0, "#C4683C"), (0.55, "#9A4A22"), (1, "#5E2810")),
           stroke=INK, strokeWidth=4, join="round")
    EXTENT += pts
# wing fold seams where the lobe meets the back pad
d.path("M402,440 C424,478 428,512 414,546", "Wing fold L", fill=NONE,
       stroke="#3A1808", strokeWidth=3.5, cap="round", opacity=55)
d.path("M596,424 C610,462 610,502 596,540", "Wing fold R", fill=NONE,
       stroke="#3A1808", strokeWidth=3.5, cap="round", opacity=55)

# seat cushion nestled in the bowl
seat = [(418, 540), (470, 528), (540, 526), (596, 540), (606, 570),
        (586, 600), (540, 614), (470, 614), (424, 598), (410, 570)]
d.path(smooth(seat, closed=True), "Seat cushion",
       fill=lin((0, 526), (0, 616), (0, "#D8784A"), (0.5, "#A8512C"), (1, "#6A2F14")),
       stroke=INK, strokeWidth=4, join="round")
EXTENT += seat
d.path(smooth([(418, 540), (470, 528), (540, 526), (596, 540)]),
       "Seat crown light", fill=NONE, stroke="#F4B88A", strokeWidth=4,
       cap="round", opacity=55)
# cushion welt
d.path(smooth(seat[4:] + seat[:1]), "Seat welt", fill=NONE, stroke="#3A1808",
       strokeWidth=3, cap="round", opacity=60)

# upholstery seams: centre spine and side tucks on the inner facing
d.path("M498,300 C494,368 494,440 500,510", "Spine seam", fill=NONE,
       stroke="#3A1808", strokeWidth=3, cap="round", opacity=40)
for sx, nm in ((-1, "L"), (1, "R")):
    d.path(f"M{500 + sx * 60},340 C{500 + sx * 78},410 {500 + sx * 74},470 {500 + sx * 56},520",
           f"Tuck seam {nm}", fill=NONE, stroke="#3A1808", strokeWidth=2.6,
           cap="round", opacity=32)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("egg extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 28, far


# --- caption ---------------------------------------------------------------------------
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
               color="#EEEADC", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B6B4A4", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
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


caption("EGG CHAIR", "WOOL · CAST ALUMINIUM")
d.finish("egg-chair-V1R00")

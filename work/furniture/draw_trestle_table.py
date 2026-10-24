#!/usr/bin/env python3
"""Trestle table — furniture field plate V1R00. Front-near view of a refectory
table: a thick oak plank top on two sawhorse trestles — sledge feet, splayed
posts, capital arms — joined by a long stretcher locked through the posts
with tusk tenons and wedge pegs. Breadboard end caps pinned with oak pegs,
iron studs on the feet. Deep olive plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Trestle Table — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241405"   # warm umber, never black
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


OAK = ((0, "#C89A5A"), (0.4, "#A8763E"), (0.75, "#7A5028"), (1, "#4A2E14"))
OAK_DARK = ((0, "#8A5E30"), (0.5, "#5E3C1C"), (1, "#34200C"))
IRON = rad((0, "#6E6A62"), (0.6, "#3C3832"), (1, "#1C1A16"))

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#171A15"), (1, "#090B08")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#4E5244", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4C4838"), (0.6, "#353224"), (1, "#1C1A12")),
        stroke="#0F0E09", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D2B8", strokeWidth=3, opacity=22)
d.shape("ellipse", "Warm glow", x=170, y=140, width=560, height=520,
        fill=rad((0, "#F0C880", 15), (0.6, "#A87848", 5), (1, "#6E4A30", 0)), stroke=NONE)

FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4A4636", 34), (1, "#131109", 70)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#DDD6BE", strokeWidth=2, opacity=18)

# --- shadow ------------------------------------------------------------------------
d.shape("ellipse", "Table shadow", x=240, y=664, width=520, height=56,
        fill=rad((0, "#050403", 62), (0.6, "#050403", 26), (1, "#050403", 0)), stroke=NONE)

# --- stretcher: long beam behind the posts --------------------------------------------
str_pts = [(318, 588), (682, 588), (688, 600), (682, 614), (318, 614), (312, 600)]
d.path(smooth(str_pts, closed=True), "Stretcher",
       fill=lin((0, 588), (0, 614), *OAK_DARK), stroke=INK, strokeWidth=3.5, join="round")
EXTENT += str_pts
d.path("M330,594 L672,594", "Stretcher light", fill=NONE, stroke="#D8AA6A",
       strokeWidth=3, cap="round", opacity=45)

# --- trestles: sledge foot, splayed post, capital arm ----------------------------------
def trestle(cx, label, lit):
    """Sledge foot on the floor, splayed post, capital arm under the top."""
    # sledge foot: long low beam, ends lifted a touch
    fx0, fx1 = cx - 62, cx + 62
    foot = [(fx0 + 6, 668), (fx1 - 6, 668), (fx1 + 2, 680), (fx1 - 4, 694),
            (cx + 30, 698), (cx - 30, 698), (fx0 + 4, 694), (fx0 - 2, 680)]
    d.path(smooth(foot, closed=True), f"{label} foot",
           fill=lin((fx0, 0), (fx1, 0), *OAK), stroke=INK, strokeWidth=4, join="round")
    EXTENT.extend(foot)
    # iron studs along the foot's face
    for i in range(3):
        d.shape("ellipse", f"{label} stud {i+1}", x=round(cx - 28 + i * 22), y=682, width=7, height=6,
                fill=IRON, stroke=INK, strokeWidth=1.2)
    # splayed post: narrow at the capital, widening toward the foot
    post = [(cx - 15, 528), (cx + 15, 528), (cx + 22, 600), (cx + 26, 660),
            (cx + 18, 668), (cx - 18, 668), (cx - 26, 660), (cx - 22, 600)]
    d.path(smooth(post, closed=True), f"{label} post",
           fill=lin((cx - 26, 0), (cx + 26, 0), *OAK), stroke=INK, strokeWidth=4, join="round")
    EXTENT.extend(post)
    # chamfer light down the post's lit edge / shade on the far edge
    if lit:
        d.path(f"M{cx - 19},545 L{cx - 23},655", f"{label} post edge light",
               fill=NONE, stroke="#E0B478", strokeWidth=3, cap="round", opacity=55)
    d.path(f"M{cx + 18},545 L{cx + 23},652", f"{label} post shade",
           fill=NONE, stroke="#3A240E", strokeWidth=4, cap="round", opacity=50)
    # capital arm: shoulder spreading under the tabletop
    cap = [(cx - 40, 514), (cx + 40, 514), (cx + 34, 526), (cx + 20, 534),
           (cx - 20, 534), (cx - 34, 526)]
    d.path(smooth(cap, closed=True), f"{label} capital",
           fill=lin((0, 514), (0, 534), *OAK_DARK), stroke=INK, strokeWidth=3.5, join="round")
    EXTENT.extend(cap)
    # pegged joint: peg through post top
    d.shape("ellipse", f"{label} peg", x=round(cx - 5), y=542, width=10, height=9,
            fill=rad((0, "#8A5E30"), (1, "#34200C")), stroke=INK, strokeWidth=1.5)
    # tusk tenon + wedge on the post's outer face (stretcher locked through)
    tx = cx - 42 if lit else cx + 26
    d.path(f"M{tx},590 L{tx + 16},588 L{tx + 16},616 L{tx},618 Z", f"{label} tenon",
           fill=lin((0, 588), (0, 618), *OAK_DARK), stroke=INK, strokeWidth=3)
    d.path(f"M{tx + 2},592 L{tx + 9},592 L{tx + 6},614 L{tx + 2},614 Z", f"{label} wedge",
           fill="#2A1808", stroke=INK, strokeWidth=1.5)


trestle(335, "Trestle L", lit=True)
trestle(665, "Trestle R", lit=False)

# shadow the top throws onto the stretcher and post heads
d.shape("ellipse", "Under-top shade", x=250, y=506, width=500, height=40,
        fill=rad((0, "#120B04", 55), (1, "#120B04", 0)), stroke=NONE)

# --- tabletop: front edge band, surface plane, breadboard ends ---------------------------
# surface plane receding to a narrower back edge (drawn first; the deep front
# band overhangs its ends so the slab silhouette blunts instead of pointing)
d.path("M216,452 L784,452 Q800,453 801,468 L803,482 Q803,489 794,489 "
       "L206,489 Q197,489 197,480 L199,466 Q200,452 216,452 Z", "Top surface",
       fill=lin((0, 452), (0, 490), (0, "#D8AA6A"), (0.5, "#BC8C4E"), (1, "#96683A")),
       stroke=INK, strokeWidth=4, join="round")
EXTENT += [(216, 452), (784, 452), (794, 489), (206, 489), (197, 470), (803, 470)]
# breadboard end strips on the surface, pinned with two pegs each
d.path("M216,452 L252,453 L250,487 L204,488 Z", "Breadboard strip L",
       fill=lin((204, 0), (252, 0), *OAK_DARK), stroke=INK, strokeWidth=3)
d.path("M784,452 L748,453 L750,487 L796,488 Z", "Breadboard strip R",
       fill=lin((748, 0), (796, 0), *OAK_DARK), stroke=INK, strokeWidth=3)
for cx, cy in [(226, 466), (242, 468), (758, 467), (774, 465)]:
    d.shape("ellipse", "Cap peg", x=cx - 3, y=cy - 3, width=7, height=6,
            fill=rad((0, "#9A6E3C"), (1, "#3A240E")), stroke=INK, strokeWidth=1.2)
# cleat grooves where the strips meet the field
d.path("M250,455 L249,486", "Cleat groove L", fill=NONE, stroke="#3A240E",
       strokeWidth=2.5, opacity=55)
d.path("M750,455 L751,486", "Cleat groove R", fill=NONE, stroke="#3A240E",
       strokeWidth=2.5, opacity=55)
# grain: long low-opacity strokes running the length of the surface
for i, (y, x0, x1) in enumerate([(462, 240, 700), (470, 280, 760), (478, 250, 640)]):
    d.path(f"M{x0},{y} C{(x0 + x1) / 2 - 40},{y - 3} {(x0 + x1) / 2 + 40},{y + 2} {x1},{y - 1}",
           f"Grain {i+1}", fill=NONE, stroke="#7A5028", strokeWidth=2.2,
           cap="round", opacity=38)
# lit front lip of the surface
d.path("M210,484 L790,484", "Top front lip light", fill=NONE, stroke="#E8C088",
       strokeWidth=3.5, cap="round", opacity=60)
# front edge band: the plank's thickness, ends rounded and just past the surface
d.path("M200,488 L800,488 Q812,488 812,498 L812,506 Q812,518 800,518 "
       "L200,518 Q188,518 188,506 L188,498 Q188,488 200,488 Z", "Top edge band",
       fill=lin((0, 488), (0, 518), *OAK_DARK), stroke=INK, strokeWidth=4, join="round")
EXTENT += [(188, 500), (812, 500), (200, 518), (800, 518)]
# a knot in the front band
d.shape("ellipse", "Top knot", x=560, y=498, width=16, height=10,
        fill=rad((0, "#3A240E"), (1, "#5E3C1C")), opacity=70, stroke=NONE)
d.path("M552,503 C556,498 566,498 570,503", "Knot ring", fill=NONE,
       stroke="#3A240E", strokeWidth=2, opacity=50, cap="round")

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("trestle extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#EEE6D2", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C0B292", justify="center")
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


caption("TRESTLE TABLE", "OAK · WROUGHT IRON")
d.finish("trestle-table-V1R00")

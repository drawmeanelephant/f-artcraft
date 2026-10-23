#!/usr/bin/env python3
"""Coat stand — field plate V1R00. Near-side view of a turned-wood hall
stand: central pole, three curling hooks up top, a ring of pegs at the
waist, three splayed cabriole feet, and one mustard scarf left hanging
on the left hook. Dark hall plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Coat Stand — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241610"   # warm dark, not black
EXTENT = []


def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


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


def ribbon(pts, w0, w1):
    """Tapered filled band through centreline pts; returns path string."""
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        p_prev = pts[max(0, i - 1)]; p_next = pts[min(n - 1, i + 1)]
        tx, ty = p_next[0] - p_prev[0], p_next[1] - p_prev[1]
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        w = w0 + (w1 - w0) * i / (n - 1)
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return smooth(left + right[::-1], closed=True), left, right


WOOD = ((0, "#9A6A44"), (0.3, "#C08E5E"), (0.5, "#6E4526"), (0.78, "#8A5A34"), (1, "#462A14"))
CX = 500.0


def wood_grad(x):
    return lin((x - 16, 0), (x + 16, 0), *WOOD)


# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#191418"), (1, "#0B090C")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6E6068", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#544A52"), (0.6, "#3B333B"), (1, "#221E24")),
        stroke="#110D12", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6CBD6", strokeWidth=3, opacity=22)
d.shape("ellipse", "Hall glow", x=330, y=180, width=340, height=480,
        fill=rad((0, "#E8C890", 10), (0.6, "#A08050", 4), (1, "#705838", 0)), stroke=NONE)

FY = 712
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#5C5258", 32), (1, "#141017", 70)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E0D4DE", strokeWidth=2, opacity=18)

# floor shadow under the splayed feet
d.shape("ellipse", "Stand shadow", x=372, y=686, width=256, height=40,
        fill=rad((0, "#04050A", 62), (0.6, "#04050A", 26), (1, "#04050A", 0)), stroke=NONE)

# --- feet (three cabriole splays; the back foot darker, behind the pole) -----------
def foot(name, p0, c, p1, w0, w1, dark=False):
    mid = [(p0[0] + c[0]) / 2 + (c[0] - (p0[0] + p1[0]) / 2) * 0.5,
           (p0[1] + c[1]) / 2 + (c[1] - (p0[1] + p1[1]) / 2) * 0.5]
    cl = [p0, mid, p1]
    path, lf, rt = ribbon(cl, w0, w1)
    d.path(path, name, fill=wood_grad((p0[0] + p1[0]) / 2), stroke="#1E120A",
           strokeWidth=2.5, join="round", opacity=62 if dark else 100)
    EXTENT.append(p1)
    EXTENT.append(lf[-1]); EXTENT.append(rt[-1])


foot("Foot back", (CX + 6, 636), (CX + 34, 668), (CX + 42, 700), 10, 7, dark=True)
foot("Foot L", (CX - 4, 632), (CX - 58, 662), (CX - 96, 702), 12, 7)
foot("Foot R", (CX + 4, 632), (CX + 58, 662), (CX + 96, 702), 12, 7)
# toe caps
for nm, (tx, ty) in (("L", (CX - 96, 702)), ("R", (CX + 96, 702)), ("B", (CX + 42, 700))):
    d.shape("ellipse", f"Toe {nm}", x=round(tx - 11), y=round(ty - 8), width=22, height=14,
            fill=wood_grad(tx), stroke="#1E120A", strokeWidth=2,
            opacity=62 if nm == "B" else 100)

# --- pole (turned silhouette, bottom -> top) ---------------------------------------
PROF = [  # (y, half-width) from base collar up to under the finial
    (652, 13), (642, 11), (620, 8), (588, 14), (566, 16), (548, 9),
    (508, 8), (478, 12), (462, 14), (448, 9), (380, 8), (330, 8.5),
    (312, 12), (296, 11), (288, 7), (272, 7)]
pole = [(CX + w, y) for y, w in PROF] + [(CX - w, y) for y, w in reversed(PROF)]
d.path(smooth(pole, closed=True), "Pole", fill=wood_grad(CX),
       stroke="#1E120A", strokeWidth=3, join="round")
EXTENT += [(CX - 16, 470), (CX + 16, 470), (CX, 272)]
# turning rings
for i, ry in enumerate((586, 470, 312)):
    d.path(f"M{CX - 14},{ry} L{CX + 14},{ry}", f"Turning ring {i}",
           fill=NONE, stroke="#2E1A0C", strokeWidth=2.2, opacity=55)
# sheen down the lit side
d.path(f"M{CX - 5},{290} C{CX - 8},{420} {CX - 7},{560} {CX - 5},{640}",
       "Pole sheen", fill=NONE, stroke="#E8C49A", strokeWidth=2.5, opacity=30, cap="round")

# --- waist peg ring -------------------------------------------------------------------
d.shape("ellipse", "Peg collar", x=CX - 20, y=456, width=40, height=18,
        fill=wood_grad(CX), stroke="#1E120A", strokeWidth=2.5)

def peg(name, ang_deg, ln=30):
    a = math.radians(ang_deg)
    bx, by = CX + math.cos(a) * 14, 466 + math.sin(a) * 8
    tx, ty = CX + math.cos(a) * (14 + ln), 466 + math.sin(a) * (8 + ln * 0.55)
    path, _, _ = ribbon([(bx, by), (tx, ty)], 4.6, 3.2)
    d.path(path, name, fill=wood_grad(tx), stroke="#1E120A", strokeWidth=2, join="round")
    d.shape("ellipse", f"{name} knob", x=round(tx - 4.6), y=round(ty - 4.6), width=10, height=10,
            fill=rad((0, "#C08E5E"), (1, "#5C3A1E")), stroke="#1E120A", strokeWidth=1.6)
    EXTENT.append((tx, ty))


peg("Peg L", 168, 36)
peg("Peg LF", 205, 28)
peg("Peg RF", -25, 28)
peg("Peg R", 12, 36)
# one peg aimed at the viewer: a short stub centred on the pole
d.shape("ellipse", "Peg front", x=CX - 5, y=468, width=10, height=8,
        fill=rad((0, "#C08E5E"), (1, "#5C3A1E")), stroke="#1E120A", strokeWidth=1.6)

# --- hooks (three curling hooks under the finial) ---------------------------------------
d.shape("ellipse", "Hook collar", x=CX - 18, y=294, width=36, height=16,
        fill=wood_grad(CX), stroke="#1E120A", strokeWidth=2.5)


def hook(name, pts, back=False):
    """Curling hook: arm out from the collar, tip curling up into a ball."""
    path, _, _ = ribbon(pts, 7.0, 5.0)
    g = wood_grad(pts[2][0])
    d.path(path, name, fill=g, stroke="#1E120A", strokeWidth=2.5,
           join="round", opacity=55 if back else 100)
    bx, by = pts[-1]
    d.shape("ellipse", f"{name} ball", x=round(bx - 8), y=round(by - 8), width=16, height=16,
            fill=rad((0, "#D09C66"), (0.6, "#8A5A34"), (1, "#462A14")),
            stroke="#1E120A", strokeWidth=2, opacity=55 if back else 100)
    d.shape("ellipse", f"{name} glint", x=round(bx - 4), y=round(by - 5), width=5, height=4,
            fill="#FFE8C8", opacity=30 if back else 55, stroke=NONE)
    EXTENT.extend(pts)


# away-facing hook: rises above the collar behind the finial
hook("Hook back", [(CX + 2, 298), (CX + 14, 282), (CX + 30, 266),
                   (CX + 38, 250), (CX + 28, 242)], back=True)
# side hooks, tips curling up
hook("Hook L", [(CX - 4, 302), (CX - 40, 298), (CX - 66, 288),
                (CX - 76, 272), (CX - 64, 260)])
hook("Hook R", [(CX + 4, 302), (CX + 40, 298), (CX + 66, 288),
                (CX + 76, 272), (CX + 64, 260)])

# finial knob on top
d.shape("ellipse", "Finial", x=CX - 13, y=246, width=26, height=26,
        fill=rad((0, "#D09C66"), (0.55, "#8A5A34"), (1, "#462A14")),
        stroke="#1E120A", strokeWidth=2.5)
d.shape("ellipse", "Finial glint", x=CX - 6, y=251, width=7, height=5,
        fill="#FFE8C8", opacity=60, stroke=NONE)
EXTENT.append((CX, 246))

# --- the scarf on the left hook ----------------------------------------------------------
# draped over the left hook's mid-arm (~458,292); the hook's curled tip stays visible
scarf_cl = [(430, 600), (428, 545), (429, 480), (432, 412), (438, 354),
            (446, 314), (456, 292), (466, 290), (473, 302), (476, 332),
            (476, 376), (474, 420)]
path, lf, rt = ribbon(scarf_cl, 13, 10)
d.path(path, "Scarf",
       fill=lin((420, 280), (476, 610), (0, "#E4B45E"), (0.4, "#C8923E"),
                (0.75, "#9A6620"), (1, "#7A4E14")),
       stroke="#3A2408", strokeWidth=3, join="round")
EXTENT += scarf_cl
# fold shading along the drape
d.path("M426,352 C424,430 425,510 427,590", "Scarf fold shade",
       fill=NONE, stroke="#6E4210", strokeWidth=4, opacity=35, cap="round")
d.path("M448,300 C456,290 466,288 473,298", "Scarf crest light",
       fill=NONE, stroke="#FFDFA0", strokeWidth=3, opacity=45, cap="round")
# weft stripes on the long tail
for i, yy in enumerate((470, 522, 574)):
    d.path(f"M418,{yy} C426,{yy + 4} 434,{yy + 4} 442,{yy}", f"Scarf stripe {i}",
           fill=NONE, stroke="#7A4E14", strokeWidth=2.4, opacity=50)
# fringe on both ends
for i, (fx, fy, sgn) in enumerate([(430, 600, 1), (474, 420, -1)]):
    for k in (-8, -2, 4):
        d.path(f"M{fx + k},{fy - 4} L{fx + k + sgn * 2},{fy + 9}",
               f"Fringe {i}{k}", fill=NONE, stroke="#8A5A18", strokeWidth=2.6,
               cap="round")
# scarf's little contact shadow on the hook arm
d.path("M446,306 C456,294 468,290 478,292", "Scarf hook shadow",
       fill=NONE, stroke="#3A2408", strokeWidth=3, opacity=40, cap="round")

# --- extent check ----------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("stand extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


# --- caption ----------------------------------------------------------------------------
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
               color="#F0E4D8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B0A096", justify="center")
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


caption("COAT STAND", "BEECH · WOOL · LACQUER")
d.finish("coat-stand-V1R00")

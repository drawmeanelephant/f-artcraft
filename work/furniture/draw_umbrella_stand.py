#!/usr/bin/env python3
"""Umbrella stand — field plate V1R00. A tall stoneware cylinder by the
door: rolled rim, glazed blue-grey body running with rain drips, a drip
tray at the foot, and three furled umbrellas leaning out — two dark, one
burgundy — crook handles catching the hall light. Seen straight on, a
touch above. Ceramic plate, rainy-entry mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Umbrella Stand — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#141210"
AX = 500
FIT = []


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}


def mix(c0, c1, t):
    a = [int(c0[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p + (q - p) * t):02X}" for p, q in zip(a, b))


def smooth(pts, closed=True, move=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def lathe(profile, ax=AX):
    """Right-half profile [(x,y)...] bottom->top -> closed symmetric silhouette."""
    left = [(2 * ax - x, y) for x, y in reversed(profile)]
    for p in profile + left:
        FIT.append(p)
    return smooth(profile + left)


def ribbon(label, spine, w0, w1, fill, ink=1.6, stroke=INK):
    n = len(spine)
    left, right = [], []
    for i, p in enumerate(spine):
        q0 = spine[max(0, i - 1)]
        q1 = spine[min(n - 1, i + 1)]
        tx, ty = q1[0] - q0[0], q1[1] - q0[1]
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        w = w0 + (w1 - w0) * i / (n - 1)
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    for p in left + right:
        FIT.append(p)
    d.path(smooth(left, closed=False) + " " + smooth(right[::-1], closed=False, move=False) + " Z",
           label, fill=fill, stroke=stroke, strokeWidth=ink, join="round")
    return left, right


def cubic(p0, p1, p2, p3, n=24):
    return [tuple((1 - t) ** 3 * p0[k] + 3 * (1 - t) ** 2 * t * p1[k] +
                  3 * (1 - t) * t * t * p2[k] + t ** 3 * p3[k] for k in (0, 1))
            for t in [i / n for i in range(n + 1)]]


# --- backdrop + plate: wet evening ---------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#141C22"), (1, "#06090C")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6E8290", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5E6E74"), (0.6, "#39464C"), (1, "#141C20")),
        stroke="#0A0E11", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4E6", strokeWidth=3, opacity=24)
# the doorway: a tall pale opening behind the stand, rain-blue light
d.path("M300,190 L300,690 L700,690 L700,190 Z", "Doorway glow",
       fill=lin(0, 190, 0, 690, (0, "#A8BEC4", 0.10), (1, "#7A929A", 0.03)),
       stroke=NONE)
d.path("M300,190 L700,190", "Lintel line", fill=NONE, stroke="#C4D4D8",
       strokeWidth=4, opacity=10)
for i, (x, y, w) in enumerate([(208, 215, 6), (782, 245, 7), (168, 615, 6), (830, 590, 7),
                               (428, 102, 6), (648, 108, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#A8C0C6", opacity=30, stroke=NONE)

HZN = 706
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#2E3A40", 0.55), (1, "#0C1216", 0.9)), stroke=NONE)
# wet flagstone sheen
d.path(f"M{PCX - hx + 8:.1f},{HZN + 4} L{PCX + hx - 8:.1f},{HZN + 4}", "Wet sheen",
       fill=NONE, stroke="#C4D8DC", strokeWidth=3, opacity=18)
d.shape("ellipse", "Stand shadow", x=390, y=738, width=230, height=44,
        fill=rad((0, "#050708", 0.65), (1, "#050708", 0)), stroke=NONE)
# the wet ring the stand sits in
d.shape("ellipse", "Wet pool", x=378, y=752, width=250, height=30,
        fill=rad((0, "#6E8A94", 0.22), (0.7, "#4E626A", 0.10), (1, "#4E626A", 0)),
        stroke=NONE)

# --- the stand: glazed stoneware cylinder ---------------------------------------------------------------
# right-half silhouette, bottom -> top: drip tray, body taper, rolled rim
body_profile = [(AX + 78, 742), (AX + 84, 736), (AX + 88, 726),   # tray foot
                (AX + 84, 716), (AX + 82, 700), (AX + 84, 640),
                (AX + 86, 560), (AX + 88, 480), (AX + 90, 430),
                (AX + 94, 424), (AX + 96, 416), (AX + 92, 410),   # rolled rim out
                (AX + 84, 408)]
d.path(lathe(body_profile), "Stand body",
       fill=lin(AX - 96, 0, AX + 96, 0,
                (0, "#2E4048"), (0.28, "#5E7A84"), (0.46, "#9AB4BC"),
                (0.58, "#6E8A94"), (0.8, "#3A4E56"), (1, "#1E2A30")),
       stroke=INK, strokeWidth=2.4, join="round")

# glaze sheen: long highlight down the left belly, dimmer one right
d.path("M416,690 C406,610 408,540 418,470", "Glaze sheen L",
       fill=NONE, stroke="#D8ECF0", strokeWidth=9, opacity=30, cap="round")
d.path("M588,680 C596,600 594,540 586,478", "Glaze sheen R",
       fill=NONE, stroke="#C4DCE2", strokeWidth=6, opacity=20, cap="round")

# painted band: two incised rings + a wave scroll between, near the rim
for i, yy in enumerate([452, 468]):
    d.path(f"M{AX - 88},{yy} C{AX - 30},{yy - 8} {AX + 30},{yy - 8} {AX + 88},{yy}",
           f"Band line {i+1}", fill=NONE, stroke="#16232A", strokeWidth=3.2, opacity=70)
for i in range(7):
    x = AX - 70 + i * 24
    d.path(f"M{x},460 q7,-8 14,0", f"Wave scroll {i+1}", fill=NONE,
           stroke="#16232A", strokeWidth=2.4, opacity=60)

# rain drips: thin glaze-run streaks down the body, each ending in a bead
for i, (x, y0, y1, w) in enumerate([(438, 500, 650, 3.4), (500, 480, 636, 4.0),
                                    (556, 496, 622, 3.0), (470, 540, 700, 2.6),
                                    (530, 520, 668, 2.8)]):
    dd = [(x - w, y0), (x + w, y0 + 2), (x + w * 0.5, y1 - 12),
          (x + w * 0.7, y1), (x, y1 + 4), (x - w * 0.7, y1), (x - w * 0.5, y1 - 12)]
    d.path(smooth(dd), f"Glaze run {i+1}",
           fill=lin(x, y0, x, y1, (0, "#BED6DC", 0.5), (1, "#7A98A2", 0.35)),
           stroke="#2A3C44", strokeWidth=1.0, opacity=80)
    d.shape("ellipse", f"Drip bead {i+1}", x=round(x - w), y=round(y1 - 2),
            width=round(w * 2.4), height=round(w * 2.4),
            fill=rad((0, "#E4F2F4", 0.8), (1, "#9ABCC4", 0.3)), stroke=NONE)

# rim: rolled lip reads as a lit ellipse band over the mouth
d.shape("ellipse", "Rim band", x=AX - 96, y=402, width=192, height=30,
        fill=lin(AX - 96, 0, AX + 96, 0, (0, "#3A505A"), (0.45, "#8AA6AE"),
                 (0.6, "#AEC8CE"), (1, "#2A3A42")), stroke=INK, strokeWidth=2.0)
# the mouth: dark wet interior
d.shape("ellipse", "Mouth", x=AX - 82, y=406, width=164, height=22,
        fill=rad((0, "#0A1216"), (0.75, "#182630"), (1, "#3A525C")),
        stroke=NONE)

# --- drip tray ring at the foot --------------------------------------------------------------------------
d.shape("ellipse", "Tray lip", x=AX - 92, y=730, width=184, height=22,
        fill=lin(AX - 92, 0, AX + 92, 0, (0, "#24343C"), (0.5, "#56707A"),
                 (1, "#1A262C")), stroke=INK, strokeWidth=1.8)
d.shape("ellipse", "Tray water", x=AX - 84, y=733, width=168, height=15,
        fill=rad((0, "#8AB4BE", 0.5), (1, "#3E5A64", 0.2)), stroke=NONE)

# --- umbrellas: furlled canopies leaning out of the mouth -------------------------------------------------
def furled(label, foot, top, w, stops, crook=None):
    """A closed umbrella stored tip-down: the ferrule dips into the stand at
    `foot`, the furled canopy widens to its shoulder at `top`, then a shaft
    rises to the handle — a J-crook or a knob."""
    spine = cubic(foot, (foot[0] + (top[0] - foot[0]) * 0.35, foot[1] - 40),
                  (top[0] - (top[0] - foot[0]) * 0.25, top[1] + 46), top)
    ribbon(label + " canopy", spine, 2.4, w,
           fill=lin(foot[0], foot[1], top[0], top[1], *stops), ink=1.7)
    # fabric fold creases along the canopy
    for j in (0.35, 0.65):
        p = spine[int(len(spine) * j)]
        q = spine[min(len(spine) - 1, int(len(spine) * j) + 6)]
        d.path(f"M{p[0]:.0f},{p[1]:.0f} L{q[0]:.0f},{q[1]:.0f}", f"{label} crease {j}",
               fill=NONE, stroke="#0C0A08", strokeWidth=1.6, opacity=55, cap="round")
    # shaft continues up from the canopy shoulder to the handle
    hx, hy = top[0] + (top[0] - foot[0]) * 0.14, top[1] - 46
    d.path(f"M{top[0]:.0f},{top[1]:.0f} L{hx:.0f},{hy:.0f}", f"{label} shaft",
           fill=NONE, stroke="#8A6A44", strokeWidth=4.2, cap="round")
    if crook:  # J-crook curving back down
        s = crook
        cr = cubic((hx, hy), (hx + s * 26, hy - 20), (hx + s * 34, hy + 14),
                   (hx + s * 16, hy + 22))
        d.path(smooth(cr, closed=False), f"{label} crook", fill=NONE,
               stroke="#8A6A44", strokeWidth=7, cap="round")
        d.path(smooth(cr, closed=False), f"{label} crook light", fill=NONE,
               stroke="#C8A068", strokeWidth=2.4, opacity=60, cap="round")
    FIT.append((hx, hy))


furled("Umbrella L", (452, 424), (392, 306), 12,
       [(0, "#22242A"), (0.5, "#4A4E56"), (1, "#2E3238")], crook=-1)
furled("Umbrella R", (548, 420), (610, 312), 12,
       [(0, "#2A1A16"), (0.5, "#5E3226"), (1, "#3A2620")], crook=1)
furled("Umbrella C", (502, 430), (510, 288), 13,
       [(0, "#1C242E"), (0.5, "#3E4E5C"), (1, "#242E38")], crook=None)
# centre umbrella gets a straight knob instead of a crook
d.path("M511,288 L516,236", "Umbrella C shaft top", fill=NONE, stroke="#8A6A44",
       strokeWidth=4.2, cap="round")
d.shape("ellipse", "Umbrella C knob", x=510, y=218, width=14, height=19,
        fill=rad((0, "#C8A068"), (1, "#6E4E28")), stroke=INK, strokeWidth=1.2)

# mouth interior reasserted over the canopy bases
d.shape("ellipse", "Mouth dark", x=AX - 78, y=410, width=156, height=18,
        fill=rad((0, "#081014"), (1, "#243840")), stroke=NONE, opacity=90)

# --- extent check ----------------------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in FIT)
print("umbrella-stand extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far

# --- captions ----------------------------------------------------------------------------------------------
d.text("UMBRELLA STAND", "Name", x=500, y=940, size=54, font="Virelai Sans",
       color="#E8F0F0", justify="center")
LINE2, SZ2, TRK = "STONEWARE · CANE · STEEL", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#AEC2C6", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)


def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o:
            return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit:
                return hit


b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("umbrella-stand-V1R00")

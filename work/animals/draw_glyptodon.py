#!/usr/bin/env python3
"""Glyptodon — field plate V1R00. An armadillo the size of a car: the dome is
the subject, a half-buried boulder of tessellated scutes humped over stubby
column legs, blunt armoured head low at the front, ringed tail dragging
behind. Pampas plate — plum dusk, dry grass, floor chord on the disc arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Glyptodon — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241812"   # warm near-black
EXTENT = []


def ext(pts):
    EXTENT.extend(pts)


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


def smooth(pts, closed=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = "M%.1f,%.1f" % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)


def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE,
                  stroke=color, strokeWidth=w, cap="round", **kw)


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#141018"), (1, "#08060C")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#6E5C78", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#3E3248"), (0.5, "#2C2436"),
                 (0.8, "#201A28"), (1, "#16101C")),
        stroke="#0C0810", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#06040C", 0.5)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8BCA8", strokeWidth=3, opacity=24)

# last of the sun — a low amber smear dying on the left horizon, inside the disc
ell("Sun smear", 300, 642, 100, 58,
    fill=rad((0, "#C87840", 30), (0.55, "#96542C", 12), (1, "#96542C", 0)),
    stroke=NONE)
# a few dusk motes high in the disc
for i, (x, y, s) in enumerate([(300, 200, 3.5), (620, 170, 3), (720, 260, 3),
                               (230, 320, 2.8), (540, 150, 3)]):
    assert on_disc(x, y, 10), i
    ell(f"Mote {i+1}", x, y, s, s, fill="#D8C8B8", opacity=28, stroke=NONE)

# --- pampas floor: chord closing on the disc arc -------------------------------------
ch = 700
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Pampas", fill=lin((0, ch), (0, 880), (0, "#6E5638"), (0.5, "#3E2E1C"),
                          (1, "#221810")), stroke=NONE)
# dry-grass sheen right at the horizon line
d.path(f"M{PCX - hch + 10:.0f},{ch + 3} Q{PCX - 120},{ch - 6} {PCX + 60},{ch + 1} "
       f"Q{PCX + 200},{ch + 8} {PCX + hch - 20:.0f},{ch + 2}",
       "Horizon sheen", fill=NONE, stroke="#C8AC74", strokeWidth=3,
       opacity=30, cap="round")

# --- ringed tail first — it drags out behind the dome ------------------------------------
d.path(smooth([(316, 570), (280, 584), (250, 610), (226, 642), (206, 668),
               (192, 684), (186, 692), (198, 696), (216, 684), (238, 658),
               (262, 630), (288, 604), (310, 596)]),
       "Tail", fill=lin((310, 570), (190, 700), (0, "#8A6844"), (1, "#4E3520")),
       stroke=INK, strokeWidth=5)
ext([(192, 684), (316, 570)])
# tail rings — scute bands circling the taper
for i, (x0, y0, x1, y1, w) in enumerate([(270, 596, 280, 620, 4.5),
                                         (246, 626, 256, 650, 4),
                                         (224, 652, 233, 674, 4),
                                         (204, 672, 212, 690, 3.5)]):
    line(f"Tail ring {i+1}", x0, y0, x1, y1, w, "#4E3520", opacity=70)

# --- the dome -------------------------------------------------------------------------
dome = [(292, 608), (306, 512), (372, 428), (468, 385), (560, 392),
        (646, 444), (702, 524), (716, 598), (676, 620), (330, 620)]
d.path(smooth(dome), "Carapace",
       fill=lin((500, 380), (500, 660), (0, "#C4A476"), (0.55, "#96714A"),
                (1, "#5E412A")),
       stroke=INK, strokeWidth=6.5)
ext(dome)

# tessellation — rosette scutes tiled on concentric arcs of the dome
DCX, DCY, DRX, DRY = 500, 622, 208, 236
rows = [(0.20, [90]), (0.40, [62, 90, 118]), (0.58, [40, 66, 90, 114, 140]),
        (0.74, [24, 48, 70, 90, 110, 132, 156]),
        (0.88, [14, 36, 57, 77, 96, 115, 136, 158, 172])]
sn = 0
for k, angles in rows:
    for deg in angles:
        a = math.radians(deg)
        x = DCX + DRX * k * math.cos(a) + (4 if deg < 90 else -4)
        y = DCY - DRY * k * math.sin(a)
        # keep tiles on the dome face, inside its silhouette
        if not ((x - DCX) ** 2 / (DRX * 0.98) ** 2 + (y - DCY) ** 2 / (DRY * 0.98) ** 2 < 1):
            continue
        sn += 1
        srx = 15 + 2.5 * k
        ell(f"Scute {sn}", x, y, srx, srx * 0.72,
            fill=lin((x - srx, y - srx), (x + srx, y + srx),
                     (0, "#D2B284"), (1, "#84603C")),
            stroke="#5C4028", strokeWidth=2.5, opacity=96)
        ell(f"Scute boss {sn}", x, y - 1, 3.8, 3, fill="#DCC49A",
            opacity=85, stroke=NONE)

# dome sheen — moonless dusk, light dies left; sheen sits high-right
ell("Dome sheen", 560, 430, 110, 42,
    fill=rad((0, "#E8CCA0", 26), (1, "#E8CCA0", 0)), stroke=NONE)

# ventral skirt — the carapace's lower rim in shadow
d.path("M322,604 Q500,636 692,602", "Skirt shadow", fill=NONE,
       stroke="#3A2818", strokeWidth=9, opacity=55, cap="round")

# --- head: blunt armoured wedge low at the front ----------------------------------------
d.path(smooth([(694, 580), (732, 564), (770, 576), (792, 602), (796, 628),
               (782, 650), (752, 658), (720, 646), (700, 616)]),
       "Head", fill=lin((700, 560), (796, 660), (0, "#8A6844"), (1, "#4E3420")),
       stroke=INK, strokeWidth=5.5)
ext([(796, 628)])
# head-shield seam over the skull
d.path("M712,592 Q750,578 784,592", "Head shield", fill=NONE,
       stroke="#4E3420", strokeWidth=4, opacity=60, cap="round")
# ear nub, eye, nostril, mouth
d.path("M730,572 Q736,562 746,564 Q744,574 736,578 Z", "Ear",
       fill="#64452A", stroke=INK, strokeWidth=3.5)
ell("Eye", 754, 612, 6.5, 7.5, fill="#140C08", stroke=NONE)
ell("Eye glint", 756, 609, 2.2, 2.2, fill="#E8DCC0", opacity=75, stroke=NONE)
ell("Nostril", 783, 626, 4, 3.2, fill="#1A0E08", opacity=90, stroke=NONE)
d.path("M766,644 Q780,648 790,641", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=3.5, opacity=75, cap="round")

# --- legs: two stubby columns visible, claws on the ground --------------------------------
# rear leg, slightly dimmer
d.path(smooth([(352, 600), (380, 596), (398, 616), (394, 660), (396, 686),
               (384, 692), (360, 692), (350, 668), (348, 630)]),
       "Rear leg", fill=lin((350, 590), (400, 700), (0, "#6E4E32"), (1, "#3E2A18")),
       stroke=INK, strokeWidth=5)
for i, x in enumerate((362, 376, 389)):
    d.path(f"M{x},688 l-3,9", f"Rear claw {i+1}", fill=NONE, stroke=INK,
           strokeWidth=3.5, cap="round")
# front leg under the dome's front edge
d.path(smooth([(636, 596), (668, 592), (688, 614), (684, 658), (688, 684),
               (674, 692), (648, 692), (638, 666), (634, 626)]),
       "Front leg", fill=lin((640, 590), (690, 700), (0, "#7A5636"), (1, "#46301C")),
       stroke=INK, strokeWidth=5)
for i, x in enumerate((650, 664, 678)):
    d.path(f"M{x},688 l-3,9", f"Front claw {i+1}", fill=NONE, stroke=INK,
           strokeWidth=3.5, cap="round")
ext([(396, 686), (688, 684)])

# belly shade between the legs
d.path("M400,616 Q520,640 634,614 L634,640 Q520,660 400,640 Z",
       "Belly shade", fill="#2E1E10", opacity=45, stroke=NONE)

# ground contact shadow
ell("Ground shadow", 500, 696, 210, 14, fill="#140C06", opacity=48, stroke=NONE)

# --- dry pampas grass: blade tufts + two plume stalks -------------------------------------
def tuft(x, y, h, n, seed):
    for j in range(n):
        dx = (j - (n - 1) / 2) * (10 + seed % 5)
        lean = ((seed * 7 + j * 13) % 17 - 8) / 8.0
        d.path(f"M{x},{y} Q{x + dx * 0.4},{y - h * 0.55} {x + dx + lean * 10:.0f},{y - h:.0f}",
               f"Blade {seed}-{j+1}", fill=NONE,
               stroke="#8A7448" if j % 2 else "#6E5C34",
               strokeWidth=3.5, cap="round", opacity=80)


for k, (x, h, n) in enumerate([(230, 46, 5), (300, 60, 6), (420, 38, 4),
                               (560, 42, 4), (620, 55, 5), (755, 48, 5),
                               (800, 36, 4)]):
    assert on_disc(x, 700 - h, 14), k
    tuft(x, 700 + 6, h, n, k + 1)

# two pampas plumes — tall stalks with feathery seed heads, at the flanks
for i, (x, h, lean) in enumerate([(262, 170, -14), (792, 150, 10)]):
    assert on_disc(x + lean, 700 - h, 12), i
    d.path(f"M{x},{702} Q{x + lean * 0.4},{702 - h * 0.6} {x + lean},{702 - h}",
           f"Plume stalk {i+1}", fill=NONE, stroke="#7A6438", strokeWidth=4,
           cap="round")
    for j in range(7):
        t = j / 6.0
        px = x + lean * (0.5 + 0.5 * t)
        py = 702 - h * (0.55 + 0.45 * t)
        d.path(f"M{px:.0f},{py:.0f} q{(j - 3) * 3},{-12} {(j - 3) * 4},{-26}",
               f"Plume {i+1}-{j+1}", fill=NONE, stroke="#C8B890",
               strokeWidth=3, opacity=58, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0C0810", strokeWidth=6)

# --- extent check -------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("glyptodon extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


# --- caption ------------------------------------------------------------------------------
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
    n = d.text(name, "Name", x=500, y=932, size=58, font="Virelai Sans",
               color="#E8D9BC", justify="center")
    m = d.text(mats, "Second line", x=500, y=970, size=22, font="Virelai Sans",
               color="#A89C8C", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=80)
    d.cmd("text.setStyle", "Second line tracking", ids=[m["id"]], tracking=240)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "second line")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" %
              (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "second line":
            assert b["width"] <= 760, b["width"]


caption("GLYPTODON", "GLYPTODON CLAVIPES")
d.finish("glyptodon-V1R00")

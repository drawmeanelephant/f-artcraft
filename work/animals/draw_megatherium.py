#!/usr/bin/env python3
"""Megatherium — field plate V1R00. The ground sloth tall enough to browse
trees: reared up on hind legs and the prop of its own tail, long foreclaws
hooked over a branch it drags down to reach the leaves. Pleistocene-plateau
plate — dusty dusk, dry scrub, floor chord on the disc arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Megatherium — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#221610"   # warm near-black
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
        fill=lin((0, 0), (0, 1000), (0, "#161014"), (1, "#080608")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#7A6858", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#463644"), (0.5, "#322630"),
                 (0.8, "#241C22"), (1, "#181216")),
        stroke="#0E0A0C", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#080408", 0.5)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8BCB0", strokeWidth=3, opacity=24)

# dusty plateau air — a wide pale hang of haze low over the horizon
ell("Dust haze", 500, 640, 330, 80,
    fill=rad((0, "#8A7060", 16), (1, "#8A7060", 0)), stroke=NONE)
# faint stars
for i, (x, y, s) in enumerate([(320, 190, 3.2), (640, 160, 3), (740, 250, 2.8),
                               (240, 300, 2.6), (560, 140, 3)]):
    assert on_disc(x, y, 10), i
    ell(f"Star {i+1}", x, y, s, s, fill="#D8CCC8", opacity=26, stroke=NONE)

# --- the browsed tree: a dry algarrobo at right, limbs reaching over the sloth --------
d.path(smooth([(792, 700), (786, 620), (778, 540), (770, 460), (762, 390),
               (766, 330), (776, 300), (786, 330), (792, 400), (800, 480),
               (808, 560), (814, 640), (816, 700)], True),
       "Tree trunk", fill=lin((760, 300), (810, 700), (0, "#5C4630"),
                              (1, "#2E1E12")), stroke=INK, strokeWidth=5)
ext([(762, 390), (816, 700)])
# limbs forking left — the lowest is the one being dragged down
d.path("M772,420 Q700,400 640,416", "Limb low", fill=NONE, stroke="#4E3822",
       strokeWidth=8, cap="round")
d.path("M766,360 Q706,330 668,336", "Limb mid", fill=NONE, stroke="#4E3822",
       strokeWidth=7, cap="round")
d.path("M776,312 Q730,270 680,272", "Limb high", fill=NONE, stroke="#4E3822",
       strokeWidth=6, cap="round")
# twig off the low limb — bent down toward the claws
d.path("M668,414 Q656,428 650,442", "Twig bent", fill=NONE, stroke="#4E3822",
       strokeWidth=4.5, cap="round")
# leaf tufts — sparse dry clusters at limb ends
for i, (cx, cy, rx, ry) in enumerate([(636, 400, 40, 22), (664, 322, 36, 20),
                                      (678, 258, 34, 18), (648, 452, 26, 16)]):
    ell(f"Leaf tuft {i+1}", cx, cy, rx, ry,
        fill=rad((0, "#6E7040", 85), (0.7, "#4E5628", 60), (1, "#3E4420", 0)),
        stroke=NONE)
    for j in range(5):
        a = math.radians(j * 72 + i * 30)
        line(f"Leaf vein {i+1}-{j+1}", cx, cy,
             cx + rx * 0.6 * math.cos(a), cy + ry * 0.6 * math.sin(a),
             2.5, "#7A8048", opacity=50)

# --- plateau floor: chord closing on the disc arc --------------------------------------
ch = 700
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Plateau", fill=lin((0, ch), (0, 880), (0, "#6E5638"), (0.5, "#3C2C1C"),
                           (1, "#201610")), stroke=NONE)
d.path(f"M{PCX - hch + 10:.0f},{ch + 3} Q{PCX - 100},{ch - 5} {PCX + 80},{ch + 1} "
       f"Q{PCX + 210},{ch + 7} {PCX + hch - 20:.0f},{ch + 2}",
       "Horizon sheen", fill=NONE, stroke="#C0A470", strokeWidth=3,
       opacity=26, cap="round")

# --- the megatherium: tripod-reared, reaching up-right -------------------------------------
# far hind leg — behind, dim
d.path(smooth([(428, 560), (452, 566), (462, 610), (460, 660), (466, 690),
               (452, 696), (432, 694), (424, 656), (420, 600)]),
       "Hind leg far", fill=lin((420, 560), (470, 700), (0, "#4E3622"),
                                (1, "#2A1A10")), stroke=INK, strokeWidth=5)

# the tail — a broad prop planted behind
d.path(smooth([(420, 540), (392, 578), (372, 622), (356, 662), (344, 692),
               (356, 700), (388, 698), (414, 676), (436, 636), (448, 590)]),
       "Tail prop", fill=lin((440, 540), (350, 700), (0, "#64482E"),
                             (1, "#38240F")), stroke=INK, strokeWidth=5.5)
ext([(344, 692)])

# body mass — the reared barrel, back over the tail, belly to the right
body = [(430, 560), (440, 490), (462, 425), (500, 372), (548, 340),
        (588, 348), (606, 392), (606, 452), (588, 530), (556, 610),
        (512, 668), (468, 682), (440, 640)]
d.path(smooth(body), "Body",
       fill=lin((430, 330), (620, 690), (0, "#8A6238"), (0.5, "#644224"),
                (1, "#3A2412")), stroke=INK, strokeWidth=6)
ext(body)

# shag — short strokes off the spine and flank
for i, (x, y, dx, dy) in enumerate([(438, 500, -14, 4), (446, 452, -16, -2),
                                     (462, 408, -14, -6), (484, 372, -12, -8),
                                     (444, 556, -16, 6), (430, 596, -12, 8),
                                     (472, 660, -8, 12), (512, 646, -6, 14),
                                     (556, 596, 8, 12), (584, 540, 10, 10),
                                     (600, 480, 12, 6), (602, 420, 12, -2)]):
    line(f"Shag {i+1}", x, y, x + dx, y + dy, 3.5, "#3A2412", opacity=60)
# belly light
ell("Belly light", 570, 500, 44, 90,
    fill=rad((0, "#A87A48", 22), (1, "#A87A48", 0)), stroke=NONE)

# near hind leg + splayed clawed foot
d.path(smooth([(496, 580), (528, 588), (540, 630), (536, 668), (544, 688),
               (530, 696), (506, 694), (496, 660), (492, 614)]),
       "Hind leg near", fill=lin((500, 580), (550, 700), (0, "#5C4026"),
                                 (1, "#322012")), stroke=INK, strokeWidth=5)
ext([(544, 688)])
# hind foot claws — three blunt hooks splayed forward
for i, (x0, y0, x1, y1) in enumerate([(532, 690, 560, 696), (520, 694, 546, 702),
                                      (506, 694, 528, 702)]):
    d.path(f"M{x0},{y0} Q{(x0 + x1) / 2:.0f},{y0 - 2} {x1},{y1}",
           f"Hind claw {i+1}", fill=NONE, stroke="#D8C8A8", strokeWidth=5.5,
           cap="round")

# head — small round sloth skull tipped up toward the branch
d.path(smooth([(540, 352), (566, 330), (596, 326), (618, 342), (620, 366),
               (606, 384), (580, 390), (556, 380), (542, 366)]),
       "Head", fill=lin((540, 320), (620, 390), (0, "#8A6238"), (1, "#4E3018")),
       stroke=INK, strokeWidth=5)
ext([(620, 366)])
# muzzle, eye, nostril — face lifted to the leaves
ell("Muzzle", 604, 360, 16, 12, fill="#5C3C20", opacity=85, stroke=NONE)
ell("Eye", 586, 352, 6, 7, fill="#140C08", stroke=NONE)
ell("Eye glint", 588, 349, 2.2, 2.2, fill="#E8DCC0", opacity=75, stroke=NONE)
ell("Nostril", 612, 354, 3.6, 3, fill="#140C08", opacity=85, stroke=NONE)
d.path("M598,370 Q610,374 616,368", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=3.5, opacity=75, cap="round")
# ear nub + brow shag
d.path("M556,338 Q560,330 568,332 Q566,340 560,344 Z", "Ear",
       fill="#4E3018", stroke=INK, strokeWidth=3)
line("Brow shag", 574, 336, 560, 330, 3.5, "#3A2412", opacity=60)

# near arm — long limb reaching up to hook the low limb
d.path(smooth([(572, 420), (600, 396), (624, 372), (644, 352), (660, 340),
               (668, 348), (660, 366), (640, 386), (614, 412), (590, 438),
               (576, 442)]),
       "Arm near", fill=lin((570, 340), (670, 440), (0, "#74512C"),
                            (1, "#452C16")), stroke=INK, strokeWidth=5)
ext([(668, 348)])
# the great claws — three long pale hooks over the limb
for i, (x0, y0, cx, cy, x1, y1) in enumerate([
        (656, 352, 690, 336, 700, 306),
        (648, 360, 678, 348, 686, 316),
        (640, 368, 664, 358, 668, 330)]):
    d.path(f"M{x0},{y0} Q{cx},{cy} {x1},{y1}", f"Foreclaw {i+1}",
           fill=NONE, stroke="#E0D0AC", strokeWidth=6.5, cap="round")
    ext([(x1, y1)])

# far arm — raised behind, dimmer
d.path(smooth([(534, 404), (556, 372), (578, 344), (592, 328), (600, 334),
               (592, 354), (574, 380), (552, 412), (540, 420)]),
       "Arm far", fill=lin((540, 330), (600, 420), (0, "#543A20"),
                           (1, "#30200F")), stroke=INK, strokeWidth=4.5)
for i, (x0, y0, x1, y1) in enumerate([(596, 332, 612, 306), (588, 340, 600, 312)]):
    d.path(f"M{x0},{y0} Q{(x0 + x1) / 2 + 4},{(y0 + y1) / 2 - 4} {x1},{y1}",
           f"Far claw {i+1}", fill=NONE, stroke="#C8B894", strokeWidth=5,
           cap="round", opacity=85)

# ground shadow under the tripod
ell("Ground shadow", 470, 698, 170, 13, fill="#140C06", opacity=48, stroke=NONE)

# --- dry scrub tufts + stones ------------------------------------------------------------
def tuft(x, y, h, n, seed, col1="#8A7448", col2="#6E5C34"):
    for j in range(n):
        dx = (j - (n - 1) / 2) * (9 + seed % 5)
        lean = ((seed * 7 + j * 13) % 17 - 8) / 8.0
        d.path(f"M{x},{y} Q{x + dx * 0.4},{y - h * 0.55} {x + dx + lean * 10:.0f},{y - h:.0f}",
               f"Scrub {seed}-{j+1}", fill=NONE,
               stroke=col1 if j % 2 else col2, strokeWidth=3.5,
               cap="round", opacity=75)


for k, (x, h, n) in enumerate([(232, 40, 5), (300, 52, 5), (620, 34, 4),
                               (740, 44, 5), (830, 30, 4), (380, 30, 4)]):
    assert on_disc(x, 700 - h, 14), k
    tuft(x, 706, h, n, k + 11)
for i, (x, y, rx, ry, op) in enumerate([(250, 730, 14, 8, 45), (740, 745, 17, 9, 42),
                                        (640, 790, 12, 7, 40), (300, 790, 11, 6, 38)]):
    assert on_disc(x, y, 10), i
    ell(f"Stone {i+1}", x, y, rx, ry, fill="#241A12", opacity=op, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0E0A0C", strokeWidth=6)

# --- extent check -------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("megatherium extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 20, far


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


caption("MEGATHERIUM", "MEGATHERIUM AMERICANUM")
d.finish("megatherium-V1R00")

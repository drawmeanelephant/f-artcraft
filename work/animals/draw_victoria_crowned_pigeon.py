#!/usr/bin/env python3
"""Victoria crowned pigeon — field plate V1R00. New Guinea island forest
floor: Goura victoria standing in full court dress — slate blue-grey mass,
deep maroon breast, red eye, and the lace crest fanned wide in a ceremonial
arc, every shaft tipped with a white spatulate flag. Wings folded with the
pale wing-bar; short rounded tail rests toward the litter.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Victoria Crowned Pigeon — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#140D0A"   # warm near-black
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


# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0A0C12"), (1, "#05060A")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#4A5E78", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#141E2A"), (0.5, "#1C2A34"),
                 (0.78, "#242E28"), (1, "#100E0C")),
        stroke="#0A0C12", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#04060C", 0.55)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B4C6D4", strokeWidth=3, opacity=24)

# canopy light high on the right — island forest gloom with one warm shaft
d.shape("ellipse", "Canopy light", x=520, y=150, width=380, height=280,
        fill=rad((0, "#8A7E4E", 18), (0.6, "#665E38", 7), (1, "#665E38", 0)),
        stroke=NONE)
for i, (x, y, s) in enumerate([(300, 220, 4), (420, 170, 3), (660, 200, 3.5),
                               (740, 300, 3), (250, 330, 3)]):
    ell(f"Mote {i+1}", x, y, s, s, fill="#C8D8DC", opacity=26, stroke=NONE)
# distant trunk silhouettes, vertical, translucent
for i, (x, w) in enumerate([(210, 26), (790, 30), (700, 18)]):
    d.path(f"M{x},120 L{x + w},120 L{x + w + 8},{ch if (ch := 660) else 660} "
           f"L{x - 8},660 Z", f"Trunk {i+1}",
           fill=lin((x, 0), (x + w, 0), (0, "#1A2622", 70), (1, "#0C1410", 70)),
           stroke=NONE, opacity=60)

# --- forest floor: chord y=742 closing on the disc arc ------------------------------
ch = 742
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Forest floor",
       fill=lin((0, ch), (0, 880), (0, "#2A261C"), (0.5, "#181410"),
                (1, "#0A0806")), stroke=NONE)
line("Floor edge light", PCX - hch + 8, ch, PCX + hch - 8, ch, 3,
     "#5E5A44", opacity=40)
# litter flecks
for i, (x, y, w) in enumerate([(270, 756, 30), (400, 770, 36), (620, 762, 34),
                               (730, 752, 28), (330, 792, 30), (540, 800, 34)]):
    line(f"Litter {i+1}", x, y, x + w, y - 4, 4, "#6E5A34", opacity=55)

# --- the pigeon: standing full-body, three-quarter, crest fanned ---------------------
SLATE_HI = "#6E88A4"
SLATE_MID = "#46586E"
SLATE_LO = "#232E3C"
MAROON_HI = "#7E3A42"
MAROON_LO = "#3E181E"
LACE = "#E8EEF2"

# tail: short rounded wedge low behind the body, resting toward the floor
tail = [(566, 640), (616, 650), (652, 686), (648, 716), (606, 726),
        (566, 700)]
ext(tail)
d.path(smooth(tail), "Tail",
       fill=lin((560, 640), (660, 726), (0, SLATE_MID), (1, SLATE_LO)),
       stroke=INK, strokeWidth=3, join="round")
line("Tail tip bar", 596, 714, 640, 700, 4, "#101A24", opacity=70)

# legs: two sturdy red-grey legs planted on the floor
for f, x in enumerate((462, 538)):
    line(f"Leg {f+1}", x, 660, x - 2, 730, 9, "#6E4A4A")
    # toes forward + one back, dark
    for j, dx in enumerate((-16, 0, 14)):
        line(f"Toe {f+1}.{j+1}", x - 2, 730, x - 2 + dx, 740, 5, "#4A3232")
    line(f"Toe back {f+1}", x - 2, 730, x - 16, 736, 5, "#3E2A2A")

# body: tall pear, breast forward-left, ceremonial upright
body = [(452, 428), (522, 420), (580, 452), (612, 520), (618, 596),
        (596, 664), (548, 700), (490, 706), (436, 686), (404, 634),
        (396, 556), (408, 484)]
ext(body)
d.path(smooth(body), "Body",
       fill=lin((390, 420), (620, 706), (0, SLATE_HI), (0.55, SLATE_MID),
                (1, SLATE_LO)),
       stroke=INK, strokeWidth=3, join="round")

# maroon breast: the species' wine-dark shield on the front
breast = [(430, 470), (470, 452), (512, 470), (528, 534), (516, 610),
          (480, 660), (442, 650), (420, 584), (416, 520)]
d.path(smooth(breast), "Maroon breast",
       fill=rad((0, MAROON_HI), (0.65, "#5E2830"), (1, MAROON_LO)),
       stroke=INK, strokeWidth=2.5, join="round", opacity=92)

# folded wing on the flank with the pale double wing-bar
wing = [(512, 460), (566, 476), (592, 534), (590, 610), (556, 664),
        (516, 648), (500, 576), (498, 508)]
d.path(smooth(wing), "Wing",
       fill=lin((500, 460), (590, 664), (0, "#3E5064"), (1, "#1A2430")),
       stroke=INK, strokeWidth=3, join="round")
d.path("M506,540 C540,534 570,540 590,554", "Wing bar 1", fill=NONE,
       stroke="#AEC4D8", strokeWidth=7, opacity=55, cap="round")
d.path("M504,568 C538,562 568,568 588,582", "Wing bar 2", fill=NONE,
       stroke="#0E1620", strokeWidth=5, opacity=60, cap="round")

# neck into the small head
neck = [(452, 428), (452, 386), (472, 356), (506, 350), (524, 376),
        (516, 420)]
ext(neck)
d.path(smooth(neck), "Neck",
       fill=lin((450, 350), (525, 428), (0, "#5E7894"), (1, "#2E3E50")),
       stroke=INK, strokeWidth=3, join="round")

# head: small and neat under the crown
head = [(452, 386), (456, 354), (482, 336), (512, 342), (524, 366),
        (516, 394), (490, 406), (464, 402)]
ext(head)
d.path(smooth(head), "Head",
       fill=rad((0, "#7E98B4"), (0.7, "#546A84"), (1, "#2E3E50")),
       stroke=INK, strokeWidth=3, join="round")
# small dark bill pointing down-left, pale tip
d.path(smooth([(456, 392), (438, 402), (430, 414), (442, 420), (456, 412),
               (464, 400)]), "Bill", fill="#1E2A34",
       stroke=INK, strokeWidth=2.5, join="round")
ell("Bill tip", 436, 414, 4, 3, fill="#C8D4DC", opacity=80, stroke=NONE)
# the red eye, ringed pale
ell("Eye ring", 488, 372, 11, 11, fill="#C8D4DC", opacity=70, stroke=NONE)
ell("Eye", 488, 372, 8, 8, fill=rad((0, "#D04030"), (1, "#8E1E18")),
    stroke=INK, strokeWidth=2)
ell("Pupil", 488, 372, 3.5, 3.5, fill="#0E0A08", stroke=NONE)
ell("Eye glint", 485, 369, 2, 2, fill="#FFFFFF", opacity=85, stroke=NONE)

# the lace crown: a fan of shafts from the crown, each tipped with lace
CX, CY = 486, 344
crest_tips = []
for i, ang in enumerate(range(-165, -14, 15)):
    a = math.radians(ang)
    R = 118 + 14 * math.sin((i / 8.0) * math.pi)
    tx, ty = CX + R * math.cos(a), CY + R * math.sin(a)
    crest_tips.append((tx, ty, a))
    # shaft, slightly curved outward — draw as quad path for control
    mx, my = CX + R * 0.55 * math.cos(a + 0.12), CY + R * 0.55 * math.sin(a + 0.12)
    d.path(f"M{CX},{CY} Q{mx:.1f},{my:.1f} {tx:.1f},{ty:.1f}",
           f"Crest shaft {i+1}", fill=NONE, stroke="#8AA2BC",
           strokeWidth=4, cap="round")
    ext([(tx, ty)])
# lace tips: pale spatulate flags at every shaft end
for i, (tx, ty, a) in enumerate(crest_tips):
    nx, ny = -math.sin(a), math.cos(a)
    tx2, ty2 = tx + math.cos(a) * 16, ty + math.sin(a) * 16
    flag = [(tx, ty), (tx + nx * 13 + math.cos(a) * 5, ty + ny * 13 + math.sin(a) * 5),
            (tx2, ty2),
            (tx - nx * 13 + math.cos(a) * 5, ty - ny * 13 + math.sin(a) * 5)]
    d.path(smooth(flag), f"Lace tip {i+1}",
           fill=lin((tx, ty), (tx2, ty2), (0, "#B8C8D8"), (1, LACE)),
           stroke=INK, strokeWidth=1.5, join="round", opacity=95)
    # lace barbs: two tiny strokes inside the flag
    for j, sgn in enumerate((-1, 1)):
        line(f"Lace barb {i+1}.{j+1}", tx + math.cos(a) * 4, ty + math.sin(a) * 4,
             tx + math.cos(a) * 12 + nx * sgn * 5,
             ty + math.sin(a) * 12 + ny * sgn * 5, 1.8, "#5E7488", opacity=70)
# crest base: the dark crown the fan springs from
d.path(smooth([(452, 356), (470, 330), (502, 326), (522, 346), (510, 362),
               (482, 362), (462, 366)]), "Crest base",
       fill="#1A2430", stroke=INK, strokeWidth=2.5, join="round")

# ceremony rim light along the back, catching the canopy shaft
d.path("M578,452 C606,500 614,560 606,616", "Back rim light", fill=NONE,
       stroke="#8A9660", strokeWidth=3.5, opacity=38, cap="round")

# contact shadow
d.shape("ellipse", "Foot shadow", x=430, y=730, width=190, height=16,
        fill=rad((0, "#000000", 55), (1, "#000000", 0)), stroke=NONE)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("pigeon extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


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


def caption(name, mats, size=58):
    n = d.text(name, "Name", x=500, y=932, size=size, font="Virelai Sans",
               color="#E8E4DA", justify="center")
    m = d.text(mats, "Second line", x=500, y=970, size=22, font="Virelai Sans",
               color="#9AA8B4", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
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


caption("VICTORIA CROWNED PIGEON", "COLUMBIFORMES · GOURA VICTORIA", size=46)
d.finish("victoria-crowned-pigeon-V1R00")

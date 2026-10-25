#!/usr/bin/env python3
"""Keel-billed toucan — field plate V1R00. Belize lowland forest: Ramphastos
sulfuratus perched on a mossy diagonal branch, body in three-quarter, the
huge bill in clear left profile — green keel, orange culmen ridge, red tip,
maroon base. Yellow throat bib, blue eye surround, black plumage, white
rump, red undertail, zygodactyl feet two-forward two-back on the branch.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Keel-Billed Toucan — Field Plate", 1000, 1000)

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
        fill=lin((0, 0), (0, 1000), (0, "#0A0E0C"), (1, "#040705")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#3E5A48", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#101C14"), (0.5, "#16281C"),
                 (0.8, "#1E2A18"), (1, "#0E100A")),
        stroke="#0A0C12", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#030804", 0.55)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8C4AE", strokeWidth=3, opacity=24)

# canopy shaft: warm green light falling from upper right
d.shape("ellipse", "Canopy light", x=480, y=140, width=400, height=300,
        fill=rad((0, "#7E9448", 20), (0.6, "#5E7038", 7), (1, "#5E7038", 0)),
        stroke=NONE)
# out-of-focus foliage blobs, translucent deep green
for i, (x, y, rx, ry) in enumerate([(210, 250, 90, 60), (290, 180, 70, 46),
                                    (760, 300, 80, 56), (700, 190, 60, 44),
                                    (170, 420, 70, 52)]):
    ell(f"Foliage {i+1}", x, y, rx, ry, fill="#16281C", opacity=70, stroke=NONE)
    ell(f"Foliage hi {i+1}", x - 14, y - 12, rx * 0.5, ry * 0.5,
        fill="#2E4A30", opacity=40, stroke=NONE)
# motes in the shaft
for i, (x, y, s) in enumerate([(560, 260, 4), (640, 330, 3), (700, 240, 3.5),
                               (500, 340, 3), (430, 260, 3)]):
    ell(f"Mote {i+1}", x, y, s, s, fill="#D8E4B8", opacity=28, stroke=NONE)

# low forest-floor shade band closing on the disc arc
ch = 800
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Floor shade", fill=lin((0, ch), (0, 880), (0, "#141A10"),
                               (1, "#080A05")), stroke=NONE)

# --- the branch: mossy diagonal, subordinate, ends inside the disc --------------------
branch = [(244, 692), (244, 676), (480, 650), (748, 614), (752, 632),
          (486, 670)]
ext(branch)
d.path(smooth(branch), "Branch",
       fill=lin((0, 610), (0, 700), (0, "#4A3A28"), (0.6, "#2E2218"),
                (1, "#181008")),
       stroke=INK, strokeWidth=3, join="round")
# moss flecks along the top edge
for i, (x, y, w) in enumerate([(300, 672, 40), (420, 660, 46), (560, 644, 38),
                               (670, 626, 34)]):
    line(f"Moss {i+1}", x, y, x + w, y - 8, 5, "#5E7A3A", opacity=60)
# leaf sprigs off the branch ends
for i, (cx, cy, sgn) in enumerate([(250, 664, -1), (742, 606, 1)]):
    for j, (dx, dy) in enumerate([(0, -34), (sgn * 22, -22), (sgn * 10, -44)]):
        pts = [(cx, cy), (cx + dx * 0.5 - sgn * 8, cy + dy * 0.5),
               (cx + dx, cy + dy), (cx + dx * 0.5 + sgn * 8, cy + dy * 0.55)]
        d.path(smooth(pts), f"Sprig {i+1}.{j+1}",
               fill=lin((cx, cy + dy), (cx, cy), (0, "#3E6030"), (1, "#1C3018")),
               stroke=INK, strokeWidth=1.5, join="round", opacity=95)

# --- the toucan: perched, three-quarter body, bill in left profile ---------------------
BLACK_HI = "#332A28"
BLACK_MID = "#1C1414"
BLACK_LO = "#0C0808"
YEL_HI = "#F4D258"
YEL_LO = "#D8A83A"
BLUE = "#4A90C0"

# tail: long, hanging down past the branch, slight outward tilt right
tail = [(548, 640), (596, 640), (606, 700), (600, 778), (576, 814),
        (546, 808), (534, 740), (534, 682)]
ext(tail)
d.path(smooth(tail), "Tail",
       fill=lin((530, 640), (610, 815), (0, BLACK_MID), (1, BLACK_LO)),
       stroke=INK, strokeWidth=3, join="round")
# red undertail coverts: the species' flag
d.path(smooth([(536, 688), (560, 676), (580, 690), (576, 726), (548, 734),
               (534, 712)]), "Undertail red",
       fill=lin((0, 676), (0, 734), (0, "#C84030"), (1, "#7E1E16")),
       stroke=INK, strokeWidth=2.5, join="round")

# body: upright pear, chest forward-left, back right
body = [(452, 452), (508, 438), (560, 458), (590, 508), (600, 566),
        (588, 634), (556, 686), (512, 700), (468, 686), (438, 640),
        (426, 574), (430, 508)]
ext(body)
d.path(smooth(body), "Body",
       fill=lin((420, 440), (600, 700), (0, BLACK_HI), (0.5, BLACK_MID),
                (1, BLACK_LO)),
       stroke=INK, strokeWidth=3, join="round")

# white rump patch tucked into the body's rear edge above the tail base
d.path(smooth([(550, 606), (580, 596), (596, 612), (588, 636), (558, 636)]),
       "Rump white",
       fill=lin((0, 596), (0, 636), (0, "#F0E8D8"), (1, "#C8BCA4")),
       stroke=INK, strokeWidth=2, join="round")

# folded wing on the flank, slightly lighter edge feathering
wing = [(540, 470), (586, 494), (592, 552), (576, 622), (540, 662),
        (508, 640), (500, 574), (510, 508)]
d.path(smooth(wing), "Wing",
       fill=lin((500, 470), (590, 660), (0, "#241C1A"), (1, "#0A0606")),
       stroke=INK, strokeWidth=3, join="round")
for i, (y0, y1) in enumerate([(520, 580), (560, 618)]):
    d.path(f"M518,{y0} C546,{y0 + 8} 566,{y1 - 8} 572,{y1}", f"Feather {i+1}",
           fill=NONE, stroke="#060404", strokeWidth=3, opacity=55, cap="round")

# yellow bib: face front + throat + chest, the species' great yellow bib
bib = [(424, 420), (452, 402), (492, 404), (516, 432), (516, 486),
       (500, 548), (470, 596), (446, 616), (428, 574), (418, 500)]
ext(bib)
d.path(smooth(bib), "Yellow bib",
       fill=lin((410, 400), (520, 620), (0, YEL_HI), (0.6, "#E8BE46"),
                (1, YEL_LO)),
       stroke=INK, strokeWidth=3, join="round")
# bib's lower edge: the fine red crescent keel-billeds carry under the bib
d.path("M434,608 C456,622 486,624 506,606", "Bib red edge", fill=NONE,
       stroke="#B03028", strokeWidth=6, opacity=85, cap="round")

# head + crown behind the bib
head = [(416, 402), (428, 352), (462, 322), (502, 320), (524, 348),
        (522, 390), (498, 420), (452, 424)]
ext(head)
d.path(smooth(head), "Head",
       fill=lin((420, 320), (520, 424), (0, "#2E2422"), (1, "#100A0A")),
       stroke=INK, strokeWidth=3, join="round")
# yellow cheek patch wrapping under the bill base
d.path(smooth([(414, 396), (428, 366), (452, 356), (470, 372), (464, 404),
               (440, 420), (420, 416)]), "Cheek yellow",
       fill=lin((0, 356), (0, 420), (0, YEL_HI), (1, "#D8B040")),
       stroke=INK, strokeWidth=2.5, join="round")

# blue eye surround + eye on the cheek patch
ell("Eye surround", 452, 386, 15, 13,
    fill=rad((0, "#6EB0D8"), (1, "#2E5E82")), stroke=INK, strokeWidth=2)
ell("Eye", 452, 386, 6.5, 6.5, fill="#0E0A08", stroke=NONE)
ell("Eye glint", 449, 383, 2.2, 2.2, fill="#FFFFFF", opacity=85, stroke=NONE)

# --- the bill: the plate's main event, full profile pointing left --------------------
# overall shape: deep at the base, tapering to a slightly dropped tip
bill = [(438, 342), (380, 330), (310, 344), (258, 378), (236, 408),
        (240, 424), (268, 432), (330, 440), (392, 448), (438, 452),
        (452, 420), (452, 372)]
ext(bill)
d.path(smooth(bill), "Bill",
       fill=lin((240, 330), (452, 452), (0, "#A8C84A"), (0.45, "#7AA838"),
                (0.8, "#4A7028"), (1, "#345020")),
       stroke=INK, strokeWidth=3, join="round")
# orange culmen ridge along the top edge
d.path("M436,346 C380,334 316,346 262,382 C246,392 238,402 237,410 "
       "C258,398 300,372 348,360 C388,350 420,348 436,352 Z",
       "Culmen orange",
       fill=lin((240, 334), (436, 360), (0, "#E89A34"), (1, "#B8681E")),
       stroke=NONE, opacity=92)
# red tip patch
d.path(smooth([(238, 402), (236, 408), (240, 424), (266, 430), (284, 424),
               (280, 404), (262, 390)]),
       "Bill tip red",
       fill=lin((236, 390), (284, 430), (0, "#D04834"), (1, "#8E221A")),
       stroke=INK, strokeWidth=2.5, join="round")
# maroon basal patch + the pale base line keel-billeds show
d.path(smooth([(410, 352), (438, 342), (452, 372), (452, 420), (438, 452),
               (414, 444), (404, 400)]),
       "Bill base maroon",
       fill=lin((404, 342), (452, 452), (0, "#5E2A22"), (1, "#381410")),
       stroke=NONE, opacity=95)
d.path("M446,360 C450,384 450,414 444,442", "Base line", fill=NONE,
       stroke="#D8E4E8", strokeWidth=4, opacity=75, cap="round")
# tomial sheen: soft light along the bill's midline
d.path("M300,400 C350,414 400,424 436,428", "Tomium light", fill=NONE,
       stroke="#D8EC9A", strokeWidth=3.5, opacity=40, cap="round")
# breath-shade at the throat where bill meets bib
d.shape("ellipse", "Bill root shade", x=430, y=410, width=40, height=60,
        fill=rad((0, "#000000", 30), (1, "#000000", 0)), stroke=NONE)

# --- feet: zygodactyl grip, two toes forward two back, blue-grey ----------------------
for f, (sx, by) in enumerate(((468, 646), (516, 640))):
    # shank down to the branch
    line(f"Shank {f+1}", sx, by - 18, sx - 2, by + 6, 8, "#4A6070")
    # two toes curling over the front lip of the branch
    for j, (dx, dy) in enumerate(((-14, 16), (2, 20))):
        d.path(f"M{sx - 2},{by + 4} Q{sx + dx},{by + dy} {sx + dx - 4},{by + dy + 12}",
               f"Foot {f+1} front toe {j+1}", fill=NONE, stroke="#5A7080",
               strokeWidth=5, cap="round")
    # two toes hooking behind the branch
    for j, (dx, dy) in enumerate(((10, 14), (18, 8))):
        d.path(f"M{sx - 2},{by + 4} Q{sx + dx},{by + dy} {sx + dx + 4},{by + dy + 10}",
               f"Foot {f+1} rear toe {j+1}", fill=NONE, stroke="#46586A",
               strokeWidth=5, cap="round")

# canopy rim light on the back
d.path("M516,442 C560,460 586,506 592,560", "Back rim light", fill=NONE,
       stroke="#7E9448", strokeWidth=3.5, opacity=40, cap="round")

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("toucan extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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


def caption(name, mats):
    n = d.text(name, "Name", x=500, y=932, size=58, font="Virelai Sans",
               color="#E8E4DA", justify="center")
    m = d.text(mats, "Second line", x=500, y=970, size=22, font="Virelai Sans",
               color="#9AAE9E", justify="center")
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


caption("KEEL-BILLED TOUCAN", "RAMPHASTOS SULFURATUS")
d.finish("keel-billed-toucan-V1R00")

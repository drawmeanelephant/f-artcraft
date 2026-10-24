#!/usr/bin/env python3
"""z-filed-fyi — commemorative plate V1R00. The Bilingual Specimen: an open
field-guide spread on the disc — left page English, right page Chinese, a
small GLM specimen pinned at the gutter like a collected butterfly.
Ink black, vermilion accent, archival paper. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("z-filed-fyi — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241A10"              # warm dark, never pure black
VERM = "#C23A1E"             # vermilion accent
PAPER_HI = "#F0E5C6"
PAPER_LO = "#CDBB90"

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None, extra=None):
    stops = [{"offset": 0, "color": c0}]
    if extra: stops += extra
    stops.append({"offset": 1, "color": c1})
    g = {"kind": "linear", "stops": stops}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#17110B", "#050403", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#3B2E1E"},
                 {"offset": 0.66, "color": "#201709"},
                 {"offset": 1, "color": "#100B05"}),
        stroke="#B08C58", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D8B0", strokeWidth=3, opacity=26)
# archival flecks
for i, (x, y, w) in enumerate([(208,240,5),(800,236,4),(158,470,4),(848,486,5),
                               (252,712,4),(742,740,5),(340,118,4),(654,112,4),
                               (146,610,3),(860,630,4),(436,816,3),(588,812,4)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Fleck {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#E8D8B0", opacity=18, stroke=NONE)
# faint cataloguing grid behind the book
for i, xx in enumerate(range(260, 745, 60)):
    d.path(f"M{xx},170 L{xx},770", f"Grid v{i+1}", fill=NONE,
           stroke="#E8D8B0", strokeWidth=1.5, opacity=6)
for i, yy in enumerate(range(200, 775, 60)):
    d.path(f"M230,{yy} L770,{yy}", f"Grid h{i+1}", fill=NONE,
           stroke="#E8D8B0", strokeWidth=1.5, opacity=6)

# --- the open book -------------------------------------------------------------
# cast shadow on the plate
d.shape("ellipse", "Book shadow", x=215, y=664, width=570, height=44,
        fill=rad({"offset": 0, "color": "#0A0703", "opacity": 0.55},
                 {"offset": 1, "color": "#0A0703", "opacity": 0}), stroke=NONE)
# cover, a touch larger than the page block, dark cloth
d.path("M208,320 Q358,296 500,328 Q642,296 792,320 "
       "L800,646 Q644,624 504,658 L496,658 Q356,624 200,646 Z",
       "Cover", fill=lin("#4A3626", "#241809", (500, 300), (500, 660)),
       stroke=INK, strokeWidth=5)
# cover edge highlight
d.path("M212,322 Q358,300 500,332 Q642,300 788,322", "Cover top edge",
       fill=NONE, stroke="#8A6A44", strokeWidth=3, opacity=55, cap="round")
# left page
d.path("M226,332 Q360,314 498,340 L498,652 Q358,626 224,642 "
       "Q216,486 226,332 Z", "Page left",
       fill=lin(PAPER_HI, PAPER_LO, (300, 320), (380, 650),
                extra=[{"offset": 0.55, "color": "#E4D6B2"}]),
       stroke="#8A7448", strokeWidth=3)
# right page
d.path("M774,332 Q640,314 502,340 L502,652 Q642,626 776,642 "
       "Q784,486 774,332 Z", "Page right",
       fill=lin("#E8DCB8", "#C4B086", (700, 320), (620, 650),
                extra=[{"offset": 0.55, "color": "#DECFA6"}]),
       stroke="#8A7448", strokeWidth=3)
# page-edge stacks along the outer margins
for j in range(3):
    off = 8 + j * 5
    d.path(f"M{226 - off*0.4},{336 + off} Q{216 - off*0.4},486 {224 - off*0.4},{638 - off}",
           f"Page edge L{j+1}", fill=NONE, stroke="#B09A6C", strokeWidth=2, opacity=40)
    d.path(f"M{774 + off*0.4},{336 + off} Q{784 + off*0.4},486 {776 + off*0.4},{638 - off}",
           f"Page edge R{j+1}", fill=NONE, stroke="#B09A6C", strokeWidth=2, opacity=40)
# gutter shadow
d.path("M486,340 Q500,496 486,650 L514,650 Q500,496 514,340 Z",
       "Gutter shade", fill=rad({"offset": 0, "color": "#3A2A12", "opacity": 0.42},
                                {"offset": 1, "color": "#3A2A12", "opacity": 0}),
       stroke=NONE)

# --- left page: English column --------------------------------------------------
d.text("FIELD NOTES", "EN header", x=356, y=392, size=15,
       font="Source Sans 3", color="#4A3820", justify="center")
d.path("M290,402 L422,402", "EN rule", fill=NONE, stroke=VERM,
       strokeWidth=3, opacity=85, cap="round")
d.text("two tongues, one guide", "EN line 1", x=344, y=434, size=11.5,
       font="Source Sans 3", color="#5E4C2E", justify="center")
for i, yy in enumerate((456, 478, 500)):
    d.path(f"M268,{yy} L444,{yy}", f"EN ruled {i+1}", fill=NONE,
           stroke="#A8905E", strokeWidth=2.5, opacity=40, cap="round")
# folio number, low on the page
d.text("spec. no. 112", "EN folio", x=356, y=596, size=10,
       font="Source Sans 3", color="#7A6438", justify="center")

# --- right page: Chinese column -------------------------------------------------
d.text("田野笔记", "CN header", x=648, y=394, size=19,
       font="Noto Sans CJK SC", color="#4A3820", justify="center")
d.path("M578,404 L718,404", "CN rule", fill=NONE, stroke=VERM,
       strokeWidth=3, opacity=85, cap="round")
d.text("双语标本", "CN line 1", x=648, y=438, size=13,
       font="Noto Sans CJK SC", color="#5E4C2E", justify="center")
d.text("采自档案深处", "CN line 2", x=648, y=462, size=11.5,
       font="Noto Sans CJK SC", color="#5E4C2E", justify="center")
for i, yy in enumerate((484, 506)):
    d.path(f"M556,{yy} L740,{yy}", f"CN ruled {i+1}", fill=NONE,
           stroke="#A8905E", strokeWidth=2.5, opacity=40, cap="round")
# small vermilion seal square beside the folio line
d.shape("rectangle", "Seal", x=700, y=586, width=16, height=16,
        fill=VERM, opacity=80, stroke=NONE)

# --- the vermilion bookmark ribbon ----------------------------------------------
d.path("M508,656 C516,690 510,716 520,744 L534,738 C524,712 532,688 520,656 Z",
       "Ribbon", fill=lin("#D8442A", "#8C2412", (510, 656), (532, 744)),
       stroke="#6E1808", strokeWidth=2.5)
d.path("M520,744 L527,732 L534,738 Z", "Ribbon notch", fill="#1A1208",
       stroke=NONE)

# --- the GLM specimen, pinned at the gutter --------------------------------------
BX = 500   # body axis
# wing shadow on the pages
for sgn in (-1, 1):
    d.path(f"M{BX+sgn*10},462 C{BX+sgn*80},410 {BX+sgn*96},438 {BX+sgn*84},470 "
           f"C{BX+sgn*78},496 {BX+sgn*36},502 {BX+sgn*10},492 Z",
           f"Wing shadow {'L' if sgn<0 else 'R'}", fill="#3A2A12", opacity=25,
           stroke=NONE)
# forewings
for sgn, tag in ((-1, "L"), (1, "R")):
    d.path(f"M{BX+sgn*7},452 C{BX+sgn*40},398 {BX+sgn*86},392 {BX+sgn*88},442 "
           f"C{BX+sgn*89},478 {BX+sgn*40},492 {BX+sgn*8},486 Z",
           f"Forewing {tag}",
           fill=lin("#3A2A1C", "#181008", (BX, 400), (BX+sgn*88, 480)),
           stroke=INK, strokeWidth=3)
    # hindwings
    d.path(f"M{BX+sgn*8},492 C{BX+sgn*50},496 {BX+sgn*66},522 {BX+sgn*54},556 "
           f"C{BX+sgn*42},576 {BX+sgn*12},556 {BX+sgn*7},524 Z",
           f"Hindwing {tag}",
           fill=lin("#33241A", "#140D06", (BX, 496), (BX+sgn*56, 566)),
           stroke=INK, strokeWidth=3)
    # vermilion submarginal spots on the forewing
    for j, (dx, dy, r) in enumerate(((56, 430, 6), (68, 452, 5), (46, 452, 4))):
        d.shape("ellipse", f"Verm spot {tag}{j+1}",
                x=BX+sgn*dx-r, y=dy-r, width=r*2, height=r*2,
                fill=VERM, opacity=88, stroke=NONE)
    # pale marginal band on the hindwing
    d.path(f"M{BX+sgn*18},528 C{BX+sgn*40},536 {BX+sgn*50},546 {BX+sgn*48},556",
           f"Hind band {tag}", fill=NONE, stroke="#E8D8B0", strokeWidth=3,
           opacity=55, cap="round")
    # a wing vein or two
    d.path(f"M{BX+sgn*10},468 C{BX+sgn*44},444 {BX+sgn*66},428 {BX+sgn*82},436",
           f"Vein {tag}a", fill=NONE, stroke="#0E0904", strokeWidth=2.5,
           opacity=50, cap="round")
# body: abdomen + thorax + head
d.shape("ellipse", "Abdomen", x=BX-6, y=486, width=12, height=66,
        fill=lin("#33241A", "#140D06", (BX, 486), (BX, 552)), stroke=INK,
        strokeWidth=2.5)
d.shape("ellipse", "Thorax", x=BX-8, y=444, width=16, height=48,
        fill=lin("#3E2C1C", "#1A110A", (BX, 444), (BX, 492)), stroke=INK,
        strokeWidth=2.5)
d.shape("ellipse", "Head", x=BX-6, y=430, width=12, height=13,
        fill="#241810", stroke=INK, strokeWidth=2)
# antennae, clubbed — ≥3pt strokes so they survive plate scale
for sgn in (-1, 1):
    d.path(f"M{BX+sgn*3},432 C{BX+sgn*16},408 {BX+sgn*26},402 {BX+sgn*34},396",
           f"Antenna {'L' if sgn<0 else 'R'}", fill=NONE, stroke=INK,
           strokeWidth=3, cap="round")
    d.shape("ellipse", f"Antenna club {'L' if sgn<0 else 'R'}",
            x=BX+sgn*34-3, y=392, width=6, height=7, fill=INK, stroke=NONE)
# the pin through the thorax
d.path(f"M{BX},398 L{BX},586", "Pin", fill=NONE, stroke="#B8BCBE",
       strokeWidth=3, cap="round")
d.shape("ellipse", "Pin head", x=BX-4, y=390, width=8, height=8,
        fill="#D8DCDe", stroke="#7A7E80", strokeWidth=1.5)
# pin drop-shadow on the page
d.path(f"M{BX+3},560 L{BX+3},596", "Pin shadow", fill=NONE,
       stroke="#3A2A12", strokeWidth=3, opacity=30, cap="round")
# the specimen label, pinned under the wings
d.shape("rectangle", "Specimen label", x=462, y=596, width=76, height=30,
        fill=lin("#F4ECD8", "#DCCDA6", (462, 596), (538, 626)),
        stroke=INK, strokeWidth=2.5)
d.text("GLM · No. 7", "Label text", x=500, y=615, size=11,
       font="Source Sans 3", color="#3A2C14", justify="center")

# --- name + role ------------------------------------------------------------------
d.text("Z.FILED.FYI", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F0E4C0", justify="center")
LINE2, SZ2, TRK = "BILINGUAL FIELD GUIDE", 24, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#C09A5E", justify="center")
d.cmd("text.setStyle", "Second line tracking", ids=[r["id"]], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("z-filed-fyi-V1R00")

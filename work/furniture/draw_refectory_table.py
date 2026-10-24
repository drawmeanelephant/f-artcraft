#!/usr/bin/env python3
"""Refectory table — field plate V1R00. Front-near view of the monastery
dining table: a long oak slab on a deep carved apron, carried by four
cup-and-cover bulb legs (turned-profile silhouettes) locked low by a
perimeter stretcher, with a third row of legs hinted behind. Breadboard
ends, butterfly keys and pegged joints on the top; two candles stage the
communal mood. Oak plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Refectory Table — Field Plate", 1000, 1000)

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


def note(*pts):
    EXTENT.extend(pts)


OAK = ((0, "#C89A5A"), (0.4, "#A8763E"), (0.75, "#7A5028"), (1, "#4A2E14"))
OAK_DARK = ((0, "#8A5E30"), (0.5, "#5E3C1C"), (1, "#34200C"))
OAK_HI = "#E0B478"
IRON = rad((0, "#6E6A62"), (0.6, "#3C3832"), (1, "#1C1A16"))

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#191410"), (1, "#0A0705")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#9A7A46", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6E5732"), (0.6, "#4A3A20"), (1, "#1E1508")),
        stroke="#120C06", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D2A4", strokeWidth=3, opacity=24)
d.shape("ellipse", "Hearth light", x=160, y=120, width=580, height=540,
        fill=rad((0, "#F2C87E", 18), (0.55, "#AE8148", 6), (1, "#6E4A28", 0)),
        stroke=NONE)
for i, (x, y, w) in enumerate([(212, 232, 6), (776, 248, 7), (174, 616, 6), (824, 594, 7),
                               (432, 106, 6), (634, 110, 7), (168, 422, 6), (838, 416, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4A46A", opacity=30, stroke=NONE)

FY = 742
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4E4230", 40), (1, "#140E06", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E8D0A0", strokeWidth=2, opacity=18)

# long soft shadow hugging the feet
d.shape("ellipse", "Table shadow", x=150, y=686, width=700, height=58,
        fill=rad((0, "#050302", 60), (0.6, "#050302", 24), (1, "#050302", 0)),
        stroke=NONE)

# --- back row of legs: darker, set higher; feet hidden behind the stretcher ----------
BULB_FAR = [(0, 9), (10, 9), (16, 6), (24, 14), (36, 17), (48, 11),
            (54, 6), (64, 5), (72, 10), (80, 12), (92, 9),
            (112, 8), (140, 8.5), (168, 9), (186, 10), (192, 8)]

def far_leg(x):
    """Back leg silhouette: (y, halfwidth) profile mapped to 502..694, dimmed."""
    L = [(x - w, 502 + y) for y, w in BULB_FAR]
    R = [(x + w, 502 + y) for y, w in reversed(BULB_FAR)]
    pts = L + R
    d.path(smooth(pts, closed=True), f"Back leg {int(x)}", fill="#2A1808",
           stroke="#140A04", strokeWidth=2.5, opacity=78)
    note(*pts)

for bx in (300, 500, 700):
    far_leg(bx)

# side stretchers receding from the front end legs to the back pair
for (x0, x1) in ((232, 296), (768, 704)):
    d.path(f"M{x0},652 L{x1},606 L{x1},622 L{x0},668 Z", f"Side stretcher {x0}",
           fill=lin((0, 606), (0, 668), *OAK_DARK), stroke=INK, strokeWidth=2.5,
           join="round", opacity=85)

# --- perimeter stretcher: the long low beam joining all front legs -------------------
d.path("M196,644 L804,644 L808,656 L804,672 L196,672 L192,656 Z", "Long stretcher",
       fill=lin((0, 644), (0, 672), *OAK_DARK), stroke=INK, strokeWidth=3, join="round")
note((196, 644), (804, 644), (196, 672), (804, 672))
d.path("M204,648 L796,648", "Stretcher lip light", fill=NONE, stroke=OAK_HI,
       strokeWidth=2.4, cap="round", opacity=45)
# pegs pinning the stretcher into the end legs
for px in (224, 776):
    d.shape("ellipse", "Stretcher peg", x=px - 4, y=654, width=8, height=7,
            fill=rad((0, "#9A6E3C"), (1, "#3A240E")), stroke=INK, strokeWidth=1.2)

# --- the four front legs: cup-and-cover bulb turning -----------------------------------
BULB = [(525, 14), (546, 14), (552, 9), (560, 8), (566, 18), (578, 25),
        (594, 26), (606, 20), (612, 12), (618, 9), (626, 7), (634, 6.5),
        (642, 12), (650, 15), (656, 12), (662, 8), (678, 9), (690, 15),
        (704, 16), (712, 12)]

def front_leg(x, lit):
    """Cup-and-cover bulb leg: (y, halfwidth) silhouette via smooth(), lit edge."""
    L = [(x - w, y) for y, w in BULB]
    R = [(x + w, y) for y, w in reversed(BULB)]
    pts = L + R
    d.path(smooth(pts, closed=True), f"Bulb leg {int(x)}",
           fill=lin((x - 26, 0), (x + 26, 0), *OAK), stroke=INK, strokeWidth=3.2, join="round")
    note(*pts)
    # turned-member highlight on the lit side, echoing the silhouette
    mid = [(x - w * 0.38, y) for y, w in BULB]
    d.path(smooth(mid), f"Bulb leg {int(x)} light", fill=NONE, stroke=OAK_HI,
           strokeWidth=2.6, opacity=38, cap="round")
    shade = [(x + w * 0.55, y) for y, w in BULB]
    d.path(smooth(shade), f"Bulb leg {int(x)} shade", fill=NONE, stroke="#2A1606",
           strokeWidth=2.8, opacity=40, cap="round")
    # foot contact dot
    d.shape("ellipse", f"Foot pad {int(x)}", x=round(x - 13), y=712, width=26, height=6,
            fill="#1E0F04", stroke=NONE, opacity=80)

for lx, lit in ((225, True), (405, True), (595, False), (775, False)):
    front_leg(lx, lit)

# --- deep apron: carved frieze + moulded lower rail ------------------------------------
d.path("M186,466 L814,466 L816,522 Q500,536 184,522 Z", "Apron",
       fill=lin((0, 466), (0, 536), (0, "#A8763E"), (0.55, "#7A5028"), (1, "#4A2E14")),
       stroke=INK, strokeWidth=3.2, join="round")
note((186, 466), (814, 466), (184, 522), (816, 522))
# gadroon lunettes: a row of small carved half-arches between the legs
for gx in range(0, 11):
    cxg = 216 + gx * 56
    d.path(f"M{cxg - 16},506 A16,10 0 0 1 {cxg + 16},506",
           f"Lunette {gx + 1}", fill=NONE, stroke="#4A2E14", strokeWidth=2.2,
           opacity=70, cap="round")
    d.path(f"M{cxg - 12},508 A12,7 0 0 1 {cxg + 12},508",
           f"Lunette light {gx + 1}", fill=NONE, stroke=OAK_HI, strokeWidth=1.6,
           opacity=40, cap="round")
# apron lower moulding line
d.path("M190,516 Q500,530 810,516", "Apron moulding", fill=NONE, stroke="#3A240E",
       strokeWidth=2.6, opacity=60)
# square pegs where the legs are mortised into the apron
for px in (225, 405, 595, 775):
    d.shape("rectangle", "Apron peg", x=px - 3.5, y=472, width=7, height=7,
            fill=rad((0, "#8A5E30"), (1, "#34200C")), stroke=INK, strokeWidth=1.2)

# iron strap ends: flat bands wrapping the apron corners
d.path("M186,468 L214,468 L214,522 L184,522 Z", "Strap L", fill=IRON,
       stroke=INK, strokeWidth=2, opacity=92)
d.path("M814,468 L786,468 L786,522 L816,522 Z", "Strap R", fill=IRON,
       stroke=INK, strokeWidth=2, opacity=92)
for sx in (198, 800):
    d.shape("ellipse", "Strap rivet", x=sx - 3, y=488, width=6, height=6,
            fill="#1C1A16", stroke="#0A0908", strokeWidth=1)

# --- tabletop: receding surface + deep front band (blunt ends, trestle lesson) ---------
d.path("M232,392 L768,392 Q782,393 788,405 L822,424 Q830,434 816,434 "
       "L184,434 Q170,434 178,424 L212,405 Q218,392 232,392 Z", "Top surface",
       fill=lin((0, 392), (0, 434), (0, "#D8AA6A"), (0.5, "#BC8C4E"), (1, "#96683A")),
       stroke=INK, strokeWidth=3.5, join="round")
note((184, 434), (816, 434), (232, 392), (768, 392))
# plank seams converging toward the back edge
for i, (fx0, fx1) in enumerate([(300, 340), (420, 460), (560, 580), (680, 720)]):
    d.path(f"M{fx0},432 L{fx1},394", f"Plank seam {i+1}", fill=NONE,
           stroke="#7A5028", strokeWidth=2, opacity=45)
# breadboard cleat lines near the ends
d.path("M216,398 L186,430", "Cleat L", fill=NONE, stroke="#3A240E", strokeWidth=2.4, opacity=55)
d.path("M784,398 L814,430", "Cleat R", fill=NONE, stroke="#3A240E", strokeWidth=2.4, opacity=55)
# butterfly keys (dovetail inlays) locking the planks
for bx in (330, 500, 660):
    d.path(f"M{bx - 10},412 L{bx - 4},408 L{bx + 4},408 L{bx + 10},412 L{bx + 4},416 L{bx - 4},416 Z",
           f"Butterfly key", fill="#2A1606", stroke=INK, strokeWidth=1.4, opacity=85)
# long grain strokes
for i, (y, x0, x1) in enumerate([(402, 250, 720), (416, 230, 780), (426, 260, 740)]):
    d.path(f"M{x0},{y} C{(x0 + x1) / 2 - 60},{y - 3} {(x0 + x1) / 2 + 60},{y + 2} {x1},{y - 1}",
           f"Grain {i+1}", fill=NONE, stroke="#7A5028", strokeWidth=2.2,
           cap="round", opacity=35)
# front edge band — the slab's thickness, blunt overhang past the surface ends
d.path("M180,434 L820,434 Q836,434 836,446 L836,452 Q836,466 820,466 "
       "L180,466 Q164,466 164,452 L164,446 Q164,434 180,434 Z", "Top edge band",
       fill=lin((0, 434), (0, 466), *OAK_DARK), stroke=INK, strokeWidth=3.5, join="round")
note((164, 450), (836, 450))
d.path("M182,438 L818,438", "Top lip light", fill=NONE, stroke="#E8C088",
       strokeWidth=3, cap="round", opacity=55)
d.shape("ellipse", "Top knot", x=560, y=444, width=16, height=10,
        fill=rad((0, "#3A240E"), (1, "#5E3C1C")), opacity=70, stroke=NONE)

# --- two candles on the slab: the communal still life --------------------------------
def candle(cx, cy, tall):
    d.shape("ellipse", "Candle glow", x=round(cx - 40), y=round(cy - 66), width=80, height=80,
            fill=rad((0, "#F2C87E", 26), (0.6, "#C08A48", 8), (1, "#C08A48", 0)), stroke=NONE)
    d.shape("ellipse", "Candle foot", x=cx - 9, y=cy - 2, width=18, height=6,
            fill=rad((0, "#D9AE5E"), (1, "#6E4E1E")), stroke=INK, strokeWidth=1.4)
    d.shape("rectangle", "Candle wax", x=cx - 4, y=cy - tall, width=8, height=tall,
            fill=lin((cx - 4, cy - tall), (cx + 4, cy), (0, "#F4EAD2"), (1, "#C4AE84")),
            stroke="#6E5630", strokeWidth=1.4)
    d.path(f"M{cx},{cy - tall - 2} L{cx},{cy - tall - 7}", "Wick", fill=NONE,
           stroke="#241405", strokeWidth=1.6)
    d.shape("ellipse", "Flame", x=cx - 3.5, y=cy - tall - 20, width=7, height=13,
            fill=rad((0, "#FFF2C8"), (0.55, "#F0BE5A"), (1, "#C87828")), stroke=NONE)

candle(380, 392, 42)
candle(625, 392, 34)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("refectory extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 24, far


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
               color="#F4E8CE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#D2B078", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=240)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" %
              (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]


caption("REFECTORY TABLE", "OAK · WROUGHT IRON · WAX")
d.finish("refectory-table-V1R00")

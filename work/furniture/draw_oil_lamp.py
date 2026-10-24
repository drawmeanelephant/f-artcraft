#!/usr/bin/env python3
"""Oil lamp — field plate V1R00. Near-side view, slightly from above so the
glass rims read: a whale-era parlour lamp — spreading brass foot, baluster
stem, a glass font half full of oil, a brass burner with a knurled wick
knob, and a bulged glass chimney over a lit wick. The flame is the only
light on the plate: warm bloom inside cool dark. 1000x1000.
Turned-ware construction: lathe-profile outlines + section ellipses.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Oil Lamp — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241812"   # warm dark, not black
AX = 500          # lamp axis
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


def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"


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


def lathe(profile):
    """Right-half profile [(x,y)...] bottom->top -> closed symmetric silhouette."""
    left = [(2 * AX - x, y) for x, y in reversed(profile)]
    for p in profile + left:
        EXTENT.append(p)
    return smooth(profile + left)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#131A1E"), (1, "#070A0C")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6A7A72", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3E4A44"), (0.6, "#28332E"), (1, "#121A17")),
        stroke="#0A0F0C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2D8", strokeWidth=3, opacity=22)

# the lamp is the light: warm bloom behind it, then the floor
d.shape("ellipse", "Lamp bloom", x=180, y=110, width=640, height=620,
        fill=rad((0, "#E89A3C", 26), (0.45, "#B06A24", 9), (1, "#B06A24", 0)),
        stroke=NONE)

FY = 712
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4C564C", 34), (1, "#0E1410", 72)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#DEE6DA", strokeWidth=2, opacity=18)
# warm pool the lamp throws on the floor
d.shape("ellipse", "Floor light pool", x=290, y=664, width=420, height=72,
        fill=rad((0, "#D89034", 22), (1, "#D89034", 0)), stroke=NONE)
# lamp shadow under the foot
d.shape("ellipse", "Lamp shadow", x=404, y=686, width=192, height=28,
        fill=rad((0, "#040604", 72), (0.65, "#040604", 30), (1, "#040604", 0)),
        stroke=NONE)

# --- brass palette ------------------------------------------------------------------
BR_D, BR_L = "#3A2210", "#C98E3E"
BR_HI = "#F2C97E"


def brass(y0, y1, lo=0.0, hi=1.0):
    return lin((0, y0), (0, y1),
               (0, BR_D), (0.42, BR_L), (0.58, BR_HI), (0.78, "#8A5A22"), (1, BR_D))


# --- foot + stem: one turned-brass silhouette ---------------------------------------
foot_profile = [(408, 692), (410, 684), (420, 674), (436, 664), (452, 657),
                (464, 652), (468, 642), (466, 628), (459, 616), (455, 604),
                (453, 590), (456, 574), (462, 562), (466, 552)]
d.path(lathe(foot_profile), "Foot and stem", fill=brass(552, 692),
       stroke=INK, strokeWidth=2.2, join="round")
# foot rim and stem turning grooves
d.shape("ellipse", "Foot rim", x=408, y=684, width=184, height=15,
        fill=NONE, stroke="#F2C97E", strokeWidth=2.2, opacity=45)
for i, (y, rx) in enumerate([(618, 11), (596, 8), (562, 10)]):
    d.shape("ellipse", f"Stem groove {i+1}", x=AX - rx, y=y - 2,
            width=2 * rx, height=4, fill=NONE, stroke="#2A180A",
            strokeWidth=1.8, opacity=50)
# left-edge sheen down the stem
d.path("M452,664 C446,640 444,610 448,578", "Stem sheen", fill=NONE,
       stroke="#F2C97E", strokeWidth=4, opacity=30, cap="round")

# --- font: glass reservoir, half full of oil -----------------------------------------
font_profile = [(464, 556), (442, 551), (426, 542), (415, 530), (409, 517),
                (408, 505), (412, 491), (422, 480), (436, 473), (452, 468),
                (466, 465)]
GLASS = lin((0, 465), (0, 556), (0, "#C8DCD2", 34), (0.55, "#9ABAB0", 16),
            (1, "#5E847A", 30))
d.path(lathe(font_profile), "Font glass", fill=GLASS,
       stroke=INK, strokeWidth=2.0, join="round")
# oil: inset blob under a level line at y ~516
oil_profile = [(458, 551), (438, 546), (425, 538), (416, 528), (412, 518)]
oil_left = [(2 * AX - x, y) for x, y in reversed(oil_profile)]
oil_top = [(2 * AX - x, 518) for x, y in [(412, 518)]]
d.path(smooth(oil_profile + oil_left + [(412, 518)]),
       "Oil pool", fill=lin((0, 512), (0, 552), (0, "#C07818"),
                            (0.6, "#8A5210"), (1, "#5A3408")),
       stroke=NONE, opacity=92)
d.shape("ellipse", "Oil surface", x=412, y=511, width=176, height=11,
        fill="#E0A83E", opacity=80, stroke="#5A3408", strokeWidth=1.6)
# glass wall highlights and a dark refracted band at the bowl bottom
d.path("M428,494 C420,508 419,524 427,540", "Font sheen L", fill=NONE,
       stroke="#F4FBF6", strokeWidth=5, opacity=38, cap="round")
d.path("M572,492 C580,508 580,524 573,538", "Font sheen R", fill=NONE,
       stroke="#DCEAE2", strokeWidth=3, opacity=20, cap="round")
d.shape("ellipse", "Font base refraction", x=438, y=544, width=124, height=16,
        fill="#2E4A42", opacity=45, stroke=NONE)
# font lip rim
d.shape("ellipse", "Font neck rim", x=466, y=460, width=68, height=10,
        fill=NONE, stroke="#EAF4EE", strokeWidth=2, opacity=45)

# --- burner: collar, gallery, wick tube, adjuster knob --------------------------------
burner_profile = [(466, 464), (462, 458), (462, 452), (468, 446), (470, 438),
                  (470, 430)]
d.path(lathe(burner_profile), "Burner collar", fill=brass(428, 466),
       stroke=INK, strokeWidth=1.8, join="round")
d.shape("ellipse", "Collar ring", x=462, y=446, width=76, height=9,
        fill=NONE, stroke="#2A180A", strokeWidth=1.6, opacity=55)
# wick tube
d.path("M488,430 L488,414 Q488,410 492,410 L508,410 Q512,410 512,414 L512,430 Z",
       "Wick tube", fill=lin((0, 408), (0, 432), (0, "#6A4218"), (0.5, BR_HI),
                             (1, "#4A2A0E")), stroke=INK, strokeWidth=1.6)
# the wick itself, charred at the top
d.path("M493,410 L493,398 Q493,394 500,394 Q507,394 507,398 L507,410 Z",
       "Wick", fill=lin((0, 392), (0, 412), (0, "#1E1410"), (1, "#4A3220")),
       stroke=INK, strokeWidth=1.2)
# knurled adjuster knob pinned to the collar's right side
d.shape("ellipse", "Knob axle", x=530, y=447, width=16, height=6,
        fill="#4A2A0E", stroke=INK, strokeWidth=1.2)
d.shape("ellipse", "Wick knob", x=540, y=441, width=18, height=18,
        fill=rad((0, BR_HI), (0.6, "#8A5A22"), (1, "#3A2210")),
        stroke=INK, strokeWidth=1.6)
for a in range(6):
    t = math.radians(a * 60)
    x1, y1 = 549 + 6.5 * math.cos(t), 450 + 6.5 * math.sin(t)
    x2, y2 = 549 + 8.6 * math.cos(t), 450 + 8.6 * math.sin(t)
    d.path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", f"Knurl {a+1}",
           fill=NONE, stroke="#2A180A", strokeWidth=1.4, opacity=70)

# --- flame: layered teardrop over the wick ---------------------------------------------
def flame(scale, cx, cy):
    p = [(cx, cy - 56 * scale), (cx + 11 * scale, cy - 30 * scale),
         (cx + 14 * scale, cy - 12 * scale), (cx + 8 * scale, cy),
         (cx, cy + 4 * scale), (cx - 8 * scale, cy),
         (cx - 14 * scale, cy - 12 * scale), (cx - 11 * scale, cy - 30 * scale)]
    for q in p:
        EXTENT.append(q)
    return smooth(p)


d.path(flame(1.0, 500, 390), "Flame outer", fill="#E8862A", opacity=78,
       stroke=NONE)
d.path(flame(0.62, 500, 396), "Flame mid", fill="#F5B84A", opacity=85,
       stroke=NONE)
d.shape("ellipse", "Flame core", x=492, y=378, width=16, height=22,
        fill=rad((0, "#FDF6DC", 95), (1, "#FBD88A", 0)), stroke=NONE)
d.shape("ellipse", "Flame base blue", x=490, y=392, width=20, height=10,
        fill="#5A7AC8", opacity=40, stroke=NONE)

# --- chimney: bulged glass tube over the burner -----------------------------------------
chim_profile = [(542, 448), (546, 436), (553, 418), (557, 398), (556, 380),
                (551, 358), (546, 330), (542, 300), (539, 268), (537, 240)]
d.path(lathe(chim_profile), "Chimney glass",
       fill=lin((0, 240), (0, 448), (0, "#EAF4EE", 16), (0.5, "#C8DCD2", 6),
                (1, "#EAF4EE", 14)),
       stroke=INK, strokeWidth=2.0, opacity=80, join="round")
# mouth: the open rim seen from slightly above
d.shape("ellipse", "Chimney mouth", x=500 - 37, y=231, width=74, height=14,
        fill="#141C18", opacity=60, stroke="#EAF4EE", strokeWidth=1.8)
d.shape("ellipse", "Chimney mouth inner", x=500 - 30, y=234, width=60, height=9,
        fill=NONE, stroke="#8AA898", strokeWidth=1.4, opacity=50)
# seat ring where the glass meets the burner gallery
d.shape("ellipse", "Chimney seat", x=500 - 43, y=443, width=86, height=11,
        fill=NONE, stroke="#EAF4EE", strokeWidth=2, opacity=40)
# vertical glass streaks: bright left, faint right, and one across the bulge
d.path("M457,258 C453,300 451,352 455,410", "Chimney streak L", fill=NONE,
       stroke="#F8FFFB", strokeWidth=7, opacity=30, cap="round")
d.path("M546,262 C550,308 552,356 549,404", "Chimney streak R", fill=NONE,
       stroke="#E8F2EA", strokeWidth=4, opacity=14, cap="round")
d.path("M452,398 C480,410 522,410 550,396", "Bulge reflection", fill=NONE,
       stroke="#F8FFFB", strokeWidth=3, opacity=22, cap="round")

# --- bloom over everything: the flame lights its own glass ------------------------------
d.shape("ellipse", "Flame bloom", x=390, y=300, width=220, height=190,
        fill=rad((0, "#FBD88A", 26), (0.6, "#E89A3C", 8), (1, "#E89A3C", 0)),
        stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("lamp extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


# --- caption ----------------------------------------------------------------------------------
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
               color="#F0E8D2", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#BEAF96", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
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


caption("OIL LAMP", "BRASS · GLASS · COTTON WICK")
d.finish("oil-lamp-V1R00")

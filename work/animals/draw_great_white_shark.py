#!/usr/bin/env python3
"""Great white shark — field plate V1R00. The open-water profile: countershaded
slate over white with the sharp flank demarcation, conical snout and the
slightly open jaw lined with teeth, black eye, five gill slits, sickle pectoral
fin and the tall unequal tail lobes. Above: the bright ruffled sea surface with
a lone swimmer silhouette; below: the cold dark of the thermocline band closing
on the disc's own arc. Small fish scatter ahead of it. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Great White Shark — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#0E1C26"   # deep blue-black, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def linO(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def radO(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

def smooth(pts, closed=True):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#08141E"), (1, "#02060A"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#7AB4D2"), (0.3, "#3E7EA0"),
                 (0.62, "#1E4E6C"), (1, "#0A2436"))
BODY_GRAD  = lin(0, 240, 0, 560, (0, "#465E70"), (0.42, "#6E8A9C"),
                 (0.56, "#A8BECA"), (0.63, "#DDE9EE"), (0.7, "#F0F7F9"), (1, "#E2EDF1"))
FIN_GRAD   = lin(0, 340, 0, 660, (0, "#4A6274"), (1, "#22323E"))
TAIL_GRAD  = lin(720, 300, 800, 560, (0, "#3E5464"), (0.5, "#5E7688"), (1, "#8AA2B2"))

# --- backdrop + open-water plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#3E7EA0", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)

# god rays: pale wedges fanning down out of the surface band
for i, (x0, x1, x2, x3, y2, op) in enumerate([(300, 350, 520, 430, 600, 16),
                                              (440, 520, 640, 520, 640, 20),
                                              (600, 656, 760, 680, 580, 14)]):
    assert all(on_disc(x, y, 10) for x, y in [(x0, 128), (x1, 130), (x2, y2), (x3, y2)])
    d.path(f"M{x0},128 L{x1},130 L{x2},{y2} L{x3},{y2} Z", f"Ray {i+1}",
           fill=linO((x0 + x1) / 2, 130, (x2 + x3) / 2, y2,
           (0, "#DCF0F8", op), (0.7, "#DCF0F8", op * 0.35), (1, "#DCF0F8", 0)), stroke=NONE)

# the sea surface seen from below: a bright ruffled band near the top of the disc
sy_ = 118
ssl, ssr = disc_x(sy_, -1), disc_x(sy_, 1)
d.path(f"M{ssl:.1f},{sy_} C260,{sy_ - 18} 380,{sy_ + 12} 500,{sy_ - 6} "
       f"C620,{sy_ - 22} 700,{sy_ + 8} {ssr:.1f},{sy_} "
       f"L{disc_x(sy_ + 34, 1):.1f},{sy_ + 34} C700,{sy_ + 46} 620,{sy_ + 22} 500,{sy_ + 36} "
       f"C380,{sy_ + 48} 260,{sy_ + 24} {disc_x(sy_ + 34, -1):.1f},{sy_ + 34} Z",
       "Surface", fill=linO(0, sy_ - 20, 0, sy_ + 40, (0, "#E4F4FA", 60), (1, "#E4F4FA", 8)),
       stroke=NONE)
d.path(f"M{ssl + 16:.1f},{sy_} C260,{sy_ - 16} 380,{sy_ + 10} 500,{sy_ - 6} "
       f"C620,{sy_ - 20} 700,{sy_ + 6} {ssr - 16:.1f},{sy_}",
       "Surface line", fill=NONE, stroke="#EAF6FA", strokeWidth=4, opacity=55, cap="round")
# the lone swimmer: small splayed silhouette drifting on the surface skin
d.path("M272,124 C286,118 306,118 318,124 C330,118 344,120 352,128 "
       "C340,132 326,130 318,132 C304,136 284,134 272,124 Z",
       "Swimmer", fill="#12303E", opacity=75, stroke=NONE)
d.path("M352,128 L368,138 M318,132 L330,146", "Swimmer limbs", fill=NONE,
       stroke="#12303E", strokeWidth=4, opacity=70, cap="round")

# marine snow drifting down through the water column
for i, (x, y, w) in enumerate([(300, 220, 3), (560, 200, 4), (700, 280, 3), (200, 380, 3),
                               (820, 420, 3), (420, 180, 4), (640, 360, 3), (280, 560, 3),
                               (760, 580, 3), (480, 640, 3), (180, 640, 3), (840, 300, 3)]):
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8E2EE", opacity=35, stroke=NONE)

# small fish scattering ahead of the shark's approach, lower left
for i, (x, y, a, s_) in enumerate([(208, 470, -30, 1.0), (246, 520, -55, 0.85),
                                    (186, 560, -15, 0.9), (268, 580, -40, 0.75)]):
    r_ = math.radians(a)
    ux, uy = math.cos(r_), math.sin(r_)
    L = 22 * s_
    d.path(f"M{x},{y} L{x + ux * L:.1f},{y + uy * L:.1f} "
           f"Q{x + ux * L * 0.6 - uy * 5:.1f},{y + uy * L * 0.6 + ux * 5:.1f} {x},{y} "
           f"Q{x + ux * L * 0.6 + uy * 5:.1f},{y + uy * L * 0.6 - ux * 5:.1f} {x + ux * L:.1f},{y + uy * L:.1f} Z",
           f"Fish {i+1}", fill="#8AA8B8", opacity=70, stroke=NONE)

# --- the shark: one silhouette, countershaded ---------------------------------------------
BODY = [
    (238, 428),   # snout tip
    (296, 388), (390, 358), (478, 348),      # forehead to back
    (510, 344),                              # dorsal fin base front
    (545, 232), (588, 366),                  # dorsal fin apex + rear base
    (660, 382), (732, 408), (758, 428),      # rear back to tail stalk
    (806, 318),                              # upper tail lobe tip
    (782, 428),                              # tail notch
    (788, 548),                              # lower tail lobe tip
    (730, 470), (700, 462),                  # tail stalk bottom
    (640, 492), (560, 516), (470, 528),      # rear belly
    (390, 522), (330, 500),                  # belly to chest
    (300, 478),                              # lower jaw corner
    (286, 462), (262, 446),                  # the open jaw's underside
]
d.path(smooth(BODY), "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=4)

# the open mouth: dark wedge under the snout
d.path("M240,426 C262,440 288,452 314,460 C300,472 284,478 268,476 "
       "C254,468 244,452 240,426 Z", "Mouth", fill="#5E2430", stroke=INK, strokeWidth=3)
# teeth: small white triangles along the upper jaw edge
for i, (x, y) in enumerate([(252, 434), (264, 441), (276, 447), (288, 452), (300, 456)]):
    d.path(f"M{x},{y} L{x + 9},{y + 4} L{x + 3},{y + 11} Z",
           f"Tooth {i+1}", fill="#F2F6F2", stroke=NONE)
# the mouth line continuing back under the eye
d.path("M314,460 C336,466 356,468 374,466", "Gape line", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=60, cap="round")

# the sharp countershade boundary etched along the flank
d.path("M258,438 C320,452 420,470 520,482 C620,492 700,486 746,452",
       "Flank line", fill=NONE, stroke="#3A5264", strokeWidth=4, opacity=45, cap="round")

# five gill slits
for i, x in enumerate([346, 362, 378, 394, 410]):
    d.path(f"M{x},420 C{x - 5},438 {x - 5},456 {x - 2},472",
           f"Gill slit {i+1}", fill=NONE, stroke="#2E4452", strokeWidth=4, opacity=70, cap="round")

# the black eye above the mouth corner
d.shape("ellipse", "Eye", x=330, y=404, width=16, height=16, fill="#0A1418", stroke=NONE)
d.shape("ellipse", "Eye glint", x=333, y=406, width=4, height=4, fill="#D8EAF2", opacity=70, stroke=NONE)
# nostril at the snout tip
d.shape("ellipse", "Nostril", x=246, y=418, width=8, height=6, fill="#14242E", opacity=80, stroke=NONE)

# pectoral fin: the long sickle sweeping down and back on the near flank
d.path("M436,500 C460,540 500,590 552,630 C560,636 556,646 546,644 "
       "C486,624 440,570 422,512 C422,504 428,498 436,500 Z",
       "Pectoral fin", fill=FIN_GRAD, stroke=INK, strokeWidth=4)
d.path("M440,512 C470,552 508,596 540,626", "Fin edge light", fill=NONE,
       stroke="#8AA2B2", strokeWidth=3, opacity=45, cap="round")
# the far pectoral fin shadow behind the belly
d.path("M500,524 C540,560 580,596 610,624", "Far fin", fill=NONE,
       stroke="#22323E", strokeWidth=10, opacity=55, cap="round")

# dorsal ridge light + flank sheen
d.path("M300,392 C360,364 440,352 508,346", "Back light", fill=NONE,
       stroke="#B8D0DC", strokeWidth=5, opacity=40, cap="round")
d.shape("ellipse", "Flank sheen", x=420, y=392, width=200, height=60,
        fill="#DCEAF0", opacity=15, stroke=NONE)

# --- thermocline: the cold dark band across the disc's floor -------------------------------
ty_ = 700
tl, tr = disc_x(ty_, -1), disc_x(ty_, 1)
d.path(f"M{tl:.1f},{ty_} C300,{ty_ - 12} 420,{ty_ + 8} 520,{ty_} "
       f"C620,{ty_ - 8} 700,{ty_ + 6} {tr:.1f},{ty_} "
       f"A{PR},{PR} 0 0 1 {tl:.1f},{ty_} Z", "Thermocline",
       fill=lin(0, ty_, 0, 880, (0, "#12344A"), (1, "#061824")), opacity=80, stroke=NONE)
# the thin bright interface line where the water turns cold
d.path(f"M{tl + 10:.1f},{ty_} C300,{ty_ - 12} 420,{ty_ + 8} 520,{ty_} "
       f"C620,{ty_ - 8} 700,{ty_ + 6} {tr - 10:.1f},{ty_}",
       "Interface line", fill=NONE, stroke="#6E9EB8", strokeWidth=3, opacity=40, cap="round")
# particles hanging at the boundary
for i, (x, y) in enumerate([(320, 690), (420, 706), (560, 694), (680, 700), (500, 716), (380, 712)]):
    d.shape("ellipse", f"Boundary fleck {i+1}", x=x, y=y, width=4, height=3,
            fill="#8AB4C8", opacity=40, stroke=NONE)

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#06141E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8D2E4", strokeWidth=3, opacity=28)

# --- name + second line ----------------------------------------------------------------------
r1 = d.text("GREAT WHITE SHARK", "Name", x=500, y=940, size=56, font="Virelai Sans",
            color="#DCF0F8", justify="center")
LINE2, SZ2, TRK = "CARCHARODON CARCHARIAS", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#9EC4D4", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for rr, lim in ((r1, 800), (r, 760)):
    b = find(layers, rr["id"])["bounds"]
    print("caption bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= lim and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("great-white-shark-V1R00")

#!/usr/bin/env python3
"""Harpy eagle — field plate V1R00. Bust, face-on: the split double crest
fanned like a crown, a flat pale-grey face with a heavy brow washed in warm
ochre, the black hooked beak, the slate breast band and white chest feathers
layered in gradient rows, all on a cool grey plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Harpy Eagle — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#24262C"   # cold slate, not black
rng = random.Random(54)

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR**2 - (y - PCY)**2)

def disc_y(x):
    return PCY + math.sqrt(PR**2 - (x - PCX)**2)

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}

def smooth(pts, closed=True, k=1.0, move=True):
    n = len(pts)
    s = ("M%.1f,%.1f" % pts[0]) if move else ""
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

def mirror(right):
    left = [(2 * PCX - x, y) for x, y in reversed(right[1:-1])]
    return right + left

def arc_closed(contour):
    """contour runs left disc point -> right disc point over the top; close it
    clockwise along the disc's own arc through the bottom."""
    (lx, ly), (rx, ry) = contour[0], contour[-1]
    for x, y in (contour[0], contour[-1]):
        assert abs(math.hypot(x - PCX, y - PCY) - PR) < 1.5, (x, y)
    return smooth(contour, closed=False) + f" A420,420 0 0 1 {lx:.1f},{ly:.1f} Z"

BG_GRAD = lin("#1A1F26", "#07090C", [0, 0], [0, 1000])
PLATE_GRAD = rad("#66727C", "#46525C", "#262E36")
FACE_GRAD = rad("#F2F3F4", "#D2D6DA", "#9AA0A6")
SLATE_GRAD = lin("#5A6068", "#2A2E34", [500, 440], [500, 880])
BAND_GRAD = lin("#3A3E44", "#1E2126", [500, 500], [500, 620])
CHEST_GRAD = lin("#FFFFFF", "#D4D8DC", [500, 600], [500, 880])
BEAK_GRAD = lin("#5A5658", "#141214", [470, 410], [530, 492])
OCHRE = "#D89A48"

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#8A98A4", opacity=7, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)
d.shape("ellipse", "Canopy light", x=230, y=60, width=540, height=380,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#DCE6EE", "opacity": 0.22},
            {"offset": 1, "color": "#DCE6EE", "opacity": 0}]}}, stroke=NONE)
# faint canopy leaves in the plate's upper corners
for i, (cx, cy, a, L) in enumerate([(196, 300, -40, 120), (256, 230, -60, 90), (170, 410, -10, 110),
                                    (804, 300, 220, 120), (744, 230, 240, 90), (830, 410, 190, 110)]):
    r = math.radians(a)
    ux, uy = math.cos(r), math.sin(r)
    nx, ny = -uy, ux
    tip = (cx + ux * L, cy + uy * L)
    m = (cx + ux * L / 2, cy + uy * L / 2)
    assert on_disc(*tip, 12) and on_disc(cx, cy, 12), i
    d.path(f"M{cx},{cy} Q{m[0] + nx * 30:.1f},{m[1] + ny * 30:.1f} {tip[0]:.1f},{tip[1]:.1f} "
           f"Q{m[0] - nx * 30:.1f},{m[1] - ny * 30:.1f} {cx},{cy} Z", f"Canopy leaf {i+1}",
           fill=lin("#8AA49A", "#4E6A62", (cx, cy), tip), opacity=22, stroke=NONE)
    d.path(f"M{cx},{cy} L{tip[0]:.1f},{tip[1]:.1f}", f"Canopy leaf {i+1} rib", fill=NONE,
           stroke="#B8CCC4", strokeWidth=3, opacity=18, cap="round")

# --- crest: two fanned lobes of long pointed feathers, behind the head -----------------
CX, CY = 500, 318
def plume(name, ang, L, w, c_tip, c_base, op=100):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    b = (CX + ux * 40, CY + uy * 40)
    tip = (CX + ux * L, CY + uy * L)
    assert on_disc(*tip, 16), (name, tip)
    m1 = (b[0] + ux * (L - 40) * 0.55 + nx * w, b[1] + uy * (L - 40) * 0.55 + ny * w)
    m2 = (b[0] + ux * (L - 40) * 0.55 - nx * w, b[1] + uy * (L - 40) * 0.55 - ny * w)
    s = (f"M{b[0] + nx * w * 0.4:.1f},{b[1] + ny * w * 0.4:.1f} "
         f"Q{m1[0]:.1f},{m1[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} "
         f"Q{m2[0]:.1f},{m2[1]:.1f} {b[0] - nx * w * 0.4:.1f},{b[1] - ny * w * 0.4:.1f} Z")
    d.path(s, name, fill=lin(c_base, c_tip, b, tip), stroke=INK, strokeWidth=3, opacity=op)
    d.path(f"M{b[0]:.1f},{b[1]:.1f} L{b[0] + ux * (L - 40) * 0.9:.1f},{b[1] + uy * (L - 40) * 0.9:.1f}",
           f"{name} shaft", fill=NONE, stroke="#B4BAC2", strokeWidth=3, opacity=45, cap="round")

# back row: long and dark, the two lobes split around the crown's centre
for side in (-1, 1):
    for j in range(7):
        f = j / 6
        ang = -90 + side * (16 + 64 * f)
        L = 250 - 28 * f + 30 * math.sin(math.pi * f) + rng.uniform(-8, 8)
        plume(f"Crest back {'L' if side < 0 else 'R'}{j+1}", ang, L, 22, "#2C3036", "#6E747C")
# front row: shorter, paler, offset between the back plumes
for side in (-1, 1):
    for j in range(6):
        f = (j + 0.5) / 6
        ang = -90 + side * (12 + 66 * f)
        L = 196 - 30 * f + 22 * math.sin(math.pi * f) + rng.uniform(-6, 6)
        plume(f"Crest front {'L' if side < 0 else 'R'}{j+1}", ang, L, 18, "#3E434A", "#9AA0A8")

# --- body: slate shoulders closing on the disc arc ------------------------------------------
y0 = 600
SH = [(disc_x(y0, -1), y0), (150, 540), (210, 492), (300, 462), (400, 452), (500, 458)]
SH = SH + [(2 * PCX - x, y) for x, y in reversed(SH[:-1])]
d.path(arc_closed(SH), "Shoulders", fill=lin("#4E545C", "#20242A", (500, 450), (500, 880)),
       stroke=INK, strokeWidth=4)

def interp(pts, v):
    for (a1, b1), (a2, b2) in zip(pts, pts[1:]):
        if a1 <= v <= a2: return b1 + (b2 - b1) * (v - a1) / (a2 - a1)
    return pts[-1][1] if v > pts[-1][0] else pts[0][1]

def sh_y(x):
    ax = abs(x - PCX)
    return interp(sorted((abs(px - PCX), py) for px, py in SH[:6]), ax)

def feather(name, x, y, w, h, c0, c1, edge, edge_op):
    """an elliptical contour feather; the next row up covers its top."""
    d.shape("ellipse", name, x=x - w / 2, y=y, width=w, height=h,
            fill=lin(c0, c1, (x, y), (x, y + h)), stroke=NONE)
    d.path(f"M{x - w * 0.44:.1f},{y + h * 0.62:.1f} Q{x:.1f},{y + h * 1.12:.1f} {x + w * 0.44:.1f},{y + h * 0.62:.1f}",
           f"{name} edge", fill=NONE, stroke=edge, strokeWidth=3, opacity=edge_op, cap="round")

def fits_disc(x, y, w, h, pad=8):
    return all(on_disc(px, py, pad) for px, py in
               [(x - w / 2, y + h / 2), (x + w / 2, y + h / 2), (x, y + h), (x - w * 0.35, y + h * 0.9),
                (x + w * 0.35, y + h * 0.9)])

# wing coverts on the shoulders, painted bottom row first so upper rows overlap
for row in range(12, -1, -1):
    yy = 470 + row * 30
    for side in (-1, 1):
        for j in range(8):
            x = PCX + side * (140 + j * 44 + (row % 2) * 22)
            w, h = 54, 50
            if yy < sh_y(x) - 6 or not fits_disc(x, yy, w, h): continue
            g = 0.5 + 0.5 * min(1, row / 10)
            feather(f"Covert r{row} {'L' if side < 0 else 'R'}{j+1}", x, yy, w, h,
                    "#727880", "#2C3036", "#A8B0B8", round(22 + 14 * (1 - g)))

# --- chest: white feathers in gradient rows, closing on the arc ------------------------------
HW = [(480, 116), (600, 162), (700, 186), (780, 180), (880, 150)]
hw = lambda y: interp(HW, y)
CL = [(PCX - hw(y), y) for y in (844, 780, 700, 620, 540)]
CL = [(PCX - 164, disc_y(PCX - 164))] + CL[1:] + [(PCX, 500)]
CL = CL + [(2 * PCX - x, y) for x, y in reversed(CL[:-1])]
d.path(arc_closed(CL), "Chest", fill=CHEST_GRAD, stroke=NONE)
for row in range(11, -1, -1):
    yy = 598 + row * 24
    for j in range(-5, 6):
        x = PCX + j * 40 + (row % 2) * 20
        w, h = 48, 44
        if abs(x - PCX) + w * 0.42 > hw(yy + h / 2) or not fits_disc(x, yy, w, h, 10): continue
        t = row / 11
        feather(f"Chest feather r{row} {j+6}", x, yy, w, h, "#FFFFFF",
                "#C6CCD2" if t < 0.5 else "#B4BAC2", "#8A929A", round(26 + 14 * t))
# chest volume: grey falls off toward both flanks
d.path(arc_closed(CL), "Chest volume", stroke=NONE, fill={"gradient": {
    "kind": "linear", "start": [PCX - 180, 700], "end": [PCX + 180, 700], "stops": [
        {"offset": 0, "color": "#3E464E", "opacity": 0.45}, {"offset": 0.28, "color": "#3E464E", "opacity": 0},
        {"offset": 0.72, "color": "#3E464E", "opacity": 0}, {"offset": 1, "color": "#3E464E", "opacity": 0.45}]}})

# breast band: slate, reaching into the shoulders, scalloped lower edge
d.path(smooth([(356, 500), (430, 486), (500, 484), (570, 486), (644, 500), (664, 556), (634, 600),
               (500, 618), (366, 600), (336, 556)]), "Breast band", fill=BAND_GRAD, stroke=NONE)
for j in range(-4, 5):
    x = PCX + j * 30
    y = 590 - abs(j) * 3
    feather(f"Band tip {j+5}", x, y, 36, 32, "#3A3E44", "#1A1D22", "#7A8088", 40)
for j, x in enumerate([420, 465, 510, 555, 600]):
    yb = 534 + abs(x - 510) * 0.12
    d.path(f"M{x - 18},{yb} Q{x},{yb + 16} {x + 18},{yb}", f"Band texture {j+1}", fill=NONE,
           stroke="#70767E", strokeWidth=3, opacity=30, cap="round")

# --- head ----------------------------------------------------------------------------------
HEAD_R = [(500, 272), (572, 276), (630, 306), (660, 362), (658, 426), (634, 482), (590, 522), (532, 542), (500, 546)]
HEAD = smooth(mirror(HEAD_R))
d.path(HEAD, "Head", fill=FACE_GRAD, stroke=INK, strokeWidth=4)
# facial disc: concentric feather arcs around each eye
for side in (-1, 1):
    ex = PCX + side * 56
    for k, rr in enumerate([60, 82, 104]):
        a0, a1 = (math.radians(100), math.radians(250)) if side < 0 else (math.radians(-70), math.radians(80))
        pts = [(ex + rr * math.cos(a0 + (a1 - a0) * t / 8), 400 + rr * 0.92 * math.sin(a0 + (a1 - a0) * t / 8))
               for t in range(9)]
        d.path(smooth(pts, closed=False), f"Facial disc {'L' if side < 0 else 'R'}{k+1}", fill=NONE,
               stroke="#8C949C", strokeWidth=3, opacity=34 - k * 6, cap="round")
# soft grey ruff feathers fringing the lower face
for side in (-1, 1):
    for j in range(6):
        a = math.radians(30 + j * 14)
        x0, y0_ = PCX + side * 128 * math.cos(a), 430 + 104 * math.sin(a)
        x1, y1 = PCX + side * 150 * math.cos(a), 438 + 124 * math.sin(a)
        d.path(f"M{x0:.1f},{y0_:.1f} L{x1:.1f},{y1:.1f}", f"Ruff {'L' if side < 0 else 'R'}{j+1}",
               fill=NONE, stroke="#7E868E", strokeWidth=3, opacity=30, cap="round")
d.path(smooth([(364, 344), (396, 302), (446, 280), (500, 274), (554, 280), (604, 302), (636, 344),
               (590, 330), (540, 322), (500, 320), (460, 322), (410, 330)]), "Crown cap",
       fill=lin("#6E747C", "#B8BEC4", (500, 276), (500, 336)), opacity=70, stroke=NONE)
# short crest feathers springing from the crown, tying the fan into the head
for j in range(13):
    f = j / 12
    ang = math.radians(-160 + 140 * f)
    bx, by = PCX + 128 * math.cos(ang), 352 + 74 * math.sin(ang)
    L = 46 + 14 * math.sin(math.pi * f)
    a2 = math.radians(-90 + (f - 0.5) * 150)
    ux, uy = math.cos(a2), math.sin(a2)
    nx, ny = -uy, ux
    tip = (bx + ux * L, by + uy * L)
    m = (bx + ux * L * 0.45, by + uy * L * 0.45)
    d.path(f"M{bx + nx * 9:.1f},{by + ny * 9:.1f} Q{m[0] + nx * 9:.1f},{m[1] + ny * 9:.1f} {tip[0]:.1f},{tip[1]:.1f} "
           f"Q{m[0] - nx * 9:.1f},{m[1] - ny * 9:.1f} {bx - nx * 9:.1f},{by - ny * 9:.1f} Z", f"Crown plume {j+1}",
           fill=lin("#9AA0A8", "#3E434A", (bx, by), tip), stroke=INK, strokeWidth=3, opacity=95)
d.path(smooth([(430, 300), (500, 290), (570, 300)], closed=False), "Crown sheen", fill=NONE,
       stroke="#FFFFFF", strokeWidth=8, opacity=26, cap="round")
d.path(smooth([(392, 500), (440, 534), (500, 544), (560, 534), (608, 500)], closed=False), "Throat shade",
       fill=NONE, stroke="#6E767E", strokeWidth=14, opacity=25, cap="round")

# warm ochre brow: a heavy ridge, low at the inner corner, that hoods the eyes
for side in (-1, 1):
    S = lambda x: PCX + side * (x - PCX)
    nm = "L" if side < 0 else "R"
    brow = [(S(504), 386), (S(530), 370), (S(572), 354), (S(618), 348), (S(628), 362), (S(588), 374),
            (S(546), 388), (S(510), 398)]
    d.path(smooth(brow), f"Brow {nm}", fill=lin(OCHRE, "#5E5A56", (S(510), 380), (S(626), 352)),
           stroke=INK, strokeWidth=3)
    d.path(smooth([(S(516), 382), (S(556), 364), (S(604), 354)], closed=False), f"Brow {nm} light",
           fill=NONE, stroke="#FFD8A0", strokeWidth=4, opacity=55, cap="round")
d.shape("ellipse", "Brow ochre wash", x=390, y=320, width=220, height=90,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": OCHRE, "opacity": 0.30},
            {"offset": 1, "color": OCHRE, "opacity": 0}]}}, stroke=NONE)

# eyes: deep umber irises under the brow
for side in (-1, 1):
    ex, ey = PCX + side * 58, 404
    nm = "L" if side < 0 else "R"
    d.shape("ellipse", f"Eye ring {nm}", x=ex - 27, y=ey - 25, width=54, height=50,
            fill=rad("#5A5E64", "#2E3238"), stroke=NONE)
    d.shape("ellipse", f"Eye {nm}", x=ex - 21, y=ey - 20, width=42, height=40,
            fill=rad("#B07A48", "#6A4426", "#2A1A10"), stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Pupil {nm}", x=ex - 11, y=ey - 10, width=22, height=21,
            fill=rad("#1A1214", "#060404"), stroke=NONE)
    d.shape("ellipse", f"Eye glint {nm}", x=ex - 10 - side * 2, y=ey - 8, width=9, height=7,
            fill="#FFFFFF", opacity=88, stroke=NONE)
    # the brow's shadow across the top of the iris makes the stare
    d.path(f"M{ex - 24},{ey - 6 + side * 4} Q{ex},{ey - 22} {ex + 24},{ey - 6 - side * 4} "
           f"Q{ex},{ey - 12} {ex - 24},{ey - 6 + side * 4} Z", f"Lid shadow {nm}", fill="#2A2420", opacity=60, stroke=NONE)

# beak: grey cere, big black hook
d.path(smooth([(460, 410), (500, 400), (540, 410), (546, 434), (500, 442), (454, 434)]), "Cere",
       fill=lin("#7A7E84", "#3E4248", (500, 400), (500, 442)), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nostril L", x=474, y=420, width=12, height=7, fill=INK, opacity=80, stroke=NONE)
d.shape("ellipse", "Nostril R", x=514, y=420, width=12, height=7, fill=INK, opacity=80, stroke=NONE)
for side in (-1, 1):
    d.path(f"M{PCX + side * 40},{444} Q{PCX + side * 60},{462} {PCX + side * 80},{462}",
           f"Gape {'L' if side < 0 else 'R'}", fill=NONE, stroke=INK, strokeWidth=4, opacity=60, cap="round")
d.path("M472,470 C478,484 488,494 500,500 C512,494 522,484 528,470", "Lower mandible",
       fill=NONE, stroke="#4A4C52", strokeWidth=4, opacity=70, cap="round")
d.path("M456,432 C448,468 466,508 500,536 C534,508 552,468 544,432 C528,444 472,444 456,432 Z",
       "Beak", fill=BEAK_GRAD, stroke=INK, strokeWidth=3)
d.path("M500,444 C500,470 500,500 500,530", "Culmen light", fill=NONE, stroke="#8A8C92",
       strokeWidth=4, opacity=55, cap="round")
d.path("M476,448 C472,468 480,490 492,508", "Beak sheen", fill=NONE, stroke="#B8BCC2",
       strokeWidth=4, opacity=35, cap="round")
# plate rim on top
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#14181C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2EA", strokeWidth=3, opacity=26)

# --- name + second line ------------------------------------------------------------------------
d.text("HARPY EAGLE", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#E4EAF0", justify="center")
LINE2, SZ2, TRK = "HARPIA HARPYJA", 22, 260
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#A4B0BA", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
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

d.finish("harpy-eagle-V1R00")

#!/usr/bin/env python3
"""Lion — field-guide plate V1R00. Face-forward portrait: the mane drawn as a
layered corona of russet rays around a tawny face, the stare level and
measuring. Savanna-gold plate under a dark umber backdrop, heat-shimmer lines
across the sky, dry-grass floor closing on the disc's own arc, one flat-top
acacia on the horizon. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Lion — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#2E1508"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def mirror(dd):
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{1000 - float(t):g},"); ex = False
        else:
            out[-1] += f"{float(t):g}"; ex = True
    return " ".join(out)

def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)

def sunburst(cx, cy, r_in, r_out, n_rays, phase=0.0, wobble=0.0):
    pts = []
    for i in range(n_rays * 2):
        a = math.radians(i * 180.0 / n_rays + phase)
        r = r_out if i % 2 == 0 else r_in
        r += wobble * math.sin(i * 2.7 + n_rays)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"

BG_GRAD = lin(0, 0, 0, 1000, (0, "#2A1608"), (1, "#0C0602"))
PLATE_GRAD = rad((0, "#F2D58F"), (0.55, "#E0B060"), (1, "#B07C30"))
GRASS_GRAD = lin(0, 720, 0, 880, (0, "#B89048"), (1, "#6E4C1C"))

# --- backdrop + savanna plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#E0B060", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A4E18", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF0C8", strokeWidth=3, opacity=45)
# sun-bleached zenith glow behind the mane
d.shape("ellipse", "Sky glow", x=260, y=120, width=480, height=300,
        fill=rad((0, "#FFEDC0"), (1, "#FFEDC0")), opacity=20, stroke=NONE)
# heat shimmer: faint wavy lines across the upper sky
for i, (y, amp, op) in enumerate([(178, 7, 16), (216, 9, 13), (258, 8, 11), (304, 10, 9)]):
    pts = "M180,%.0f" % y + "".join(
        " Q%.0f,%.0f %.0f,%.0f" % (x + 42.5, y + (amp if k % 2 == 0 else -amp), x + 85, y)
        for k, x in enumerate(range(180, 775, 85)))
    d.path(pts, f"Shimmer {i+1}", fill=NONE, stroke="#FFF6DC", strokeWidth=4, opacity=op, cap="round")

# dry-grass floor: top edge sways, bottom closes on the disc arc
ly = 738
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path(f"M{CX-ldx:.1f},{ly} C320,722 430,730 520,726 C620,722 700,730 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Grass floor", fill=GRASS_GRAD, stroke=NONE)
# parched highlight along the horizon line
d.path(f"M{CX-ldx+8:.1f},{ly-2} C320,720 430,728 520,724 C620,720 700,728 {CX+ldx-8:.1f},{ly-2}",
       "Horizon light", fill=NONE, stroke="#F0D28A", strokeWidth=5, opacity=40, cap="round")
# grass tufts along the horizon
for i, (x, h) in enumerate([(250,26),(296,20),(356,30),(414,22),(470,28),(540,24),(600,30),
                            (656,20),(712,26),(752,18),(206,18),(792,16)]):
    for j, dx in enumerate([-6, 0, 6]):
        bend = dx * 1.6
        d.path(f"M{x+dx},{ly+6} Q{x+dx+bend},{ly+6-h*0.6} {x+dx+bend*1.4},{ly+6-h}",
               f"Tuft {i+1}.{j+1}", fill=NONE, stroke="#5E3E14", strokeWidth=3, opacity=55, cap="round")
# lone flat-top acacia, right of centre on the horizon
ax, ay = 700, 662
d.path(f"M{ax},{ly+4} C{ax-4},{ly-30} {ax-8},{ly-52} {ax-14},{ay+16} "
       f"M{ax},{ly+4} C{ax+6},{ly-34} {ax+12},{ly-56} {ax+18},{ay+18}",
       "Acacia trunk", fill=NONE, stroke="#3E2808", strokeWidth=6, opacity=70, cap="round")
d.path(f"M{ax-72},{ay+14} C{ax-58},{ay-8} {ax-20},{ay-16} {ax+2},{ay-14} "
       f"C{ax+30},{ay-16} {ax+62},{ay-6} {ax+76},{ay+12} "
       f"C{ax+50},{ay+20} {ax-40},{ay+22} {ax-72},{ay+14} Z",
       "Acacia canopy", fill="#4A300C", opacity=65, stroke=NONE)
for px, py in [(ax-72, ay+14), (ax+76, ay+12), (ax-14, ay+16), (ax+18, ay+18)]:
    assert on_disc(px, py, 30), (px, py)
# dust flecks inside the disc
for i, (x, y, w) in enumerate([(180,330,5),(830,320,5),(160,520,6),(852,500,5),(230,660,4),
                               (770,690,5),(140,430,4),(870,410,5),(400,120,5),(610,110,4),
                               (330,140,4),(690,150,5),(300,790,4),(660,800,5),(500,840,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w, fill="#8A6224", opacity=35, stroke=NONE)

# --- the mane: a layered corona -------------------------------------------------
# outer dark sunburst
d.path(sunburst(500, 450, 214, 272, 24, wobble=6), "Mane outer",
       fill=rad((0, "#8A4A1E"), (0.6, "#6A3412"), (1, "#48200A")),
       stroke=INK, strokeWidth=5, join="round")
# mid sunburst, offset phase, warmer
d.path(sunburst(500, 450, 182, 234, 18, phase=10, wobble=5), "Mane mid",
       fill=rad((0, "#D8963C"), (0.65, "#B06A22"), (1, "#7E4210")),
       stroke=INK, strokeWidth=4, join="round")
# ears peeking out of the mane at 10 and 2 o'clock; the inner disc buries their base
EAR = "M398,328 C370,316 358,288 372,268 C388,248 418,248 434,268 C446,284 444,308 428,326 Z"
pair(EAR, "Ear", fill=rad((0, "#B8802E"), (1, "#6E3A0E")), stroke=INK, strokeWidth=4)
pair("M402,312 C386,304 380,286 390,274 C400,264 418,266 426,278 C432,288 428,304 416,312 Z",
     "Inner ear", fill="#F0C884", opacity=55, stroke=NONE)
# inner mane disc
d.shape("ellipse", "Mane inner", x=318, y=268, width=364, height=364,
        fill=rad((0, "#EEB45A"), (0.7, "#C07E2E"), (1, "#925417")),
        stroke=INK, strokeWidth=5)
# stray corona rays escaping the inner disc
for i, (a0, l) in enumerate([(206,40),(232,34),(258,42),(284,36),(312,40),
                             (340,34),(8,38),(34,34),(62,40),(88,34),(116,38),(150,32)]):
    a = math.radians(a0)
    x0, y0 = 500 + 172*math.cos(a), 450 + 172*math.sin(a)
    x1, y1 = 500 + (172+l)*math.cos(a), 450 + (172+l)*math.sin(a)
    xm, ym = 500 + (172+l*0.55)*math.cos(a+0.06), 450 + (172+l*0.55)*math.sin(a+0.06)
    d.path(f"M{x0:.0f},{y0:.0f} Q{xm:.0f},{ym:.0f} {x1:.0f},{y1:.0f}",
           f"Mane wisp {i+1}", fill=NONE, stroke="#5E2C0C", strokeWidth=7, opacity=70, cap="round")
# inner locks: curved strokes falling from the crown around the face
for i, (a0, sweep, ln_) in enumerate([(150,-14,58),(178,-10,66),(208,-16,60),(238,-8,64),
                                      (268,-14,56),(300,-10,58),(332,-14,52),(30,-12,56)]):
    a = math.radians(a0)
    x0, y0 = 500 + 150*math.cos(a), 450 + 150*math.sin(a)
    x1, y1 = 500 + (150+ln_)*math.cos(a + math.radians(sweep)), 450 + (150+ln_)*math.sin(a + math.radians(sweep))
    xm, ym = 500 + (150+ln_*0.5)*math.cos(a + math.radians(sweep*0.8)), \
             450 + (150+ln_*0.5)*math.sin(a + math.radians(sweep*0.8))
    d.path(f"M{x0:.0f},{y0:.0f} Q{xm:.0f},{ym:.0f} {x1:.0f},{y1:.0f}",
           f"Mane lock {i+1}", fill=NONE, stroke="#7A3E10", strokeWidth=9, opacity=60, cap="round")

# --- face ------------------------------------------------------------------------
HEAD = ("M500,326 C566,326 620,368 632,438 C640,494 622,552 580,590 "
        "C556,612 528,622 500,622 C472,622 444,612 420,590 "
        "C378,552 360,494 368,438 C380,368 434,326 500,326 Z")
d.path(HEAD, "Face", fill=rad((0, "#F0C076"), (0.62, "#D69C4C"), (1, "#A86A24")),
       stroke=INK, strokeWidth=6)
# crown shadow where the mane overhangs
d.path("M392,352 C440,330 560,330 608,352 C560,344 440,344 392,352 Z",
       "Crown shadow", fill="#8A4E16", opacity=40, stroke=NONE)
d.shape("ellipse", "Brow light", x=430, y=352, width=140, height=44, fill="#FFE8B8", opacity=22, stroke=NONE)
# pale muzzle field: cheeks + chin blended into the tawny face
d.path("M500,442 C528,442 546,462 556,486 C588,494 606,520 602,552 "
       "C598,590 556,612 500,612 C444,612 402,590 398,552 "
       "C394,520 412,494 444,486 C454,462 472,442 500,442 Z",
       "Muzzle pale", fill=rad((0, "#F8E4BC"), (1, "#E4BE80")), opacity=92, stroke=NONE)
# faint cheekbone shade lines
pair("M388,470 C382,500 386,530 400,552", "Cheek shade",
     fill=NONE, stroke="#A86A24", strokeWidth=7, opacity=35, cap="round")

# --- the level stare --------------------------------------------------------------
EYE = "M414,432 C432,414 466,412 486,430 C470,448 434,450 414,432 Z"
pair(EYE, "Eye", fill=rad((0, "#F0B446"), (0.65, "#C07E20"), (1, "#7A4A10")),
     stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pupil L", x=448, y=424, width=12, height=14, fill="#160C04", stroke=NONE)
d.shape("ellipse", "Pupil R", x=540, y=424, width=12, height=14, fill="#160C04", stroke=NONE)
d.shape("ellipse", "Glint L", x=451, y=427, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=543, y=427, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
# level, measured lids — the stare that measures distance
pair("M410,430 C430,410 468,408 490,428", "Upper lid",
     fill=NONE, stroke=INK, strokeWidth=7, cap="round")
pair("M408,414 C428,400 462,398 486,408", "Brow",
     fill=NONE, stroke="#6E3C10", strokeWidth=8, opacity=45, cap="round")
pair("M420,446 C438,452 462,450 478,440", "Lower lid light",
     fill=NONE, stroke="#FFE8B8", strokeWidth=4, opacity=55, cap="round")

# --- nose + mouth -------------------------------------------------------------------
d.path("M470,486 C482,478 518,478 530,486 C534,502 522,518 500,522 C478,518 466,502 470,486 Z",
       "Nose", fill=lin(0, 478, 0, 522, (0, "#8A4638"), (1, "#4A2018")), stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nose glint", x=482, y=485, width=12, height=5, fill="#FFD8C0", opacity=45, stroke=NONE)
d.path("M500,522 L500,540", "Philtrum", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
pair("M500,540 C488,550 470,554 454,550", "Mouth",
     fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# chin tuft + lower-lip shade
d.path("M470,566 C484,578 516,578 530,566 C524,590 476,590 470,566 Z",
       "Chin tuft", fill="#F8E4BC", opacity=80, stroke=NONE)
d.path("M472,592 C488,600 512,600 528,592", "Chin shade",
     fill=NONE, stroke="#A86A24", strokeWidth=7, opacity=30, cap="round")
# whisker dots + faint whiskers
for j, (x, y) in enumerate([(438,510),(452,516),(434,524),(450,530),(466,512),(460,524)]):
    d.shape("ellipse", f"Whisker dot L{j+1}", x=x-3, y=y-3, width=6, height=6,
            fill="#7A4A1A", opacity=55, stroke=NONE)
    d.shape("ellipse", f"Whisker dot R{j+1}", x=1000-x-3, y=y-3, width=6, height=6,
            fill="#7A4A1A", opacity=55, stroke=NONE)
for j, (x1, y1, x2, y2) in enumerate([(446,514,344,490),(448,524,338,520),(452,534,350,550)]):
    pair(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-8} {x2},{y2}", f"Whisker {j+1}",
         fill=NONE, stroke="#FFF0D0", strokeWidth=2, opacity=55, cap="round")

# --- caption ---------------------------------------------------------------------------
d.text("LION", "Name", x=500, y=942, size=60, font="Virelai Sans",
       color="#F6E4B8", justify="center")
o = d.text("PANTHERA LEO", "Binomial", x=500, y=976, size=22, font="Virelai Sans",
           color="#C9A468", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Binomial tracking", ids=[o["id"]], tracking=400)

d.finish("lion-V1R00")

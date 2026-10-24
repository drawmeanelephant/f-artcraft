#!/usr/bin/env python3
"""Eurasian lynx — field-guide plate V1R00. Ear tufts like antennae tuned to
the forest floor: stern front portrait, the long inky tufts, the pale cheek
ruff flaring below each jaw, faint spots in the gray-tawny coat. Birch plate,
hare-tracks mood: cold dawn through white trunks, a hare's dotted trail
crossing snow that closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Eurasian Lynx — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#241A12"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

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

def trunk(p_top, p_bot, w_top, w_bot, label, fill):
    """A birch trunk as a tapered chord: both ends land on the disc arc."""
    dx, dy = p_bot[0]-p_top[0], p_bot[1]-p_top[1]
    ln = math.hypot(dx, dy)
    nx, ny = -dy/ln, dx/ln
    pts = [(p_top[0]+nx*w_top/2, p_top[1]+ny*w_top/2),
           (p_bot[0]+nx*w_bot/2, p_bot[1]+ny*w_bot/2),
           (p_bot[0]-nx*w_bot/2, p_bot[1]-ny*w_bot/2),
           (p_top[0]-nx*w_top/2, p_top[1]-ny*w_top/2)]
    dd = "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"
    d.path(dd, label, fill=fill, stroke=NONE)
    return nx, ny

BG_GRAD = lin(0, 0, 0, 1000, (0, "#101A26"), (1, "#060A10"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#5E788E"), (0.35, "#9CB2C2"),
                 (0.62, "#D0D6CC"), (1, "#EAE0C8"))
COAT_GRAD = rad((0, "#CDB69A"), (0.6, "#A08668"), (1, "#5E4A34"))
BUST_GRAD = lin(0, 620, 0, 880, (0, "#967E62"), (1, "#584631"))
TUFT_GRAD = lin(0, 96, 0, 240, (0, "#080606"), (1, "#2C201A"))
PALE_GRAD = rad((0, "#F4EEE0"), (1, "#D4C6AE"))
IRIS_GRAD = rad((0, "#E8C268"), (0.7, "#B48A30"), (1, "#7A5A1C"))
BIRCH_GRAD = lin(0, 60, 0, 880, (0, "#E6E2D6"), (0.6, "#D2CCC0"), (1, "#B8B0A0"))

# --- backdrop + dawn plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#26364A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2EEDF", strokeWidth=3, opacity=45)

# dawn glow low behind the shoulders
d.shape("ellipse", "Dawn glow", x=230, y=560, width=540, height=240,
        fill="#F4E4BE", opacity=24, stroke=NONE)

# --- birch trunks: tapered chords, all four corners inside the disc ------------------
L_TOP = (172, 252); L_BOT = (232, 758)
nx, ny = trunk(L_TOP, L_BOT, 42, 46, "Birch L", BIRCH_GRAD)
R_TOP = (828, 252); R_BOT = (768, 758)
trunk(R_TOP, R_BOT, 42, 46, "Birch R", BIRCH_GRAD)
# lenticel dashes across the trunks
for i, (x, y, w) in enumerate([(162,300,26),(176,370,22),(168,450,30),(182,540,24),
                               (196,630,28),(212,700,20)]):
    d.path(f"M{x},{y} q{w/2},-{3+i%3} {w},0", f"Lenticel L{i+1}", fill=NONE,
           stroke="#3A3028", strokeWidth=7, opacity=75, cap="round")
for i, (x, y, w) in enumerate([(816,300,26),(804,380,22),(812,470,30),(800,560,24),
                               (786,650,26)]):
    d.path(f"M{x},{y} q{w/2},-{3+i%2} {w},0", f"Lenticel R{i+1}", fill=NONE,
           stroke="#3A3028", strokeWidth=6, opacity=70, cap="round")
# birch branch stubs
d.path("M205,320 q-32,-40 -62,-52", "Branch L", fill=NONE,
       stroke="#3A3028", strokeWidth=6, opacity=60, cap="round")
d.path("M795,320 q32,-40 62,-52", "Branch R", fill=NONE,
       stroke="#3A3028", strokeWidth=6, opacity=60, cap="round")

# --- snow floor closing on the disc arc + a hare's trail ----------------------------
sy = 748
sl, sr = rim_x(sy, side=-1), rim_x(sy, side=1)
d.path(f"M{sl:.1f},{sy} C330,738 410,756 500,750 C590,744 680,742 {sr:.1f},{sy} "
       f"A{R},{R} 0 0 1 {sl:.1f},{sy} Z", "Snow field",
       fill=lin(0, 740, 0, 880, (0, "#E2E6DC"), (0.5, "#C4CCC4"), (1, "#96A4A0")),
       stroke=NONE)
d.path(f"M{sl+10:.0f},{sy} C330,738 410,756 500,750 C590,744 680,742 {sr-10:.0f},{sy}",
       "Snow line", fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=50, cap="round")
# hare tracks: paired prints hopping in from the rim, fading behind the bust
for i, (x, y, s, sgn) in enumerate([(222,762,1.05,1),(262,782,1.0,1),(302,800,0.95,1),
                               (778,762,1.05,-1),(738,782,1.0,-1),(698,800,0.95,-1)]):
    for j, (ox, oy) in enumerate([(0,0),(11*sgn,-6),(24*sgn,2),(34*sgn,-4)]):
        d.shape("ellipse", f"Track {i+1}.{j+1}", x=x+ox*s, y=y+oy*s,
                width=8.5*s, height=5.5*s, fill="#46564F", opacity=62, stroke=NONE)

# --- shoulders / bust (closes on the disc arc) --------------------------------------
by = 800
bdx = math.sqrt(R*R - (by - CY)**2)
d.path(f"M366,614 C336,672 300,738 {CX-bdx:.1f},{by} "
       f"A{R},{R} 0 0 0 {CX+bdx:.1f},{by} "
       f"C700,738 664,672 634,614 Z",
       "Bust", fill=BUST_GRAD, stroke=NONE)
pair("M366,616 C336,672 300,738 262,794", "Shoulder line", fill=NONE,
     stroke=INK, strokeWidth=6, cap="round")
# pale throat + chest blaze
d.path("M418,642 C430,708 466,772 500,838 C534,772 570,708 582,642 C550,664 450,664 418,642 Z",
       "Throat white", fill=PALE_GRAD, opacity=82, stroke=NONE)
pair("M330,724 C362,704 394,694 422,694", "Chest fur", fill=NONE,
     stroke="#584631", strokeWidth=5, opacity=32, cap="round")
pair("M300,774 C340,752 380,744 412,746", "Chest fur 2", fill=NONE,
     stroke="#584631", strokeWidth=5, opacity=28, cap="round")
# faint lynx spots scattered on the shoulders
for i, (x, y, w) in enumerate([(360,700,12),(420,730,10),(585,700,12),(530,745,9),
                               (330,760,11),(655,765,10),(465,768,8)]):
    d.shape("ellipse", f"Bust spot {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#4A3826", opacity=40, stroke=NONE)

# --- ears: tall, wide-set, black backs ----------------------------------------------
EAR_L = "M350,468 C326,394 314,296 322,204 C364,256 422,326 464,388 Z"
d.path(EAR_L, "Ear L", fill=lin(322, 200, 322, 460, (0, "#3A2A1E"), (1, "#8A6A4A")),
       stroke=INK, strokeWidth=6)
d.path(mirror(EAR_L), "Ear R", fill=lin(678, 200, 678, 460, (0, "#3A2A1E"), (1, "#8A6A4A")),
       stroke=INK, strokeWidth=6)
INNER_L = "M362,444 C348,386 340,312 342,248 C374,292 414,342 446,390 Z"
pair(INNER_L, "Inner ear", fill=lin(0, 248, 0, 444, (0, "#7A6248"), (1, "#C4A888")),
     opacity=85, stroke=NONE)
for j, (a, b, c2) in enumerate([((362,432),(354,384),(352,336)), ((378,420),(374,374),(368,326)),
                                 ((394,412),(394,374),(388,334)), ((410,406),(412,372),(406,342))]):
    pair(f"M{a[0]},{a[1]} Q{b[0]},{b[1]} {c2[0]},{c2[1]}", f"Ear fringe {j+1}",
         fill=NONE, stroke="#F2EBDC", strokeWidth=3, opacity=40, cap="round")
pair("M336,258 C334,316 340,384 354,442", "Ear rim light", fill=NONE,
     stroke="#E0D2B8", strokeWidth=4, opacity=28, cap="round")

# --- the tufts: long inky antennae off each ear tip ----------------------------------
TUFT = ("M318,240 C310,196 304,150 312,104 C320,132 326,146 328,158 "
        "C332,142 336,130 342,116 C346,152 348,196 344,240 Z")
d.path(TUFT, "Tuft L", fill=TUFT_GRAD, stroke=NONE)
d.path(mirror(TUFT), "Tuft R", fill=TUFT_GRAD, stroke=NONE)
pair("M316,182 Q304,152 300,120", "Tuft flick outer", fill=NONE,
     stroke="#140E0C", strokeWidth=4, cap="round")
pair("M340,186 Q350,160 356,134", "Tuft flick inner", fill=NONE,
     stroke="#140E0C", strokeWidth=3, cap="round")
pair("M326,220 C322,186 320,154 318,128", "Tuft sheen", fill=NONE,
     stroke="#8A7A8E", strokeWidth=3, opacity=35, cap="round")

# --- head ----------------------------------------------------------------------------
HEAD = ("M500,376 C582,376 648,408 670,472 C688,530 668,592 632,630 "
        "C596,666 548,682 500,682 C452,682 404,666 368,630 "
        "C332,592 312,530 330,472 C352,408 418,376 500,376 Z")
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Crown light", x=416, y=388, width=170, height=56,
        fill="#E8D4B4", opacity=22, stroke=NONE)
# faint spots across crown and temples — lynx spotting is muted
for i, (x, y, w) in enumerate([(430,400,10),(470,392,8),(530,392,8),(570,402,10),
                               (400,436,9),(462,424,7),(540,426,7),(600,440,9),
                               (370,480,10),(630,482,10),(500,406,7)]):
    d.shape("ellipse", f"Crown spot {i+1}", x=x, y=y, width=w, height=w*0.65,
            fill="#4A3826", opacity=45, stroke=NONE)

# --- the cheek ruff: pale fur flaring below each jaw — the lynx signature --------------
pair("M372,560 C344,596 322,644 316,700 C336,686 356,682 372,688 "
     "C356,700 344,716 340,734 C368,722 392,702 404,676 "
     "C420,646 424,606 418,578 C402,568 386,562 372,560 Z",
     "Ruff", fill=PALE_GRAD, opacity=92, stroke=NONE)
pair("M368,586 C352,616 342,652 340,686", "Ruff crease", fill=NONE,
     stroke="#8A7658", strokeWidth=5, opacity=40, cap="round")
pair("M382,640 C372,664 362,686 350,706", "Ruff crease 2", fill=NONE,
     stroke="#8A7658", strokeWidth=4, opacity=32, cap="round")
# ruff fringe points
for j, (x, y) in enumerate([(330,700),(352,712),(378,700)]):
    d.path(f"M{x},{y} l10,-26 l8,28 Z", f"Ruff tip {j+1}",
           fill="#E8DEC8", opacity=85, stroke=NONE)
    d.path(f"M{1000-x-18},{y} l10,-26 l8,28 Z", f"Ruff tip R{j+1}",
           fill="#E8DEC8", opacity=85, stroke=NONE)

# pale eye surrounds
pair("M394,474 C412,460 444,458 462,468 C446,474 416,478 394,474 Z", "Brow white",
     fill=PALE_GRAD, opacity=80, stroke=NONE)

# --- eyes: wide-set, level amber stare --------------------------------------------------
EYE_L = "M396,502 C412,484 448,478 466,496 C452,518 418,524 396,502 Z"
pair(EYE_L, "Eye", fill=IRIS_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pupil L", x=426, y=486, width=14, height=30, fill="#140C06", stroke=NONE)
d.shape("ellipse", "Pupil R", x=560, y=486, width=14, height=30, fill="#140C06", stroke=NONE)
d.shape("ellipse", "Glint L", x=429, y=492, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=563, y=492, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
pair("M392,496 C416,476 450,476 470,498", "Upper lid", fill=NONE,
     stroke=INK, strokeWidth=7, cap="round")

# --- muzzle ------------------------------------------------------------------------------
d.path("M500,530 C520,530 532,558 540,576 C566,582 598,598 602,624 "
       "C602,648 558,666 500,666 C442,666 398,648 398,624 "
       "C402,598 434,582 460,576 C468,558 480,530 500,530 Z",
       "Muzzle white", fill=PALE_GRAD, opacity=92, stroke=NONE)
pair("M422,602 C434,594 454,596 460,606 C452,616 430,616 422,602 Z", "Whisker spot",
     fill="#241812", opacity=82, stroke=NONE)
for j, (x, y) in enumerate([(432,618),(446,622),(440,632)]):
    d.shape("ellipse", f"Whisker dot L{j+1}", x=x, y=y, width=4, height=4,
            fill="#6A5644", opacity=60, stroke=NONE)
    d.shape("ellipse", f"Whisker dot R{j+1}", x=1000-x-4, y=y, width=4, height=4,
            fill="#6A5644", opacity=60, stroke=NONE)
# nose: gray-brick with dark rim
d.path("M480,576 C492,570 508,570 520,576 C518,590 508,598 500,600 C492,598 482,590 480,576 Z",
       "Nose", fill=lin(0, 570, 0, 600, (0, "#A87A6C"), (1, "#6E4038")),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nose glint", x=490, y=576, width=9, height=4, fill="#FFFFFF", opacity=40, stroke=NONE)
d.path("M500,600 L500,620", "Philtrum", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
pair("M500,620 C488,630 476,632 464,628", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M472,646 C488,654 512,654 528,646", "Chin shade", fill=NONE,
       stroke="#B8A88E", strokeWidth=6, opacity=45, cap="round")
# whiskers — long, pale, sparse
for j, (x1, y1, x2, y2) in enumerate([(426,606,306,584),(428,614,302,620),(432,622,312,652),
                                      (574,606,694,584),(572,614,698,620),(568,622,688,652)]):
    d.path(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-6} {x2},{y2}", f"Whisker {j+1}",
           fill=NONE, stroke="#F4EEE0", strokeWidth=2.5, opacity=60, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#1E2C3E", strokeWidth=6)

# --- name --------------------------------------------------------------------------------
d.text("EURASIAN LYNX", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#D8E0E8", justify="center")

d.finish("eurasian-lynx-V1R00")

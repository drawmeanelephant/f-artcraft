#!/usr/bin/env python3
"""American pika — field plate V1R00. The mountain's smallest farmer:
a round-eared haymaker perched on talus, a bundled mouthful of sedge
sticking out of its jaws, a started haypile curing on the flat stone
beside it. Talus plate, alpenglow mood — snow peaks catching the last
rose light behind the boulder field, angular scree closing on the disc
arc. 1000x1000. House style: gradients + translucent shading, never
flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("American Pika — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#171420"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0C0E1A"), (1, "#05060C"))
PLATE_GRAD = rad((0, "#7E7488"), (0.5, "#453E58"), (1, "#181422"))
ROCK_GRAD = lin(0, 560, 0, 880, (0, "#5E5870"), (0.6, "#3C3650"), (1, "#1E1A2C"))
COAT      = rad((0, "#B89A72"), (0.55, "#8E7250"), (1, "#54402C"))
BELLY     = rad((0, "#D8C4A0"), (1, "#A8896A"))

# --- backdrop + alpenglow plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(145,115,4),(855,125,5),(112,440,3),(880,500,4),
                               (175,735,4),(858,755,4),(265,145,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8D2E0", opacity=28, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#7E7488", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#221C30", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCD4E4", strokeWidth=3, opacity=38)

# alpenglow: the rose light pooling over the high cirque
d.shape("ellipse", "Alpenglow", x=330, y=210, width=560, height=300,
        fill=rad((0, "#F0A8A0", 40), (0.55, "#F0A8A0", 13), (1, "#F0A8A0", 0)),
        stroke=NONE)
# early stars pricking through above the glow
for i, (x, y, w) in enumerate([(300,140,4),(450,115,5),(585,145,4),(215,250,3),
                               (370,190,4),(505,165,3),(175,410,4),(720,130,4)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8E2EA", opacity=50, stroke=NONE)

# --- the cirque: snow peaks sawtoothing across the plate, rose-lit -------------------
yl2, yr2 = 596, 596
xl2, xr2 = disc_x(yl2, -1), disc_x(yr2, 1)
d.path(f"M{xl2:.1f},{yl2} L240,560 L300,470 L350,520 L420,430 L480,540 "
       f"L540,470 L610,545 L680,480 L760,560 L{xr2:.1f},{yr2} Z",
       "Far cirque", fill="#443C52", opacity=95, stroke=NONE)
# rose caps: the last light burning on each summit, seated wide on the ridge
for i, (px, py, s) in enumerate([(300, 470, 1.3), (420, 430, 1.5), (540, 470, 1.2),
                                 (680, 480, 1.3), (350, 520, 0.9), (610, 545, 0.9)]):
    d.path(f"M{px - 30*s},{py + 34*s} L{px},{py - 2*s} L{px + 30*s},{py + 34*s} "
           f"C{px + 16*s},{py + 42*s} {px - 16*s},{py + 42*s} {px - 30*s},{py + 34*s} Z",
           f"Alpen cap {i+1}", fill="#F0B8AC", opacity=92, stroke=NONE)
    # shaded lee face so the cap reads as snow, not a pennant
    d.path(f"M{px},{py - 2*s} L{px + 30*s},{py + 34*s} "
           f"C{px + 16*s},{py + 40*s} {px + 6*s},{py + 40*s} {px},{py + 36*s} Z",
           f"Alpen shade {i+1}", fill="#B07878", opacity=55, stroke=NONE)
# snow veins below the caps
for i, (x0, y0, x1, y1) in enumerate([(420, 448, 396, 492), (300, 486, 322, 512),
                                      (540, 484, 566, 520), (680, 496, 660, 528)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Snow vein {i+1}", fill=NONE,
           stroke="#E8C8C0", strokeWidth=3, opacity=55, cap="round")

# --- talus: angular scree piling onto the floor arc ----------------------------------
fy = 664
fl, fr = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fl:.1f},{fy} L300,648 L430,660 L560,646 L680,658 L{fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Talus floor", fill=ROCK_GRAD, stroke=NONE)
d.path(f"M{fl+8:.1f},{fy} L300,648 L430,660 L560,646 L680,658 L{fr-8:.1f},{fy}",
       "Talus crest light", fill=NONE, stroke="#D8B8C0", strokeWidth=4,
       opacity=26, cap="round")
# boulder field: angular shards with rose rims, sizes falling off with depth
def rock(cx, cy, w, h, lean, lab, op=100):
    pts = [(cx - w*0.5 + lean*0.2, cy), (cx - w*0.42, cy - h*0.62),
           (cx - w*0.1 + lean, cy - h), (cx + w*0.38, cy - h*0.55),
           (cx + w*0.5, cy)]
    d.path("M" + " L".join(f"{p[0]:.0f},{p[1]:.0f}" for p in pts) + " Z",
           lab, fill=lin(0, cy - h, 0, cy, (0, "#6A6480"), (1, "#322C44")),
           stroke=INK, strokeWidth=4, opacity=op)
    d.path(f"M{pts[2][0]:.0f},{pts[2][1]:.0f} L{pts[3][0]:.0f},{pts[3][1]:.0f}",
           lab + " rim", fill=NONE, stroke="#E8B8B0", strokeWidth=3.5,
           opacity=40, cap="round")
rock(250, 780, 180, 130, -30, "Boulder L")
rock(640, 800, 220, 150, 20, "Boulder R")
rock(430, 850, 260, 170, -15, "Boulder C")
rock(160, 700, 110, 80, -20, "Scree L", op=90)
rock(760, 700, 120, 90, 15, "Scree R", op=90)
# small shards
for i, (x, y, w, a) in enumerate([(300,710,46,-15),(520,730,54,10),(700,760,40,-20),
                                  (390,790,44,25),(560,830,48,-10),(330,830,36,15)]):
    assert on_disc(x, y - w * 0.3, 4), (x, y)
    t = math.radians(a); c, s = math.cos(t), math.sin(t)
    h = w * 0.5
    pts = [(-w/2, h/2), (-w*0.3, -h/2), (w*0.35, -h*0.35), (w/2, h/2)]
    d.path("M" + " L".join(f"{x+px*c-py*s:.0f},{y+px*s+py*c:.0f}" for px, py in pts) + " Z",
           f"Shard {i+1}", fill="#48415A", opacity=95, stroke=NONE)

# --- the haypile curing on the flat stone beside the pika ----------------------------
# a loose cone of drying sedge on boulder R's top
for j, (dx, dy, dr) in enumerate([(-30, 0, -70), (-10, -6, -40), (10, -4, -10),
                                  (28, 0, 30), (0, -12, -55), (-20, -10, -95)]):
    x0, y0 = 700 + dx, 652 + dy
    d.path(f"M{x0},{y0} C{x0 + 6},{y0 - 22} {x0 + dr*0.4},{y0 - 36} {x0 + dr*0.7},{y0 - 46}",
           f"Hay blade {j+1}", fill=NONE, stroke="#9AA858", strokeWidth=3.5,
           opacity=90, cap="round")
d.path("M666,652 C684,644 716,644 734,652", "Haypile base", fill=NONE,
       stroke="#7A8844", strokeWidth=8, opacity=80, cap="round")
# one alpine bloom drying in the pile
d.path("M688,606 m-7,0 a7,7 0 1,0 14,0 a7,7 0 1,0 -14,0", "Dry bloom",
       fill="#C8A85E", stroke=NONE)

# contact shadow under the pika on its perch
d.shape("ellipse", "Body shadow", x=430, y=626, width=220, height=44,
        fill="#080610", opacity=50, stroke=NONE)

# === the pika: a round haymaker perched in profile, facing left ======================
# hindquarters rounding onto the stone, chest lifted — a furry egg on end
d.path("M530,470 "                                   # crown between the ears
       "C578,472 614,506 624,556 "                   # back curving down right
       "C632,596 626,630 602,648 "                   # rump onto the stone
       "C570,664 524,668 490,660 "                   # seat on the rock
       "C462,654 446,636 444,610 "                   # belly bottom
       "C442,580 448,548 460,524 "                   # chest rising
       "C468,500 480,484 496,476 "                   # throat
       "C508,470 518,468 530,470 Z",
       "Body", fill=COAT, stroke=INK, strokeWidth=6)
# pale belly wash under the chin and down the front
d.path("M488,520 C470,552 462,596 472,628 C480,652 508,662 536,660 "
       "C510,648 496,616 494,576 C492,550 494,532 488,520 Z",
       "Belly wash", fill=BELLY, opacity=45, stroke=NONE)
# grizzled guard hairs over the dome
for i, (x, y, dx, dy) in enumerate([(560,490,14,-10),(596,530,14,-6),(616,576,12,-2),
                                    (606,620,10,2),(470,540,-12,-4),(458,580,-12,-2)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Guard hair {i+1}",
           fill=NONE, stroke="#C8A878", strokeWidth=2.5, opacity=55, cap="round")

# round ears tucked onto the crown — the pika's trademark discs
for sgn, lab in ((-1, "L"), (1, "R")):
    ex, ey = 530 + sgn * 30, 446 + sgn * 4
    d.shape("ellipse", f"Ear {lab}", x=ex-23, y=ey-24, width=46, height=48,
            fill=rad((0, "#A8896A"), (1, "#5E462E")), stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Ear in {lab}", x=ex-12, y=ey-10, width=24, height=26,
            fill="#6E5034", opacity=85, stroke=NONE)

# hind foot folded at the front of the seat — the haunch paw
d.path("M470,624 C458,612 458,596 470,588 C484,580 502,586 506,600 "
       "C510,614 500,628 486,630 C478,632 472,630 470,624 Z",
       "Hind paw", fill="#8A6A48", stroke=INK, strokeWidth=3.5)
for j in range(2):
    d.path(f"M{468+j*10},{600} q8,-4 14,2", f"Paw toe {j+1}", fill=NONE,
           stroke="#2A1E12", strokeWidth=2.5, opacity=70, cap="round")
# forepaw braced under the chin, gripping the hay
d.path("M492,556 C484,544 486,530 498,526 C510,522 520,530 520,542 "
       "C520,554 510,564 500,564 C496,564 494,560 492,556 Z",
       "Forepaw", fill="#7E5E3E", stroke=INK, strokeWidth=3)

# --- the mouthful of hay: a bundled fan of sedge gripped in the jaws -----------------
# stems fanning forward-down out of the mouth
for j, (ex, ey, bow) in enumerate([(404, 560, -14), (396, 574, -4), (400, 588, 8),
                                   (410, 600, 18), (396, 548, -24), (388, 562, -16)]):
    x0, y0 = 462, 512
    mx = (x0 + ex) / 2 + bow
    my = (y0 + ey) / 2
    col = "#A8B868" if j % 2 else "#7E9048"
    d.path(f"M{x0},{y0} Q{mx},{my} {ex},{ey}", f"Hay stem {j+1}",
           fill=NONE, stroke=col, strokeWidth=4, cap="round")
# seed heads flagging on two tips
for j, (x, y) in enumerate([(396, 546), (402, 598)]):
    d.shape("ellipse", f"Hay head {j+1}", x=x-5, y=y-9, width=10, height=18,
            fill="#C8B868", stroke=NONE)

# --- head: blunt rabbit face with the round dark eye --------------------------------
d.path("M530,462 "                                   # crown
       "C556,464 572,482 574,506 "                   # back of skull
       "C576,524 570,540 556,550 "                   # jaw curve
       "C540,560 520,562 504,556 "                   # chin
       "C484,550 470,536 468,518 "                   # cheek
       "C466,500 474,480 490,470 "                   # snout bridge
       "C502,462 516,460 530,462 Z",                 # crown
       "Head", fill=rad((0, "#BC9E78"), (0.65, "#96785A"), (1, "#5E4830")),
       stroke=INK, strokeWidth=5)
# pale chin patch under the mouthful
d.path("M478,536 C488,548 506,554 522,552 C510,544 500,534 494,522 "
       "C486,520 480,526 478,536 Z", "Chin patch", fill="#D8C4A0",
       opacity=50, stroke=NONE)
# the eye: round, dark, set high
d.shape("ellipse", "Eye", x=516, y=488, width=26, height=28,
        fill="#140E08", stroke=NONE)
d.shape("ellipse", "Glint", x=522, y=494, width=7, height=7,
        fill="#FFFFFF", opacity=92, stroke=NONE)
# nose tucked into the hay
d.path("M466,506 C458,502 456,494 464,490 C474,486 482,492 482,502 "
       "C482,510 472,510 466,506 Z", "Nose", fill="#241A10", stroke=NONE)
d.path("M470,512 C478,520 490,524 500,524", "Mouth", fill=NONE,
       stroke="#5E4228", strokeWidth=3, opacity=80, cap="round")
# whiskers laid back over the bundle
for j, (y0, dy) in enumerate([(502, -8), (510, 0), (518, 8)]):
    d.path(f"M470,{y0} C496,{y0+dy} 516,{y0+dy+2} 532,{y0+dy}",
           f"Whisker {j+1}", fill=NONE, stroke="#C8B494",
           strokeWidth=2.5, opacity=55, cap="round")
# rose alpenglow rim on the back
d.path("M574,490 C596,520 606,560 604,600", "Rim light", fill=NONE,
       stroke="#F0B8AC", strokeWidth=6, opacity=30, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#100C18", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
r1 = d.text("AMERICAN PIKA", "Name", x=500, y=962, size=56, font="Virelai Sans",
            color="#DCD4E4", justify="center")

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
b = find(layers, r1["id"])["bounds"]
print("name bounds", {k: round(v) for k, v in b.items()})
assert b["width"] <= 800 and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("american-pika-V1R00")

#!/usr/bin/env python3
"""Tarsier — field-guide plate V1R00. Near-frontal portrait: two huge amber
eyes taking a third of the face, ears like cupped leaves, thin bony fingers
with disc pads gripping a vertical stem. Dark tropical plate, one warm rim
light from the right; the foliage closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tarsier — Field Plate", 1000, 1000)

INK = "#1E150E"
RIM = "#FFB25A"                    # the one warm rim light, from the right
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

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

def on_disc(deg):
    t = math.radians(deg)
    return CX + R*math.cos(t), CY + R*math.sin(t)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#10221A"), (1, "#040A07"))
PLATE_GRAD = rad((0, "#3F6A4B"), (0.62, "#23412F"), (1, "#11221A"))
FUR_GRAD = rad((0, "#DCC6A2"), (0.7, "#B39272"), (1, "#7C6248"))
BODY_GRAD = lin(0, 560, 0, 870, (0, "#A88866"), (1, "#5E4834"))
EAR_GRAD = lin(240, 0, 400, 0, (0, "#B88E70"), (1, "#8A6650"))
IRIS_GRAD = rad((0, "#FFE38E"), (0.55, "#F2A734"), (1, "#8E4F10"))
STEM_GRAD = lin(474, 0, 526, 0, (0, "#24321E"), (0.55, "#55663E"), (0.85, "#7C7A46"), (1, "#C58A44"))
PAD_GRAD = rad((0, "#E6C2A0"), (1, "#A57A5C"))
FOLIAGE_GRAD = lin(0, 480, 0, 880, (0, "#2E5A38"), (1, "#0E2115"))

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w, o) in enumerate([(70,120,6,40),(150,50,4,30),(40,420,5,35),(930,90,6,40),
                                  (890,40,4,30),(955,380,5,35),(60,800,5,30),(940,780,5,30)]):
    d.shape("ellipse", f"Firefly {i+1}", x=x, y=y, width=w, height=w, fill="#E8D27A", opacity=o, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A140E", strokeWidth=6)
# warm rim light washing in from the right
for k, (a, bulge, op) in enumerate([(72, 700, 5), (58, 770, 6), (44, 830, 7), (30, 880, 8)]):
    gx0, gy0 = on_disc(-a); gx1, gy1 = on_disc(a)
    d.path(f"M{gx0:.1f},{gy0:.1f} A{R},{R} 0 0 1 {gx1:.1f},{gy1:.1f} "
           f"C{bulge},{CY + 220} {bulge},{CY - 220} {gx0:.1f},{gy0:.1f} Z",
           f"Rim glow {k+1}", fill=RIM, opacity=op, stroke=NONE)
for i, (x, y, w) in enumerate([(220,190,6),(300,130,5),(700,140,6),(780,250,5),(170,330,5),
                               (830,380,6),(250,420,4),(760,470,5)]):
    d.shape("ellipse", f"Spore {i+1}", x=x, y=y, width=w, height=w, fill="#E8D27A", opacity=45, stroke=NONE)

# understorey foliage, both masses closing on the disc arc
lx0, ly0 = on_disc(172); lx1, ly1 = on_disc(104)
d.path(f"M{lx0:.1f},{ly0:.1f} Q160,470 222,512 Q182,540 214,578 Q284,566 330,628 "
       f"Q282,650 300,700 Q356,700 372,770 Q338,790 352,826 Q378,846 {lx1:.1f},{ly1:.1f} "
       f"A{R},{R} 0 0 1 {lx0:.1f},{ly0:.1f} Z",
       "Foliage L", fill=FOLIAGE_GRAD, opacity=92, stroke=NONE)
rx0, ry0 = on_disc(76); rx1, ry1 = on_disc(8)
d.path(f"M{rx0:.1f},{ry0:.1f} Q622,846 648,826 Q662,790 628,770 Q644,700 700,700 "
       f"Q718,650 670,628 Q716,566 786,578 Q818,540 778,512 Q840,470 {rx1:.1f},{ry1:.1f} "
       f"A{R},{R} 0 0 1 {rx0:.1f},{ry0:.1f} Z",
       "Foliage R", fill=FOLIAGE_GRAD, opacity=92, stroke=NONE)
# leaf midribs (lighter, translucent)
for i, dd in enumerate(["M110,560 Q170,530 214,516", "M150,640 Q240,610 322,630",
                        "M210,740 Q290,720 364,768", "M890,560 Q830,530 786,516",
                        "M850,640 Q760,610 678,630", "M790,740 Q710,720 636,768"]):
    d.path(dd, f"Leaf rib {i+1}", fill=NONE, stroke="#6E9A62", strokeWidth=4, opacity=40, cap="round")

# --- body (behind the stem) ---------------------------------------------------------
d.path("M500,560 C590,560 650,640 652,730 C654,800 600,856 500,862 "
       "C400,856 346,800 348,730 C350,640 410,560 500,560 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.path("M640,680 C650,720 650,770 628,812", "Body rim", fill=NONE, stroke=RIM,
       strokeWidth=6, opacity=45, cap="round")
for i, dd in enumerate(["M388,700 C380,730 380,760 388,790", "M612,700 C620,730 620,760 612,790",
                        "M420,820 C440,836 460,844 480,848", "M580,820 C560,836 540,844 520,848"]):
    d.path(dd, f"Body fur {i+1}", fill=NONE, stroke="#4A3828", strokeWidth=4, opacity=40, cap="round")

THIGH = "M362,770 C350,704 394,670 430,692 C458,710 456,800 434,840 C414,868 372,850 362,770 Z"
pair(THIGH, "Thigh", fill=lin(0, 680, 0, 860, (0, "#B39272"), (1, "#6A523C")), stroke=INK, strokeWidth=5)
pair("M380,760 C378,730 392,708 412,704", "Thigh light", fill=NONE, stroke="#E2CCA8", strokeWidth=5, opacity=35, cap="round")
d.path(mirror("M364,730 C358,770 366,812 392,846"), "Thigh rim", fill=NONE, stroke=RIM, strokeWidth=5, opacity=55, cap="round")

# --- the vertical stem, both ends closing on the disc arc ---------------------------
sx0, sx1 = 474, 526
top = CY - math.sqrt(R*R - (CX - sx0)**2)
bot = CY + math.sqrt(R*R - (CX - sx0)**2)
d.path(f"M{sx0},{top:.1f} L{sx0},{bot:.1f} A{R},{R} 0 0 0 {sx1},{bot:.1f} "
       f"L{sx1},{top:.1f} A{R},{R} 0 0 0 {sx0},{top:.1f} Z",
       "Stem", fill=STEM_GRAD, stroke=NONE)
d.path(f"M{sx1 - 4},{top + 8:.1f} L{sx1 - 4},{bot - 8:.1f}", "Stem rim light",
       fill=NONE, stroke=RIM, strokeWidth=4, opacity=55, cap="round")
d.path(f"M{sx0 + 4},{top + 8:.1f} L{sx0 + 4},{bot - 8:.1f}", "Stem shade",
       fill=NONE, stroke="#0E160C", strokeWidth=6, opacity=40, cap="round")
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0A140E", strokeWidth=6)
for i, y in enumerate([150, 250, 840]):
    d.path(f"M{sx0},{y} Q500,{y + 8} {sx1},{y}", f"Stem node {i+1}",
           fill=NONE, stroke="#1A2414", strokeWidth=4, opacity=60, cap="round")
    d.path(f"M{sx0 + 2},{y - 5} Q500,{y + 2} {sx1 - 2},{y - 5}", f"Stem node light {i+1}",
           fill=NONE, stroke="#A8A060", strokeWidth=3, opacity=35, cap="round")

# --- arms + the bony fingers gripping the stem (arm tops tuck under the head) ----------
def tube(dd, label, w=10, fill="#B08C6C"):
    d.path(dd, f"{label} outline", fill=NONE, stroke=INK, strokeWidth=w + 6, cap="round")
    d.path(dd, label, fill=NONE, stroke=fill, strokeWidth=w, cap="round")

def pad(x, y, label, r=10):
    d.shape("ellipse", label, x=x - r, y=y - r*0.9, width=2*r, height=1.8*r,
            fill=PAD_GRAD, stroke=INK, strokeWidth=3)

ARM = lin(0, 620, 0, 840, (0, "#B39272"), (1, "#7C6248"))
# left hand high, fingers fan rightward across the stem
d.path("M392,600 C372,650 384,700 426,730 C444,742 464,734 466,716 "
       "C462,690 446,650 440,600 Z", "Arm L", fill=ARM, stroke=INK, strokeWidth=5)
for k, (y0, y1) in enumerate([(704, 694), (722, 720), (740, 746)]):
    tube(f"M462,{y0} C488,{y0 + 4} 518,{y1 + 4} 542,{y1}", f"Finger L{k+1}")
    d.shape("ellipse", f"Knuckle L{k+1}", x=496, y=(y0 + y1)/2 - 3, width=14, height=12,
            fill="#C4A27E", stroke=INK, strokeWidth=3)
    pad(547, y1, f"Finger pad L{k+1}", r=11)
d.shape("ellipse", "Palm L", x=430, y=690, width=42, height=66, fill=ARM, stroke=INK, strokeWidth=5)
d.path("M440,700 C436,716 436,736 442,748", "Palm L light", fill=NONE, stroke="#E2CCA8", strokeWidth=4, opacity=35, cap="round")
# right hand lower, fingers fan leftward
d.path("M608,640 C628,690 618,760 580,800 C564,812 544,804 544,786 "
       "C550,756 566,700 560,640 Z", "Arm R", fill=ARM, stroke=INK, strokeWidth=5)
d.path("M616,680 C620,720 612,760 592,788", "Arm R rim", fill=NONE, stroke=RIM, strokeWidth=5, opacity=60, cap="round")
for k, (y0, y1) in enumerate([(786, 778), (804, 804), (822, 830)]):
    tube(f"M538,{y0} C512,{y0 + 4} 482,{y1 + 4} 458,{y1}", f"Finger R{k+1}")
    d.shape("ellipse", f"Knuckle R{k+1}", x=490, y=(y0 + y1)/2 - 3, width=14, height=12,
            fill="#C4A27E", stroke=INK, strokeWidth=3)
    pad(453, y1, f"Finger pad R{k+1}", r=11)
d.shape("ellipse", "Palm R", x=528, y=772, width=42, height=66, fill=ARM, stroke=INK, strokeWidth=5)
d.path("M562,786 C566,800 566,816 560,828", "Palm R rim", fill=NONE, stroke=RIM, strokeWidth=4, opacity=55, cap="round")
for k, y in enumerate([694, 720, 746]):
    d.path(f"M552,{y - 4} C556,{y - 2} 558,{y + 1} 557,{y + 4}", f"Pad rim {k+1}",
           fill=NONE, stroke=RIM, strokeWidth=3, opacity=60, cap="round")

# --- ears: big cupped leaves, thin and veined ----------------------------------------
EAR = ("M384,364 C328,362 250,338 220,288 C194,242 212,186 260,178 "
       "C324,168 386,216 408,288 C416,322 412,364 384,364 Z")
pair(EAR, "Ear", fill=EAR_GRAD, stroke=INK, strokeWidth=6)
pair("M374,344 C330,342 268,322 244,284 C226,252 236,210 266,206 "
     "C316,200 364,238 382,292 C388,316 388,344 374,344 Z", "Ear cup",
     fill=lin(240, 200, 384, 344, (0, "#F0C9A8"), (1, "#A57658")), opacity=70, stroke=NONE)
pair("M286,222 C282,258 300,300 340,334", "Ear cup shadow", fill=NONE, stroke="#5E3E2C",
     strokeWidth=12, opacity=25, cap="round")
for j, dd in enumerate(["M368,336 C334,300 296,260 266,224", "M374,326 C360,284 340,242 316,212",
                        "M360,340 C318,326 278,306 250,276", "M312,276 L288,268", "M330,246 L338,226"]):
    pair(dd, f"Ear vein {j+1}", fill=NONE, stroke="#7A5440", strokeWidth=3, opacity=55, cap="round")
d.path(mirror("M226,292 C200,248 210,190 260,180"), "Ear rim light", fill=NONE, stroke=RIM,
       strokeWidth=5, opacity=60, cap="round")

# --- head ---------------------------------------------------------------------------
HEAD = ("M500,300 C612,300 714,372 714,482 C714,584 644,652 562,676 "
        "C532,684 468,684 438,676 C356,652 286,584 286,482 C286,372 388,300 500,300 Z")
d.path(HEAD, "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
d.path("M690,400 C712,450 714,520 690,580 C672,620 640,648 604,664", "Head rim light",
       fill=NONE, stroke=RIM, strokeWidth=7, opacity=55, cap="round")
d.shape("ellipse", "Crown light", x=400, y=312, width=200, height=50, fill="#FFF2DA", opacity=16, stroke=NONE)
for i, dd in enumerate(["M470,318 C474,306 482,298 492,294", "M508,294 C518,298 526,306 530,318",
                        "M440,326 C440,314 444,304 452,298", "M560,326 C560,314 556,304 548,298",
                        "M306,530 C310,552 320,572 334,588", "M694,530 C690,552 680,572 666,588",
                        "M340,610 C352,626 368,640 386,650", "M660,610 C648,626 632,640 614,650"]):
    d.path(dd, f"Fur tuft {i+1}", fill=NONE, stroke="#6A5038", strokeWidth=4, opacity=60, cap="round")

# --- the eyes: a third of the face -----------------------------------------------------
pair("M420,398 C480,398 510,446 510,494 C510,552 470,590 420,590 "
     "C364,590 326,548 326,494 C326,440 364,398 420,398 Z", "Eye socket",
     fill="#3A2818", opacity=55, stroke=NONE)
d.shape("ellipse", "Iris L", x=344, y=414, width=152, height=152, fill=IRIS_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Iris R", x=504, y=414, width=152, height=152, fill=IRIS_GRAD, stroke=INK, strokeWidth=5)
for side, cx in (("L", 420), ("R", 580)):
    for k in range(10):
        a = math.radians(k*36 + 8)
        x0, y0 = cx + 34*math.cos(a), 490 + 34*math.sin(a)
        x1, y1 = cx + 66*math.cos(a), 490 + 66*math.sin(a)
        d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", f"Iris fibre {side}{k+1}",
               fill=NONE, stroke="#B86A14", strokeWidth=3, opacity=35, cap="round")
    d.shape("ellipse", f"Pupil {side}", x=cx - 30, y=460, width=60, height=60, fill="#0E0805", stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=cx - 28, y=446, width=22, height=22, fill="#FFFFFF", opacity=92, stroke=NONE)
    d.shape("ellipse", f"Glint {side}2", x=cx + 14, y=520, width=10, height=10, fill="#FFE6A8", opacity=60, stroke=NONE)
    d.path(f"M{cx - 58},{470} C{cx - 40},{436} {cx + 10},{424} {cx + 46},{440}", f"Iris top shade {side}",
           fill=NONE, stroke="#6E3A0A", strokeWidth=10, opacity=30, cap="round")
# warm reflection on the right edge of each iris
d.path("M480,456 C494,480 494,512 478,540", "Iris rim L", fill=NONE, stroke=RIM, strokeWidth=5, opacity=45, cap="round")
d.path("M640,456 C654,480 654,512 638,540", "Iris rim R", fill=NONE, stroke=RIM, strokeWidth=5, opacity=60, cap="round")
d.path("M492,420 C496,450 500,520 500,560", "Nose ridge shade", fill=NONE, stroke="#5A4230",
       strokeWidth=6, opacity=45, cap="round")

# --- muzzle ---------------------------------------------------------------------------
d.shape("ellipse", "Muzzle", x=440, y=570, width=120, height=90, fill="#E8D4B2", opacity=55, stroke=NONE)
d.path("M488,592 C488,584 512,584 512,592 C512,602 506,608 500,608 C494,608 488,602 488,592 Z",
       "Nose", fill=lin(0, 584, 0, 608, (0, "#6E4A36"), (1, "#3A2418")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=494, y=588, width=8, height=4, fill="#FFFFFF", opacity=45, stroke=NONE)
d.path("M500,608 L500,624", "Philtrum", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M462,626 C478,640 522,640 538,626", "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M470,650 C488,660 512,660 530,650", "Chin shade", fill=NONE, stroke="#7C6248",
       strokeWidth=6, opacity=35, cap="round")
for j, dd in enumerate(["M456,606 Q400,590 352,598", "M458,618 Q404,614 360,628"]):
    pair(dd, f"Whisker {j+1}", fill=NONE, stroke="#F2E2C4", strokeWidth=2, opacity=55, cap="round")

# --- name -----------------------------------------------------------------------------
d.text("TARSIER", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E6D6B4", justify="center")

d.finish("tarsier-V1R00")

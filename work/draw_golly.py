#!/usr/bin/env python3
"""Golly the guillotine — vector portrait, 900x1100."""
import sys
sys.path.insert(0, "/home/hatch/workspace/vectorcraft/work")
from vc import Draw, NONE

d = Draw()
d.new_doc("Golly — Vector Portrait", 900, 1100)

INK = "#5E3A17"; WOOD = "#B57E42"; WOOD_D = "#96652F"; GOLD = "#D9A441"; BLADE = "#C9CFD4"

d.shape("rectangle", "Background", x=0, y=0, width=900, height=1100, fill="#F7EBC8", stroke=NONE)
d.shape("ellipse", "Halo", x=100, y=80, width=700, height=900, fill="#F1DFB2", stroke=NONE)
d.shape("ellipse", "Ground shadow", x=190, y=1032, width=520, height=44, fill="#000000", opacity=10, stroke=NONE)

# legs, socks, shoes
for lbl, x in [("L", 338), ("R", 528)]:
    d.shape("rectangle", f"Leg {lbl}", x=x, y=950, width=34, height=64, fill=WOOD_D, stroke=INK, strokeWidth=4)
    d.shape("rectangle", f"Sock {lbl}", x=x - 4, y=940, width=42, height=22, radius=6, fill="#FFFFFF", stroke=INK, strokeWidth=3)
d.path("M270,1010 C270,982 300,968 345,968 C390,968 415,985 415,1010 C415,1028 400,1036 375,1036 "
       "L300,1036 C280,1036 270,1026 270,1010 Z", "Shoe L", fill="#7A4A26", stroke=INK, strokeWidth=5)
d.path("M460,1010 C460,982 490,968 535,968 C580,968 605,985 605,1010 C605,1028 590,1036 565,1036 "
       "L490,1036 C470,1036 460,1026 460,1010 Z", "Shoe R", fill="#7A4A26", stroke=INK, strokeWidth=5)

# uprights + grain
d.shape("rectangle", "Post L", x=215, y=185, width=78, height=690, fill=WOOD, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Post R", x=607, y=185, width=78, height=690, fill=WOOD, stroke=INK, strokeWidth=5)
d.path("M240,220 C235,400 245,600 238,840", "Grain L", fill=NONE, stroke=WOOD_D, strokeWidth=4, opacity=60)
d.path("M632,220 C638,400 628,600 635,840", "Grain R", fill=NONE, stroke=WOOD_D, strokeWidth=4, opacity=60)
# base + foot blocks
d.shape("rectangle", "Base beam", x=185, y=872, width=530, height=56, radius=10, fill=WOOD, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Foot block L", x=165, y=846, width=120, height=34, radius=8, fill=WOOD_D, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Foot block R", x=615, y=846, width=120, height=34, radius=8, fill=WOOD_D, stroke=INK, strokeWidth=4)

# top beam + knob
d.path("M195,192 C195,108 300,66 450,66 C600,66 705,108 705,192 C705,208 692,216 676,216 "
       "L224,216 C208,216 195,208 195,192 Z", "Top beam", fill=WOOD, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Knob stem", x=436, y=30, width=28, height=32, fill=GOLD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Knob ball", x=426, y=0, width=48, height=44, fill=GOLD, stroke=INK, strokeWidth=4)
# pulley rope
d.shape("rectangle", "Pulley rope", x=437, y=216, width=26, height=84, fill="#C89B5F", stroke=INK, strokeWidth=3)
for i, y in enumerate([232, 254, 276]):
    d.path(f"M439,{y} L461,{y + 8}", f"Rope twist {i+1}", fill=NONE, stroke="#A87C3F", strokeWidth=3)

# blade gear: crossbar, knobs, blade
d.shape("rectangle", "Crossbar", x=302, y=298, width=296, height=62, radius=10, fill=WOOD_D, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Crossbar knob L", x=277, y=310, width=38, height=38, fill=GOLD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Crossbar knob R", x=585, y=310, width=38, height=38, fill=GOLD, stroke=INK, strokeWidth=3)
for i, x in enumerate([352, 442, 532]):
    d.shape("ellipse", f"Crossbar bolt {i+1}", x=x, y=321, width=16, height=16, fill=GOLD, stroke="#8A6420", strokeWidth=2)
d.path("M312,368 L588,368 L588,452 C520,522 430,562 312,580 Z", "Blade", fill=BLADE, stroke="#6E767C", strokeWidth=4)
d.path("M312,368 L588,368 L588,420 C500,470 410,490 312,496 Z", "Blade facet", fill="#E3E8EB", opacity=65, stroke=NONE)
d.path("M330,556 C430,538 520,492 572,448", "Blade edge", fill=NONE, stroke="#F4F7F8", strokeWidth=9, cap="round")

# side rope + tassel (outside the right post)
d.path("M706,216 C716,320 716,430 708,528", "Side rope", fill=NONE, stroke="#C89B5F", strokeWidth=11)
d.shape("ellipse", "Tassel ball", x=688, y=529, width=38, height=38, fill=WOOD, stroke=INK, strokeWidth=3)
d.path("M690,562 L724,562 L732,616 C714,628 700,628 682,616 Z", "Tassel skirt", fill="#C89B5F", stroke=INK, strokeWidth=3)

# lunette board + face
d.shape("rectangle", "Lunette board", x=288, y=596, width=324, height=292, radius=22, fill="#A9713A", stroke=INK, strokeWidth=5)
for i, (x, y) in enumerate([(310, 616), (574, 616), (310, 852), (574, 852)]):
    d.shape("ellipse", f"Board bolt {i+1}", x=x, y=y, width=16, height=16, fill=GOLD, stroke="#8A6420", strokeWidth=2)
d.shape("ellipse", "Face", x=360, y=626, width=180, height=180, fill="#FFF3C4", stroke=INK, strokeWidth=6)
d.path("M392,668 C404,654 428,652 440,662", "Brow L", fill=NONE, stroke=INK, strokeWidth=8, cap="round")
d.path("M460,662 C472,652 496,654 508,668", "Brow R", fill=NONE, stroke=INK, strokeWidth=8, cap="round")
d.shape("ellipse", "Eye white L", x=382, y=678, width=52, height=66, fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye white R", x=466, y=678, width=52, height=66, fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=398, y=700, width=24, height=32, fill="#2A1C10", stroke=NONE)
d.shape("ellipse", "Pupil R", x=482, y=700, width=24, height=32, fill="#2A1C10", stroke=NONE)
d.shape("ellipse", "Glint L", x=403, y=705, width=9, height=9, fill="#FFFFFF", stroke=NONE)
d.shape("ellipse", "Glint R", x=487, y=705, width=9, height=9, fill="#FFFFFF", stroke=NONE)
d.path("M392,756 C414,806 486,806 508,756 C484,742 416,742 392,756 Z", "Mouth", fill="#7A2E1A", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Tongue", x=418, y=770, width=64, height=24, fill="#E87A7A", stroke=NONE)

# arms + gloves
d.path("M222,650 C160,640 128,606 120,556", "Arm L", fill=NONE, stroke=WOOD_D, strokeWidth=38, cap="round")
d.shape("ellipse", "Glove palm L", x=62, y=478, width=84, height=64, fill="#FFFFFF", stroke=INK, strokeWidth=4)
for i, (x, y, h) in enumerate([(66, 448, 34), (94, 440, 38), (122, 448, 34)]):
    d.shape("ellipse", f"Finger L{i+1}", x=x, y=y, width=22, height=h, fill="#FFFFFF", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Thumb L", x=126, y=498, width=32, height=22, fill="#FFFFFF", stroke=INK, strokeWidth=3)
d.path("M678,668 C736,678 758,716 748,758", "Arm R", fill=NONE, stroke=WOOD_D, strokeWidth=38, cap="round")
d.shape("ellipse", "Glove R", x=700, y=742, width=66, height=78, fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Thumb R", x=690, y=766, width=26, height=32, fill="#FFFFFF", stroke=INK, strokeWidth=3)

# polka-dot bowtie
d.path("M446,905 L374,870 C350,858 336,872 338,905 C336,938 350,952 374,940 L446,905 Z",
       "Bowtie L", fill="#F2668B", stroke=INK, strokeWidth=4)
d.path("M454,905 L526,870 C550,858 564,872 562,905 C564,938 550,952 526,940 L454,905 Z",
       "Bowtie R", fill="#F2668B", stroke=INK, strokeWidth=4)
for i, (x, y, c) in enumerate([(372, 896, "#FFD23F"), (392, 928, "#3FA7D6"), (356, 920, "#7BC950"),
                               (500, 896, "#3FA7D6"), (484, 928, "#FFD23F"), (522, 920, "#FF8C42")]):
    d.shape("ellipse", f"Bowtie dot {i+1}", x=x, y=y, width=17, height=17, fill=c, stroke=NONE)
d.shape("ellipse", "Bowtie knot", x=433, y=888, width=34, height=34, fill="#3FA7D6", stroke=INK, strokeWidth=4)

# post bolts last, on top
for i, (x, y) in enumerate([(243, 139), (635, 139), (243, 827), (635, 827)]):
    d.shape("ellipse", f"Post bolt {i+1}", x=x, y=y, width=22, height=22, fill=GOLD, stroke="#8A6420", strokeWidth=3)

d.finish("golly")

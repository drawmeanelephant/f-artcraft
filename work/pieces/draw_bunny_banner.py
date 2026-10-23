#!/usr/bin/env python3
"""Filed & Forgotten ERROR bunny — Twitter banner scene, 1500x500."""
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("ERROR Bunny — Banner", 1500, 500)

INK = "#38332A"; BUNNY = "#B3A88F"; RED = "#B03A2E"

# filing cabinets
d.shape("rectangle", "Cabinets", x=0, y=0, width=1500, height=500, fill="#76755F", stroke=NONE)
for col in range(4):
    for row in range(2):
        cx, cy = col * 375, row * 250
        d.shape("rectangle", f"Label {col}-{row}", x=cx + 132, y=cy + 56, width=110, height=44,
                radius=6, fill="#8F8C74", stroke="#4C4B38", strokeWidth=3)
        d.path(f"M{cx + 132},{cy + 148} L{cx + 242},{cy + 148}", f"Handle {col}-{row}",
               fill=NONE, stroke="#4C4B38", strokeWidth=10, cap="round")
for i, x in enumerate([375, 750, 1125]):
    d.shape("rectangle", f"Seam {i+1}", x=x - 3, y=0, width=6, height=500, fill="#55543F", stroke=NONE)
d.shape("rectangle", "Seam mid", x=0, y=247, width=1500, height=6, fill="#55543F", stroke=NONE)

# bunny, centre-right
d.path("M858,120 C852,60 862,20 885,12 C908,20 914,60 910,120 Z", "Ear L",
       fill=BUNNY, stroke=INK, strokeWidth=6)
d.path("M950,120 C944,60 954,20 977,12 C1000,20 1006,60 1002,120 Z", "Ear R",
       fill=BUNNY, stroke=INK, strokeWidth=6)
d.path("M870,108 C866,66 872,36 885,28 C898,36 902,66 900,108 Z", "Inner ear L", fill="#8F8672", stroke=NONE)
d.path("M962,108 C958,66 964,36 977,28 C990,36 994,66 992,108 Z", "Inner ear R", fill="#8F8672", stroke=NONE)
# body + belly + feet + tail
d.shape("ellipse", "Body", x=815, y=278, width=230, height=222, fill=BUNNY, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Belly", x=865, y=330, width=130, height=150, fill="#C4BBA3", stroke=NONE)
d.shape("ellipse", "Tail", x=1022, y=378, width=52, height=52, fill="#CFC6AC", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Foot L", x=812, y=462, width=88, height=30, fill=BUNNY, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Foot R", x=960, y=462, width=88, height=30, fill=BUNNY, stroke=INK, strokeWidth=5)
# head
d.shape("ellipse", "Head", x=825, y=95, width=210, height=180, fill=BUNNY, stroke=INK, strokeWidth=7)
d.path("M872,148 C884,136 904,134 916,142", "Brow L", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
d.path("M944,142 C956,134 976,136 988,148", "Brow R", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
d.shape("ellipse", "Eye L", x=890, y=158, width=30, height=44, fill="#26221C", stroke=NONE)
d.shape("ellipse", "Eye R", x=940, y=158, width=30, height=44, fill="#26221C", stroke=NONE)
d.path("M905,242 C918,230 942,230 955,242", "Frown", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
for lbl, dd in [("Whisker L1", "M776,196 L842,204"), ("Whisker L2", "M774,224 L840,226"),
                ("Whisker R1", "M1084,196 L1018,204"), ("Whisker R2", "M1086,224 L1020,226")]:
    d.path(dd, lbl, fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# arms to the papers
d.path("M848,332 C824,346 816,356 830,370", "Arm L", fill=NONE, stroke=BUNNY, strokeWidth=34, cap="round")
d.path("M1012,332 C998,350 984,360 962,364", "Arm R", fill=NONE, stroke=BUNNY, strokeWidth=34, cap="round")
# the dreaded paperwork
d.path(rot_rect_path(858, 362, 118, 148, -10), "Paper back", fill="#EDEAE0", stroke=INK, strokeWidth=4)
d.path(rot_rect_path(896, 352, 118, 148, 7), "Paper front", fill="#F4F1E6", stroke=INK, strokeWidth=4)
for i, (x, y, w) in enumerate([(862, 318, 62), (868, 344, 70), (874, 370, 58)]):
    d.path(f"M{x},{y} L{x + w},{y + 4}", f"Paper line {i+1}", fill=NONE, stroke="#9A958A", strokeWidth=5, cap="round")

# ERROR stamp, right
d.shape("rectangle", "Stamp box", x=1150, y=118, width=312, height=122, radius=14,
        fill=NONE, stroke=RED, strokeWidth=10)
d.shape("rectangle", "Stamp inner", x=1162, y=130, width=288, height=98, radius=8,
        fill=NONE, stroke=RED, strokeWidth=3)
d.text("ERROR", "Stamp text", x=1306, y=138, size=74, font="Source Sans 3",
       color=RED, justify="center")
doc = d.call("inspect_document", {"kind": "Type"}, "inspect type")
for n in (doc or {}).get("nodes", []):
    if str(n.get("name", "")).startswith("ERROR"):
        d.call("run_command", {"command": "text.setStyle",
               "params": {"id": n["id"], "style": "Bold"}}, "bold stamp")

d.finish("bunny-banner")

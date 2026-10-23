#!/usr/bin/env python3
"""ERROR bunny banner v2 — same scene, portrait-grade: gradients, shading, detail. 1500x500."""
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("ERROR Bunny — Banner v2", 1500, 500)

INK = "#38332A"
RED = "#B03A2E"

CAB_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E7D68"}, {"offset": 1, "color": "#61604A"}]}}
PLATE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9C9980"}, {"offset": 1, "color": "#82806A"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#BFB198"}, {"offset": 1, "color": "#A2987E"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2B69C"}, {"offset": 0.7, "color": "#B3A88F"}, {"offset": 1, "color": "#9C9077"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C0B49A"}, {"offset": 0.75, "color": "#AFa486"}, {"offset": 1, "color": "#989073"}]}}
BELLY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D5CBB1"}, {"offset": 1, "color": "#B4A991"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6F3E9"}, {"offset": 1, "color": "#DBD7C7"}]}}

# --- filing cabinets ---------------------------------------------------------
d.shape("rectangle", "Cabinets", x=0, y=0, width=1500, height=500, fill=CAB_GRAD, stroke=NONE)
for col in range(4):
    for row in range(2):
        cx, cy = col * 375, row * 250
        # subtle drawer shading: darker at the drawer bottom
        d.shape("rectangle", f"Drawer shade {col}-{row}", x=cx, y=cy + 190, width=375, height=60,
                fill="#4A4936", opacity=18, stroke=NONE)
        d.shape("rectangle", f"Label {col}-{row}", x=cx + 132, y=cy + 56, width=110, height=44,
                radius=6, fill=PLATE_GRAD, stroke="#4C4B38", strokeWidth=3)
        d.path(f"M{cx + 132},{cy + 148} L{cx + 242},{cy + 148}", f"Handle {col}-{row}",
               fill=NONE, stroke="#4C4B38", strokeWidth=10, cap="round")
for i, x in enumerate([375, 750, 1125]):
    d.shape("rectangle", f"Seam {i+1}", x=x - 3, y=0, width=6, height=500, fill="#55543F", stroke=NONE)
d.shape("rectangle", "Seam mid", x=0, y=247, width=1500, height=6, fill="#55543F", stroke=NONE)

# --- ground shadow under the bunny --------------------------------------------
d.shape("ellipse", "Ground shadow", x=796, y=470, width=268, height=34,
        fill="#333126", opacity=28, stroke=NONE)

# --- bunny --------------------------------------------------------------------
# ears (behind head), shaded
d.path("M858,120 C852,60 862,20 885,12 C908,20 914,60 910,120 Z", "Ear L",
       fill=EAR_GRAD, stroke=INK, strokeWidth=6)
d.path("M950,120 C944,60 954,20 977,12 C1000,20 1006,60 1002,120 Z", "Ear R",
       fill=EAR_GRAD, stroke=INK, strokeWidth=6)
d.path("M870,108 C866,66 872,36 885,28 C898,36 902,66 900,108 Z", "Inner ear L",
       fill="#8F8672", stroke=NONE)
d.path("M962,108 C958,66 964,36 977,28 C990,36 994,66 992,108 Z", "Inner ear R",
       fill="#8F8672", stroke=NONE)
d.path("M881,42 C887,70 889,94 888,114", "Ear shade L", fill=NONE, stroke="#8A7D63",
       strokeWidth=6, opacity=35)
d.path("M973,42 C979,70 981,94 980,114", "Ear shade R", fill=NONE, stroke="#8A7D63",
       strokeWidth=6, opacity=35)

# body, shaded, with gradient belly
d.shape("ellipse", "Body", x=815, y=278, width=230, height=222, fill=BODY_GRAD,
        stroke=INK, strokeWidth=7)
d.path("M1022,336 C1040,378 1040,430 1020,466", "Body shade R", fill=NONE,
       stroke="#857A5F", strokeWidth=12, opacity=32)
d.shape("ellipse", "Belly", x=865, y=330, width=130, height=150, fill=BELLY_GRAD, stroke=NONE)
d.shape("ellipse", "Tail", x=1022, y=378, width=52, height=52, fill="#CFC6AC",
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Foot L", x=812, y=462, width=88, height=30, fill=EAR_GRAD,
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Foot R", x=960, y=462, width=88, height=30, fill=EAR_GRAD,
        stroke=INK, strokeWidth=5)

# head: shaped path, radial gradient
d.path("M930,90 C1000.6,90 1045.9,137.4 1044.9,195.6 C1043.9,251.4 998,290 930,290 "
       "C862,290 816.1,251.4 815.1,195.6 C814.1,137.4 859.4,90 930,90 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Head highlight", x=850, y=102, width=120, height=44,
        fill="#FFFFFF", opacity=10, stroke=NONE)
d.shape("ellipse", "Cheek shade L", x=838, y=228, width=40, height=20,
        fill="#8F8672", opacity=28, stroke=NONE)
d.shape("ellipse", "Cheek shade R", x=982, y=228, width=40, height=20,
        fill="#8F8672", opacity=28, stroke=NONE)
d.path("M845,272 C885,292 975,292 1015,272 C975,284 885,284 845,272 Z", "Chin shadow",
       fill="#8F8672", opacity=32, stroke=NONE)

# face: worried brows, heavy-lidded tall eyes, wavy worried mouth
d.path("M868,156 C882,144 904,142 918,150", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=8, cap="round")
d.path("M942,150 C956,142 978,144 992,156", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=8, cap="round")
d.shape("ellipse", "Eye L", x=890, y=166, width=36, height=62, fill="#26221C", stroke=NONE)
d.shape("ellipse", "Eye R", x=934, y=166, width=36, height=62, fill="#26221C", stroke=NONE)
d.path("M886,192 C900,178 918,178 930,190", "Lid L", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
d.path("M930,190 C942,178 960,178 974,192", "Lid R", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
d.shape("ellipse", "Glint L", x=900, y=186, width=8, height=8, fill="#FFFFFF",
        opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=944, y=186, width=8, height=8, fill="#FFFFFF",
        opacity=85, stroke=NONE)
d.path("M902,244 C912,234 924,244 930,238 C936,244 948,234 958,244", "Worried mouth",
       fill=NONE, stroke=INK, strokeWidth=7, cap="round")
for lbl, dd in [("Whisker L1", "M786,196 C810,200 828,202 846,204"),
                ("Whisker L2", "M782,218 L848,220"),
                ("Whisker L3", "M788,240 C810,236 830,232 848,228"),
                ("Whisker R1", "M1074,196 C1050,200 1032,202 1014,204"),
                ("Whisker R2", "M1078,218 L1012,220"),
                ("Whisker R3", "M1072,240 C1050,236 1030,232 1012,228")]:
    d.path(dd, lbl, fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# arms to the papers
d.path("M848,332 C824,346 816,356 830,370", "Arm L", fill=NONE, stroke="#A79D83",
       strokeWidth=34, cap="round")
d.path("M1012,332 C998,350 984,360 962,364", "Arm R", fill=NONE, stroke="#A79D83",
       strokeWidth=34, cap="round")

# the dreaded paperwork
d.path(rot_rect_path(846, 368, 118, 148, -10), "Paper back", fill="#E9E5D8",
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Paper shadow", x=832, y=424, width=120, height=24,
        fill="#8F8672", opacity=35, stroke=NONE)
d.path(rot_rect_path(892, 356, 118, 148, 7), "Paper front", fill=PAPER_GRAD,
       stroke=INK, strokeWidth=4)
for i, (x, y, w) in enumerate([(858, 322, 64), (864, 348, 72), (870, 374, 60)]):
    d.path(f"M{x},{y} L{x + w},{y + 4}", f"Paper line {i+1}", fill=NONE,
           stroke="#9A958A", strokeWidth=5, cap="round")

# ERROR stamp, right — clean double box, faint second strike for distress
d.shape("rectangle", "Stamp box", x=1150, y=118, width=312, height=122, radius=14,
        fill=NONE, stroke=RED, strokeWidth=10)
d.shape("rectangle", "Stamp inner", x=1162, y=130, width=288, height=98, radius=8,
        fill=NONE, stroke=RED, strokeWidth=3)
d.text("ERROR", "Stamp echo", x=1308, y=140, size=74, font="Source Sans 3",
       color=RED, justify="center", opacity=22)
d.text("ERROR", "Stamp text", x=1306, y=138, size=74, font="Source Sans 3",
       color=RED, justify="center")
doc = d.call("inspect_document", {"kind": "Type"}, "inspect type")
for n in (doc or {}).get("nodes", []):
    nm = str(n.get("name", ""))
    if nm.startswith("Stamp"):
        d.call("run_command", {"command": "text.setStyle",
               "params": {"id": n["id"], "style": "Bold"}}, "bold stamp")

d.finish("bunny-banner-v2")

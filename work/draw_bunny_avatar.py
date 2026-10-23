#!/usr/bin/env python3
"""Filed & Forgotten ERROR bunny — Twitter profile badge, 1000x1000."""
import sys
sys.path.insert(0, "/home/hatch/workspace/vectorcraft/work")
from vc import Draw, NONE

d = Draw()
d.new_doc("ERROR Bunny — Profile Badge", 1000, 1000)

INK = "#38332A"; BUNNY = "#B3A88F"; SHADE = "#968B72"; INNER = "#8F8672"

# backdrop: dark square, aged-paper badge circle
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill="#2E2A24", stroke=NONE)
d.shape("ellipse", "Badge", x=30, y=30, width=940, height=940, fill="#D9C69C", stroke="#8A7648", strokeWidth=6)
d.shape("ellipse", "Badge inner ring", x=58, y=58, width=884, height=884, fill=NONE, stroke="#B39B6B", strokeWidth=3)
# aged speckles
for i, (x, y, w) in enumerate([(180,240,10),(820,200,8),(240,760,9),(790,720,11),(150,520,7),(860,480,8),
                               (330,140,7),(660,130,9),(420,880,8),(590,90,7),(110,350,8),(890,640,7)]):
    d.shape("ellipse", f"Age spot {i+1}", x=x, y=y, width=w, height=w, fill="#B39B6B", opacity=40, stroke=NONE)

# ears (behind head)
d.path("M402,392 C382,268 388,138 424,66 C438,40 462,40 474,68 C496,140 500,272 492,392 Z",
       "Ear L", fill=BUNNY, stroke=INK, strokeWidth=7)
d.path("M508,392 C500,272 504,140 526,68 C538,40 562,40 576,66 C612,138 618,268 598,392 Z",
       "Ear R", fill=BUNNY, stroke=INK, strokeWidth=7)
d.path("M424,360 C414,262 418,168 440,112 C449,92 463,94 470,116 C484,176 486,272 480,360 Z",
       "Inner ear L", fill=INNER, stroke=NONE)
d.path("M520,360 C514,272 516,176 530,116 C537,94 551,92 560,112 C582,168 586,262 576,360 Z",
       "Inner ear R", fill=INNER, stroke=NONE)

# head
d.shape("ellipse", "Head", x=285, y=330, width=430, height=400, fill=BUNNY, stroke=INK, strokeWidth=7)
# worried brows
d.path("M398,478 C416,460 448,456 468,468", "Brow L", fill=NONE, stroke=INK, strokeWidth=9, cap="round")
d.path("M532,468 C552,456 584,460 602,478", "Brow R", fill=NONE, stroke=INK, strokeWidth=9, cap="round")
# big sad eyes
d.shape("ellipse", "Eye L", x=422, y=492, width=46, height=66, fill="#26221C", stroke=NONE)
d.shape("ellipse", "Eye R", x=532, y=492, width=46, height=66, fill="#26221C", stroke=NONE)
# frown
d.path("M462,648 C480,632 520,632 538,648", "Frown", fill=NONE, stroke=INK, strokeWidth=8, cap="round")
# whiskers
for lbl, dd in [("Whisker L1", "M238,556 L330,566"), ("Whisker L2", "M232,592 L328,594"),
                ("Whisker L3", "M240,628 L332,612"), ("Whisker R1", "M762,556 L670,566"),
                ("Whisker R2", "M768,592 L672,594"), ("Whisker R3", "M760,628 L668,612")]:
    d.path(dd, lbl, fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# bowtie
d.path("M496,792 L414,748 C386,732 368,748 370,790 C368,832 386,848 414,832 L496,792 Z",
       "Bowtie L", fill="#26221C", stroke=NONE)
d.path("M504,792 L586,748 C614,732 632,748 630,790 C632,832 614,848 586,832 L504,792 Z",
       "Bowtie R", fill="#26221C", stroke=NONE)
d.shape("rectangle", "Bowtie knot", x=478, y=762, width=44, height=58, radius=12, fill="#38332A", stroke=NONE)

# ERROR wordmark
d.text("ERROR", "ERROR text", x=500, y=852, size=72, font="Source Sans 3",
       color="#4A3A28", justify="center")
doc = d.call("inspect_document", {"kind": "Type"}, "inspect type")
for n in (doc or {}).get("nodes", []):
    if str(n.get("name", "")).startswith("ERROR"):
        d.call("run_command", {"command": "text.setStyle",
               "params": {"id": n["id"], "style": "Bold"}}, "bold ERROR")

d.finish("bunny-avatar")

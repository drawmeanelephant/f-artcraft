#!/usr/bin/env python3
"""ERROR bunny avatar v2 — portrait-grade: gradients, shading, detail. 1000x1000."""
import sys
sys.path.insert(0, "/home/hatch/workspace/vectorcraft/work")
from vc import Draw, NONE

d = Draw()
d.new_doc("ERROR Bunny — Profile Badge v2", 1000, 1000)

INK = "#38332A"
BADGE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E7D5AB"}, {"offset": 0.72, "color": "#D9C69C"}, {"offset": 1, "color": "#C2A878"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2B69C"}, {"offset": 0.7, "color": "#B3A88F"}, {"offset": 1, "color": "#9C9077"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#BFB198"}, {"offset": 1, "color": "#A2987E"}]}}

# --- badge -------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill="#2B2721", stroke=NONE)
d.shape("ellipse", "Badge", x=30, y=30, width=940, height=940, fill=BADGE_GRAD, stroke="#8A7648", strokeWidth=6)
d.shape("ellipse", "Badge inner ring", x=58, y=58, width=884, height=884, fill=NONE, stroke="#B39B6B", strokeWidth=3)
# age: stains, a coffee ring, speckles
d.shape("ellipse", "Stain 1", x=120, y=620, width=300, height=190, fill="#A8874F", opacity=8, stroke=NONE)
d.shape("ellipse", "Stain 2", x=600, y=110, width=260, height=160, fill="#A8874F", opacity=8, stroke=NONE)
d.path("M212,318 A232,232 0 0 1 402,168", "Coffee ring", fill=NONE, stroke="#8A6A34", strokeWidth=7, opacity=18)
for i, (x, y, w) in enumerate([(180,240,10),(820,200,8),(240,760,9),(790,720,11),(150,520,7),(860,480,8),
                               (330,140,7),(660,130,9),(420,880,8),(590,90,7),(110,350,8),(890,640,7),
                               (205,430,6),(795,330,6),(300,860,6),(700,855,7)]):
    d.shape("ellipse", f"Age spot {i+1}", x=x, y=y, width=w, height=w, fill="#A8874F", opacity=45, stroke=NONE)

# --- ears: left straight, right leaning, both shaded ---------------------------
d.path("M398,402 C378,262 384,122 420,50 C434,20 462,18 476,48 C500,122 506,266 496,402 Z",
       "Ear L", fill=EAR_GRAD, stroke=INK, strokeWidth=7)
d.path("M508,402 C506,272 522,132 564,54 C582,22 610,24 618,54 C630,132 622,274 598,402 Z",
       "Ear R", fill=EAR_GRAD, stroke=INK, strokeWidth=7)
d.path("M424,368 C414,264 418,168 440,110 C449,88 464,90 471,114 C485,176 487,274 481,368 Z",
       "Inner ear L", fill="#8F8672", stroke=NONE)
d.path("M534,368 C530,272 538,172 562,112 C572,88 587,90 592,116 C602,178 600,276 590,368 Z",
       "Inner ear R", fill="#8F8672", stroke=NONE)
d.path("M470,70 C488,150 492,260 488,380", "Ear shade L", fill=NONE, stroke="#8A7D63", strokeWidth=10, opacity=35)
d.path("M596,84 C612,160 610,280 600,382", "Ear shade R", fill=NONE, stroke="#8A7D63", strokeWidth=10, opacity=35)

# --- head: shaped path, radial gradient -----------------------------------------
d.path("M500,318 C640,318 730,420 728,545 C726,665 635,748 500,748 C365,748 274,665 272,545 "
       "C270,420 360,318 500,318 Z", "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=8)
# fur tufts between the ears
d.path("M452,326 L470,296 L486,322 L502,294 L516,320", "Fur tuft", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# cheek shading + chin shadow
d.shape("ellipse", "Cheek shade L", x=300, y=596, width=64, height=32, fill="#8F8672", opacity=30, stroke=NONE)
d.shape("ellipse", "Cheek shade R", x=636, y=596, width=64, height=32, fill="#8F8672", opacity=30, stroke=NONE)
d.path("M336,688 C404,736 596,736 664,688 C596,712 404,712 336,688 Z", "Chin shadow",
       fill="#8F8672", opacity=35, stroke=NONE)
# head top highlight
d.shape("ellipse", "Head highlight", x=360, y=340, width=280, height=90, fill="#FFFFFF", opacity=10, stroke=NONE)

# --- face: heavy lids, tall eyes, wavy worried mouth ------------------------------
d.path("M382,464 C410,436 452,430 484,448", "Brow L", fill=NONE, stroke=INK, strokeWidth=11, cap="round")
d.path("M516,448 C548,430 590,436 618,464", "Brow R", fill=NONE, stroke=INK, strokeWidth=11, cap="round")
d.shape("ellipse", "Eye L", x=406, y=502, width=54, height=90, fill="#26221C", stroke=NONE)
d.shape("ellipse", "Eye R", x=540, y=502, width=54, height=90, fill="#26221C", stroke=NONE)
d.path("M402,528 C426,508 458,508 478,526", "Lid L", fill=NONE, stroke=INK, strokeWidth=9, cap="round")
d.path("M522,526 C542,508 574,508 598,528", "Lid R", fill=NONE, stroke=INK, strokeWidth=9, cap="round")
d.shape("ellipse", "Glint L", x=418, y=522, width=8, height=8, fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=552, y=522, width=8, height=8, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M452,656 C468,640 486,654 500,644 C514,654 532,640 548,656", "Worried mouth",
       fill=NONE, stroke=INK, strokeWidth=9, cap="round")
# whiskers, slightly curved
for lbl, dd in [("Whisker L1", "M246,556 C290,562 320,566 348,570"), ("Whisker L2", "M240,594 L344,598"),
                ("Whisker L3", "M248,632 C292,624 320,618 346,612"), ("Whisker R1", "M754,556 C710,562 680,566 652,570"),
                ("Whisker R2", "M760,594 L656,598"), ("Whisker R3", "M752,632 C708,624 680,618 654,612")]:
    d.path(dd, lbl, fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# --- bowtie: bigger, shaded, highlight stitch --------------------------------------
d.path("M494,802 L388,742 C352,722 330,746 334,798 C330,850 352,874 388,854 L494,802 Z",
       "Bowtie L", fill="#23201B", stroke=NONE)
d.path("M506,802 L612,742 C648,722 670,746 666,798 C670,850 648,874 612,854 L506,802 Z",
       "Bowtie R", fill="#23201B", stroke=NONE)
d.path("M352,758 C380,748 420,756 452,772", "Bowtie sheen L", fill=NONE, stroke="#5A544C", strokeWidth=6, opacity=70, cap="round")
d.path("M548,772 C580,756 620,748 648,758", "Bowtie sheen R", fill=NONE, stroke="#5A544C", strokeWidth=6, opacity=70, cap="round")
d.shape("rectangle", "Bowtie knot", x=470, y=766, width=60, height=68, radius=14, fill="#322E28", stroke=NONE)
d.path("M484,778 L484,822", "Knot crease", fill=NONE, stroke="#191713", strokeWidth=5, cap="round")
d.path("M516,778 L516,822", "Knot crease 2", fill=NONE, stroke="#191713", strokeWidth=5, cap="round")

# --- ERROR --------------------------------------------------------------------------
d.text("ERROR", "ERROR text", x=500, y=948, size=80, font="Source Sans 3",
       color="#43331F", justify="center")
doc = d.call("inspect_document", {"kind": "Type"}, "inspect type")
for n in (doc or {}).get("nodes", []):
    if str(n.get("name", "")).startswith("ERROR"):
        d.call("run_command", {"command": "text.setStyle",
               "params": {"id": n["id"], "style": "Bold"}}, "bold ERROR")

d.finish("bunny-avatar-v2")

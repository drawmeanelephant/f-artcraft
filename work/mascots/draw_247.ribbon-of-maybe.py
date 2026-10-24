#!/usr/bin/env python3
"""Ribbon of Maybe — mascot portrait V1R00.
A ribbon mascot already knotted into a silk bow around an open, empty box —
the knot does not check contents — ceremonial shears waiting on the floor
beside it. 1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ribbon of Maybe — Mascot Portrait", 1000, 1000)

INK = "#33222C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#261620"}, {"offset": 1, "color": "#100A12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A6E78"}, {"offset": 0.7, "color": "#5E4652"},
    {"offset": 1, "color": "#2E2129"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4C3A46"}, {"offset": 1, "color": "#231A22"}]}}
BOX_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9AE84"}, {"offset": 1, "color": "#8A6E4E"}]}}
BOX_SIDE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A7E5C"}, {"offset": 1, "color": "#6A5238"}]}}
FLAP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B89870"}, {"offset": 1, "color": "#7C6044"}]}}
SILK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E88CA4"}, {"offset": 0.55, "color": "#C25A78"},
    {"offset": 1, "color": "#8E3A54"}]}}
SILK_DARK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A84A66"}, {"offset": 1, "color": "#6E2A40"}]}}
STEEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8DDE2"}, {"offset": 1, "color": "#8E969E"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4C47A"}, {"offset": 1, "color": "#9A7434"}]}}
GLOOM = "#1A1018"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#96788A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D4E0", strokeWidth=3, opacity=50)
# ceremonial glow: the spotlight an occasion leaves behind
d.shape("ellipse", "Glow", x=195, y=130, width=610, height=540,
        fill="#F4D8E4", opacity=9, stroke=NONE)
for i, (x, y, w) in enumerate([(190,230,8),(804,232,7),(158,516,9),(836,540,8),
                               (252,764,7),(750,746,9),(134,388,6),(864,390,7),
                               (394,112,7),(612,110,8),(334,820,6),(668,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A5464", opacity=45, stroke=NONE)
# expectant motes: the atmosphere of something about to be announced
for i, (x, y, w) in enumerate([(268,300,7),(742,286,9),(318,196,5),(688,190,6),
                               (500,168,5),(224,420,6),(778,430,7)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0CADC", opacity=30, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#160F16",
       strokeWidth=4, opacity=70)

# --- the empty box -------------------------------------------------------------
d.shape("ellipse", "Box shadow", x=330, y=682, width=370, height=28,
        fill="#0E0810", opacity=50, stroke=NONE)
# open flaps first: wide panels hinged on the front edge, splayed past the bow
d.path("M366,505 L436,505 L368,392 L296,392 Z", "Flap L",
       fill=FLAP_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M296,392 L368,392", "Flap L flute", fill=NONE, stroke="#6A5238",
       strokeWidth=4, opacity=80)
d.path("M564,505 L634,505 L704,392 L632,392 Z", "Flap R",
       fill=FLAP_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M632,392 L704,392", "Flap R flute", fill=NONE, stroke="#6A5238",
       strokeWidth=4, opacity=80)
# interior: a held space, not a missing lid
d.path("M382,470 L618,470 L668,480 L640,505 L360,505 Z", "Box interior",
       fill=GLOOM, stroke=INK, strokeWidth=4, join="round")
d.path("M394,478 L606,478 L640,484 L622,498 L376,498 Z", "Interior gloom",
       fill="#0C060C", stroke=NONE, opacity=80)
# front + side faces
d.path("M360,505 L640,505 L640,700 L360,700 Z", "Box front",
       fill=BOX_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M640,505 L676,482 L676,676 L640,700 Z", "Box side",
       fill=BOX_SIDE, stroke=INK, strokeWidth=5, join="round")
# corrugated edge along the top of the front face
d.path("M360,505 L640,505 L640,518 L360,518 Z", "Front lip",
       fill="#A8896A", stroke=INK, strokeWidth=3, opacity=85)
# manifest label: still blank, placed clear of both bands
d.path("M382,540 L452,540 L452,586 L382,586 Z", "Blank label",
       fill="#E8DCC4", stroke=INK, strokeWidth=3, opacity=90)
d.path("M391,552 L443,552 M391,564 L431,564 M391,576 L439,576",
       "Label lines", fill=NONE, stroke="#B8A88E", strokeWidth=3,
       cap="round", opacity=60)

# --- the ribbon: wrapped, knotted, undecided ------------------------------------
# vertical band down the front
d.path("M474,518 L534,518 L534,700 L474,700 Z", "Band V",
       fill=SILK_DARK, stroke=INK, strokeWidth=4)
d.path("M474,518 L474,700", "Band V edge", fill=NONE, stroke="#5E2438",
       strokeWidth=3, opacity=70)
# horizontal band around the middle
d.path("M360,592 L640,592 L640,632 L360,632 Z", "Band H",
       fill=SILK_GRAD, stroke=INK, strokeWidth=4)
d.path("M372,602 L628,602", "Band H sheen", fill=NONE, stroke="#F4B8C8",
       strokeWidth=4, cap="round", opacity=55)
# tails: spilling from the knot down the front, ends cut on the bias
d.path("M486,468 C464,516 456,556 460,602 L492,608 L478,636 C448,580 452,516 474,462 Z",
       "Tail L", fill=SILK_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M520,466 C546,514 554,554 548,604 L516,612 L532,640 C562,582 556,514 532,460 Z",
       "Tail R", fill=SILK_DARK, stroke=INK, strokeWidth=4, join="round")
# bow loops: the bow centered, the way it is tied every time
d.path("M500,444 C418,396 348,404 338,456 C332,500 396,516 450,496 "
       "C472,487 490,466 500,444 Z",
       "Loop L", fill=SILK_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M504,444 C586,396 656,404 666,456 C672,500 608,516 554,496 "
       "C532,487 514,466 504,444 Z",
       "Loop R", fill=SILK_GRAD, stroke=INK, strokeWidth=5, join="round")
# loop creases + sheen
d.path("M490,448 C442,424 394,430 376,454", "Loop L fold", fill=NONE,
       stroke="#7E2E48", strokeWidth=4, cap="round", opacity=70)
d.path("M514,448 C562,424 610,430 628,454", "Loop R fold", fill=NONE,
       stroke="#7E2E48", strokeWidth=4, cap="round", opacity=70)
d.path("M388,448 C414,430 452,428 480,440", "Loop L sheen", fill=NONE,
       stroke="#F8C8D4", strokeWidth=5, cap="round", opacity=60)
d.path("M524,440 C552,428 590,430 616,448", "Loop R sheen", fill=NONE,
       stroke="#F8C8D4", strokeWidth=5, cap="round", opacity=60)

# --- the knot: the mascot's face, tied before there was anything to tie to ------
d.path("M460,424 C460,398 480,384 502,384 C524,384 544,398 544,424 "
       "C544,450 524,462 502,462 C480,462 460,450 460,424 Z",
       "Knot", fill=SILK_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Knot hi", x=474, y=394, width=32, height=17,
        fill="#FFFFFF", opacity=30, stroke=NONE)
# eyes: bright, ceremonially certain
d.shape("ellipse", "Eye L", x=477, y=414, width=15, height=19,
        fill="#FFF6F8", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye R", x=506, y=414, width=15, height=19,
        fill="#FFF6F8", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil L", x=482, y=420, width=7, height=9,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=511, y=420, width=7, height=9,
        fill=INK, stroke=NONE)
# hopeful mouth: enthusiasm slightly ahead of event status
d.path("M487,444 C494,451 510,451 517,444", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Cheek L", x=462, y=434, width=17, height=9,
        fill="#F4A0B4", opacity=50, stroke=NONE)
d.shape("ellipse", "Cheek R", x=526, y=434, width=17, height=9,
        fill="#F4A0B4", opacity=50, stroke=NONE)

# --- the ceremonial shears: real, occasion pending ------------------------------
d.shape("ellipse", "Shears shadow", x=662, y=678, width=200, height=17,
        fill="#0E0810", opacity=45, stroke=NONE)
# blades crossed, tips open toward the box
d.path("M714,666 L842,634 L850,646 L718,682 Z", "Blade T",
       fill=STEEL, stroke=INK, strokeWidth=4, join="round")
d.path("M720,642 L846,680 L838,692 L712,658 Z", "Blade B",
       fill=STEEL, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Pivot", x=710, y=656, width=17, height=17,
        fill=BRASS, stroke=INK, strokeWidth=3)
# brass finger loops
d.shape("ellipse", "Loop T", x=646, y=634, width=48, height=32,
        fill=NONE, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Loop T in", x=646, y=634, width=48, height=32,
        fill=NONE, stroke="#C9A45C", strokeWidth=9, opacity=70)
d.shape("ellipse", "Loop B", x=642, y=670, width=50, height=32,
        fill=NONE, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Loop B in", x=642, y=670, width=50, height=32,
        fill=NONE, stroke="#C9A45C", strokeWidth=9, opacity=70)
d.path("M694,652 L712,660 M692,678 L712,668", "Shanks", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# a waiting gleam on the top blade
d.path("M742,660 L810,642", "Blade gleam", fill=NONE, stroke="#FFFFFF",
       strokeWidth=3, cap="round", opacity=60)

# --- captions -------------------------------------------------------------------
d.text("RIBBON OF MAYBE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#F0D8E4", justify="center")
r = d.text("DECORATED INDETERMINACY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B89CAE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("247.ribbon-of-maybe-V1R00")

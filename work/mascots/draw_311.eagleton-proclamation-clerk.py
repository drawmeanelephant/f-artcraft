#!/usr/bin/env python3
"""Eagleton Proclamation Clerk — mascot portrait V1R00.
He does not invent policy; he notices what the room was already kneeling to.
A dust-covered banner mid-unroll above the ledger, the phrase transcribed
in green ink, the years of dust noted first. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Eagleton Proclamation Clerk — Mascot Portrait", 1000, 1000)

INK = "#2E1E12"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E1410"}, {"offset": 1, "color": "#0F0A07"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8F7350"}, {"offset": 0.7, "color": "#5C452E"},
    {"offset": 1, "color": "#33241A"}]}}
CLOTH_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8E3430"}, {"offset": 1, "color": "#552022"}]}}
ROLL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A2C2A"}, {"offset": 1, "color": "#401A1A"}]}}
ROBE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#52453A"}, {"offset": 0.75, "color": "#372D24"},
    {"offset": 1, "color": "#221B15"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4BE90"}, {"offset": 0.72, "color": "#C4976A"},
    {"offset": 1, "color": "#96683F"}]}}
VISOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E8A5C"}, {"offset": 1, "color": "#265238"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E6C6"}, {"offset": 1, "color": "#C9B78E"}]}}
GREEN = "#2E6B46"
GREEN_LT = "#4E8A62"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A5E42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D9C096", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(206,240,8),(792,236,7),(168,540,9),(830,556,8),
                               (256,760,7),(744,748,9),(146,402,6),(854,398,7),
                               (402,120,7),(606,116,8),(340,820,6),(660,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#57402C", opacity=45, stroke=NONE)

# --- the banner, mid-unroll: left half open, right end still a fat roll --------
# cloth: top edge sagging gently, hem sagging deeper, hem tacked to the disc arc
d.path("M258,196 C400,214 560,214 742,192 L736,296 C560,318 420,318 264,298 Z",
       "Banner cloth", fill=CLOTH_GRAD, stroke=INK, strokeWidth=5,
       join="round")
# cloth shading: dust film over the whole panel + fold shadows
d.path("M258,196 C400,214 560,214 742,192 L740,226 C560,246 400,246 260,228 Z",
       "Dust film top", fill="#C9B088", opacity=28, stroke=NONE)
for fx in (360, 500, 640):
    d.path(f"M{fx},212 C{fx-6},244 {fx-4},272 {fx-8},302",
           f"Banner fold {fx}", fill=NONE, stroke="#3E1414",
           strokeWidth=4, opacity=40, cap="round")
# the recovered phrase, faded but legible — lettering the room obeyed for years
t = d.text("OBEY WHAT YOU KNOW", "Banner phrase", x=500, y=263, size=28,
           font="Virelai Sans", color="#E8D5A8", justify="center")
if t and t.get("id"):
    d.cmd("object.setProps", "phrase fade", ids=[t["id"]], opacity=80)
# dust settled heavier over the words at both ends
d.shape("ellipse", "Dust on phrase L", x=300, y=238, width=90, height=26,
        fill="#C9B088", opacity=30, stroke=NONE)
d.shape("ellipse", "Dust on phrase R", x=610, y=244, width=80, height=24,
        fill="#C9B088", opacity=26, stroke=NONE)
# speckles of basement weather across the cloth
for i, (x, y, w) in enumerate([(290,226,5),(430,236,4),(560,224,5),(700,216,4),
                               (340,286,4),(480,292,5),(640,284,4)]):
    d.shape("ellipse", f"Banner dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8C4A0", opacity=45, stroke=NONE)
# left roll: still fat — the unspooled part yet to be registered
d.path("M264,196 C258,240 258,278 262,306 C270,322 290,322 296,306 "
       "C302,278 300,236 296,192 Z", "Left roll", fill=ROLL_GRAD,
       stroke=INK, strokeWidth=5)
d.shape("ellipse", "Left roll end", x=252, y=180, width=50, height=24,
        fill="#5C2422", stroke=INK, strokeWidth=4)
# right roll: the end already unwound, hanging loose
d.path("M774,196 C778,240 774,280 768,306 C760,320 742,320 736,306 "
       "C730,280 732,236 736,196 Z", "Right roll", fill=ROLL_GRAD,
       stroke=INK, strokeWidth=5)
d.shape("ellipse", "Right roll end", x=734, y=184, width=42, height=20,
        fill="#5C2422", stroke=INK, strokeWidth=4)
# the loose tail the clerk is paying out — it ends in his raised fist
d.path("M288,306 C280,340 294,366 312,384", "Unroll tail", fill=NONE,
       stroke="#6B2A28", strokeWidth=14, cap="round")
# gold fringe along the hem, heritage hardware
for i, x in enumerate(range(288, 720, 54)):
    y = 302 + 10 * math.sin((x - 288) / 432 * math.pi)
    d.path(f"M{x},{y:.0f} L{x+4},{y+22:.0f}", f"Fringe {i+1}", fill=NONE,
           stroke="#C9A45C", strokeWidth=4, cap="round", opacity=85)

# --- the ledger, open on the desk, ruled in green ------------------------------
# desk edge: a dark mass the clerk works over, ending on the disc's own arc
d.path("M196,762 L804,762 L830,806 A420,420 0 0 1 170,806 Z", "Desk",
       fill="#2A1E14", stroke=INK, strokeWidth=5, join="round")
d.path("M196,762 L804,762", "Desk edge", fill=NONE, stroke="#8A6E4C",
       strokeWidth=4, opacity=60, cap="round")
# cover peeking past the pages
d.path("M404,668 L720,650 L732,772 L416,790 Z", "Ledger cover",
       fill="#4A3423", stroke=INK, strokeWidth=5, join="round")
# pages: two leaves parted at the gutter
d.path("M418,662 L566,676 L562,768 L414,752 Z", "Page left",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M566,676 L712,660 L722,748 L562,768 Z", "Page right",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M566,676 L562,768", "Gutter", fill=NONE, stroke="#8A7A5C",
       strokeWidth=3, opacity=80)
# green ruling + entries already on file
for i, t in enumerate([0.15, 0.35, 0.55, 0.75]):
    y0 = 686 + i * 16
    d.path(f"M428,{y0} L552,{y0+10}", f"Rule L{i+1}", fill=NONE,
           stroke=GREEN_LT, strokeWidth=2, opacity=60)
for i, t in enumerate([0.15, 0.35, 0.55, 0.75]):
    y0 = 680 + i * 16
    d.path(f"M576,{y0+8} L700,{y0-6}", f"Rule R{i+1}", fill=NONE,
           stroke=GREEN_LT, strokeWidth=2, opacity=60)
# the intake order: years of dust noted first, phrase second, obedience third
d.text("RECOVERED", "Ledger entry", x=672, y=692, size=13,
       font="Virelai Sans", color=GREEN, justify="center")
d.path("M426,716 C450,708 480,714 504,706 C520,702 534,708 546,704",
       "Dust-note line", fill=NONE, stroke=GREEN, strokeWidth=2.5,
       cap="round", opacity=80)
# ink pot at the ledger's left, green to the brim
d.shape("ellipse", "Ink pot shadow", x=294, y=742, width=56, height=14,
        fill="#140C08", opacity=50, stroke=NONE)
d.path("M304,700 L336,700 L340,742 L300,742 Z", "Ink pot",
       fill="#241A12", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Ink surface", x=304, y=694, width=32, height=12,
        fill=GREEN, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Ink glint", x=310, y=697, width=8, height=4,
        fill="#8AC49C", opacity=80, stroke=NONE)

# --- the clerk: robed, visored, mid-transcription -------------------------------
# robe: a seated bell of administrative gravity
d.path("M402,760 C392,690 396,626 428,590 C452,564 546,564 572,590 "
       "C606,624 612,690 604,760 Z", "Robe", fill=ROBE_GRAD,
       stroke=INK, strokeWidth=5, join="round")
# robe shading: lapel light, skirt shadow
d.shape("ellipse", "Robe light", x=430, y=586, width=90, height=60,
        fill="#7A6A54", opacity=35, stroke=NONE)
# collar: the white of the office, still clean
d.path("M466,586 L500,622 L534,586 L520,574 L500,592 L480,574 Z",
       "Collar", fill="#EFE6D2", stroke=INK, strokeWidth=3.5,
       join="round")
# buttons down the placket
for i, y in enumerate([640, 676, 712]):
    d.shape("ellipse", f"Button {i+1}", x=493, y=y, width=12, height=12,
            fill="#C9A45C", stroke=INK, strokeWidth=2.5)
# head
d.shape("ellipse", "Head", x=432, y=418, width=136, height=124,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
# ears
for ex in (430, 570):
    d.shape("ellipse", f"Ear {ex}", x=ex - 10, y=478, width=20, height=24,
            fill="#C4976A", stroke=INK, strokeWidth=3.5)
# the green eyeshade: a translucent band the audit permitted
d.path("M424,462 C452,450 548,450 576,462 L576,492 C548,480 452,480 424,492 Z",
       "Eyeshade", fill=VISOR_GRAD, stroke=INK, strokeWidth=4,
       join="round", opacity=85)
d.path("M424,468 C400,462 392,470 388,478", "Eyeshade strap L",
       fill=NONE, stroke="#265238", strokeWidth=5, cap="round")
d.path("M576,468 C596,464 604,470 608,478", "Eyeshade strap R",
       fill=NONE, stroke="#265238", strokeWidth=5, cap="round")
# eyes below the shade, mild and certain
d.shape("ellipse", "Eye L", x=470, y=498, width=13, height=16,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=517, y=498, width=13, height=16,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=473, y=501, width=4, height=4,
        fill="#FFF6E4", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=520, y=501, width=4, height=4,
        fill="#FFF6E4", opacity=85, stroke=NONE)
# pince-nez riding low on the nose
d.shape("ellipse", "Lens L", x=462, y=508, width=28, height=22,
        fill=NONE, stroke="#C9A45C", strokeWidth=3)
d.shape("ellipse", "Lens R", x=510, y=508, width=28, height=22,
        fill=NONE, stroke="#C9A45C", strokeWidth=3)
d.path("M490,518 L510,518", "Spec bridge", fill=NONE, stroke="#C9A45C",
       strokeWidth=3, cap="round")
# the clerk's mouth: neither approval nor doubt — transcription
d.path("M484,540 C496,545 508,545 518,540", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# --- right arm raised, paying out the roll --------------------------------------
d.path("M434,596 C390,530 350,460 320,394", "Sleeve raised",
       fill=NONE, stroke="#372D24", strokeWidth=26, cap="round")
d.shape("ellipse", "Cuff raised", x=310, y=384, width=26, height=22,
        fill="#EFE6D2", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Hand on tail", x=300, y=366, width=34, height=30,
        fill="#E4BE90", stroke=INK, strokeWidth=4)
# dust sifted loose where his grip works the roll
for i, (x, y, w) in enumerate([(326,404,6),(305,428,5),(336,442,4),(295,452,5)]):
    d.shape("ellipse", f"Fresh dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8C4A0", opacity=50, stroke=NONE)

# --- left arm to the open page, pen in green ------------------------------------
d.path("M566,616 C600,660 624,690 634,712", "Sleeve writing",
       fill=NONE, stroke="#372D24", strokeWidth=26, cap="round")
d.shape("ellipse", "Cuff writing", x=622, y=694, width=24, height=20,
        fill="#EFE6D2", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Writing hand", x=622, y=700, width=34, height=28,
        fill="#E4BE90", stroke=INK, strokeWidth=4)
# the pen: nib down to the rule line
d.path("M648,706 L622,734", "Pen shaft", fill=NONE, stroke="#1E4A30",
       strokeWidth=6, cap="round")
d.path("M622,734 L612,744 L626,746 Z", "Pen nib", fill="#C9A45C",
       stroke=INK, strokeWidth=2.5, join="round")
# wet green where the nib just passed
d.path("M588,748 C600,744 612,748 622,744", "Fresh ink", fill=NONE,
       stroke=GREEN, strokeWidth=3, cap="round")

# --- dust drifting down over everything: the parliamentary weather ---------------
for i, (x, y, w) in enumerate([(300,340,5),(380,380,4),(540,350,5),(620,400,4),
                               (330,470,4),(580,470,5),(260,430,5),(500,390,4),
                               (700,500,4),(420,540,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8C4A0", opacity=32, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("EAGLETON PROCLAMATION CLERK", "Name", x=500, y=930, size=48,
       font="Virelai Sans", color="#EBDCBE", justify="center")
r = d.text("BANNER PHRASE REGISTRAR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C4A87C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("311.eagleton-proclamation-clerk-V1R00")

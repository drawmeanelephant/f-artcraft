#!/usr/bin/env python3
"""Pump Razorbackfuel — mascot portrait V1R00.
Boar-like mascot stamping fuel receipts with a hoof at a rural gas
station under neon. 1000x1000. House style: gradients + translucent
shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pump Razorbackfuel — Mascot Portrait", 1000, 1000)

INK = "#2A1E22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1618"}, {"offset": 1, "color": "#050B0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E4E4C"}, {"offset": 0.7, "color": "#1C3232"},
    {"offset": 1, "color": "#101E1E"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D89A78"}, {"offset": 0.68, "color": "#A86A50"},
    {"offset": 1, "color": "#7C4A38"}]}}
SNOUT = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0BC9C"}, {"offset": 1, "color": "#C98A6E"}]}}
PUMP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A6662"}, {"offset": 1, "color": "#2A3E3C"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A4A34"}, {"offset": 1, "color": "#453023"}]}}
DIAL = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E8CE"}, {"offset": 1, "color": "#C9A888"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#E87EA0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8D8D0", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E5E58", opacity=45, stroke=NONE)

# --- neon sign, upper left ------------------------------------------------------
d.path("M212,700 L212,330", "Sign pole", fill=NONE, stroke=INK,
       strokeWidth=9, cap="round")
d.path("M212,340 L300,340", "Sign arm", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
d.shape("ellipse", "Neon halo", x=118, y=270, width=260, height=150,
        fill="#FF7EA8", opacity=14, stroke=NONE)
d.shape("rectangle", "Sign panel", x=160, y=296, width=176, height=76,
        fill="#141C20", stroke=INK, strokeWidth=5, radius=12)
d.text("FUEL", "Neon word", x=248, y=352, size=44, font="Virelai Sans",
       color="#FFA8C4", justify="center")
d.shape("rectangle", "Neon underline", x=178, y=360, width=140, height=5,
        fill="#FF7EA8", opacity=85, stroke=NONE, radius=2)
# one flickered-out segment
d.shape("rectangle", "Flicker gap", x=238, y=360, width=16, height=5,
        fill="#141C20", stroke=NONE)

# --- ground ----------------------------------------------------------------------
d.shape("ellipse", "Ground shadow", x=220, y=700, width=580, height=64,
        fill="#040A0A", opacity=60, stroke=NONE)
d.shape("ellipse", "Neon puddle pink", x=180, y=712, width=220, height=26,
        fill="#FF7EA8", opacity=13, stroke=NONE)
d.shape("ellipse", "Neon puddle teal", x=560, y=724, width=240, height=24,
        fill="#7EDCCB", opacity=10, stroke=NONE)

# --- vintage pump, right ----------------------------------------------------------
d.shape("ellipse", "Pump shadow", x=692, y=706, width=150, height=24,
        fill="#040A0A", opacity=55, stroke=NONE)
d.path("M712,480 C712,458 730,446 758,446 C786,446 804,458 804,480 L804,700 L712,700 Z",
       "Pump body", fill=PUMP, stroke=INK, strokeWidth=6, join="round")
d.shape("ellipse", "Pump dial", x=730, y=486, width=56, height=56,
        fill=DIAL, stroke=INK, strokeWidth=5)
d.path("M758,514 L772,500", "Dial needle", fill=NONE, stroke="#B4543C",
       strokeWidth=4, cap="round")
d.shape("rectangle", "Pump window", x=724, y=560, width=68, height=44,
        fill="#1A2624", stroke=INK, strokeWidth=4, radius=6)
d.text("29¢", "Price", x=758, y=590, size=20, font="Virelai Sans",
       color="#E8D8A8", justify="center")
d.path("M712,640 L804,640", "Pump belt", fill=NONE, stroke=INK,
       strokeWidth=4, opacity=60)
# hose looping off the pump's right flank
d.path("M804,560 C846,566 850,620 826,646 C812,660 800,656 796,644",
       "Fuel hose", fill=NONE, stroke="#1E2E2C", strokeWidth=10, cap="round")
d.path("M796,644 L786,668", "Nozzle", fill=NONE, stroke=INK,
       strokeWidth=8, cap="round")

# --- crate counter with receipts ---------------------------------------------------
d.path("M630,616 L812,606 L820,724 L640,730 Z", "Crate",
       fill=WOOD, stroke=INK, strokeWidth=6, join="round")
d.path("M636,656 L816,648 M640,692 L818,686", "Plank lines", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=55)
# receipt on the crate top, being stamped
d.path("M632,600 L722,594 L728,626 L638,632 Z", "Receipt top",
       fill="#F2ECDC", stroke=INK, strokeWidth=4, join="round")
for i, (x0, x1) in enumerate([(644,682),(646,700),(648,668)]):
    d.path(f"M{x0},{608+i*6} L{x1},{606+i*6}", f"Receipt line {i+1}",
           fill=NONE, stroke="#8A8078", strokeWidth=3, opacity=80)
# stamp, pressed by the hoof
d.path("M664,552 L688,552 L684,578 L668,578 Z", "Stamp handle",
       fill="#B4543C", stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Stamp base", x=656, y=578, width=40, height=16,
        fill=INK, stroke=NONE, radius=3)
# fluttering receipts
d.path("M640,486 L692,478 L698,504 L646,512 Z", "Receipt fly 1",
       fill="#F2ECDC", stroke=INK, strokeWidth=3, opacity=95, join="round")
d.path("M652,492 L682,488 M654,500 L684,496", "Fly lines 1", fill=NONE,
       stroke="#8A8078", strokeWidth=2, opacity=70)
d.path("M806,632 L848,624 L854,646 L812,654 Z", "Receipt fly 2",
       fill="#F2ECDC", stroke=INK, strokeWidth=3, opacity=90, join="round")
d.path("M816,638 L842,634 M818,646 L844,642", "Fly lines 2", fill=NONE,
       stroke="#8A8078", strokeWidth=2, opacity=70)

# --- the boar ------------------------------------------------------------------------
d.shape("ellipse", "Boar shadow", x=300, y=700, width=280, height=40,
        fill="#040A0A", opacity=55, stroke=NONE)
# rear legs
d.shape("rectangle", "Hind leg", x=330, y=640, width=52, height=80,
        fill="#8A5442", stroke=INK, strokeWidth=5, radius=12)
d.shape("rectangle", "Hind hoof", x=328, y=706, width=56, height=22,
        fill=INK, stroke=NONE, radius=8)
d.shape("rectangle", "Mid leg", x=430, y=650, width=50, height=72,
        fill="#96604A", stroke=INK, strokeWidth=5, radius=12)
d.shape("rectangle", "Mid hoof", x=428, y=708, width=54, height=20,
        fill=INK, stroke=NONE, radius=8)
# body
d.shape("ellipse", "Body", x=296, y=420, width=300, height=280,
        fill=BODY, stroke=INK, strokeWidth=6)
# razorback bristle ridge along the spine
d.path("M312,500 L330,452 L346,486 L366,440 L384,476 L406,434 L424,470 "
       "L448,430 L466,466 L490,430 L506,462",
       "Bristle ridge", fill=NONE, stroke="#5A3428", strokeWidth=10,
       cap="round", join="round")
d.path("M312,500 L330,452 L346,486 L366,440 L384,476 L406,434 L424,470 "
       "L448,430 L466,466 L490,430 L506,462",
       "Bristle tips", fill=NONE, stroke=INK, strokeWidth=3,
       cap="round", join="round", opacity=70)
# curly tail
d.path("M300,560 C282,556 274,540 282,528 C288,520 298,522 298,531",
       "Tail", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
# ear
d.path("M506,420 C512,392 534,378 552,384 C548,410 534,426 514,430 Z",
       "Ear", fill="#96604A", stroke=INK, strokeWidth=5, join="round")
# snout
d.shape("ellipse", "Snout", x=566, y=500, width=92, height=72,
        fill=SNOUT, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Nostril L", x=592, y=524, width=12, height=16,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Nostril R", x=622, y=522, width=12, height=16,
        fill=INK, stroke=NONE)
# tusk
d.path("M576,566 C570,548 576,534 590,528 C586,544 588,556 596,564 Z",
       "Tusk", fill="#F2E4C8", stroke=INK, strokeWidth=4, join="round")
# grin under the snout
d.path("M580,586 C600,598 630,596 646,582", "Grin", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# eye, boisterous
d.shape("ellipse", "Eye", x=540, y=466, width=20, height=24, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye glint", x=546, y=471, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M532,452 C544,444 560,444 570,452", "Brow", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=70)
# belly shading
d.shape("ellipse", "Belly shade", x=340, y=560, width=180, height=110,
        fill="#7C4A38", opacity=35, stroke=NONE)
# raised foreleg pressing the stamp
d.path("M560,590 C596,598 634,592 664,566", "Foreleg", fill=NONE,
       stroke="#A86A50", strokeWidth=34, cap="round")
d.path("M560,590 C596,598 634,592 664,566", "Foreleg seam", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=55, cap="round")
d.shape("ellipse", "Stamping hoof", x=650, y=540, width=36, height=26,
        fill=INK, stroke=NONE)

# --- neon light kisses ------------------------------------------------------------
d.shape("ellipse", "Neon kiss on back", x=330, y=436, width=120, height=60,
        fill="#FF7EA8", opacity=12, stroke=NONE)
d.shape("ellipse", "Teal kiss on snout", x=586, y=500, width=60, height=40,
        fill="#7EDCCB", opacity=12, stroke=NONE)
# drifting night bugs drawn to the neon
for i, (x, y, w) in enumerate([(140,420,4),(300,250,4),(360,300,5),(210,470,4)]):
    d.shape("ellipse", f"Moth {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFC4D8", opacity=55, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("PUMP RAZORBACKFUEL", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#EAF2EE", justify="center")
r = d.text("ROADSIDE RACONTEUR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8FC2BA", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("204.pump-razorbackfuel-V1R00")

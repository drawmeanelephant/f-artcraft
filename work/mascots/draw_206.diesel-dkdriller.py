#!/usr/bin/env python3
"""Diesel DKDriller — mascot portrait V1R00.
Mascot coated in spectral crude stamping diesel receipts at a fuel
pump. 1000x1000. House style: gradients + translucent shading,
never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Diesel DKDriller — Mascot Portrait", 1000, 1000)

INK = "#241A26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0B0E14"}, {"offset": 1, "color": "#05070B"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E3A54"}, {"offset": 0.7, "color": "#1C2438"},
    {"offset": 1, "color": "#0E1420"}]}}
CRUDE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#33284A"}, {"offset": 0.6, "color": "#1E1830"},
    {"offset": 1, "color": "#120E1E"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8AE7E"}, {"offset": 1, "color": "#A87850"}]}}
HAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0C25E"}, {"offset": 1, "color": "#B8862E"}]}}
PUMP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#46536E"}, {"offset": 1, "color": "#28304A"}]}}
DRUM = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A4432"}, {"offset": 1, "color": "#4A2A20"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#D8A84E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D2EC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A4664", opacity=45, stroke=NONE)

# --- faint derrick silhouette, upper left ------------------------------------------
d.path("M180,560 L260,300 L340,560 M214,470 L306,470 M232,410 L288,410 "
       "M248,355 L272,355 M180,560 L340,560 M260,300 L260,560",
       "Derrick", fill=NONE, stroke="#5E6E96", strokeWidth=4, opacity=18,
       join="round")
# tiny flare off the derrick crown
d.path("M256,292 C252,278 258,266 266,258 C270,270 274,282 268,292 Z",
       "Derrick flare", fill="#E8A84E", opacity=35, stroke=NONE)

# --- ground ----------------------------------------------------------------------
d.shape("ellipse", "Ground shadow", x=220, y=696, width=580, height=64,
        fill="#04070C", opacity=60, stroke=NONE)
# iridescent crude puddle under the mascot
d.shape("ellipse", "Crude puddle", x=300, y=690, width=300, height=44,
        fill="#14101F", opacity=90, stroke=NONE)
d.path("M330,708 C380,700 470,700 560,706", "Puddle sheen teal",
       fill=NONE, stroke="#5EC8B8", strokeWidth=4, opacity=40, cap="round")
d.path("M350,718 C410,712 480,712 540,716", "Puddle sheen violet",
       fill=NONE, stroke="#8E7AD8", strokeWidth=3, opacity=35, cap="round")
d.path("M370,700 C400,696 440,696 470,698", "Puddle sheen gold",
       fill=NONE, stroke="#D8B25E", strokeWidth=3, opacity=30, cap="round")

# --- oil drum with the receipt stack ---------------------------------------------------
d.path("M222,610 L306,610 L312,700 L216,700 Z", "Drum",
       fill=DRUM, stroke=INK, strokeWidth=5, join="round")
d.path("M220,632 L308,632 M218,670 L310,670", "Drum ribs", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=55)
d.shape("ellipse", "Drum lid", x=222, y=600, width=84, height=22,
        fill="#5A3428", stroke=INK, strokeWidth=4)
# stacked receipts on the lid
d.path("M234,586 L292,582 L296,598 L238,602 Z", "Receipt stack 1",
       fill="#EAE4D2", stroke=INK, strokeWidth=3, join="round")
d.path("M238,572 L290,568 L294,584 L242,588 Z", "Receipt stack 2",
       fill="#F4EEE0", stroke=INK, strokeWidth=3, join="round")
d.path("M246,576 L280,574", "Stack line", fill=NONE, stroke="#9A9284",
       strokeWidth=2, opacity=70)

# --- the pump, right ----------------------------------------------------------------------
d.shape("ellipse", "Pump shadow", x=668, y=692, width=170, height=28,
        fill="#04070C", opacity=55, stroke=NONE)
d.path("M684,470 C684,448 702,436 732,436 C762,436 780,448 780,470 L780,692 L684,692 Z",
       "Pump body", fill=PUMP, stroke=INK, strokeWidth=6, join="round")
# amber gauge lamp
d.shape("ellipse", "Gauge halo", x=700, y=470, width=64, height=64,
        fill="#F0B85E", opacity=18, stroke=NONE)
d.shape("ellipse", "Gauge", x=706, y=476, width=52, height=52,
        fill="#1A2234", stroke=INK, strokeWidth=4)
d.path("M732,502 L744,490", "Gauge needle", fill=NONE, stroke="#F0B85E",
       strokeWidth=4, cap="round")
d.shape("rectangle", "Pump band", x=684, y=546, width=96, height=30,
        fill="#141C2C", stroke=INK, strokeWidth=3)
d.text("DSL", "Band label", x=732, y=568, size=17, font="Virelai Sans",
       color="#E8C87E", justify="center")
# nozzle holstered on the flank
d.path("M780,540 L802,540 L800,576 L784,576 Z", "Nozzle boot",
       fill=INK, stroke=NONE, opacity=90, join="round")
d.path("M792,576 C796,610 788,640 794,668", "Nozzle hose", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round", opacity=80)
# ledger shelf jutting left off the pump
d.path("M608,584 L684,580 L684,604 L610,608 Z", "Ledger shelf",
       fill="#3A4660", stroke=INK, strokeWidth=4, join="round")
# receipt on the shelf being stamped
d.path("M616,566 L676,562 L680,584 L620,588 Z", "Receipt on shelf",
       fill="#F4EEE0", stroke=INK, strokeWidth=3, join="round")
d.path("M626,572 L662,570 M628,578 L666,576", "Shelf receipt lines",
       fill=NONE, stroke="#9A9284", strokeWidth=2, opacity=70)

# --- the driller ----------------------------------------------------------------------------
d.shape("ellipse", "Driller shadow", x=330, y=684, width=250, height=36,
        fill="#04070C", opacity=55, stroke=NONE)
# boots
d.shape("rectangle", "Boot L", x=356, y=656, width=54, height=44,
        fill=INK, stroke=NONE, radius=10)
d.shape("rectangle", "Boot R", x=478, y=656, width=54, height=44,
        fill=INK, stroke=NONE, radius=10)
# crude-coated body: heavy rounded coat
d.path("M444,420 C386,428 350,486 348,556 C346,606 352,646 358,676 "
       "C400,690 496,690 540,672 C546,640 552,604 550,556 "
       "C546,484 508,428 444,420 Z",
       "Crude coat", fill=CRUDE, stroke=INK, strokeWidth=6, join="round")
# spectral crude drips down the coat
for i, (x, y, h) in enumerate([(372,560,96),(418,600,76),(470,590,90),
                               (516,560,84),(396,520,60),(494,520,66)]):
    d.path(f"M{x},{y} C{x-3},{y+h*0.5} {x+3},{y+h*0.7} {x},{y+h}",
           f"Crude drip {i+1}", fill=NONE, stroke="#0E0A18",
           strokeWidth=9, opacity=80, cap="round")
for i, (x, y, h) in enumerate([(376,564,88),(474,594,82),(520,564,76)]):
    d.path(f"M{x},{y} C{x-3},{y+h*0.5} {x+3},{y+h*0.7} {x},{y+h}",
           f"Crude sheen {i+1}", fill=NONE, stroke="#8E7AD8",
           strokeWidth=3, opacity=55, cap="round")
for i, (x, y, h) in enumerate([(422,604,70),(400,524,54)]):
    d.path(f"M{x},{y} C{x-3},{y+h*0.5} {x+3},{y+h*0.7} {x},{y+h}",
           f"Crude sheen t{i+1}", fill=NONE, stroke="#5EC8B8",
           strokeWidth=3, opacity=50, cap="round")
# collar of clean coat fur peeking out
d.path("M398,446 C420,430 470,428 494,444 C480,462 414,464 398,446 Z",
       "Collar", fill="#5E4A38", stroke=INK, strokeWidth=4, join="round")
# head
d.shape("ellipse", "Head", x=408, y=356, width=80, height=76,
        fill=SKIN, stroke=INK, strokeWidth=5)
# hardhat
d.path("M398,384 C396,346 420,324 448,324 C476,324 500,346 498,384 "
       "L512,384 C514,396 506,402 494,400 L402,400 C390,402 382,396 384,384 Z",
       "Hardhat", fill=HAT, stroke=INK, strokeWidth=5, join="round")
d.path("M448,324 L448,398", "Hat ridge", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=45)
# grime smudge on cheek
d.shape("ellipse", "Grime", x=452, y=402, width=26, height=14,
        fill="#1E1830", opacity=45, stroke=NONE)
# tired-steadfast eyes + flat mouth
d.shape("ellipse", "Eye L", x=424, y=384, width=13, height=16, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=458, y=384, width=13, height=16, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=427, y=387, width=4, height=4,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=461, y=387, width=4, height=4,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M430,414 C440,418 456,418 466,414", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# arm reaching to the stamp on the shelf
d.path("M520,500 C556,516 596,534 628,548", "Arm", fill=NONE,
       stroke="#1E1830", strokeWidth=34, cap="round")
d.path("M520,500 C556,516 596,534 628,548", "Arm seam", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=60, cap="round")
# crude sheen along the arm
d.path("M532,508 C560,520 590,534 614,544", "Arm sheen", fill=NONE,
       stroke="#5EC8B8", strokeWidth=4, opacity=45, cap="round")
# stamp in the dripping glove
d.path("M622,530 L646,530 L642,556 L626,556 Z", "Stamp handle",
       fill="#8E5A3C", stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Stamp base", x=614, y=556, width=40, height=14,
        fill=INK, stroke=NONE, radius=3)
d.shape("ellipse", "Glove", x=614, y=522, width=34, height=24,
        fill="#0E0A18", stroke=INK, strokeWidth=4)
# drip falling off the elbow
d.path("M528,540 C526,566 530,592 526,614", "Elbow drip", fill=NONE,
       stroke="#0E0A18", strokeWidth=7, opacity=80, cap="round")
d.shape("ellipse", "Drip bead", x=520, y=616, width=12, height=14,
        fill="#1E1830", stroke="#5EC8B8", strokeWidth=2, opacity=90)

# --- stray receipts + droplets --------------------------------------------------------
d.path("M600,640 L650,632 L656,656 L606,664 Z", "Receipt floor",
       fill="#EAE4D2", stroke=INK, strokeWidth=3, opacity=90, join="round")
d.path("M610,646 L640,642 M612,652 L644,648", "Floor receipt lines",
       fill=NONE, stroke="#9A9284", strokeWidth=2, opacity=70)
for i, (x, y, w) in enumerate([(330,660,8),(560,670,7),(590,700,6),(310,690,6)]):
    d.shape("ellipse", f"Droplet {i+1}", x=x, y=y, width=w, height=w,
            fill="#8E7AD8", opacity=50, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("DIESEL DKDRILLER", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E8E2F2", justify="center")
r = d.text("CRUDE CUSTODIAN", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A89CD2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("206.diesel-dkdriller-V1R00")

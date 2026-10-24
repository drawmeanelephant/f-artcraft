#!/usr/bin/env python3
"""HAI-0442 Triage Tracy — haiku plate V1R00. Profit over survival made
visual: an ECG trace that smooths into the declining LOS curve, the
discharge planner sliding down it, the criteria sheet whose blanks were
never written, stamped DENIED. Clinical teal ink, one coral heartbeat.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0442 Triage Tracy — Haiku Plate", 1000, 1000)

INK = "#1E2A22"
CORAL = "#E86A5A"
CREAM = "#E6E2D2"
SOFT = "#9FC0B4"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#111B18"}, {"offset": 1, "color": "#070C0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5E56"}, {"offset": 0.7, "color": "#243E38"},
    {"offset": 1, "color": "#0F1C18"}]}}
CURVE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7EB4A4"}, {"offset": 1, "color": "#3E5E56"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8E2D0"}, {"offset": 1, "color": "#B8B09A"}]}}
FIG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A8A80"}, {"offset": 1, "color": "#30463E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E7A6C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D0E4DC", strokeWidth=3, opacity=40)
d.shape("ellipse", "Clinical pool", x=290, y=330, width=420, height=380,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#7EB4A4", "opacity": 0.20},
            {"offset": 1, "color": "#7EB4A4", "opacity": 0}]}},
        stroke=NONE)

# --- the monitor grid: graph paper the heartbeat rides on -------------------------
for i, x in enumerate(range(200, 801, 100)):
    d.path(f"M{x},400 L{x},680", f"Grid V {i+1}", fill=NONE,
           stroke="#5E7E74", strokeWidth=1.5, opacity=20)
for i, y in enumerate(range(420, 741, 80)):
    d.path(f"M200,{y} L800,{y}", f"Grid H {i+1}", fill=NONE,
           stroke="#5E7E74", strokeWidth=1.5, opacity=20)

# --- the trace: heartbeat that becomes the margin curve -----------------------------
# two clean QRS beats, then biology bends into logistics
TRACE = ("M150,500 L250,500 L268,470 L286,530 L304,436 L322,560 "
         "L338,500 L420,500 L438,468 L456,532 L474,440 L492,556 "
         "L508,500 L560,500 C630,500 650,590 720,650 L800,716")
d.path(TRACE, "Trace glow", fill=NONE, stroke=CORAL, strokeWidth=16,
       opacity=15, cap="round", join="round")
d.path(TRACE, "Trace ECG", fill=NONE, stroke=CORAL, strokeWidth=6,
       cap="round", join="round")
# where the curve turns, the colour goes cold — re-draw the bend in margin teal
d.path("M560,500 C630,500 650,590 720,650 L800,716", "Margin bend",
       fill=NONE, stroke="#8AC4B0", strokeWidth=6, cap="round",
       opacity=75)
d.text("los", "Curve label", x=774, y=732, size=15,
       font="Virelai Sans", color=SOFT, justify="center")
d.text("bpm", "ECG label", x=180, y=470, size=15,
       font="Virelai Sans", color="#E8A89E", justify="center")
# the junction marker — the exact point the decision happens
d.shape("ellipse", "Bend marker", x=551, y=491, width=18, height=18,
        fill="#0F1C18", stroke="#E8A89E", strokeWidth=3.5)

# --- the discharge planner: small figure riding the curve down ----------------------
# seated on the line at the bottom of the bend, clipboard in lap
r = d.shape("ellipse", "Planner body", x=676, y=596, width=56, height=66,
            fill=FIG, stroke=INK, strokeWidth=4)
IDS = [(r or {}).get("id")]
r = d.shape("ellipse", "Planner head", x=686, y=566, width=36, height=36,
            fill=FIG, stroke=INK, strokeWidth=4)
IDS.append((r or {}).get("id"))
r = d.shape("rectangle", "Planner board", x=700, y=622, width=34,
            height=24, radius=3, fill=PAPER, stroke=INK, strokeWidth=3)
IDS.append((r or {}).get("id"))
IDS = [i for i in IDS if i]
if IDS:
    d.call("transform", {"ids": IDS, "rotate": 28, "origin": [704, 620]},
           "tilt planner")
# motion ticks under the slide
for i, (x, y) in enumerate([(755, 668), (775, 684), (795, 700)]):
    d.path(f"M{x},{y} l16,10", f"Slide tick {i+1}", fill=NONE,
           stroke="#8AC4B0", strokeWidth=3, cap="round", opacity=70)

# --- the criteria sheet: exist but were never written -------------------------------
d.shape("rectangle", "Sheet shadow", x=352, y=196, width=280, height=290,
        radius=4, fill="#0C1410", opacity=30, stroke=NONE)
d.shape("rectangle", "Criteria sheet", x=342, y=186, width=280, height=290,
        radius=4, fill=PAPER, stroke=INK, strokeWidth=5)
d.text("CRITERIA", "Sheet header", x=482, y=226, size=19,
       font="Virelai Sans", color="#3A352A", justify="center")
d.path("M372,244 L592,244", "Header rule", fill=NONE, stroke="#8A8068",
       strokeWidth=2, opacity=80)
# rows: a few written, the rest ghosted — never written
ROWS = [("los exceeded", True), ("peer review clicked", True),
        ("cost outlier", True), ("patient need", False),
        ("clinical sense", False)]
for i, (label, written) in enumerate(ROWS):
    y = 268 + i * 38
    if written:
        d.shape("rectangle", f"Row {i+1} box", x=368, y=y, width=16,
                height=16, fill=NONE, stroke="#4A4438", strokeWidth=2.5)
        d.path(f"M371,{y+8} L376,{y+14} L383,{y+3}", f"Row {i+1} check",
               fill=NONE, stroke="#4A4438", strokeWidth=2.5, cap="round")
        d.text(label, f"Row {i+1} text", x=394, y=y + 13, size=13,
               font="Virelai Sans", color="#4A4438", justify="left")
    else:
        d.shape("rectangle", f"Row {i+1} box", x=368, y=y, width=16,
                height=16, fill=NONE, stroke="#8A8068", strokeWidth=2,
                dash=[3, 3])
        d.path(f"M394,{y+10} L586,{y+10}", f"Row {i+1} ghost",
               fill=NONE, stroke="#8A8068", strokeWidth=2.5,
               dash=[6, 6], opacity=60)
# the stamp — struck across the rows that were never written
r = d.shape("rectangle", "Denied stamp box", x=392, y=404, width=176,
            height=50, radius=6, fill=NONE, stroke=CORAL, strokeWidth=5)
ids = [(r or {}).get("id")]
r = d.text("DENIED", "Denied stamp", x=480, y=439, size=27,
           font="Virelai Sans", color=CORAL, justify="center")
ids.append((r or {}).get("id"))
ids = [i for i in ids if i]
if ids:
    d.call("transform", {"ids": ids, "rotate": -9, "origin": [480, 429]},
           "tilt denied")

# --- the margin: a coin outweighing the heart ---------------------------------------
# small balance dish lower-left: coin pan sunk, heart pan up
d.path("M286,690 L286,772", "Scale post", fill=NONE, stroke=INK,
       strokeWidth=5)
d.path("M222,700 L350,712", "Scale beam", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M222,700 L222,724 M204,724 Q222,748 240,724 Z", "Pan L",
       fill=NONE, stroke=INK, strokeWidth=3, join="round")
d.path("M350,712 L350,752 M332,752 Q350,776 368,752 Z", "Pan R",
       fill=NONE, stroke=INK, strokeWidth=3, join="round")
# coin on the right pan — it sinks lower
d.shape("ellipse", "Coin", x=340, y=742, width=20, height=10,
        fill="#C8A850", stroke=INK, strokeWidth=2.5)
# small heart on the left pan — riding high, unfunded
d.path("M214,712 C210,704 222,700 224,708 C226,700 238,704 234,712 "
       "L224,722 Z",
       "Pan heart", fill=CORAL, stroke=INK, strokeWidth=2.5)
d.path("M330,790 L670,790", "Ground rule", fill=NONE, stroke="#3E5E56",
       strokeWidth=2, opacity=60)

# --- caption stack: key line over the name ------------------------------------------
r = d.text("BIOLOGY BENDS.", "Key line", x=500, y=898, size=22,
           font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=300)
d.text("TRIAGE TRACY", "Name", x=500, y=944, size=56,
       font="Virelai Sans", color=CREAM, justify="center")

d.finish("hai-0442-triage-tracy-V1R00")

#!/usr/bin/env python3
"""HAI-0445 Deepfake Dave — haiku plate V1R00. The CEO denied the video he
never made — the stock still moved. Dave feeds a source photo into the
render screen: half a real face, half pixels, an alibi mid-play, an
exhibit tag already clipped on, a watermark ring that was never filled in.
Stock ticker slides on the floor. Warm dark ink, 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
import math

d = Draw()
d.new_doc("HAI-0445 Deepfake Dave — Haiku Plate", 1000, 1000)

INK = "#241C26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161022"}, {"offset": 1, "color": "#080510"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#483A72"}, {"offset": 0.7, "color": "#2C2148"},
    {"offset": 1, "color": "#160E2A"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2044"}, {"offset": 1, "color": "#140E24"}]}}
BEZEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#463E56"}, {"offset": 1, "color": "#26202F"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#123A44"}, {"offset": 1, "color": "#081E26"}]}}
HOODIE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E5A96"}, {"offset": 0.75, "color": "#4A3A6E"},
    {"offset": 1, "color": "#332850"}]}}
CLAPPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C3E48"}, {"offset": 1, "color": "#22232C"}]}}
FACE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0CDA8"}, {"offset": 1, "color": "#C99A72"}]}}
CYAN = "#7EDCE8"
BONE = "#EFE3CE"
DIM = "#A898C8"
RED = "#C45A52"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E5E96", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CFEA", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(192, 232, 8), (800, 226, 7), (158, 528, 9),
                               (836, 542, 8), (248, 762, 7), (750, 750, 9),
                               (132, 392, 6), (864, 388, 7), (392, 112, 7),
                               (612, 110, 8), (330, 820, 6), (668, 818, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#56477E", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A1A",
       strokeWidth=4, opacity=70)

# --- ghost telemetry high on the plate ----------------------------------------
d.text("WATERMARK CHECK: SKIPPED", "Ghost 1", x=500, y=140, size=13,
       font="Virelai Sans", color="#7A6C96", justify="center")
d.text("SOURCE FRAME RETAINED — SIGNED BY NO ONE", "Ghost 2", x=500, y=163,
       size=12, font="Virelai Sans", color="#6A5C86", justify="center")

# --- render screen (right): the face that never happened ------------------------
d.shape("ellipse", "Screen glow", x=540, y=150, width=300, height=240,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#7EDCE8", "opacity": 0.12},
            {"offset": 1, "color": "#7EDCE8", "opacity": 0}]}},
        stroke=NONE)
d.shape("rectangle", "Screen bezel", x=555, y=185, width=265, height=205,
        fill=BEZEL, stroke=INK, strokeWidth=5, radius=10)
d.shape("rectangle", "Render screen", x=569, y=199, width=237, height=150,
        fill=SCREEN, stroke="#061418", strokeWidth=3, radius=6)
# the face: left half honest, right half dissolving into pixels
d.path("M688,222 C720,222 742,246 742,276 C742,308 720,332 688,332 "
       "C656,332 636,308 636,276 C636,246 656,222 688,222 Z",
       "Render face", fill=FACE, stroke=INK, strokeWidth=4, opacity=95)
for i, (x, y, s, o) in enumerate([(722, 232, 15, 80), (738, 252, 12, 68),
                                  (730, 282, 14, 75), (716, 308, 11, 62),
                                  (748, 268, 9, 52), (708, 226, 9, 58),
                                  (754, 292, 8, 44), (726, 322, 9, 55)]):
    d.shape("rectangle", f"Pixel {i+1}", x=x, y=y, width=s, height=s,
            fill="#F0CDA8", opacity=o, stroke=NONE)
for i, (x, y, s) in enumerate([(762, 240, 7), (768, 278, 6), (758, 312, 7)]):
    d.shape("rectangle", f"Stray pixel {i+1}", x=x, y=y, width=s, height=s,
            fill=CYAN, opacity=45, stroke=NONE)
# one honest eye, one pixel-block eye; its mouth is the play button
d.shape("ellipse", "Eye real", x=655, y=262, width=13, height=16,
        fill="#241C26", stroke=NONE)
d.shape("rectangle", "Eye block", x=697, y=260, width=14, height=14,
        fill="#241C26", stroke=NONE, radius=2)
# scanline mid-sweep
d.path("M636,290 L762,290", "Scanline", fill=NONE, stroke=CYAN,
       strokeWidth=3, opacity=55)
# alibi mid-play: translucent play button over the mouth zone
d.shape("ellipse", "Play disc", x=663, y=282, width=48, height=48,
        fill="#0E2A34", opacity=60, stroke=CYAN, strokeWidth=2.5)
d.path("M684,296 L684,316 L702,306 Z", "Play wedge", fill=CYAN, opacity=85,
       stroke=NONE)
# exhibit tag clipped to the bezel — already evidence
d.path("M582,172 L628,164 L636,194 L590,202 Z", "Exhibit tag",
       fill="#D8C89A", stroke=INK, strokeWidth=3, join="round")
d.text("EXHIBIT", "Exhibit word", x=592, y=183, size=9, font="Virelai Sans",
       color="#5A4526", justify="left")
d.text("A-1", "Exhibit no", x=593, y=195, size=10, font="Source Sans 3",
       color="#3A2A18", justify="left")
# watermark ring bottom-right of the screen: promised, never filled in
d.shape("ellipse", "Watermark ring", x=738, y=305, width=34, height=34,
        fill=NONE, stroke=CYAN, strokeWidth=2.5, dash=[4, 4], opacity=55)
d.text("W", "Watermark glyph", x=755, y=332, size=13, font="Virelai Sans",
       color=CYAN, justify="center")
d.shape("rectangle", "Screen stand", x=668, y=390, width=40, height=60,
        fill=BEZEL, stroke=INK, strokeWidth=4)
d.path("M643,450 L733,450 L743,464 L633,464 Z", "Screen foot",
       fill=BEZEL, stroke=INK, strokeWidth=4)

# --- stock ticker on the floor: it moved ----------------------------------------
d.shape("rectangle", "Ticker panel", x=300, y=718, width=400, height=82,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#201840"},
            {"offset": 1, "color": "#120C26"}]}},
        opacity=90, stroke="#56477E", strokeWidth=3, radius=8)
for i in range(6):
    d.path(f"M{330 + i * 68},736 L{330 + i * 68},784", f"Grid v {i+1}",
           fill=NONE, stroke="#3A2F5A", strokeWidth=1.5, opacity=50)
d.path("M318,752 L682,752", "Grid h", fill=NONE, stroke="#3A2F5A",
       strokeWidth=1.5, opacity=50)
# the line: flat, a shrug, then the drop
d.path("M316,740 L380,738 L430,744 L470,741 L520,758 L560,782 "
       "L640,790", "Ticker line", fill=NONE, stroke=RED, strokeWidth=5,
       cap="round", join="round")
d.path("M640,790 L662,793 L646,778", "Ticker arrow", fill=NONE, stroke=RED,
       strokeWidth=5, cap="round", join="round")
d.path("M316,740 L380,738 L430,744 L470,741", "Ticker glow", fill=NONE,
       stroke="#E8A89A", strokeWidth=2, opacity=40, cap="round")
d.text("CLOSE", "Ticker label", x=316, y=790, size=9, font="Virelai Sans",
       color="#7A6C96", justify="left")

# --- Dave: clapperboard-headed operator -----------------------------------------
d.shape("ellipse", "Dave shadow", x=230, y=688, width=230, height=28,
        fill="#0A0616", opacity=45, stroke=NONE)
# body: hoodie blob
d.path("M345,540 C420,540 462,595 462,650 C462,695 420,715 345,715 "
       "C270,715 228,695 228,650 C228,595 270,540 345,540 Z",
       "Dave body", fill=HOODIE, stroke=INK, strokeWidth=6)
d.path("M305,560 C325,585 365,585 385,560", "Hood fold", fill=NONE,
       stroke="#2E2448", strokeWidth=7, cap="round", opacity=70)
d.path("M305,655 L385,655 L375,690 L315,690 Z", "Pocket",
       fill="#3A2E58", stroke=INK, strokeWidth=4, join="round", opacity=85)
# arm offering the photo to the machine
d.path("M450,610 C475,590 482,565 478,542", "Arm R", fill=NONE,
       stroke="#4A3A6E", strokeWidth=18, cap="round")
d.shape("ellipse", "Hand R", x=462, y=528, width=26, height=24,
        fill="#8A76B0", stroke=INK, strokeWidth=4)
# the source photo pinched in his fingers — a face too small to consent
d.path("M470,470 L545,470 L545,545 L470,545 Z", "Source photo",
       fill="#E8DCC8", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Source face", x=488, y=488, width=40, height=40,
        fill=FACE, stroke=INK, strokeWidth=3)
d.path("M495,505 L503,505 M512,505 L520,505", "Source eyes", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
d.path("M500,518 C505,521 512,521 517,518", "Source smile", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
# feed line from the photo to the screen: one-way trip
d.path("M546,475 C582,442 598,398 610,352", "Feed arrow", fill=NONE,
       stroke=CYAN, strokeWidth=4, dash=[7, 6], cap="round", opacity=70)
d.path("M610,352 L597,355 M610,352 L603,369", "Feed head", fill=NONE,
       stroke=CYAN, strokeWidth=4, cap="round", opacity=70)
d.path("M240,615 C222,635 220,660 230,678", "Arm L", fill=NONE,
       stroke="#4A3A6E", strokeWidth=18, cap="round")
# head: clapperboard
d.path("M270,440 L270,545 L430,545 L430,440 Z", "Board",
       fill=CLAPPER, stroke=INK, strokeWidth=6, join="round")
d.path("M270,440 L270,403 L430,403 L430,440", "Clap bar", fill="#2A2D36",
       stroke=INK, strokeWidth=5)
for i in range(5):
    x0 = 273 + i * 32
    d.path(f"M{x0},439 L{x0+22},405 L{x0+38},405 L{x0+16},439 Z",
           f"Clap stripe {i+1}", fill="#E8E4DC", stroke=NONE, opacity=90)
# face on the board: calm, pleased — he has an alibi
d.path("M300,487 C307,495 318,495 325,487", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M375,487 C382,495 393,495 400,487", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M325,517 C340,527 360,527 375,517", "Smirk", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.text("TAKE ∞", "Take label", x=283, y=535, size=12, font="Virelai Sans",
       color="#8A94A8", justify="left")

# --- the detector: a magnifier that arrived too late ----------------------------
d.shape("ellipse", "Detector glass", x=330, y=245, width=64, height=64,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#7EDCE8", "opacity": 0.18},
            {"offset": 1, "color": "#7EDCE8", "opacity": 0.05}]}},
        stroke="#9A8CB8", strokeWidth=5)
d.path("M388,296 L414,324", "Detector handle", fill=NONE, stroke="#9A8CB8",
       strokeWidth=8, cap="round")
# what it sees: three stray pixels, magnified
for i, (x, y, s) in enumerate([(348, 262, 9), (362, 276, 7), (346, 284, 6)]):
    d.shape("rectangle", f"Lens pixel {i+1}", x=x, y=y, width=s, height=s,
            fill=CYAN, opacity=60, stroke=NONE)

# --- captions --------------------------------------------------------------------
k = d.text("the stock still moved.", "Key line", x=500, y=896, size=23,
           font="Virelai Sans", color="#C8BEE0", justify="center")
if k and k.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[k["id"]], tracking=260)
d.text("DEEPFAKE DAVE", "Name", x=500, y=941, size=56, font="Virelai Sans",
       color=BONE, justify="center")
r = d.text("THE COURT DOESN'T KNOW WHAT IS TRUE", "Role", x=500, y=973,
           size=19, font="Virelai Sans", color="#8E80B0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=180)

d.finish("hai-0445-deepfake-dave-V1R00")

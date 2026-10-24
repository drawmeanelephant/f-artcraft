#!/usr/bin/env python3
"""Severance Cordial — mascot portrait V1R00.
A small glass of ruby cordial beside its bottle, set on top of an exit
packet: hospitality poured over a termination. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Severance Cordial — Mascot Portrait", 1000, 1000)

INK = "#2A1A1C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#160E12"}, {"offset": 1, "color": "#080407"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E3A44"}, {"offset": 0.7, "color": "#45242E"},
    {"offset": 1, "color": "#241318"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A2E2A"}, {"offset": 1, "color": "#1E1110"}]}}
PACKET_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0CC9E"}, {"offset": 1, "color": "#B09468"}]}}
BACK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9B586"}, {"offset": 1, "color": "#9A8258"}]}}
BOTTLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E3240"}, {"offset": 1, "color": "#2E1218"}]}}
LIQUID_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8586A"}, {"offset": 1, "color": "#8A1E2E"}]}}
LABEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFE0BC"}, {"offset": 1, "color": "#C8B488"}]}}
WAX_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B04A58"}, {"offset": 1, "color": "#6E1E2C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A26A74", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2D8D2", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E343C", opacity=45, stroke=NONE)

# --- glowing EXIT sign, upper right ---------------------------------------------
d.shape("ellipse", "Exit glow", x=596, y=150, width=160, height=90,
        fill="#7EE8A0", opacity=10, stroke=NONE)
d.path("M676,140 L676,158", "Sign hanger", fill=NONE, stroke="#4A3238",
       strokeWidth=4)
d.shape("rectangle", "Exit sign", x=612, y=158, width=128, height=54,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#1E4A34"}, {"offset": 1, "color": "#0E281C"}]}},
        stroke=INK, strokeWidth=4, radius=8)
d.text("EXIT", "Exit letters", x=676, y=192, size=30, font="Virelai Sans",
       color="#9EF0BC", justify="center")

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#160E0C",
       strokeWidth=4, opacity=70)

# --- the exit packet --------------------------------------------------------------
d.shape("ellipse", "Packet shadow", x=270, y=688, width=460, height=26,
        fill="#0C0606", opacity=50, stroke=NONE)
d.path(rot_rect_path(490, 630, 440, 140, 3), "Packet back sheet",
       fill=BACK_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Exit packet", x=270, y=556, width=460, height=136,
        fill=PACKET_GRAD, stroke=INK, strokeWidth=5)
# envelope flap seams
d.path("M270,556 L500,640 L730,556", "Flap seam", fill=NONE,
       stroke="#8A7550", strokeWidth=3.5, opacity=75)
d.path("M270,692 L440,614 M730,692 L560,614", "Flap lower seams", fill=NONE,
       stroke="#8A7550", strokeWidth=3, opacity=45)
# wax seal with string
d.path("M480,640 L480,692 M520,640 L520,692", "Seal strings", fill=NONE,
       stroke="#8A2E3E", strokeWidth=3, opacity=60)
d.shape("ellipse", "Wax seal", x=478, y=598, width=44, height=44,
        fill=WAX_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Wax inner", x=488, y=608, width=24, height=24,
        fill=NONE, stroke="#5E1A26", strokeWidth=2.5, opacity=70)
d.text("EXIT PACKET", "Packet label", x=500, y=682, size=15,
       font="Virelai Sans", color="#6A5638", justify="center")
d.shape("ellipse", "Stamp ring", x=640, y=580, width=52, height=52,
        fill=NONE, stroke="#9A4A42", strokeWidth=3, opacity=45)
d.shape("ellipse", "Stamp core", x=654, y=594, width=24, height=24,
        fill="#9A4A42", opacity=28, stroke=NONE)

# --- the bottle, standing on the packet --------------------------------------------
d.shape("ellipse", "Bottle shadow", x=330, y=548, width=130, height=16,
        fill="#7A6444", opacity=50, stroke=NONE)
# cork + neck
d.shape("rectangle", "Cork", x=382, y=288, width=26, height=34,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#D8B888"}, {"offset": 1, "color": "#A07850"}]}},
        stroke=INK, strokeWidth=4, radius=5)
d.path("M368,322 L422,322 L428,348 L362,348 Z", "Neck", fill=BOTTLE_GRAD,
       stroke=INK, strokeWidth=4)
# foil over the cork
d.path("M376,286 L414,286 L416,306 L374,306 Z", "Foil cap", fill="#8A2E3E",
       stroke=INK, strokeWidth=3, join="round")
# shoulders into body
d.path("M362,348 C340,362 330,382 330,404 L330,556 L460,556 L460,404 "
       "C460,382 450,362 428,348 Z", "Bottle body", fill=BOTTLE_GRAD,
       stroke=INK, strokeWidth=5, join="round")
# shoulder sheen
d.path("M344,380 C352,366 366,356 382,352", "Bottle sheen", fill=NONE,
       stroke="#B06A78", strokeWidth=6, cap="round", opacity=55)
# bottle label
d.shape("rectangle", "Bottle label", x=348, y=430, width=94, height=74,
        fill=LABEL_GRAD, stroke=INK, strokeWidth=3.5, radius=4)
d.path("M356,444 L434,444 M356,492 L434,492", "Label rules", fill=NONE,
       stroke="#8A7550", strokeWidth=2.5, opacity=70)
d.text("CORDIAL", "Label word", x=395, y=474, size=17, font="Virelai Sans",
       color="#4A3226", justify="center")

# --- the cordial glass, small, on the packet ----------------------------------------
d.shape("ellipse", "Glass shadow", x=560, y=548, width=110, height=14,
        fill="#7A6444", opacity=50, stroke=NONE)
# stem + foot first so the bowl overlaps cleanly
d.path("M596,512 L604,512 L606,548 L594,548 Z", "Stem", fill="#CFE0DC",
       stroke=INK, strokeWidth=3, opacity=85)
d.path("M570,548 C570,556 586,562 600,562 C614,562 630,556 630,548 Z",
       "Foot", fill="#CFE0DC", stroke=INK, strokeWidth=3.5, opacity=85)
# liquid inside the bowl
d.path("M568,458 L632,458 C632,496 620,514 600,514 C580,514 568,496 568,458 Z",
       "Cordial", fill=LIQUID_GRAD, stroke="#5E1420", strokeWidth=3)
d.path("M568,458 C580,450 620,450 632,458", "Meniscus", fill=NONE,
       stroke="#F0929E", strokeWidth=3.5, cap="round", opacity=80)
# glass bowl outline, translucent
d.path("M558,430 L642,430 C642,486 624,516 600,516 C576,516 558,486 558,430 Z",
       "Glass bowl", fill="#E8F4F0", stroke=INK, strokeWidth=4, opacity=30)
d.path("M566,434 L574,434 C574,470 582,494 594,506", "Glass sheen",
       fill=NONE, stroke="#FFFFFF", strokeWidth=4, cap="round", opacity=45)

# --- tent card: with the house's compliments -----------------------------------------
d.path(rot_rect_path(508, 521, 104, 54, -7), "Tent card",
       fill=LABEL_GRAD, stroke=INK, strokeWidth=3)
d.text("WITH OUR", "Card line 1", x=505, y=518, size=10, font="Virelai Sans",
       color="#4A3226", justify="center")
d.text("COMPLIMENTS", "Card line 2", x=503, y=534, size=10,
       font="Virelai Sans", color="#4A3226", justify="center")

# --- two spilled drops -------------------------------------------------------------
d.shape("ellipse", "Drop 1", x=656, y=600, width=12, height=8,
        fill="#8A1E2E", opacity=75, stroke=NONE)
d.shape("ellipse", "Drop 2", x=682, y=614, width=7, height=5,
        fill="#8A1E2E", opacity=60, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("SEVERANCE CORDIAL", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F2D8D2", justify="center")
r = d.text("ENDINGS DRESSED AS HOSPITALITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8989E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("319.severance-cordial-V1R00")

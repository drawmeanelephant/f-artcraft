#!/usr/bin/env python3
"""Escalady — mascot portrait V1R00.
She stands very straight on the staircase, routing slip held flat at the
angle of presentation, not transport. One step per reporting period; the
stairs show wear where she stands. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Escalady — Mascot Portrait", 1000, 1000)

INK = "#261C26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181018"}, {"offset": 1, "color": "#0C0810"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#766078"}, {"offset": 0.7, "color": "#4A3C50"},
    {"offset": 1, "color": "#262030"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#463A4A"}, {"offset": 1, "color": "#221A28"}]}}
STAIR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#544458"}, {"offset": 1, "color": "#2E2438"}]}}
CARPET_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A4452"}, {"offset": 1, "color": "#5E2E3C"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C4B6D0"}, {"offset": 0.72, "color": "#9688AC"},
    {"offset": 1, "color": "#665A7C"}]}}
HAIR = "#3E3448"
PAGE = "#EFE4CC"
GILT = "#D8B86A"

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#96869E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCCFE0", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(184,238,8),(808,234,7),(150,520,9),(842,540,8),
                               (250,766,7),(750,750,9),(126,392,6),(868,392,7),
                               (388,110,7),(620,108,8),(334,824,6),(668,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5C4C64", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#140E18",
       strokeWidth=4, opacity=70)

# --- the staircase: ascending right, the flight already reserved ------------------
# sawtooth profile: 7 steps rising from the floor line, tread 78 / riser 40,
# (170,700) up to a top landing at y=420 — the mass stays inside the disc
X0, Y0, TW, RH, N = 170, 700, 78, 40, 7
TOP = Y0 - N*RH                      # top landing height: 420
seg = [f"M{X0},{Y0}"]
for i in range(N):
    seg.append(f"L{X0+(i+1)*TW},{Y0-i*RH}")        # tread across
    seg.append(f"L{X0+(i+1)*TW},{Y0-(i+1)*RH}")    # riser up
seg.append(f"L830,{TOP} L830,{Y0} Z")              # landing right, down to floor
d.path(" ".join(seg), "Staircase", fill=STAIR_GRAD, stroke=INK,
       strokeWidth=5, join="round")
# tread tops, so each step reads
for i in range(N):
    tx, ty = X0 + i*TW, Y0 - i*RH
    d.path(f"M{tx},{ty} L{tx+TW},{ty}", f"Tread {i+1}", fill=NONE,
           stroke="#6E5C76", strokeWidth=4, opacity=85)
# the carpet runner: a full-width ribbon draped over every tread and riser
top = [f"M{X0+10},{Y0-6}"]
for i in range(N):
    top.append(f"L{X0+(i+1)*TW},{Y0-i*RH-6}")
    top.append(f"L{X0+(i+1)*TW},{Y0-(i+1)*RH-6}")
top.append(f"L830,{TOP-6}")
bot = [f"L830,{TOP+12}", f"L{X0+N*TW},{TOP+12}"]
for i in reversed(range(N)):
    bot.append(f"L{X0+(i+1)*TW},{Y0-i*RH+12}")
    bot.append(f"L{X0+(i+1)*TW},{Y0-(i-1)*RH+12}" if i > 0
               else f"L{X0+10},{Y0+12}")
bot.append("Z")
d.path(" ".join(top + bot), "Carpet runner", fill=CARPET_GRAD, stroke=INK,
       strokeWidth=3, join="round", opacity=95)
d.path(" ".join(top), "Runner sheen", fill=NONE, stroke="#B0646E",
       strokeWidth=3, join="round", opacity=65)
# the worn patch: a single flattened hollow on her step
d.shape("ellipse", "Wear patch", x=488, y=533, width=70, height=9,
        fill="#584A60", stroke=NONE, opacity=80)

# banister on the far side: straight rail + balusters, passing behind her
d.path("M180,655 L716,378", "Rail", fill=NONE, stroke="#2C2232",
       strokeWidth=7, cap="round")
for i, bx in enumerate([300, 380, 610, 690]):
    tread_y = Y0 - ((bx - X0) // TW) * RH
    rail_y = 655 - (bx - 180) * 277 / 536
    d.path(f"M{bx},{rail_y+4} L{bx},{tread_y}", f"Baluster {i+1}",
           fill=NONE, stroke="#2C2232", strokeWidth=4)
d.path("M180,655 L180,700", "Newel post", fill=NONE, stroke="#2C2232",
       strokeWidth=6)
d.shape("ellipse", "Newel finial", x=171, y=640, width=18, height=18,
        fill="#584A60", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Top finial", x=707, y=366, width=18, height=18,
        fill="#584A60", stroke=INK, strokeWidth=3)

# the floor above: a doorway on the top landing no floor plan includes
d.path("M710,420 L710,322 C710,288 738,272 768,272 C798,272 824,288 824,322 "
       "L824,420 Z", "Upper doorway", fill="#17101C", stroke=INK,
       strokeWidth=5)
d.path("M720,420 L720,324 C720,298 742,284 768,284 C794,284 814,298 814,324 "
       "L814,420 Z", "Door inner", fill="#0C0710", stroke="#3E3246",
       strokeWidth=2, opacity=90)

# a discreet arrow, the only signage the institution commits to
d.path("M262,340 L262,288 M246,306 L262,286 L278,306", "Up arrow",
       fill=NONE, stroke=GILT, strokeWidth=6, cap="round", join="round",
       opacity=80)

# --- Escalady: columnar, patient, ascending ---------------------------------------
d.shape("ellipse", "Escalady shadow", x=456, y=536, width=92, height=11,
        fill="#100A14", opacity=50, stroke=NONE)
# robe: a straight column from shoulder to step — she does not lean
d.path("M500,292 C464,292 454,328 452,370 L448,538 "
       "C448,550 470,552 500,552 C530,552 552,550 552,538 "
       "L548,370 C546,328 536,292 500,292 Z",
       "Robe", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Robe hi", x=462, y=340, width=38, height=140,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# the ceremonial sash: pale, vertical, unhurried
d.path("M492,296 L492,536", "Sash", fill=NONE, stroke="#DCCFE0",
       strokeWidth=14, opacity=55)
d.path("M492,296 L492,536", "Sash edge", fill=NONE, stroke="#8A7A9C",
       strokeWidth=3, opacity=60)
# hem hint: two shoe points at the step
d.shape("ellipse", "Shoe L", x=464, y=538, width=22, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe R", x=516, y=538, width=22, height=10,
        fill=INK, stroke=NONE)

# head: bowed the least a bow can be and still be legible
d.path("M506,214 C548,214 572,242 572,278 C572,312 544,334 506,334 "
       "C468,334 440,312 440,278 C440,242 464,214 506,214 Z",
       "Head", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# hair: drawn back smooth, low chignon
d.path("M444,270 C444,234 470,210 506,210 C542,210 568,234 568,270 "
       "C548,248 528,242 506,242 C484,242 464,248 444,270 Z",
       "Hair cap", fill=HAIR, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Chignon", x=548, y=248, width=26, height=30,
        fill=HAIR, stroke=INK, strokeWidth=4)
# eyes: downcast arcs, serene
d.path("M466,282 C474,290 486,290 494,282", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M522,282 C530,290 542,290 550,282", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# brows level, mouth a neutral line: not quite a promise
d.path("M468,270 L494,270 M522,270 L548,270", "Brows", fill=NONE,
       stroke="#4E4258", strokeWidth=3, cap="round")
d.path("M492,310 L522,310", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")

# arms: both sleeves converging on the slip, presented forward
d.path("M458,352 C446,384 452,406 470,420", "Sleeve L", fill=NONE,
       stroke="#847698", strokeWidth=15, cap="round")
d.path("M552,352 C564,384 558,406 542,420", "Sleeve R", fill=NONE,
       stroke="#847698", strokeWidth=15, cap="round")
# the routing slip: flat, uncreased, at the angle of presentation
d.path("M448,406 L556,398 L560,420 L452,428 Z", "Routing slip",
       fill=PAGE, stroke=INK, strokeWidth=4, join="round")
d.path("M460,414 L540,408 M462,420 L532,415", "Slip lines", fill=NONE,
       stroke="#B0A284", strokeWidth=2, opacity=80)
# both hands under it — accepting with the whole gesture
d.shape("ellipse", "Palm L", x=450, y=416, width=24, height=16,
        fill="#B4A6C4", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Palm R", x=536, y=410, width=24, height=16,
        fill="#B4A6C4", stroke=INK, strokeWidth=3)

# the visibility beam: she is the one part of the process lit
d.path("M465,90 L537,90 L574,548 L422,548 Z", "Light shaft",
       fill="#E8DCEE", opacity=8, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("ESCALADY", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E4DAE8", justify="center")
r = d.text("ONE STEP PER REPORTING PERIOD", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A898B4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("245.escalady-V1R00")

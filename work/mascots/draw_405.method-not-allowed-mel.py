#!/usr/bin/env python3
"""Method Not Allowed Mel — mascot portrait V1R00.
A clerk of verbs at a service window: laminated card of allowed methods held
to the glass, your DELETE request sliding politely back under it.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Method Not Allowed Mel — Mascot Portrait", 1000, 1000)

INK = "#26221F"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#131B18"}, {"offset": 1, "color": "#070B09"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5148"}, {"offset": 0.7, "color": "#24352C"},
    {"offset": 1, "color": "#101B15"}]}}
FRAME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C8A05C"}, {"offset": 1, "color": "#7C5A28"}]}}
BOOTH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E443A"}, {"offset": 1, "color": "#182720"}]}}
SHIRT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8E0CC"}, {"offset": 1, "color": "#BFB49A"}]}}
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0DDBC"}, {"offset": 1, "color": "#D4B88E"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4F0DE"}, {"offset": 1, "color": "#D8D2B8"}]}}
GLASS_TINT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DCEEEC"}, {"offset": 1, "color": "#9ABEBA"}]}}
VISOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8AC49A"}, {"offset": 1, "color": "#4E8A62"}]}}
RED = "#B8372A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7A6C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6E6DC", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(194,234,8),(799,231,7),(157,525,9),(838,541,8),
                               (244,764,7),(756,750,9),(135,391,6),(861,395,7),
                               (393,111,7),(611,113,8),(335,821,6),(663,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#385044", opacity=45, stroke=NONE)

# --- the service window ----------------------------------------------------------
# wall opening with brass frame
d.shape("rectangle", "Window opening", x=252, y=196, width=496, height=470,
        fill=BOOTH, stroke=INK, strokeWidth=7, radius=14)
d.shape("rectangle", "Brass frame", x=252, y=196, width=496, height=470,
        fill=NONE, stroke=FRAME, strokeWidth=8, radius=14)
# little sign plate screwed above the window
d.path(rot_rect_path(500, 168, 190, 42, 0), "Sign plate", fill=FRAME,
       stroke=INK, strokeWidth=5)
r0 = d.text("REQUESTS", "Sign word", x=500, y=176, size=17,
            font="Virelai Sans", color="#2E2114", justify="center")
if r0 and r0.get("id"):
    d.cmd("text.setStyle", "sign track", ids=[r0["id"]], tracking=140)

# --- Mel, behind the glass ----------------------------------------------------------
# shirt + collar
d.path("M500,470 C575,470 630,520 638,600 L642,666 L358,666 L362,600 "
       "C370,520 425,470 500,470 Z", "Shirt", fill=SHIRT, stroke=INK,
       strokeWidth=7)
d.path("M466,478 L500,540 L534,478", "Collar V", fill=NONE, stroke=INK,
       strokeWidth=5, join="round")
d.path("M486,548 L514,548 L510,572 L490,572 Z", "Bowtie knot", fill="#5E4A3A",
       stroke=INK, strokeWidth=4, join="round")
d.path("M458,540 L490,556 L458,572 Z M542,540 L510,556 L542,572 Z",
       "Bowtie wings", fill="#5E4A3A", stroke=INK, strokeWidth=4, join="round")
# head
d.shape("ellipse", "Head", x=412, y=288, width=176, height=160,
        fill=FACE, stroke=INK, strokeWidth=7)
# clerk's translucent green visor
d.path("M414,330 C420,288 580,288 586,330 L586,352 C560,322 440,322 414,352 Z",
       "Visor", fill=VISOR, stroke=INK, strokeWidth=6, join="round",
       opacity=90)
d.path("M404,346 L596,346 L586,368 L414,368 Z", "Visor brim", fill=VISOR,
       stroke=INK, strokeWidth=5, join="round", opacity=80)
d.path("M428,306 C470,290 530,290 572,306", "Visor sheen", fill=NONE,
       stroke="#EAFBEE", strokeWidth=5, cap="round", opacity=45)
# half-moon spectacles + bridge
d.shape("ellipse", "Lens L", x=440, y=378, width=52, height=44, fill="#FBF6E8",
        stroke=INK, strokeWidth=4, opacity=75)
d.shape("ellipse", "Lens R", x=508, y=378, width=52, height=44, fill="#FBF6E8",
        stroke=INK, strokeWidth=4, opacity=75)
d.path("M492,392 C496,388 504,388 508,392", "Specs bridge", fill=NONE,
       stroke=INK, strokeWidth=4)
d.path("M436,390 L414,384 M564,390 L586,384", "Specs arms", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# eyes through the lenses — gentle, unbothered
d.shape("ellipse", "Eye L", x=456, y=392, width=12, height=14, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Eye R", x=532, y=392, width=12, height=14, fill=INK,
        stroke=NONE)
# the polite, infuriating smile
d.path("M470,438 C485,448 515,448 530,438", "Smile", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.shape("ellipse", "Cheek L", x=440, y=428, width=26, height=14,
        fill="#E8AFA0", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=534, y=428, width=26, height=14,
        fill="#E8AFA0", opacity=45, stroke=NONE)

# --- the laminated card, held up against the glass -----------------------------------
d.path("M552,430 L726,462 L706,606 L532,574 Z", "Card", fill=CARD,
       stroke=INK, strokeWidth=6, join="round")
# laminate gloss: one diagonal sheen band
d.path("M596,438 L640,447 L560,580 L530,575 Z", "Card sheen", fill="#FFFFFF",
       opacity=28, stroke=NONE)
r1 = d.text("ALLOWED METHODS", "Card head", x=627, y=486, size=13,
            font="Virelai Sans", color="#4A4030", justify="center")
if r1 and r1.get("id"):
    d.cmd("text.setStyle", "card track", ids=[r1["id"]], tracking=60)
d.path("M566,496 L694,521", "Card rule", fill=NONE, stroke="#8A8064",
       strokeWidth=3, opacity=80)
# rows: check + verb (checks drawn — Virelai has no check glyph)
for i, verb in enumerate(["GET", "HEAD", "OPTIONS"]):
    cy = 504 + i*24
    d.path(f"M576,{cy} l7,8 l14,-15", f"Check {i+1}", fill=NONE,
           stroke="#4E8A62", strokeWidth=4, cap="round", join="round")
    d.text(verb, f"Verb {i+1}", x=638, y=cy+9, size=14, font="Virelai Sans",
           color="#3A3226", justify="center")
# everything else: a firm ruled-out line, parallel to the card's tilt
d.path("M566,578 L690,596", "Deny rule", fill=NONE, stroke=RED,
       strokeWidth=5, cap="round", opacity=85)
# arm holding the card from below — fingers under the bottom corner
d.path("M548,640 C552,622 556,610 562,600", "Arm holding card", fill=NONE,
       stroke=SHIRT, strokeWidth=26, cap="round")
d.shape("ellipse", "Hand card", x=544, y=588, width=30, height=26, fill=FACE,
        stroke=INK, strokeWidth=5)

# --- the glass itself ------------------------------------------------------------------
d.shape("rectangle", "Glass pane", x=262, y=206, width=476, height=400,
        fill=GLASS_TINT, stroke=NONE, opacity=16, radius=8)
d.path("M300,600 L470,220 L520,220 L350,600 Z", "Glass streak 1",
       fill="#FFFFFF", opacity=8, stroke=NONE)
d.path("M540,600 L640,380 L700,380 L600,600 Z", "Glass streak 2",
       fill="#FFFFFF", opacity=6, stroke=NONE)

# --- counter + the request sliding back -------------------------------------------------
# counter rail — the glass sits in it, save the little arched slot
d.shape("rectangle", "Counter", x=210, y=640, width=580, height=54,
        fill=FRAME, stroke=INK, strokeWidth=6, radius=8)
d.path("M222,652 L778,652", "Counter top light", fill=NONE, stroke="#F0D49A",
       strokeWidth=3, opacity=50)
# the slot under the glass where requests come back
d.path("M430,640 L430,664 C430,678 570,678 570,664 L570,640 Z", "Slot",
       fill="#14100C", stroke=INK, strokeWidth=4)
# the returned request, half-out of the slot on the viewer's side
d.path(rot_rect_path(490, 726, 190, 84, -4), "Request form", fill=CARD,
       stroke=INK, strokeWidth=5)
r2 = d.text("REQUEST FORM", "Form head", x=484, y=704, size=10,
            font="Virelai Sans", color="#6E5844", justify="center")
if r2 and r2.get("id"):
    d.cmd("text.setStyle", "form track", ids=[r2["id"]], tracking=60)
r3 = d.text("METHOD:  DELETE", "Form method", x=484, y=728, size=13,
            font="Virelai Sans", color="#3A3226", justify="center")
# DELETE, struck through — not the correct kind of doing
d.path("M512,724 L580,721", "DELETE strike", fill=NONE, stroke=RED,
       strokeWidth=4, cap="round", opacity=90)
# the verdict stamp
d.path(rot_rect_path(486, 758, 128, 26, -4), "Stamp box", fill=NONE,
       stroke=RED, strokeWidth=3, opacity=85)
r4 = d.text("NOT A METHOD", "Stamp word", x=486, y=764, size=11,
            font="Virelai Sans", color=RED, justify="center")
if r4 and r4.get("id"):
    d.cmd("text.setStyle", "stamp track", ids=[r4["id"]], tracking=60)
# Mel's fingertips still on the form's far edge, mid-slide
d.path("M382,702 C392,696 402,692 412,690", "Sliding arm", fill=NONE,
       stroke=SHIRT, strokeWidth=22, cap="round")
d.shape("ellipse", "Sliding hand", x=404, y=680, width=28, height=24,
        fill=FACE, stroke=INK, strokeWidth=5)

# --- captions ----------------------------------------------------------------------------
d.text("METHOD NOT ALLOWED MEL", "Name", x=500, y=930, size=48,
       font="Virelai Sans", color="#DDE8DC", justify="center")
r = d.text("VERB GATEKEEPER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9CBCA4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("405.method-not-allowed-mel-V1R00")

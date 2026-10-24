#!/usr/bin/env python3
"""Corelock the Flavor Warden — mascot portrait V1R00.
An Arkansas Black apple warden standing silent before a locked metadata
vault in a shadowed orchard. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Corelock the Flavor Warden — Mascot Portrait", 1000, 1000)

INK = "#2A1620"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16101E"}, {"offset": 1, "color": "#080510"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#54405E"}, {"offset": 0.7, "color": "#332542"},
    {"offset": 1, "color": "#181026"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E2240"}, {"offset": 1, "color": "#120C1C"}]}}
VAULT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6A7288"}, {"offset": 0.72, "color": "#454C60"},
    {"offset": 1, "color": "#242A3A"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#565E72"}, {"offset": 1, "color": "#282E3E"}]}}
APPLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A2438"}, {"offset": 0.68, "color": "#47111F"},
    {"offset": 1, "color": "#220912"}]}}
KEY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4BC62"}, {"offset": 1, "color": "#93702C"}]}}
CARD_TAG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D6B0"}, {"offset": 1, "color": "#B09A6C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E4A6E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFC0DC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#413050", opacity=45, stroke=NONE)

# --- shadowed orchard rows -----------------------------------------------------
d.shape("ellipse", "Orchard L", x=108, y=170, width=220, height=320,
        fill="#120C1C", opacity=60, stroke=NONE)
d.shape("ellipse", "Orchard R", x=700, y=180, width=200, height=310,
        fill="#120C1C", opacity=60, stroke=NONE)
for i, (x, y) in enumerate([(205,320),(235,420),(760,330),(790,430),(180,505)]):
    d.shape("ellipse", f"Hanging dark fruit {i+1}", x=x, y=y, width=18, height=22,
            fill="#2E1220", opacity=75, stroke=NONE)
    d.path(f"M{x+9},{y} L{x+9},{y-10}", f"Fruit stem {i+1}", fill=NONE,
           stroke="#1E2430", strokeWidth=3, cap="round", opacity=70)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0614",
       strokeWidth=4, opacity=70)

# --- the metadata vault: a great round door ------------------------------------
d.shape("ellipse", "Vault shadow", x=280, y=660, width=440, height=34,
        fill="#070410", opacity=55, stroke=NONE)
d.shape("ellipse", "Vault outer", x=268, y=178, width=464, height=464,
        fill=VAULT_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Vault door", x=302, y=212, width=396, height=396,
        fill=DOOR_GRAD, stroke=INK, strokeWidth=5)
# rivets around the rim
for i in range(14):
    a = math.radians(i * (360/14) - 90)
    cx, cy = 500 + 216*math.cos(a), 410 + 216*math.sin(a)
    d.shape("ellipse", f"Rivet {i+1}", x=cx-7, y=cy-7, width=14, height=14,
            fill="#78809A", stroke=INK, strokeWidth=2)
# door banding
for i, y in enumerate([300, 520]):
    d.path(f"M330,{y} L670,{y}", f"Door band {i+1}", fill=NONE,
           stroke="#1C2230", strokeWidth=6, opacity=60)
d.text("METADATA VAULT", "Vault label", x=500, y=262, size=22,
       font="Virelai Sans", color="#A8B0C4", justify="center")
# toe-tag hanging off the door: the vault stayed shut for three days
d.path("M352,556 C356,575 358,590 360,604", "Tag string", fill=NONE,
       stroke="#6A7288", strokeWidth=3, opacity=80)
d.path("M322,604 L398,604 L392,646 L316,646 Z", "Seal tag",
       fill=CARD_TAG, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Tag eyelet", x=352, y=608, width=10, height=10,
        fill="#2A1620", stroke=NONE)
d.text("SEALED 72H", "Tag text", x=355, y=636, size=13,
       font="Virelai Sans", color="#4A3A28", justify="center")
# central lock wheel: ring + spokes + hub
d.shape("ellipse", "Wheel ring", x=425, y=335, width=150, height=150,
        fill=NONE, stroke="#8A92A8", strokeWidth=12)
for i in range(4):
    a = math.radians(i * 90 + 45)
    x2, y2 = 500 + 62*math.cos(a), 410 + 62*math.sin(a)
    d.path(f"M500,410 L{x2:.0f},{y2:.0f}", f"Spoke {i+1}", fill=NONE,
           stroke="#8A92A8", strokeWidth=10, cap="round")
d.shape("ellipse", "Wheel hub", x=482, y=392, width=36, height=36,
        fill="#9AA2B8", stroke=INK, strokeWidth=4)
# keyhole plate below the wheel
d.shape("ellipse", "Keyhole head", x=482, y=520, width=36, height=36,
        fill="#1A2030", stroke=INK, strokeWidth=4)
d.path("M493,548 L507,548 L512,584 L488,584 Z", "Keyhole slot",
       fill="#1A2030", stroke=INK, strokeWidth=4, join="round")

# --- spectral mist hugging the vault base --------------------------------------
d.shape("ellipse", "Mist L", x=230, y=620, width=240, height=46,
        fill="#C8D0E8", opacity=8, stroke=NONE)
d.shape("ellipse", "Mist R", x=540, y=630, width=260, height=42,
        fill="#C8D0E8", opacity=8, stroke=NONE)

# --- the warden: an Arkansas Black apple ---------------------------------------
d.shape("ellipse", "Apple shadow", x=400, y=668, width=200, height=28,
        fill="#070410", opacity=55, stroke=NONE)
# feet, planted wide like a guard
d.shape("ellipse", "Foot L", x=428, y=650, width=48, height=26,
        fill="#1C0A12", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=524, y=650, width=48, height=26,
        fill="#1C0A12", stroke=INK, strokeWidth=4)
# apple body: round with a crown dip and bottom dimples
d.path("M500,468 C516,452 552,448 580,472 C614,500 622,558 600,612 "
       "C586,648 558,670 536,662 C522,656 512,660 500,660 "
       "C488,660 478,656 464,662 C442,670 414,648 400,612 "
       "C378,558 386,500 420,472 C448,448 484,452 500,468 Z",
       "Black apple body", fill=APPLE_GRAD, stroke=INK, strokeWidth=6)
# crimson sheen on the cheek
d.shape("ellipse", "Apple sheen", x=420, y=500, width=60, height=90,
        fill="#A83850", opacity=28, stroke=NONE)
# stem + single dark leaf
d.path("M500,462 C502,442 496,430 488,420", "Stem", fill=NONE,
       stroke="#1E2430", strokeWidth=7, cap="round")
d.path("M478,430 C460,422 454,406 462,394 C480,400 488,414 478,430 Z",
       "Stem leaf", fill="#2E3A30", stroke=INK, strokeWidth=3, join="round")
# warden's face: level stare, flat mouth — the silent kind
d.path("M438,506 L472,516", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
d.path("M528,516 L562,506", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
d.shape("ellipse", "Eye L", x=444, y=520, width=22, height=14,
        fill="#E8D8C0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye R", x=534, y=520, width=22, height=14,
        fill="#E8D8C0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil L", x=452, y=524, width=8, height=8,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=540, y=524, width=8, height=8,
        fill=INK, stroke=NONE)
d.path("M468,584 L532,584", "Flat mouth", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
# left arm folded across the body
d.path("M404,560 C430,596 470,606 512,600", "Arm folded", fill=NONE,
       stroke="#47111F", strokeWidth=18, cap="round")
# right arm out, holding the warden's key upright
d.path("M596,548 C630,540 650,516 656,488", "Arm R", fill=NONE,
       stroke="#47111F", strokeWidth=18, cap="round")
# the key: bow, shaft, two teeth — brass, too big for any door but this one
d.shape("ellipse", "Key bow", x=634, y=396, width=52, height=52,
        fill=NONE, stroke="#C89E46", strokeWidth=10)
d.path("M660,448 L660,540", "Key shaft", fill=NONE, stroke="#C89E46",
       strokeWidth=10, cap="round")
d.path("M660,540 L682,540 M660,516 L678,516", "Key teeth", fill=NONE,
       stroke="#C89E46", strokeWidth=9, cap="round")
d.shape("ellipse", "Key glint", x=646, y=406, width=14, height=14,
        fill="#F4E0A0", opacity=70, stroke=NONE)

# --- fallen apples on the floor ------------------------------------------------
for i, (x, y, s) in enumerate([(310,668,30),(700,672,26),(228,646,22)]):
    d.shape("ellipse", f"Fallen apple {i+1}", x=x, y=y, width=s, height=int(s*0.92),
            fill=APPLE_GRAD, stroke=INK, strokeWidth=3)
    d.path(f"M{x+s/2:.0f},{y} L{x+s/2+2:.0f},{y-9}", f"Fallen stem {i+1}",
           fill=NONE, stroke="#1E2430", strokeWidth=3, cap="round")

# --- captions ------------------------------------------------------------------
d.text("CORELOCK THE FLAVOR WARDEN", "Name", x=500, y=930, size=40,
       font="Virelai Sans", color="#D8CCE4", justify="center")
r = d.text("FLAVOR ENFORCER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9A86AE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("216.corelock-flavorwarden-V1R00")

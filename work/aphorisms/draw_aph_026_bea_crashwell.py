#!/usr/bin/env python3
"""APH-026 Bea Crashwell — motivational-poster aphorism plate V1R00.
A corporate SUCCESS-style poster: black card, gilt frame, big tracked
headline, and where the mountain-at-sunrise should be, a server rack
monolith against an amber dawn — every blade glowing green except the
one pulled out and smoking, wearing a WITNESS toe tag. Punchline in the
caption slot. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-026 Bea Crashwell — Motivational Poster", 1000, 1000)

INK = "#14100C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221A12"}, {"offset": 1, "color": "#0C0806"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E2E1E"}, {"offset": 0.7, "color": "#231A10"},
    {"offset": 1, "color": "#130D08"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E1A15"}, {"offset": 1, "color": "#0D0A07"}]}}
RACK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E3E4A"}, {"offset": 1, "color": "#1E1E28"}]}}
BLADE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A5A68"}, {"offset": 1, "color": "#38383F"}]}}
GOLD = "#B8914A"
FRAME = "#C8B380"
HEAD = "#EDE0C0"
PUNCH = "#D8C49A"
LED_G = "#4CE87A"
LED_R = "#E85A4A"
SMOKE = "#B8BCC8"
CREAM = "#EDE0C0"
FAINT = "#9A8468"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A5A38", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8BE8A", strokeWidth=3, opacity=35)
d.shape("ellipse", "Patina 1", x=200, y=170, width=200, height=110,
        fill="#4E3A24", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=200, height=110,
        fill="#4E3A24", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(215, 280, 7), (790, 255, 8), (165, 480, 6),
                               (838, 475, 7), (250, 655, 6), (755, 665, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#7A5C38", opacity=35, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#2A2118", strokeWidth=4)
# gilt inner frames
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# headline
r = d.text("PERFORMANCE WAS FLAWLESS", "Headline", x=500, y=PY + 60,
           size=26, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "headline tracking", ids=[r["id"]], tracking=40)
# rule + diamond ornament under the headline
d.path("M340,238 L472,238 M528,238 L660,238", "Headline rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 238, 11, 11, 45), "Headline diamond",
       fill=GOLD, opacity=85, stroke=NONE)

# --- the image: server rack at dawn -------------------------------------------------
# amber sunrise glow where the mountain peak would be
d.shape("ellipse", "Dawn glow", x=370, y=255, width=260, height=90,
        fill="#E8A850", opacity=20, stroke=NONE)
d.shape("ellipse", "Dawn core", x=430, y=270, width=140, height=50,
        fill="#F0C070", opacity=25, stroke=NONE)
# floor shadow
d.shape("ellipse", "Rack shadow", x=375, y=505, width=250, height=26,
        fill="#000000", opacity=40, stroke=NONE)
# rack monolith
RX0, RY0, RW0, RH0 = 405, 270, 190, 240
d.shape("rectangle", "Rack", x=RX0, y=RY0, width=RW0, height=RH0,
        radius=5, fill=RACK_GRAD, stroke="#0E0E14", strokeWidth=4)
# top edge sheen
d.path(f"M{RX0 + 8},{RY0 + 8} L{RX0 + RW0 - 8},{RY0 + 8}", "Rack sheen",
       fill=NONE, stroke="#5A5A68", strokeWidth=2.5, opacity=70)
# mounting ears
for i, sy in enumerate([RY0 + 14, RY0 + RH0 - 24]):
    d.shape("rectangle", f"Ear L{i+1}", x=RX0 - 10, y=sy, width=12,
            height=12, radius=2, fill="#2A2A34", stroke="#0E0E14",
            strokeWidth=2)
    d.shape("rectangle", f"Ear R{i+1}", x=RX0 + RW0 - 2, y=sy, width=12,
            height=12, radius=2, fill="#2A2A34", stroke="#0E0E14",
            strokeWidth=2)

PULLED = 4                       # slot index of the doomed blade
for j in range(8):
    sy = RY0 + 12 + j * 27
    if j == PULLED:
        # empty slot: a dark hollow where the blade was
        d.shape("rectangle", f"Slot {j} empty", x=RX0 + 12, y=sy,
                width=RW0 - 24, height=21, fill="#101016",
                stroke="#0E0E14", strokeWidth=2)
        continue
    d.shape("rectangle", f"Blade {j}", x=RX0 + 12, y=sy,
            width=RW0 - 24, height=21, radius=2, fill="#2E2E3A",
            stroke="#14141C", strokeWidth=1.5)
    # status LEDs, all green — the rest glowing
    for k, lx in enumerate([RX0 + 20, RX0 + 30]):
        d.shape("ellipse", f"LED {j}.{k}", x=lx, y=sy + 7, width=6,
                height=6, fill=LED_G, stroke=NONE)
    d.shape("ellipse", f"LEDhalo {j}", x=RX0 + 16, y=sy + 4,
            width=22, height=12, fill=LED_G, opacity=18, stroke=NONE)
    # vent ticks
    for k in range(3):
        tx = RX0 + RW0 - 40 + k * 10
        d.path(f"M{tx},{sy + 5} L{tx},{sy + 16}", f"Vent {j}.{k}",
               fill=NONE, stroke="#14141C", strokeWidth=2)

# --- the pulled blade: smoking, tagged -----------------------------------------------
bsy = RY0 + 12 + PULLED * 27
# half-drawn out of its slot to the right, at a slight dying tilt
d.path(rot_rect_path(RX0 + RW0 + 45, bsy + 14, 130, 20, 5), "Pulled blade",
       fill=BLADE_GRAD, stroke="#14141C", strokeWidth=2.5)
# its dead LED — the only red eye in the rack
d.path(rot_rect_path(RX0 + RW0 + 62, bsy + 9, 7, 7, 5), "Dead LED",
       fill=LED_R, stroke=NONE)
d.shape("ellipse", "Dead LED halo", x=RX0 + RW0 + 56, y=bsy + 4,
        width=18, height=14, fill=LED_R, opacity=25, stroke=NONE)
# smoke wisps curling off the exposed end
d.path("M698,398 C706,380 692,368 700,352 C706,338 698,328 703,316",
       "Smoke 1", fill=NONE, stroke=SMOKE, strokeWidth=4,
       cap="round", opacity=35)
d.path("M708,400 C718,384 706,370 714,354", "Smoke 2", fill=NONE,
       stroke=SMOKE, strokeWidth=3, cap="round", opacity=25)
d.path("M690,402 C684,388 692,376 688,362", "Smoke 3", fill=NONE,
       stroke=SMOKE, strokeWidth=2.5, cap="round", opacity=20)
# a spark or two for good measure
d.shape("ellipse", "Spark 1", x=704, y=386, width=5, height=5,
        fill="#F0C070", opacity=80, stroke=NONE)
d.shape("ellipse", "Spark 2", x=694, y=400, width=4, height=4,
        fill="#F0C070", opacity=60, stroke=NONE)
# the toe tag on the blade's end — the witness, marked
d.path("M700,410 L714,430", "Tag string", fill=NONE, stroke=FRAME,
       strokeWidth=1.5, opacity=80)
d.path(rot_rect_path(722, 444, 66, 26, 8), "Witness tag",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#E4D4AE"},
           {"offset": 1, "color": "#BFA678"}]}},
       stroke="#6E5A38", strokeWidth=2)
d.shape("ellipse", "Tag eyelet", x=710, y=424, width=7, height=7,
        fill=NONE, stroke="#6E5A38", strokeWidth=2)
d.text("WITNESS", "Tag text", x=724, y=449, size=10,
       font="Source Sans 3", color="#4A3A22", justify="center")

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("THE WITNESS HAS BEEN DELETED.", "Punchline", x=500,
           y=PY + PH - 34, size=21, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punchline tracking", ids=[r["id"]], tracking=105)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=GOLD,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("BEA CRASHWELL", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("PERFORMANCE WAS FLAWLESS", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-026-bea-crashwell-V1R00")

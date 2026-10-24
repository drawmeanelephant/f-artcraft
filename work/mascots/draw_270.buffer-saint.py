#!/usr/bin/env python3
"""Buffer Saint — mascot portrait V1R00.
The Saint interposed between a descending hammer and a tall glass pane,
absorbing the impact so the archive can keep writing: the blow lands on
it, the pane only ripples faintly — damage held in a deferred queue.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Buffer Saint — Mascot Portrait", 1000, 1000)

INK = "#2C1E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101218"}, {"offset": 1, "color": "#07080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E6068"}, {"offset": 0.7, "color": "#42444C"},
    {"offset": 1, "color": "#26282E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C3E44"}, {"offset": 1, "color": "#1C1E22"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C0AC88"}, {"offset": 0.7, "color": "#9C8A66"},
    {"offset": 1, "color": "#766448"}]}}
HAMMER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A929C"}, {"offset": 1, "color": "#565E68"}]}}
HANDLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5638"}, {"offset": 1, "color": "#4E3320"}]}}
GLASS = "#A8CCD8"
GOLD = "#D8B464"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8E8E80", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCDCC8", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#484A50", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#101216",
       strokeWidth=4, opacity=70)

# --- the glass pane, right; standing, gleaming, intact ------------------------------
d.shape("ellipse", "Pane sheen floor", x=620, y=672, width=220, height=26,
        fill=GLASS, opacity=10, stroke=NONE)
d.shape("rectangle", "Pane base", x=640, y=686, width=168, height=14,
        fill="#2A2E34", stroke=INK, strokeWidth=3.5, radius=4)
d.shape("rectangle", "Glass pane", x=648, y=298, width=152, height=392,
        fill=GLASS, opacity=13, stroke="#C8DEE8", strokeWidth=4)
d.path("M656,310 L656,678", "Pane edge L", fill=NONE, stroke="#E4F0F4",
       strokeWidth=3, opacity=50)
d.path("M792,310 L792,678", "Pane edge R", fill=NONE, stroke="#E4F0F4",
       strokeWidth=3, opacity=30)
# diagonal reflections
d.path("M664,330 L780,560 M700,312 L788,470", "Pane glare", fill=NONE,
       stroke="#E4F0F4", strokeWidth=5, opacity=18, cap="round")
# the ripple the Saint let through — queued, not delivered
for i, (w, h, op) in enumerate([(64, 54, 22), (104, 88, 14)]):
    d.shape("ellipse", f"Pane ripple {i+1}", x=700-w/2, y=440-h/2,
            width=w, height=h, fill=NONE, stroke="#C8DEE8",
            strokeWidth=3, opacity=op)
# two hairline cracks, already tired of waiting
d.path("M700,440 L734,458 M700,440 L676,478 M700,440 L742,430",
       "Hairline cracks", fill=NONE, stroke="#D8E8EE", strokeWidth=3,
       cap="round", opacity=32)

# --- the hammer, mid-blow from the upper left -----------------------------------------
d.path("M190,235 C250,290 300,330 345,355", "Swing arc 1", fill=NONE,
       stroke="#D8D0B8", strokeWidth=4, cap="round", opacity=28)
d.path("M168,272 C232,322 288,362 338,392", "Swing arc 2", fill=NONE,
       stroke="#D8D0B8", strokeWidth=4, cap="round", opacity=22)
d.path("M185,248 L292,372", "Handle", fill=NONE, stroke="#6A4428",
       strokeWidth=16, cap="round")
d.path("M185,248 L292,372", "Handle grain", fill=NONE, stroke="#8A6238",
       strokeWidth=6, cap="round", opacity=60)
d.path(rot_rect_path(305, 385, 112, 66, 42), "Hammer head",
       fill=HAMMER_GRAD, stroke=INK, strokeWidth=4.5)
d.path(rot_rect_path(288, 372, 50, 8, 42), "Head glint", fill=NONE,
       stroke="#D8E0E6", strokeWidth=4, cap="round", opacity=65)

# --- the impact, absorbed --------------------------------------------------------------
for i, (w, h, op, sw) in enumerate([(72, 58, 30, 4), (112, 90, 22, 3.5),
                                    (152, 122, 15, 3)]):
    d.shape("ellipse", f"Impact ring {i+1}", x=345-w/2, y=428-h/2,
            width=w, height=h, fill=NONE, stroke="#F0E4C4",
            strokeWidth=sw, opacity=op)
d.path("M352,442 L388,458 M330,448 L312,482 M348,412 L336,380",
       "Impact ticks", fill=NONE, stroke="#F0E4C4", strokeWidth=3.5,
       cap="round", opacity=45)

# --- the Saint, holding the shock so the log stays readable -----------------------------
d.shape("ellipse", "Mascot shadow", x=400, y=688, width=190, height=16,
        fill="#0E0A06", opacity=35, stroke=NONE)
d.shape("ellipse", "Body", x=412, y=488, width=164, height=202,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# the stole, worn over the impact
d.path("M452,494 L478,494 L522,676 L496,676 Z", "Stole",
       fill=GOLD, opacity=82, stroke=INK, strokeWidth=2.5)
d.path("M487,540 L487,556 M481,548 L493,548", "Stole mark", fill=NONE,
       stroke="#5E4416", strokeWidth=3, cap="round", opacity=80)
# head, eyes shut against the arithmetic
d.shape("ellipse", "Head", x=426, y=348, width=132, height=128,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for ex in (438, 546):
    d.shape("ellipse", f"Ear {ex}", x=ex-11, y=344, width=26, height=24,
            fill="#9C8A66", stroke=INK, strokeWidth=3.5)
d.path("M458,414 C464,420 472,420 478,414", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M502,414 C508,420 516,420 522,414", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M478,446 C486,451 496,451 504,446", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# halo, still level
d.shape("ellipse", "Halo glow", x=428, y=292, width=128, height=48,
        fill=GOLD, opacity=14, stroke=NONE)
d.shape("ellipse", "Halo", x=446, y=306, width=92, height=22,
        fill=NONE, stroke=GOLD, strokeWidth=5)
# left arm raised into the blow, palm open
d.path("M424,536 C390,505 365,470 352,442", "Arm raised", fill=NONE,
       stroke="#9C8A66", strokeWidth=17, cap="round")
d.shape("ellipse", "Palm up", x=334, y=418, width=28, height=26,
        fill="#9C8A66", stroke=INK, strokeWidth=3.5)
# right arm out toward the pane, marshalling the queue
d.path("M566,540 C600,556 622,588 630,624", "Arm low", fill=NONE,
       stroke="#9C8A66", strokeWidth=17, cap="round")
d.shape("ellipse", "Palm low", x=618, y=618, width=26, height=22,
        fill="#9C8A66", stroke=INK, strokeWidth=3.5)

# --- stray motes of deferred impact ------------------------------------------------------
for i, (x, y, w) in enumerate([(300,300,5),(420,270,5),(590,320,6),(250,470,5),
                               (810,380,5),(560,220,5),(200,600,6)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8E4D4", opacity=35, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("BUFFER SAINT", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#ECE8D6", justify="center")
r = d.text("THE DAMAGE ARRIVES ON TIME", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C0BCA0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("270.buffer-saint-V1R00")

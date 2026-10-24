#!/usr/bin/env python3
"""Ribbon Latency — mascot portrait V1R00.
The oversized ceremonial scissors stand posed for the photograph, blades
open in a proud V, closing on the air where the ribbon should have been.
Between the brass stanchions the ribbon already hangs in two torn halves,
severed ends drooping; the tear pre-dates the tool, on schedule. A camera
flash goes off anyway. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ribbon Latency — Mascot Portrait", 1000, 1000)

INK = "#33161E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#26121C"}, {"offset": 1, "color": "#0F060C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9C8088"}, {"offset": 0.7, "color": "#664852"},
    {"offset": 1, "color": "#37222E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3038"}, {"offset": 1, "color": "#221219"}]}}
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0BC6A"}, {"offset": 1, "color": "#9A7232"}]}}
STEEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8DCE4"}, {"offset": 1, "color": "#7E8494"}]}}
RIBBON_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C84858"}, {"offset": 1, "color": "#8C2636"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#AC8E96", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D4D8", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5A4048", opacity=50, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#180A10",
       strokeWidth=4, opacity=70)

# --- stanchions + the already-torn ribbon ---------------------------------------
for i, sx in enumerate([252, 748]):
    d.shape("ellipse", f"Base {i+1}", x=sx - 36, y=688, width=72,
            height=16, fill=BRASS_GRAD, stroke=INK, strokeWidth=4)
    d.shape("rectangle", f"Post {i+1}", x=sx - 9, y=452, width=18,
            height=240, fill=BRASS_GRAD, stroke=INK, strokeWidth=4,
            radius=6)
    d.shape("ellipse", f"Ball {i+1}", x=sx - 15, y=424, width=30,
            height=30, fill=BRASS_GRAD, stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Ball glint {i+1}", x=sx - 8, y=429, width=9,
            height=9, fill="#FFF4D8", opacity=75, stroke=NONE)

# ribbon left half — strung from the post, severed end drooping at the gap
d.path("M262,442 C340,450 408,462 456,486 L448,494 L460,502 L446,508 L456,520 "
       "C408,498 336,482 262,472 Z", "Ribbon left", fill=RIBBON_GRAD,
       stroke=INK, strokeWidth=4)
# ribbon right half — mirror, hanging off its own tear
d.path("M738,442 C660,450 592,464 546,488 L554,496 L542,504 L556,510 L546,522 "
       "C594,500 664,484 738,472 Z", "Ribbon right", fill=RIBBON_GRAD,
       stroke=INK, strokeWidth=4)
# ribbon sheen — it still photographs beautifully
d.path("M272,452 C344,459 404,470 448,489", "Sheen L", fill=NONE,
       stroke="#F0A0AA", strokeWidth=4, cap="round", opacity=50)
d.path("M728,452 C658,460 600,472 556,492", "Sheen R", fill=NONE,
       stroke="#F0A0AA", strokeWidth=4, cap="round", opacity=50)
# torn strands curling off each severed end
d.path("M452,514 C458,542 448,562 432,574", "Strand L", fill=NONE,
       stroke="#A83242", strokeWidth=5, cap="round")
d.path("M548,516 C542,544 552,566 566,578", "Strand R", fill=NONE,
       stroke="#A83242", strokeWidth=5, cap="round")

# ribbon cuttings already on the floor — the improvisation that beat it
for i, (x0, flip) in enumerate([(330, 1), (650, -1)]):
    d.path(f"M{x0},682 C{x0 + 18 * flip},672 {x0 + 30 * flip},684 "
           f"{x0 + 16 * flip},694 C{x0 + 6 * flip},700 {x0 - 6 * flip},694 "
           f"{x0},686", f"Cutting {i+1}", fill=NONE, stroke="#B03848",
           strokeWidth=6, cap="round", opacity=85)

# --- the scissors, posed ---------------------------------------------------------
d.shape("ellipse", "Scissor shadow", x=430, y=686, width=150, height=18,
        fill="#14080E", opacity=45, stroke=NONE)
# blades open in a V — closing on the air above the tear
d.path("M492,516 C474,444 442,360 406,296 L422,286 C462,350 492,432 506,502 Z",
       "Blade L", fill=STEEL_GRAD, stroke=INK, strokeWidth=5)
d.path("M508,516 C526,444 558,360 594,296 L578,286 C538,350 508,432 494,502 Z",
       "Blade R", fill=STEEL_GRAD, stroke=INK, strokeWidth=5)
d.path("M470,392 C478,438 488,478 496,502", "Edge L", fill=NONE,
       stroke="#F4F6FA", strokeWidth=3, cap="round", opacity=60)
d.path("M530,392 C522,438 512,478 504,502", "Edge R", fill=NONE,
       stroke="#F4F6FA", strokeWidth=3, cap="round", opacity=60)
# the nothing between them: a faint scheduled star where the cut was booked
d.path("M500,330 L500,368 M486,349 L514,349", "Booked cut", fill=NONE,
       stroke="#E8DCC0", strokeWidth=4, cap="round", opacity=55)

# handle shanks sweeping down to the finger loops it stands on
d.path("M494,520 C478,560 462,594 446,618", "Shank L", fill=NONE,
       stroke="#B08A3E", strokeWidth=13, cap="round")
d.path("M506,520 C522,560 538,594 554,618", "Shank R", fill=NONE,
       stroke="#B08A3E", strokeWidth=13, cap="round")
# finger loops — the feet it poses on
for i, cx in enumerate([434, 566]):
    d.shape("ellipse", f"Loop {i+1}", x=cx - 34, y=616, width=68,
            height=76, fill=BRASS_GRAD, stroke=INK, strokeWidth=5)
    d.shape("ellipse", f"Loop hole {i+1}", x=cx - 16, y=636, width=32,
            height=38, fill="#241419", stroke=INK, strokeWidth=3)

# pivot boss — the face, composed for the camera
d.shape("ellipse", "Pivot", x=482, y=500, width=36, height=36,
        fill="#E4C478", stroke=INK, strokeWidth=4.5)
d.shape("ellipse", "Eye L", x=491, y=511, width=5, height=7,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=504, y=511, width=5, height=7,
        fill=INK, stroke=NONE)
d.path("M491,524 C496,528 504,528 509,524", "Photo smile", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")

# --- the photograph: flash + frame brackets ---------------------------------------
d.path("M296,196 L296,250 M269,223 L323,223 M277,204 L315,242 M315,204 L277,242",
       "Flash", fill=NONE, stroke="#F4E8C8", strokeWidth=5,
       cap="round", opacity=85)
d.shape("ellipse", "Flash core", x=289, y=216, width=14, height=14,
        fill="#FFF8E4", opacity=90, stroke=NONE)
d.path("M348,160 L348,178 M357,169 L339,169", "Sparkle 1", fill=NONE,
       stroke="#F4E8C8", strokeWidth=3.5, cap="round", opacity=60)
d.path("M238,268 L238,284 M247,276 L229,276", "Sparkle 2", fill=NONE,
       stroke="#F4E8C8", strokeWidth=3.5, cap="round", opacity=45)
# viewfinder brackets — the photo being taken
for i, (x, y, sx, sy) in enumerate([(210,160,1,1),(790,160,-1,1),
                                    (210,560,1,-1),(790,560,-1,-1)]):
    d.path(f"M{x},{y + 34 * sy} L{x},{y} L{x + 34 * sx},{y}",
           f"Bracket {i+1}", fill=NONE, stroke="#E8D8C0",
           strokeWidth=4, cap="round", opacity=45)

# dust motes in the flash
for i, (x, y, w) in enumerate([(360,300,4),(680,270,5),(220,470,4),(790,450,5),
                               (420,150,4),(600,145,5),(340,620,4),(700,630,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8D8CC", opacity=35, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("RIBBON LATENCY", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E4E6", justify="center")
r = d.text("CEREMONIAL DELAY ENTITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C0A8B0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("280.ribbon-latency-V1R00")

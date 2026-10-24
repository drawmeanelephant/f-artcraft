#!/usr/bin/env python3
"""rc-book.sh — The Binder. Necropolis plate V1R00.
A bookbinder's sewing frame in a chained library: an enormous report
tome stitched spine-up, signature by signature, other bound volumes
hanging by chains along the wall — each a book-report that stays inside
its authorized boundary. Leather, linen thread, and chain. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Book — Necropolis Plate", 1000, 1000)

INK = "#221A12"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#151009"}, {"offset": 1, "color": "#0A0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#54402E"}, {"offset": 0.7, "color": "#322618"},
    {"offset": 1, "color": "#16100E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C2318"}, {"offset": 1, "color": "#120D08"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C422C"}, {"offset": 1, "color": "#332216"}]}}
LEATHER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A3B26"}, {"offset": 1, "color": "#4A2014"}]}}
LEATHER_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C2C1C"}, {"offset": 1, "color": "#361408"}]}}
PAGES = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D3A8"}, {"offset": 1, "color": "#B09B6E"}]}}
PAGES_LT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E2BC"}, {"offset": 1, "color": "#C4AE7E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A744E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D3B0", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#63503A", opacity=35, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A06",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Frame shadow", x=300, y=682, width=400, height=22,
        fill="#050302", opacity=55, stroke=NONE)

# --- the chain rail along the library wall ----------------------------------------
d.path("M170,236 L830,236", "Chain rail", fill=NONE, stroke="#3E3020",
       strokeWidth=6, opacity=85)
for i, rx in enumerate([240, 760]):
    d.shape("ellipse", f"Rail ring {i+1}", x=rx-5, y=234, width=10,
            height=10, fill=NONE, stroke="#7A828C", strokeWidth=3)

def chain(x0, y0, x1, y1, n, label):
    for i in range(n + 1):
        t = i / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        d.shape("ellipse", f"{label} link {i+1}", x=x-3, y=y-4, width=7,
                height=9, fill=NONE, stroke="#7A828C", strokeWidth=2)

# --- chained volumes on the wall -----------------------------------------------------
# left book, hanging tilted from its clasp
d.path("M226,384 L262,368 L312,430 L276,446 Z", "Chained book L", fill=LEATHER,
       stroke=INK, strokeWidth=4, join="round")
d.path("M262,368 L312,430 L304,438 L254,376 Z", "Book L fore-edge", fill=PAGES,
       stroke=INK, strokeWidth=3, join="round")
d.path("M240,392 L288,436", "Book L clasp", fill=NONE, stroke="#C9A24E",
       strokeWidth=4, cap="round")
chain(240, 240, 262, 380, 9, "Chain L")
# right book
d.path("M700,390 L736,374 L780,442 L744,458 Z", "Chained book R",
       fill=LEATHER_DK, stroke=INK, strokeWidth=4, join="round")
d.path("M736,374 L780,442 L772,450 L728,382 Z", "Book R fore-edge",
       fill=PAGES, stroke=INK, strokeWidth=3, join="round")
d.path("M714,398 L762,444", "Book R clasp", fill=NONE, stroke="#C9A24E",
       strokeWidth=4, cap="round")
chain(760, 240, 734, 386, 10, "Chain R")

# --- the sewing frame ---------------------------------------------------------------
# uprights + top bar + base plank
d.shape("rectangle", "Post L", x=352, y=270, width=24, height=320,
        fill=WOOD, stroke=INK, strokeWidth=5, radius=3)
d.shape("rectangle", "Post R", x=624, y=270, width=24, height=320,
        fill=WOOD, stroke=INK, strokeWidth=5, radius=3)
d.shape("rectangle", "Top bar", x=336, y=252, width=328, height=28,
        fill=WOOD, stroke=INK, strokeWidth=5, radius=4)
d.shape("rectangle", "Base plank", x=328, y=588, width=344, height=30,
        fill=WOOD, stroke=INK, strokeWidth=5, radius=4)
d.path("M336,596 L672,596", "Plank highlight", fill=NONE, stroke="#8A6440",
       strokeWidth=3, opacity=50)
# feet
d.shape("rectangle", "Foot L", x=340, y=618, width=60, height=16,
        fill=WOOD, stroke=INK, strokeWidth=4, radius=3)
d.shape("rectangle", "Foot R", x=600, y=618, width=60, height=16,
        fill=WOOD, stroke=INK, strokeWidth=4, radius=3)
# sewing cords stretched between top bar and base (linen)
for i, cx in enumerate([436, 500, 564]):
    d.path(f"M{cx},280 L{cx},588", f"Cord {i+1}", fill=NONE,
           stroke="#E8DCBE", strokeWidth=3, opacity=80)
    d.shape("ellipse", f"Cord tack {i+1}", x=cx-4, y=584, width=8, height=8,
            fill="#B09B6E", stroke=INK, strokeWidth=2)

# --- the great tome, spine-up on the cords ---------------------------------------------
# leather covers splayed open, page block fanned either side of the ridge
d.path("M498,396 C432,412 372,452 340,512 L340,544 L500,532 Z",
       "Cover L", fill=LEATHER, stroke=INK, strokeWidth=5, join="round")
d.path("M502,396 C568,412 628,452 660,512 L660,544 L500,532 Z",
       "Cover R", fill=LEATHER, stroke=INK, strokeWidth=5, join="round")
d.path("M490,404 C436,420 388,456 362,504 L490,522 Z",
       "Page block L", fill=PAGES, stroke=INK, strokeWidth=3, join="round")
d.path("M510,404 C564,420 612,456 638,504 L510,522 Z",
       "Page block R", fill=PAGES_LT, stroke=INK, strokeWidth=3, join="round")
# signature edges: stepped ridges along each fan
for i, (x0, y0, x1, y1) in enumerate([
        (462, 416, 372, 496), (442, 424, 388, 486),
        (538, 416, 628, 496), (558, 424, 612, 486),
        (480, 412, 408, 462), (520, 412, 592, 462)]):
    d.path(f"M{x0},{y0} C{(x0+x1)/2},{(y0+y1)/2-6} {x1},{y1-8} {x1},{y1}",
           f"Signature edge {i+1}", fill=NONE, stroke="#8A7450",
           strokeWidth=2, opacity=60)
# spine ridge with three raised sewing bands over the cords
d.path("M456,406 C478,388 522,388 544,406", "Spine ridge", fill=NONE,
       stroke="#5C2C1C", strokeWidth=12, cap="round")
for i, (lx, ly) in enumerate([(436, 448), (500, 392), (564, 448)]):
    d.path(f"M{lx-6},{ly+4} C{lx-2},{ly-4} {lx+2},{ly-4} {lx+6},{ly+4}",
           f"Sewing loop {i+1}", fill=NONE, stroke="#E8DCBE",
           strokeWidth=3, cap="round")

# --- the needle + trailing thread, mid-stitch -------------------------------------------
d.path("M544,410 C580,440 604,478 612,518 C616,540 612,558 606,572",
       "Trailing thread", fill=NONE, stroke="#E8DCBE", strokeWidth=3,
       opacity=90, cap="round")
d.path("M606,572 L622,584", "Needle", fill=NONE, stroke="#B8C0C8",
       strokeWidth=3, cap="round")
d.shape("ellipse", "Needle eye", x=604, y=570, width=6, height=6,
        fill=NONE, stroke="#B8C0C8", strokeWidth=2)
# spool of linen thread resting on the base
d.shape("rectangle", "Spool", x=668, y=556, width=26, height=34,
        fill=WOOD, stroke=INK, strokeWidth=3, radius=4)
d.path("M668,566 L694,566 M668,578 L694,578", "Spool windings", fill=NONE,
       stroke="#E8DCBE", strokeWidth=3, opacity=85)

# --- fallen signature + awl on the floor --------------------------------------------------
d.path("M250,660 L300,652 L308,680 L256,688 Z", "Fallen signature",
       fill=PAGES, stroke=INK, strokeWidth=3, join="round")
d.path("M262,668 L296,663 M264,676 L298,671", "Signature folds", fill=NONE,
       stroke="#8A7450", strokeWidth=2, opacity=70)
d.path("M716,664 L766,676", "Awl shaft", fill=NONE, stroke="#5C422C",
       strokeWidth=6, cap="round")
d.path("M766,676 L788,682", "Awl point", fill=NONE, stroke="#B8C0C8",
       strokeWidth=3, cap="round")

# --- captions ------------------------------------------------------------------
d.text("RC-BOOK", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E8DAC2", justify="center")
r = d.text("BINDING THE REPORTS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B09B78", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-book-V1R00")

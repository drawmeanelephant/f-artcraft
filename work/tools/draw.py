#!/usr/bin/env python3
"""Draw Fart Knocker (burger-octopus) live in VectorCraft via MCP remote."""
import json, sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_client import MCP

m = MCP(["--connect", "127.0.0.1:7979"])
m.init()

errors = []
done = []

def call(tool, args, label):
    try:
        r = m.call(tool, args)
        done.append(label)
        rid = r.get("id") if isinstance(r, dict) else None
        print(f"ok  {label}  -> {rid if rid else r}")
        return r
    except Exception as e:
        errors.append((label, str(e)))
        print(f"ERR {label}: {e}")
        return None

def shape(shape_, label, **kw):
    a = {"shape": shape_, "name": label}
    a.update(kw)
    return call("draw_shape", a, label)

def path(d, label, **kw):
    a = {"d": d, "name": label}
    a.update(kw)
    return call("draw_path", a, label)

NONE = "none"

# --- new document -----------------------------------------------------------
call("run_command", {"command": "file.new", "params": {
    "name": "Fart Knocker — Vector Self-Portrait",
    "width": 800, "height": 1000, "units": "Pixels",
    "backgroundContents": "white", "colorMode": "rgb"}}, "file.new 800x1000")

# --- backdrop ---------------------------------------------------------------
shape("rectangle", "Background", x=0, y=0, width=800, height=1000, fill="#FBF3E2", stroke=NONE)
shape("ellipse", "Backdrop halo", x=90, y=120, width=620, height=620, fill="#F4E5C4", stroke=NONE)
shape("star", "Sparkle L", cx=108, cy=170, radius1=26, radius2=8, points=4, fill="#E3A008", stroke=NONE)
shape("star", "Sparkle R", cx=694, cy=250, radius1=20, radius2=6, points=4, fill="#E3A008", stroke=NONE)
shape("ellipse", "Ground shadow", x=175, y=878, width=450, height=52, fill="#000000", opacity=10, stroke=NONE)

OCTO = "#C25127"
# --- back tentacles -----------------------------------------------------------
path("M322,728 C235,748 162,722 150,656 C144,616 178,588 210,602 C232,611 230,640 208,644",
     "Tentacle back L", fill=NONE, stroke=OCTO, strokeWidth=62, cap="round")
path("M478,728 C565,748 638,722 650,656 C656,616 622,588 590,602 C568,611 570,640 592,644",
     "Tentacle back R", fill=NONE, stroke=OCTO, strokeWidth=62, cap="round")
# --- octopus body -------------------------------------------------------------
path("M312,622 C296,700 292,790 300,862 L500,862 C508,790 504,700 488,622 C440,600 360,600 312,622 Z",
     "Octopus body", fill=OCTO, stroke=NONE)
# --- mid tentacles ------------------------------------------------------------
path("M332,792 C262,814 204,796 194,738 C187,696 216,672 244,686 C264,696 258,726 236,726",
     "Tentacle mid L", fill=NONE, stroke=OCTO, strokeWidth=62, cap="round")
path("M468,792 C538,814 596,796 606,738 C613,696 584,672 556,686 C536,696 542,726 564,726",
     "Tentacle mid R", fill=NONE, stroke=OCTO, strokeWidth=62, cap="round")
# --- front tentacles ----------------------------------------------------------
path("M368,798 C344,862 300,890 252,872 C212,857 202,812 232,792 C256,776 284,792 280,816 C277,836 254,840 244,824",
     "Tentacle front L", fill=NONE, stroke=OCTO, strokeWidth=68, cap="round")
path("M432,798 C456,862 500,890 548,872 C588,857 598,812 568,792 C544,776 516,792 520,816 C523,836 546,840 556,824",
     "Tentacle front R", fill=NONE, stroke=OCTO, strokeWidth=68, cap="round")
# --- suckers ------------------------------------------------------------------
SUCK = "#F6CD96"
for i, (x, y, w, h) in enumerate([
        (276, 852, 18, 13), (240, 838, 16, 12), (216, 806, 15, 11), (252, 798, 13, 10),
        (506, 852, 18, 13), (544, 838, 16, 12), (569, 806, 15, 11), (535, 798, 13, 10),
        (222, 752, 15, 11), (206, 716, 13, 10), (563, 752, 15, 11), (581, 716, 13, 10)]):
    shape("ellipse", f"Sucker {i+1}", x=x, y=y, width=w, height=h, fill=SUCK, stroke=NONE)

# --- bottom bun (the face) ------------------------------------------------------
shape("rectangle", "Bottom bun", x=168, y=502, width=464, height=152, radius=72, fill="#F0AC5E", stroke=NONE)
path("M196,606 C260,646 540,646 604,606 C540,628 260,628 196,606 Z",
     "Bottom bun shading", fill="#D98E3F", opacity=50, stroke=NONE)
# --- face ---------------------------------------------------------------------
shape("ellipse", "Eye L", x=316, y=548, width=18, height=24, fill="#201812", stroke=NONE)
shape("ellipse", "Eye R", x=466, y=548, width=18, height=24, fill="#201812", stroke=NONE)
shape("ellipse", "Eye glint L", x=320, y=552, width=6, height=6, fill="#FFFFFF", stroke=NONE)
shape("ellipse", "Eye glint R", x=470, y=552, width=6, height=6, fill="#FFFFFF", stroke=NONE)
shape("ellipse", "Cheek L", x=238, y=588, width=30, height=15, fill="#E2703A", opacity=35, stroke=NONE)
shape("ellipse", "Cheek R", x=532, y=588, width=30, height=15, fill="#E2703A", opacity=35, stroke=NONE)
path("M366,590 C384,610 416,610 434,590", "Smile", fill=NONE, stroke="#7A3E14", strokeWidth=6, cap="round")

# --- patty --------------------------------------------------------------------
shape("rectangle", "Beef patty", x=162, y=420, width=476, height=96, radius=46, fill="#5C3421", stroke=NONE)
for i, (x, y, w, h, c) in enumerate([
        (220, 455, 15, 8, "#472818"), (300, 478, 15, 8, "#472818"), (390, 448, 15, 8, "#472818"),
        (470, 480, 15, 8, "#472818"), (560, 452, 15, 8, "#472818"), (520, 436, 13, 7, "#472818"),
        (350, 468, 14, 8, "#74482C"), (430, 460, 14, 8, "#74482C"), (582, 482, 13, 7, "#74482C")]):
    shape("ellipse", f"Patty speckle {i+1}", x=x, y=y, width=w, height=h, fill=c, opacity=75, stroke=NONE)

# --- cheese (with drips) --------------------------------------------------------
path("M158,415 L642,415 L642,450 L610,450 C608,478 582,478 580,450 "
     "C578,512 548,514 546,452 C544,432 528,432 526,450 C524,484 494,486 492,450 "
     "C490,540 458,542 456,452 C454,432 438,432 436,450 C434,486 404,488 402,450 "
     "C400,514 370,516 368,452 C366,432 350,432 348,450 C346,482 318,484 316,450 "
     "C314,506 284,508 282,452 C280,432 264,432 262,450 C260,480 232,482 230,450 "
     "C228,472 200,474 198,452 C196,436 176,434 174,448 L158,450 Z",
     "Cheese with drips", fill="#F7A81B", stroke=NONE)

# --- tomatoes -------------------------------------------------------------------
for label, x in [("Tomato L", 182), ("Tomato R", 422)]:
    shape("rectangle", label, x=x, y=378, width=196, height=46, radius=23, fill="#D93A2B", stroke=NONE)
shape("rectangle", "Tomato C", x=302, y=378, width=196, height=46, radius=23, fill="#D93A2B", stroke=NONE)
for label, x in [("Tomato shine L", 202), ("Tomato shine C", 322), ("Tomato shine R", 442)]:
    shape("rectangle", label, x=x, y=387, width=120, height=11, radius=5, fill="#EE7A68", opacity=80, stroke=NONE)

# --- lettuce --------------------------------------------------------------------
path("M158,380 C178,348 208,400 238,368 C268,338 298,400 328,370 C358,340 388,400 418,370 "
     "C448,340 478,400 508,368 C538,338 568,400 598,370 C618,350 642,358 642,378 L642,396 "
     "C622,418 592,374 562,402 C532,428 502,374 472,402 C442,428 412,374 382,402 "
     "C352,428 322,374 292,402 C262,428 232,374 202,400 C182,416 158,410 158,396 Z",
     "Lettuce shadow", fill="#4C8F31", stroke=NONE)
path("M158,368 C178,336 208,388 238,356 C268,326 298,388 328,358 C358,328 388,388 418,358 "
     "C448,328 478,388 508,356 C538,326 568,388 598,358 C618,338 642,346 642,366 L642,384 "
     "C622,406 592,362 562,390 C532,416 502,362 472,390 C442,416 412,362 382,390 "
     "C352,416 322,362 292,390 C262,416 232,362 202,388 C182,404 158,398 158,384 Z",
     "Lettuce", fill="#66B946", stroke=NONE)

# --- top bun --------------------------------------------------------------------
bun = None
try:
    bun = m.call("draw_path", {"d": "M156,352 C156,208 262,102 400,102 C538,102 644,208 644,352 "
                                        "C644,370 628,380 606,380 L194,380 C172,380 156,370 156,352 Z",
                               "name": "Top bun",
                               "fill": {"gradient": {"kind": "radial", "stops": [
                                   {"offset": 0, "color": "#EBA93E"}, {"offset": 1, "color": "#BC6414"}]}},
                               "stroke": NONE})
    done.append("Top bun (gradient)")
    print("ok  Top bun (gradient)")
except Exception as e:
    errors.append(("Top bun gradient", str(e)))
    print(f"gradient bun failed ({e}); flat fallback")
    path("M156,352 C156,208 262,102 400,102 C538,102 644,208 644,352 "
         "C644,370 628,380 606,380 L194,380 C172,380 156,370 156,352 Z",
         "Top bun", fill="#CE8125", stroke=NONE)
shape("ellipse", "Bun highlight", x=245, y=138, width=210, height=80, fill="#FFFFFF", opacity=15, stroke=NONE)
shape("ellipse", "Bun highlight 2", x=292, y=126, width=90, height=32, fill="#FFFFFF", opacity=12, stroke=NONE)

# --- sesame seeds -----------------------------------------------------------------
seeds = [(330,150),(400,146),(465,152),
         (265,185),(335,182),(410,180),(480,186),(540,192),
         (225,220),(300,218),(375,216),(450,220),(520,222),(575,228),
         (205,255),(275,252),(350,250),(430,254),(505,256),(565,262),
         (215,295),(290,292),(365,290),(445,294),(520,296),(570,300),
         (250,330),(330,328),(470,330),(545,332)]
for i, (x, y) in enumerate(seeds):
    w, h = (16, 9) if i % 2 == 0 else (10, 15)
    shape("ellipse", f"Sesame {i+1}", x=x, y=y, width=w, height=h, fill="#F9DE82", stroke="#D9A441", strokeWidth=1)

# --- bowtie -----------------------------------------------------------------------
path("M398,694 L342,662 C320,650 306,664 308,694 C306,724 320,738 342,726 L398,694 Z",
     "Bowtie L", fill="#1C1C1C", stroke=NONE)
path("M402,694 L458,662 C480,650 494,664 492,694 C494,724 480,738 458,726 L402,694 Z",
     "Bowtie R", fill="#1C1C1C", stroke=NONE)
shape("rectangle", "Bowtie knot", x=381, y=670, width=38, height=48, radius=11, fill="#2A2A2A", stroke=NONE)

# --- monocle (over the right eye, ring rides up over the patty) ---------------------
shape("ellipse", "Monocle glass", x=416, y=503, width=118, height=118, fill="#CFEAF2", opacity=30, stroke=NONE)
shape("ellipse", "Monocle ring", x=416, y=503, width=118, height=118, fill=NONE, stroke="#C99700", strokeWidth=7)
path("M438,528 L464,504", "Monocle glint", fill=NONE, stroke="#FFFFFF", strokeWidth=7, opacity=60, cap="round")
path("M534,562 L636,562", "Monocle bridge", fill=NONE, stroke="#C99700", strokeWidth=6, cap="round")
path("M528,610 C548,668 540,728 500,782", "Monocle chain", fill=NONE, stroke="#C99700",
     strokeWidth=4, dash=[0.1, 12], cap="round")

# --- type ---------------------------------------------------------------------------
call("add_text", {"text": "FART KNOCKER", "x": 400, "y": 30, "size": 46,
                  "font": "Source Sans 3", "color": "#4A2C14", "justify": "center"}, "Title")
call("add_text", {"text": "VECTOR SELF-PORTRAIT · DRAWN LIVE IN VECTORCRAFT", "x": 400, "y": 950, "size": 17,
                  "font": "Source Sans 3", "color": "#A0713F", "justify": "center"}, "Caption")

print(f"\nDONE steps={len(done)} errors={len(errors)}")
for lbl, e in errors:
    print(" -", lbl, ":", e[:300])
json.dump({"done": done, "errors": errors}, open("/home/hatch/workspace/vectorcraft/work/draw-log.json", "w"), indent=1)

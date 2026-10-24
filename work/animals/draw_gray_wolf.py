#!/usr/bin/env python3
"""Gray wolf — field-guide plate V1R00. Head and shoulders in profile, nose
into the wind: level amber eye, ears up, a heavy ruff breaking into hackle
points at the chest. Snow-dusk plate under a dark navy backdrop, wind streaks
carrying snow off the timberline, spruce silhouettes on a drift floor that
closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Gray Wolf — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#171C24"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#161F2E"), (1, "#06090F"))
PLATE_GRAD = rad((0, "#BCC8DA"), (0.55, "#8494B2"), (1, "#4E5E7C"))
COAT_GRAD = lin(0, 280, 0, 720, (0, "#A9ADB8"), (0.55, "#7E8492"), (1, "#565C68"))
DARK_GRAD = lin(0, 280, 0, 560, (0, "#5E6472"), (1, "#3A3F4A"))
PALE_GRAD = rad((0, "#F0F2F6"), (1, "#C6CCD8"))
SNOW_GRAD = lin(0, 730, 0, 880, (0, "#E8EDF4"), (1, "#AAB6C8"))

# --- backdrop + snow-dusk plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#8494B2", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#36445E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8EEF6", strokeWidth=3, opacity=40)
# thin dusk band low on the left horizon — last light on the treeline
d.path("M150,610 C220,596 300,594 380,604 C300,616 220,618 150,610 Z",
       "Dusk band", fill="#E8C89A", opacity=16, stroke=NONE)
# wind streaks: long curves travelling left at nose height and above
for i, (y, op, w_) in enumerate([(250, 20, 7), (300, 16, 5), (352, 14, 4), (430, 18, 6), (505, 12, 4)]):
    d.path(f"M850,{y} C700,{y-18} 520,{y+14} 380,{y-6} C300,{y-14} 230,{y-8} 170,{y+4}",
           f"Wind {i+1}", fill=NONE, stroke="#F0F4FA", strokeWidth=w_, opacity=op, cap="round")
# driven snow
for i, (x, y, w) in enumerate([(200,260,4),(300,180,5),(420,140,4),(620,130,5),(740,200,4),
                               (820,300,4),(160,380,5),(840,420,4),(240,470,4),(700,330,3),
                               (330,330,3),(560,210,3),(180,540,4),(860,540,3),(400,560,3)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w, fill="#FFFFFF", opacity=70, stroke=NONE)

# drift floor: soughing top edge, bottom closes on the disc arc
ly = 745
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path(f"M{CX-ldx:.1f},{ly} C320,724 440,738 540,732 C640,726 700,736 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Drift", fill=SNOW_GRAD, stroke=NONE)
d.path(f"M{CX-ldx+8:.1f},{ly-2} C320,722 440,734 540,728 C640,722 700,732 {CX+ldx-8:.1f},{ly-2}",
       "Drift light", fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=45, cap="round")

# timberline spruces on the drift, right of centre
def spruce(x, base, h, label, op=78):
    w = h * 0.42
    n = 5
    dd = f"M{x-4},{base} L{x+4},{base} L{x+3},{base - h*0.14} "
    for k in range(n):
        f = k / (n - 1)
        yy = base - h * (0.22 + 0.78 * f)
        ww = w * (1 - f * 0.85)
        dd += f"L{x + ww:.1f},{yy + h*0.10:.1f} L{x + ww*0.60:.1f},{yy:.1f} "
    dd += f"L{x},{base - h:.1f} "
    for k in reversed(range(n)):
        f = k / (n - 1)
        yy = base - h * (0.22 + 0.78 * f)
        ww = w * (1 - f * 0.85)
        dd += f"L{x - ww*0.60:.1f},{yy:.1f} L{x - ww:.1f},{yy + h*0.10:.1f} "
    dd += "Z"
    for px, py in [(x - w, base - h * 0.3), (x + w, base - h * 0.3), (x, base - h)]:
        assert on_disc(px, py, 10), (px, py)
    d.path(dd, label, fill="#2A3448", opacity=op, stroke=NONE)
    # snow on the tips
    d.path(f"M{x-3},{base-h*0.99} L{x},{base-h-6} L{x+3},{base-h*0.99} Z",
           f"{label} snowcap", fill="#E8EEF6", opacity=70, stroke=NONE)

spruce(742, ly + 16, 150, "Spruce 1")
spruce(762, ly + 14, 104, "Spruce 2", 66)
spruce(686, ly + 18, 84, "Spruce 3", 56)
spruce(240, ly + 12, 88, "Spruce far", 46)

# --- wolf: head + shoulders in profile, nose into the wind ------------------------
# ears first: their deep bases get buried by the silhouette so they grow out of the skull
d.path("M540,372 C544,332 556,296 578,268 C586,288 594,316 598,344 "
       "C586,362 562,372 540,372 Z",
       "Ear far", fill=DARK_GRAD, stroke=INK, strokeWidth=5)
d.path("M452,376 C460,332 478,292 506,258 C514,250 524,252 530,260 "
       "C544,282 550,316 544,350 C542,362 538,372 532,380 Z",
       "Ear near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# one silhouette: nose tip → muzzle → skull → neck → shoulder → hackled chest → jaw
SILH = ("M296,452 C314,434 348,422 382,416 C404,404 424,386 444,366 "
        "C466,344 498,334 528,338 C556,342 576,360 586,386 "
        "C624,418 650,466 656,524 C662,586 648,656 620,710 "
        "L606,694 L592,716 L576,694 L560,718 L544,696 L528,718 L512,696 "
        "L496,716 L480,694 L466,712 L452,692 L440,706 "
        "C428,664 424,610 430,556 C434,528 422,506 402,496 "
        "C378,492 348,488 330,484 C312,478 298,466 296,452 Z")
d.path(SILH, "Wolf", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# ear details on the visible part
d.path("M478,344 C482,318 492,296 506,282 C512,296 516,316 512,336 "
       "C502,344 488,348 478,344 Z",
       "Ear inner", fill="#3A2E28", opacity=70, stroke=NONE)
d.path("M472,336 C476,314 484,294 498,278", "Ear rim light",
       fill=NONE, stroke="#E8EEF6", strokeWidth=3, opacity=40, cap="round")

# dark saddle down the back of the neck
d.path("M576,396 C616,424 644,470 652,524 C658,580 648,640 626,690 "
       "C620,640 612,580 592,530 C578,490 560,448 546,424 Z",
       "Saddle", fill=DARK_GRAD, opacity=75, stroke=NONE)
for i, dd in enumerate(["M610,470 C622,510 628,556 622,600",
                        "M584,500 C596,540 602,584 598,626",
                        "M636,520 C642,556 640,592 632,624"]):
    d.path(dd, f"Guard hair {i+1}", fill=NONE, stroke="#32363F", strokeWidth=4, opacity=40, cap="round")

# pale cheek + throat ruff, hugging the jaw and dissolving at the chest
d.path("M404,470 C396,496 398,526 412,548 C402,562 402,584 416,600 "
       "C436,620 472,626 500,614 C524,604 538,584 538,560 "
       "C538,536 522,514 498,502 C470,488 436,476 404,470 Z",
       "Cheek ruff", fill=PALE_GRAD, opacity=88, stroke=NONE)
for i, dd in enumerate(["M404,516 C424,524 444,524 458,516",
                        "M406,552 C428,562 452,564 470,556",
                        "M424,586 C444,596 466,600 486,594"]):
    d.path(dd, f"Ruff fur {i+1}", fill=NONE, stroke="#9AA2B0", strokeWidth=4, opacity=45, cap="round")

# muzzle shading: dark bridge, pale lower jaw
d.path("M310,448 C332,432 362,422 392,420 C408,406 426,392 446,380 "
       "C430,398 412,414 400,430 C380,436 354,444 336,456 C326,462 316,458 310,448 Z",
       "Muzzle bridge", fill=DARK_GRAD, opacity=55, stroke=NONE)
d.path("M320,468 C340,476 368,480 392,482 C380,490 354,490 336,484 C326,480 320,475 320,468 Z",
       "Lower jaw pale", fill=PALE_GRAD, opacity=60, stroke=NONE)
# nose leather, tucked onto the muzzle tip
d.path("M294,452 C290,440 296,430 308,428 C320,426 330,434 330,446 C330,458 320,466 308,464 C300,462 296,458 294,452 Z",
       "Nose", fill=rad((0, "#3E4450"), (1, "#14181E")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=300, y=434, width=8, height=5, fill="#FFFFFF", opacity=40, stroke=NONE)
# mouth + lip line
d.path("M318,468 C340,476 364,480 388,482", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M322,460 C328,464 334,466 340,466", "Lip corner",
       fill=NONE, stroke=INK, strokeWidth=3, cap="round")

# the eye: level, amber, reading the wind
d.path("M420,428 C432,412 458,408 476,420 C464,438 436,442 420,428 Z",
       "Eye", fill=rad((0, "#E8B23C"), (0.6, "#B07E20"), (1, "#6E4A10")),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil", x=444, y=419, width=11, height=13, fill="#0E0A04", stroke=NONE)
d.shape("ellipse", "Glint", x=447, y=422, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M416,426 C430,410 460,406 480,418", "Upper lid",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M424,440 C438,446 458,444 472,436", "Lower lid light",
       fill=NONE, stroke="#E8EEF6", strokeWidth=3, opacity=45, cap="round")
d.path("M414,412 C434,400 460,398 480,406", "Brow",
       fill=NONE, stroke="#32363F", strokeWidth=7, opacity=35, cap="round")

# hackle texture along the chest front
for i, dd in enumerate(["M436,600 C430,620 430,644 438,662",
                        "M456,650 C452,668 454,686 462,698",
                        "M620,600 C626,622 626,648 618,670",
                        "M596,640 C600,660 598,680 590,694"]):
    d.path(dd, f"Hackle {i+1}", fill=NONE, stroke="#3A3F4A", strokeWidth=4, opacity=40, cap="round")

# --- caption ---------------------------------------------------------------------------
d.text("GRAY WOLF", "Name", x=500, y=942, size=56, font="Virelai Sans",
       color="#E4EAF2", justify="center")
o = d.text("CANIS LUPUS", "Binomial", x=500, y=976, size=22, font="Virelai Sans",
           color="#9EACC4", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Binomial tracking", ids=[o["id"]], tracking=400)

d.finish("gray-wolf-V1R00")

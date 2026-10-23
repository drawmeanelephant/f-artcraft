#!/usr/bin/env python3
"""Maned wolf — field-guide plate V1R00. Full body, side profile facing left,
to show the absurd leg length: russet coat, black stockings, black mane,
huge ears, white throat and tail tip. Cerrado dusk palette: low sun, grass
tufts and a crooked cerrado tree; the ground band closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Maned Wolf — Field Plate", 1000, 1000)

INK = "#3A2420"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C1A32"}, {"offset": 1, "color": "#0E0812"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFDDB0"}, {"offset": 0.6, "color": "#F0A57C"},
    {"offset": 1, "color": "#A2627E"}]}}
GROUND_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A4A5E"}, {"offset": 1, "color": "#4E2E44"}]}}
COAT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E98A4A"}, {"offset": 0.7, "color": "#C8622C"},
    {"offset": 1, "color": "#94421E"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EE9656"}, {"offset": 0.7, "color": "#CF6A32"},
    {"offset": 1, "color": "#9C4820"}]}}
STOCK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A2A26"}, {"offset": 1, "color": "#120C0B"}]}}
STOCK_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A1E1C"}, {"offset": 1, "color": "#0C0808"}]}}
MANE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E2C28"}, {"offset": 1, "color": "#100A09"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D87A40"}, {"offset": 1, "color": "#A04A22"}]}}
INNER_EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFF4E8"}, {"offset": 1, "color": "#EBC6B4"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8763C"}, {"offset": 1, "color": "#9A4620"}]}}

# --- backdrop + dusk plate --------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A4660", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF0DC", strokeWidth=3, opacity=50)
d.shape("ellipse", "Dusk haze", x=160, y=170, width=260, height=120, fill="#FFE6C8", opacity=14, stroke=NONE)
# low sun behind the wolf's legs
d.shape("ellipse", "Sun glow", x=510, y=500, width=260, height=260, fill="#FFE2B0", opacity=28, stroke=NONE)
d.shape("ellipse", "Sun", x=560, y=560, width=160, height=160, fill="#FFEFC8", opacity=60, stroke=NONE)
for i, (x, y, w) in enumerate([(770,300,6),(820,460,7),(190,360,6),(150,520,7),(400,110,6),
                               (600,112,7),(700,200,5),(300,160,5),(860,560,5),(140,430,5)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#B9707E", opacity=35, stroke=NONE)

# crooked cerrado tree, faint, far left (all vertices inside the disc)
d.path("M222,770 C230,720 214,690 232,650 C244,622 232,600 248,576", "Tree trunk",
       fill=NONE, stroke="#6E3C52", strokeWidth=10, opacity=40, cap="round")
d.path("M232,650 C210,630 196,620 180,618 M244,612 C266,596 280,594 296,598", "Tree branches",
       fill=NONE, stroke="#6E3C52", strokeWidth=6, opacity=40, cap="round")
for i, (x, y, w, h) in enumerate([(150,590,70,36),(214,548,84,44),(268,574,64,34)]):
    d.shape("ellipse", f"Tree crown {i+1}", x=x, y=y, width=w, height=h, fill="#7A4660", opacity=34, stroke=NONE)

# ground band: top edge across, bottom closes on the disc arc
d.path("M222,775 C360,764 640,764 778,775 A420,420 0 0 1 222,775 Z",
       "Ground", fill=GROUND_GRAD, opacity=85, stroke=NONE)
d.path("M240,778 C380,768 620,768 760,778", "Ground rim light", fill=NONE,
       stroke="#FFD2A8", strokeWidth=3, opacity=35, cap="round")
# grass tufts on the horizon
for i, x in enumerate([256, 300, 470, 540, 712, 750]):
    for j, (dx, h, lean) in enumerate([(-6, 26, -8), (0, 36, 2), (6, 24, 10)]):
        d.path(f"M{x+dx},{772} Q{x+dx+lean/2},{772-h/2} {x+dx+lean},{772-h}",
               f"Grass {i+1}.{j+1}", fill=NONE, stroke="#5E3448", strokeWidth=3, opacity=70, cap="round")

d.shape("ellipse", "Wolf shadow", x=330, y=772, width=380, height=24, fill="#3A2030", opacity=35, stroke=NONE)

# --- limb ribbons -------------------------------------------------------------------
def limb(label, pts, widths, fill, **kw):
    n = len(pts)
    L, R = [], []
    for i in range(n):
        ax, ay = pts[max(i - 1, 0)]
        bx, by = pts[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = widths[i] / 2
        L.append((pts[i][0] + nx*w, pts[i][1] + ny*w))
        R.append((pts[i][0] - nx*w, pts[i][1] - ny*w))
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    ex, ey = pts[-1]
    dd += " Q%.1f,%.1f %.1f,%.1f" % (ex, ey + widths[-1]*0.6, R[-1][0], R[-1][1])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(R[:-1])) + " Z"
    d.path(dd, label, fill=fill, **kw)

def paw(label, cx, fill):
    d.path(f"M{cx-18},{782} C{cx-20},{770} {cx-6},{764} {cx+8},{766} "
           f"C{cx+16},{768} {cx+18},{776} {cx+16},{782} Z", label, fill=fill, stroke=INK, strokeWidth=3)

# far legs, behind the body
limb("Leg far front", [(426,470),(436,560),(448,660),(458,740),(462,770)],
     [32,24,20,17,17], STOCK_FAR_GRAD, stroke=INK, strokeWidth=3)
paw("Paw far front", 456, STOCK_FAR_GRAD)
limb("Leg far hind", [(604,470),(606,560),(608,646),(598,700),(590,770)],
     [40,28,20,17,17], STOCK_FAR_GRAD, stroke=INK, strokeWidth=3)
paw("Paw far hind", 584, STOCK_FAR_GRAD)

# --- tail ----------------------------------------------------------------------------
d.path("M662,414 C712,428 746,484 752,546 C756,592 746,626 724,632 "
       "C702,636 696,606 694,580 C688,530 674,486 650,456 Z",
       "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=5)
d.path("M694,576 C698,606 704,634 724,632 C746,628 756,594 752,556 "
       "C738,570 716,578 694,576 Z", "Tail tip white", fill="#FBF2E6", opacity=92, stroke=NONE)
for i, dd in enumerate(["M686,450 C708,480 722,516 728,552", "M700,444 C724,474 738,508 742,540"]):
    d.path(dd, f"Tail fur {i+1}", fill=NONE, stroke="#8A3E1C", strokeWidth=4, opacity=40, cap="round")

# --- body + neck (one shape, rising to the head) ---------------------------------------
d.path("M300,336 C318,384 336,430 350,470 C352,510 380,532 420,524 "
       "C470,506 540,500 610,510 C644,516 672,506 680,476 "
       "C690,440 670,410 640,402 C560,386 470,388 420,392 "
       "C392,370 370,330 356,296 Z",
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# belly shade + back light
d.path("M380,516 C440,500 540,494 640,506", "Belly shade", fill=NONE,
       stroke="#7A3416", strokeWidth=14, opacity=26, cap="round")
d.path("M470,404 C540,398 600,402 650,414", "Back light", fill=NONE,
       stroke="#FFD0A0", strokeWidth=10, opacity=26, cap="round")
d.path("M480,500 C520,486 570,484 610,492", "Belly pale", fill=NONE,
       stroke="#F6C9A0", strokeWidth=8, opacity=30, cap="round")
# white throat bib
d.path("M302,338 C314,372 326,404 336,434 C352,420 356,388 348,348 Z",
       "Throat white", fill="#FBF2E6", opacity=85, stroke=NONE)

# --- near legs (in front), black stockings ------------------------------------------------
limb("Leg near front", [(394,470),(398,560),(396,660),(394,740),(392,772)],
     [36,28,23,19,19], STOCK_GRAD, stroke=INK, strokeWidth=4)
paw("Paw near front", 386, STOCK_GRAD)
limb("Leg near hind", [(628,470),(650,560),(672,648),(664,702),(658,772)],
     [46,32,23,19,19], STOCK_GRAD, stroke=INK, strokeWidth=4)
paw("Paw near hind", 652, STOCK_GRAD)
# stocking sheen
for lbl, dd in [("Front leg sheen", "M388,580 C390,650 388,710 386,750"),
                ("Hind leg sheen", "M652,600 C660,630 664,650 658,700")]:
    d.path(dd, lbl, fill=NONE, stroke="#8A7068", strokeWidth=4, opacity=40, cap="round")

# russet shoulder + haunch overlap the top of the stockings
d.path("M366,430 C398,420 422,452 420,500 C418,532 410,552 398,564 "
       "C384,544 370,500 366,430 Z", "Shoulder", fill=COAT_GRAD, stroke=NONE)
d.path("M590,420 C640,410 678,440 674,490 C670,530 654,560 640,574 "
       "C620,546 602,502 590,420 Z", "Haunch", fill=COAT_GRAD, stroke=NONE)
d.path("M398,564 C410,552 418,532 420,500", "Shoulder edge", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=60, cap="round")
d.path("M640,574 C654,560 670,530 674,490", "Haunch edge", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=60, cap="round")
d.shape("ellipse", "Haunch light", x=604, y=436, width=52, height=34, fill="#FFD0A0", opacity=24, stroke=NONE)

# --- black mane: nape to mid-back, tufted lower edge -------------------------------------
d.path("M336,274 C352,306 378,346 412,374 C452,394 498,392 540,392 "
       "L528,406 L506,400 L494,414 L472,404 L456,418 L440,404 L422,414 "
       "L414,398 L396,400 L398,384 L378,382 L382,366 L364,360 L370,344 "
       "L352,336 L356,318 L340,308 Z",
       "Mane", fill=MANE_GRAD, stroke=INK, strokeWidth=3)
for i, dd in enumerate(["M350,296 C366,326 388,356 416,378", "M430,386 C460,394 494,396 524,396"]):
    d.path(dd, f"Mane sheen {i+1}", fill=NONE, stroke="#7A625A", strokeWidth=4, opacity=45, cap="round")

# --- ears + head ---------------------------------------------------------------------------
d.path("M330,276 C334,226 346,188 366,158 C380,190 384,236 372,284 Z",
       "Ear far", fill=EAR_GRAD, stroke=INK, strokeWidth=4)
d.path("M341,268 C344,232 352,204 364,182 C372,206 374,240 366,272 Z",
       "Ear far inner", fill="#E8C0AE", opacity=60, stroke=NONE)
d.path("M352,268 C372,284 376,318 362,342 C346,364 316,370 292,372 "
       "C266,374 240,368 220,358 C208,352 210,340 220,334 "
       "C246,320 268,298 290,280 C308,266 332,260 352,268 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=6)
# dark muzzle
d.path("M264,312 C248,326 232,330 220,334 C208,340 208,352 220,358 "
       "C236,366 252,370 270,372 C262,352 260,332 264,312 Z",
       "Muzzle dark", fill=MANE_GRAD, opacity=90, stroke=NONE)
d.path("M218,334 C210,336 204,342 206,348 C210,354 220,352 224,346 Z",
       "Nose", fill="#0E0908", stroke=NONE)
d.path("M226,360 C240,366 256,368 270,368", "Mouth", fill=NONE,
       stroke="#0E0908", strokeWidth=4, cap="round")
# white cheek / jaw patch
d.path("M282,370 C300,368 322,364 340,354 C330,368 312,376 290,378 Z",
       "Jaw white", fill="#FBF2E6", opacity=80, stroke=NONE)
d.path("M300,280 C322,272 342,274 352,284", "Crown light", fill=NONE,
       stroke="#FFD8B0", strokeWidth=8, opacity=30, cap="round")
# amber eye
d.shape("ellipse", "Eye", x=280, y=304, width=22, height=15, fill="#E8A030", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=288, y=305, width=8, height=13, fill="#1A0E08", stroke=NONE)
d.shape("ellipse", "Eye glint", x=284, y=307, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M276,306 C284,298 298,298 306,304", "Upper lid", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# near ear: huge, upright
d.path("M298,288 C292,236 298,190 314,150 C336,176 356,226 350,274 Z",
       "Ear near", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
d.path("M308,276 C305,238 309,202 316,174 C330,198 342,232 340,266 Z",
       "Ear near inner", fill=INNER_EAR_GRAD, opacity=88, stroke=NONE)
d.path("M306,270 C303,232 306,196 314,164", "Ear rim shade", fill=NONE,
       stroke="#7A3416", strokeWidth=4, opacity=35, cap="round")

# --- name -------------------------------------------------------------------------------------
d.text("MANED WOLF", "Name", x=500, y=960, size=48, font="Virelai Sans",
       color="#F6DCC8", justify="center")

d.finish("maned-wolf-V1R00")

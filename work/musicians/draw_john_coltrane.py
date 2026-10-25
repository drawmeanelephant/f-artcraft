#!/usr/bin/env python3
"""John Coltrane — milestone card V1R00. Tenor sax mid-phrase on a neck
strap, head tipped down over the horn, eyes closed — sheets-of-sound
energy inside an otherwise still figure. Deep indigo plate, dim haze.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("John Coltrane — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#18141A"                    # warm dark ink, never pure black


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def rot_ellipse(cx, cy, a, b, deg):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    pts = []
    for i in range(8):
        u = 2 * math.pi * i / 8
        x, y = a * math.cos(u), b * math.sin(u)
        pts.append((cx + x * c - y * s, cy + x * s + y * c))
    return smooth(pts)


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def rim_x(y, side=-1):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)


def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit


BG_GRAD = lin(0, 0, 0, 1000, (0, "#131020"), (1, "#060510"))
PLATE_GRAD = rad((0, "#6E628E"), (0.5, "#463C66"), (1, "#1E1A30"))
SUIT_GRAD = lin(350, 600, 660, 800, (0, "#2C2A38"), (0.55, "#1A1824"), (1, "#0C0A12"))
SUIT_DIM = lin(350, 600, 660, 800, (0, "#1E1C28"), (1, "#0A0810"))
SKIN_GRAD = rad((0, "#96623A"), (0.6, "#6E4426"), (1, "#442412"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#3A3650"), (0.55, "#282438"), (1, "#12101C"))
BRASS_GRAD = lin(520, 500, 650, 720, (0, "#D8B468"), (0.55, "#A8843C"), (1, "#5C441C"))

# --- backdrop + deep indigo plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A2440", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C0BCD8", strokeWidth=3, opacity=38)

# a dim violet pool high left + sparse haze — the room is quiet
d.shape("ellipse", "Light pool", x=260, y=150, width=400, height=240,
        fill="#C8C4E0", opacity=11, stroke=NONE)
for i, (x, y, w) in enumerate([(345, 320, 90), (590, 240, 70), (722, 350, 80),
                               (265, 470, 60), (748, 495, 64), (475, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#C0BCD4", opacity=9, stroke=NONE)

# --- club floor, closing on the disc arc ---------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#7E7898", strokeWidth=5, opacity=36, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=330, y=758, width=380, height=30,
        fill="#08070E", opacity=34, stroke=NONE)

# --- Coltrane: half-figure, head bowed over the tenor --------------------------------
# forearms first — both come forward onto the horn, roots under the torso
# left forearm (viewer's left) rising to the upper stack
d.path(smooth([(372, 700), (400, 664), (436, 636), (478, 612),
               (512, 596), (532, 598), (534, 618), (514, 632),
               (478, 648), (442, 672), (410, 706), (390, 730)]),
       "Forearm L", fill=SUIT_GRAD, stroke=INK, strokeWidth=5)
# right forearm (viewer's right) in to the lower stack
d.path(smooth([(636, 688), (620, 660), (602, 642), (580, 632),
               (562, 634), (556, 652), (568, 668), (592, 684),
               (614, 704), (630, 726)]),
       "Forearm R", fill=SUIT_GRAD, stroke=INK, strokeWidth=5)

# torso — plain dark suit widening to the floor
d.path(smooth([(354, 634), (330, 684), (340, 742), (356, 790),
               (658, 790), (666, 724), (652, 662), (616, 624),
               (566, 594), (470, 590), (410, 602)]),
       "Suit", fill=SUIT_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the torso turns
d.path(smooth([(568, 596), (616, 626), (650, 670), (660, 732),
               (654, 788), (568, 790), (562, 712), (554, 642)]),
       "Suit shade", fill=SUIT_DIM, opacity=58, stroke=NONE)
# shirt wedge + narrow dark tie
d.path(smooth([(456, 598), (480, 642), (494, 704), (498, 782),
               (530, 784), (532, 704), (524, 642), (508, 602),
               (482, 594)]),
       "Shirt front", fill=lin(476, 602, 526, 782, (0, "#E2E0EA"), (1, "#A8A4B8")),
       stroke=INK, strokeWidth=3.5)
d.path(smooth([(488, 610), (499, 616), (507, 610), (511, 646),
               (505, 706), (496, 742), (488, 706), (484, 646)]),
       "Tie", fill=lin(488, 610, 507, 742, (0, "#201C2C"), (1, "#0E0C14")),
       stroke=INK, strokeWidth=3)
# notch lapels
d.path(smooth([(456, 596), (432, 632), (424, 694), (438, 760),
               (468, 780), (480, 760), (468, 700), (480, 648),
               (472, 616)]),
       "Lapel L", fill=lin(434, 602, 474, 780, (0, "#38344A"), (1, "#181422")),
       stroke=INK, strokeWidth=3.5)
d.path(smooth([(514, 598), (534, 634), (542, 700), (532, 770),
               (550, 780), (560, 722), (552, 658), (542, 618)]),
       "Lapel R", fill=lin(532, 602, 558, 780, (0, "#38344A"), (1, "#181422")),
       stroke=INK, strokeWidth=3.5)

# neck — mostly swallowed: the bowed head drives the chin into the collar
d.path("M464,548 C464,558 462,568 458,578 C470,588 492,588 504,578 "
       "C500,568 498,556 498,546 Z", "Neck", fill=lin(460, 546, 500, 588,
       (0, "#845834"), (1, "#5C381C")), stroke=INK, strokeWidth=3.5)

# head — tipped down: crown forward and wide, chin tucked to the collar
d.path(smooth([(426, 424), (424, 460), (432, 498), (452, 528),
               (476, 546), (500, 544), (520, 526), (532, 496),
               (534, 454), (526, 412), (504, 384), (476, 374),
               (450, 380)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
# chin-tuck shadow under the jaw
d.path("M460,538 C474,548 492,550 506,544 C498,554 472,554 460,538 Z",
       "Jaw tuck", fill="#3C2210", opacity=45, stroke=NONE)
# ears sit low on a bowed head
d.path("M424,462 C416,466 414,478 420,488 C426,492 432,488 434,478 "
       "C434,468 430,460 424,462 Z", "Ear L", fill="#5C381C",
       stroke=INK, strokeWidth=3)
d.path("M530,458 C538,462 540,474 534,484 C528,488 522,484 520,474 "
       "C520,464 524,456 530,458 Z", "Ear R", fill="#5C381C",
       stroke=INK, strokeWidth=3)

# short cropped hair — a dark cap, clean hairline
d.path(smooth([(426, 432), (420, 396), (432, 360), (462, 338),
               (496, 332), (524, 344), (542, 370), (548, 402),
               (544, 426), (536, 438), (528, 414), (510, 398),
               (484, 392), (458, 396), (438, 410), (430, 434)]),
       "Hair", fill=lin(428, 334, 546, 432, (0, "#241A14"), (1, "#0E0A08")),
       stroke=INK, strokeWidth=4)
d.path("M438,410 C460,394 486,390 512,398", "Hairline", fill=NONE,
       stroke="#0C0806", strokeWidth=3.5, opacity=70, cap="round")

# face — eyes closed mid-phrase; the stillness is the point
# relaxed level brows, riding low because the head is down
d.path("M440,448 C452,442 466,440 478,444", "Brow L", fill=NONE,
       stroke="#221610", strokeWidth=4.5, opacity=80, cap="round")
d.path("M498,444 C510,440 522,440 532,444", "Brow R", fill=NONE,
       stroke="#221610", strokeWidth=4.5, opacity=80, cap="round")
# closed lids — soft downward arcs, a faint crease above each
d.path("M440,466 C450,472 464,474 476,470", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M442,460 C452,464 464,465 474,462", "Crease L", fill=NONE,
       stroke="#4A2C16", strokeWidth=2.5, opacity=55, cap="round")
d.path("M496,464 C506,470 518,472 528,468", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M498,458 C508,462 518,463 526,460", "Crease R", fill=NONE,
       stroke="#4A2C16", strokeWidth=2.5, opacity=55, cap="round")
# nose — foreshortened by the bowed head
d.path("M484,468 C481,480 478,490 475,496 C480,502 489,502 493,497",
       "Nose", fill=NONE, stroke="#4A2C16", strokeWidth=3.5,
       opacity=80, cap="round")
# the moustache — a filled band over the mouthpiece corner
d.path(smooth([(458, 504), (470, 500), (486, 499), (500, 502),
               (502, 510), (488, 514), (472, 514), (460, 510)]),
       "Moustache", fill=lin(458, 500, 502, 514, (0, "#2A1A12"), (1, "#120C08")),
       stroke=NONE)
# mouth hidden behind the mouthpiece — only the lower lip reads
d.path("M464,518 C474,524 490,525 500,520", "Lower lip", fill=NONE,
       stroke="#6E3420", strokeWidth=3.5, opacity=70, cap="round")

# --- the tenor sax on its strap, body down the chest, bell low right -------------------
# neck strap — one thin line from behind the collar to the horn neck join
d.path("M474,568 C502,582 522,586 538,584", "Neck strap", fill=NONE,
       stroke="#100C12", strokeWidth=3, opacity=80, cap="round")

# mouthpiece entering the mouth from below-right
d.path("M498,516 L522,540 L514,548 L490,524 Z", "Mouthpiece",
       fill="#3A2C18", stroke=INK, strokeWidth=2.5)
# the swan neck — tenor neck arcs down-over into the body top
d.path(smooth([(518, 536), (536, 556), (550, 574), (556, 596),
               (544, 598), (534, 580), (522, 562), (506, 550)],
             closed=True),
       "Sax neck", fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
# neck cork band
d.path("M514,544 L526,538 L530,546 L518,552 Z", "Neck cork",
       fill="#C8B088", stroke=INK, strokeWidth=2)
# body tube — long column down the chest, tenor-width
d.path(smooth([(536, 594), (562, 592), (570, 624), (572, 664),
               (566, 694), (550, 706), (536, 698), (532, 664),
               (531, 626)]),
       "Sax body", fill=BRASS_GRAD, stroke=INK, strokeWidth=3.5)
# body tube light — one sheen line along the left edge
d.path("M540,600 C538,630 538,660 542,690", "Body sheen", fill=NONE,
       stroke="#F2DC9E", strokeWidth=3, opacity=55, cap="round")
# the bow — U-bend at the bottom turning out to the bell
d.path(smooth([(552, 700), (570, 706), (592, 702), (610, 688),
               (620, 668), (616, 650), (600, 646), (588, 656),
               (578, 672), (566, 688), (552, 694)]),
       "Bow", fill=BRASS_GRAD, stroke=INK, strokeWidth=3.5)
# bell flare rising off the bow, mouth tilted out toward the viewer
d.path(smooth([(602, 654), (620, 634), (646, 612), (676, 596),
               (686, 606), (674, 626), (652, 650), (626, 666)]),
       "Bell flare", fill=BRASS_GRAD, stroke=INK, strokeWidth=3.5)
d.path(rot_ellipse(682, 602, 30, 48, -42), "Bell mouth",
       fill=rad((0, "#4E340E"), (0.7, "#7C5620"), (1, "#C89C50")),
       stroke=INK, strokeWidth=3.5)
d.path("M664,586 C676,577 692,575 704,582", "Bell lip", fill=NONE,
       stroke="#F2D88E", strokeWidth=4.5, opacity=80, cap="round")
# key column down the body + key-guard dots on the bow
for i, (kx, ky) in enumerate([(552, 606), (553, 626), (554, 646), (556, 666)]):
    d.shape("ellipse", f"Key {i+1}", x=kx - 5, y=ky - 4, width=10, height=8,
            fill=rad((0, "#E8CC8E"), (1, "#96742E")), stroke=INK, strokeWidth=2)
d.path("M584,680 C592,686 606,684 612,676", "Key guard", fill=NONE,
       stroke="#E8CC8E", strokeWidth=3, opacity=70, cap="round")
# octave key pip on the neck
d.path("M534,560 l10,6", "Octave key", fill=NONE, stroke="#E8CC8E",
       strokeWidth=3.5, cap="round")

# faint sound arcs off the bell — the sheets of sound, kept quiet
for i, rr in enumerate((70, 98, 126)):
    a0, a1 = math.radians(-64), math.radians(-14)
    p = "M%.1f,%.1f A%.0f,%.0f 0 0 1 %.1f,%.1f" % (
        682 + rr * math.cos(a0), 602 + rr * math.sin(a0), rr, rr,
        682 + rr * math.cos(a1), 602 + rr * math.sin(a1))
    d.path(p, f"Sound arc {i+1}", fill=NONE, stroke="#D8CCF0",
           strokeWidth=3, opacity=30 - i * 6, cap="round")

# hands over the horn — left high on the stack, right low by the bow
d.path(smooth([(516, 592), (532, 582), (552, 582), (564, 592),
               (562, 608), (548, 618), (530, 616), (516, 606)]),
       "Left hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{526 + i * 2},{598 + i * 6} C536,{594 + i * 6} 548,{594 + i * 6} 556,{600 + i * 6}",
           f"L finger {i+1}", fill=NONE, stroke="#4A2812",
           strokeWidth=3, opacity=70, cap="round")
d.path(smooth([(566, 640), (584, 630), (606, 632), (620, 646),
               (618, 662), (602, 672), (582, 670), (566, 656)]),
       "Right hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{578 + i * 2},{646 + i * 7} C588,{642 + i * 7} 600,{644 + i * 7} 608,{650 + i * 7}",
           f"R finger {i+1}", fill=NONE, stroke="#4A2812",
           strokeWidth=3, opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#241F36", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("JOHN COLTRANE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E2DEEC", justify="center")
LINE2, YEAR, SZ2, TRK = "A LOVE SUPREME · 1965", "1965", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=22, font="Virelai Sans",
           color="#AFA8C8", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)
# Virelai Sans has no digit glyphs — set the year in Source Sans 3
off = len(LINE2[:LINE2.index(YEAR)].encode("utf-8"))
d.cmd("text.setRangeStyle", "Year digits font", id=r["id"], start=off,
      end=off + len(YEAR), font="Source Sans 3")

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("john-coltrane-V1R00")

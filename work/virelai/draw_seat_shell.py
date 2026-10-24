#!/usr/bin/env python3
"""VirelaiOS figcraft sheet — the seat shell, V1R00 (#1262).
Six 1280x720 frames on a 4008x1628 sheet: desktop at rest, window chrome
anatomy, menubar + open menu, notifications, lock curtain, welcome tour.
Geometry copied from the shipped seat: RailHeight 22, ChromeH/W 20/148,
FocusW 216, godMenuW 96, titlebar 28, GOWELCOME 512x384.
Ground truth: VirelaiOS site/desktop.md, user/go/gotabwm/{tabs,seatpaint,
chrome,launcher,lockcurtain}.go, user/go/welcome/{tour,main}.go,
docs/ui-primitives.md v2. Tokens: virelai/design/tokens (sheet of record).
"""
import sys, os, json, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import DARK as DK, WALL_TOP, WALL_BOT

d = Draw()
d.new_doc("VirelaiOS — Seat Shell", 4008, 1628)

UI, UISB, MONO, DISP = "Inter", "Inter SemiBold", "JetBrains Mono", "Virelai Sans"
PAGE_TOP, PAGE_BOT = "#16161F", "#101018"
PANEL, EDGE = "#1D1D29", "#3A3A4E"
TITLE, BODY, MUT, FAINT, MONO_C = "#E8ECF4", "#C9D0DE", "#7E8798", "#565E70", "#9FB2C8"
GOLD = "#E8B95C"

def lin(c0, c1, start, end):
    return {"gradient": {"kind": "linear", "stops": [
        {"offset": 0, "color": c0}, {"offset": 1, "color": c1}],
        "start": [round(v, 1) for v in start], "end": [round(v, 1) for v in end]}}

def rr(x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} L{x+w},{y+h-r} "
            f"Q{x+w},{y+h} {x+w-r},{y+h} L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")

def plate(x, y, w, h, r, label, fill, stroke=EDGE, sw=1, **kw):
    return d.path(rr(x, y, w, h, r), label, fill=fill, stroke=stroke, strokeWidth=sw, **kw)

def T(s, label, x, y, size, font=UI, color=BODY, j="left"):
    return d.text(s, label, x=x, y=y, size=size, font=font, color=color, justify=j)

def ring_in(x, y, w, h, r, label, color=DK["Accent"], sw=2, inset=1):
    d.path(rr(x + inset, y + inset, w - 2 * inset, h - 2 * inset, r - inset), label,
           fill=NONE, stroke=color, strokeWidth=sw)

def cross(cx, cy, s, label, color, sw=1.6):
    d.path(f"M{cx-s},{cy-s} L{cx+s},{cy+s} M{cx+s},{cy-s} L{cx-s},{cy+s}",
           label, fill=NONE, stroke=color, strokeWidth=sw, cap="round")

def fake_shadow(x, y, w, h, r, label):
    d.path(rr(x + 2, y + 4, w + 4, h + 6, r + 2), f"{label} halo",
           fill="#000000", opacity=12, stroke=NONE)
    d.path(rr(x, y + 4, w, h, r), f"{label} core", fill="#000000", opacity=24, stroke=NONE)

# --- page + header -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=4008, height=1628,
        fill=lin(PAGE_TOP, PAGE_BOT, (2004, 0), (2004, 1628)), stroke=NONE)
T("VIRELAIOS", "wordmark", 40, 52, 15, font=DISP, color=GOLD)
T("THE SEAT SHELL", "title", 40, 86, 30, font=DISP, color=TITLE)
T("figcraft design sheet — every frame 1280×720, the real scanout size · "
  "gotabwm chrome · cites virelai/design/tokens · issue #1262",
  "subtitle", 40, 104, 12, font=UI, color=MUT)
T("ground truth: VirelaiOS site/desktop.md · user/go/gotabwm · docs/ui-primitives.md v2",
  "hdr cite", 3968, 52, 11, font=UI, color=FAINT, j="right")
T("shipped geometry — the rail rides the top 22px of the scanout", "hdr note",
  3968, 72, 11, font=UI, color=FAINT, j="right")

# --- shared seat chrome ---------------------------------------------------------
def wall(x, y, w=1280, h=720, label="wall"):
    plate(x, y, w, h, 2, label, lin(WALL_TOP, WALL_BOT, (x, y), (x, y + h)), EDGE)

def rail(x, y, cells, label="rail"):
    """cells: (title, kind) kind in idle|focus|pin|frozen|notify|hover."""
    d.shape("rectangle", f"{label} strip", x=x, y=y, width=1280, height=22,
            fill=DK["Bg"], stroke=NONE)
    cx = x
    for i, (title, kind) in enumerate(cells):
        w = 30 + len(title) * 7 + 18 + (14 if kind == "notify" else 0)
        face = {"idle": DK["BtnIdle"], "focus": DK["Selection"], "pin": DK["BtnIdle"],
                "frozen": DK["BtnIdle"], "notify": DK["BtnIdle"],
                "hover": DK["BtnHover"]}[kind]
        plate(cx, y, w, 22, 3, f"{label} cell {i}", face, NONE)
        tx = cx + 10
        if kind == "pin":
            d.path(f"M{cx+9},{y+7} L{cx+14},{y+11} L{cx+9},{y+15} L{cx+4},{y+11} Z",
                   f"{label} pin {i}", fill=DK["Muted"], stroke=NONE)
            tx = cx + 22
        T(title, f"{label} t {i}", tx, y + 15.5, 12, font=UI, color=DK["Text"])
        if kind == "focus":
            d.path(f"M{cx+1.5},{y} L{cx+1.5},{y+22}", f"{label} mark {i}",
                   fill=NONE, stroke=DK["Accent"], strokeWidth=3)
        if kind == "frozen":
            plate(cx + w - 26, y + 4, 4, 14, 2, f"{label} frz {i}", DK["Warning"], NONE)
        if kind == "notify":
            plate(cx + w - 38, y + 5, 16, 12, 6, f"{label} bdg {i}", DK["Accent"], NONE)
            T("2", f"{label} bdg n {i}", cx + w - 30, y + 14.5, 9, font=UI,
              color=DK["OnAccent"], j="center")
        cross(cx + w - 9, y + 11, 3.5, f"{label} x {i}", DK["Muted"])
        cx += w + 2
    # space pills, right edge — pill wraps name in PadX inside a strip plate
    px = x + 1280 - 8
    for i, (nm, on) in enumerate(reversed([("1", False), ("2", True)])):
        pw = 12 + len(nm) * 7 + 8
        px -= pw
        plate(px, y + 3, pw, 16, 8, f"{label} sp {nm}",
              DK["Accent"] if on else DK["ChromeBg"], NONE)
        T(nm, f"{label} sp t {nm}", px + pw / 2, y + 14.5, 10, font=UI,
          color=DK["OnAccent"] if on else DK["Muted"], j="center")
        px -= 4

def dockband(x, y, focus="GOTERM", label="dock"):
    """bottom chrome: god menu + PWR at left, focus badge + clock at right."""
    by = y + 720 - 28
    # god menu + power buttons — small seat glyphs on the bottom band
    plate(x + 8, by + 4, 96, 20, 4, f"{label} god", DK["Surface"], DK["Border"])
    T("GOD", f"{label} god t", x + 16, by + 18, 10, font=MONO, color=DK["Muted"])
    T("≡", f"{label} god g", x + 94, by + 18, 12, font=UI, color=DK["Muted"], j="center")
    plate(x + 112, by + 4, 108, 20, 4, f"{label} pwr", DK["Surface"], DK["Border"])
    T("SNAP · PWR", f"{label} pwr t", x + 122, by + 18, 10, font=MONO, color=DK["Muted"])
    # focus badge (216) + clock (148) at right, inset 8
    fx = x + 1280 - 8 - 148 - 4 - 216
    plate(fx, by, 216, 20, 10, f"{label} focus", DK["Surface"], DK["Border"])
    T(focus, f"{label} focus t", fx + 14, by + 14.5, 12, font=UI, color=DK["Text"])
    plate(fx + 176, by + 3, 34, 14, 7, f"{label} focus app", DK["Accent"], NONE)
    T("APP", f"{label} focus app t", fx + 193, by + 13.5, 8.5, font=UI,
      color=DK["OnAccent"], j="center")
    plate(x + 1280 - 8 - 148, by, 148, 20, 4, f"{label} clock", DK["Surface"], DK["Border"])
    T("14:32:07", f"{label} clock t", x + 1280 - 8 - 148 + 74, by + 14.5, 12,
      font=UI, color=DK["Text"], j="center")

def toast(x, y, title, sub, label, w=290):
    fake_shadow(x, y, w, 50, 8, f"{label} sh")
    plate(x, y, w, 50, 8, f"{label} pl", DK["Surface"], DK["Border"])
    plate(x + 3, y + 6, 2, 38, 1, f"{label} rule", DK["Accent"], NONE)
    T(title, f"{label} ti", x + 16, y + 21, 13, font=UI, color=DK["Text"])
    T(sub, f"{label} su", x + 16, y + 39, 10, font=UI, color=DK["Muted"])

def caption(x, y, s, label):
    T(s, label, x, y, 10.5, font=UI, color=MUT)

def noteline(x, y, tx, ty, s, label):
    d.path(f"M{x},{y} L{tx},{ty}", f"{label} lead", fill=NONE,
           stroke=FAINT, strokeWidth=1)
    T(s, f"{label} txt", x, y, 10, font=MONO, color=MUT)

# ==== FRAME helper ==============================================================
def frameno(i, name, tag):
    x = 40 + (i % 3) * 1324
    y = 128 if i < 3 else 884
    ly = y - 12
    T(f"0{i+1}", f"f{i} num", x, ly, 15, font=UISB, color=GOLD)
    T(name, f"f{i} name", x + 36, ly, 14, font=UISB, color=TITLE)
    T(tag, f"f{i} tag", x + 1272, ly, 10.5, font=MONO, color=FAINT, j="right")
    wall(x, y)
    return x, y

# ==== FRAME 0 — DESKTOP AT REST =================================================
x, y = frameno(0, "DESKTOP AT REST", "rail h22 · full-viewport tabs · bottom band")
rail(x, y, [("GOFILES", "pin"), ("GOTERM", "focus"), ("GOEDIT", "idle"),
            ("GOSET", "frozen"), ("GOSTORE", "notify")])
# focused tab's viewport: its own buffer on the seam-B model
d.shape("rectangle", "f0 viewport", x=x, y=y + 22, width=1280, height=670,
        fill=DK["Bg"], stroke=NONE)
T("app viewport — the focused tab's own pixel buffer (seam B)", "f0 vp t",
  x + 640, y + 370, 12, font=UI, color=FAINT, j="center")
T("the seat composes on COMPOSITE_TICK; apps never touch the scanout", "f0 vp t2",
  x + 640, y + 390, 10.5, font=UI, color=FAINT, j="center")
dockband(x, y, focus="GOTERM")
noteline(x + 300, y + 52, x + 300, y + 24, "tab rail — cells: pin · focus · idle · frozen · notify", "f0 n1")
noteline(x + 900, y + 640, x + 1100, y + 686, "focus badge + clock — bottom-right", "f0 n2")
noteline(x + 60, y + 660, x + 60, y + 688, "god menu + PWR — bottom-left", "f0 n3")

# ==== FRAME 1 — WINDOW CHROME ANATOMY ===========================================
x, y = frameno(1, "WINDOW CHROME ANATOMY", "titlebar 28 · focus ring inside · snap guide")
# tile-zone overlay (snap guide, mid-drag)
plate(x + 36, y + 76, 560, 600, 8, "f1 zone", DK["Accent"], DK["Accent"], 1.4,
      opacity=16)
plate(x + 36, y + 76, 560, 600, 8, "f1 zone edge", NONE, DK["Accent"], 1.4)
T("TILE ZONE", "f1 zone t", x + 316, y + 636, 13, font=UISB,
  color=DK["Accent"], j="center")
T("pane-tree leaf · ctrl+alt+arrows", "f1 zone t2", x + 316, y + 656, 10.5,
  font=UI, color=DK["Muted"], j="center")
# unfocused window behind
fake_shadow(x + 150, y + 118, 420, 270, 8, "f1 w0 sh")
plate(x + 150, y + 118, 420, 270, 8, "f1 w0", DK["Surface"], DK["Border"])
plate(x + 150, y + 118, 420, 28, 8, "f1 w0 tb", DK["Surface"], DK["Border"])
T("notes — unfocused", "f1 w0 t", x + 166, y + 136, 12, font=UI, color=DK["Muted"])
cm0 = x + 150 + 420 - 12
d.path(f"M{cm0-73},{y+132} L{cm0-63},{y+132}", "f1 w0 g min", fill=NONE,
       stroke=DK["Muted"], strokeWidth=1.6, cap="round")
plate(cm0 - 49, y + 127, 10, 10, 2, "f1 w0 g max", NONE, DK["Muted"], 1.4)
cross(cm0 - 20, y + 132, 4, "f1 w0 g close", DK["Muted"], 1.8)
d.shape("rectangle", "f1 w0 body", x=x + 158, y=y + 154, width=404, height=226,
        fill=DK["ChromeBg"], stroke=NONE)
# focused window, mid-drag offset over the zone
fake_shadow(x + 560, y + 196, 480, 330, 8, "f1 w1 sh")
plate(x + 560, y + 196, 480, 330, 8, "f1 w1", DK["Surface"], DK["Border"])
ring_in(x + 560, y + 196, 480, 330, 8, "f1 w1 ring")
plate(x + 560, y + 196, 480, 28, 8, "f1 w1 tb", DK["Surface"], DK["Border"])
plate(x + 572, y + 202, 16, 16, 4, "f1 w1 icon", DK["Accent"], NONE)
T("G", "f1 w1 icon t", x + 580, y + 214.5, 11, font=UISB, color=DK["OnAccent"], j="center")
T("gofiles — ~/docs", "f1 w1 t", x + 596, y + 214, 12, font=UI, color=DK["Text"])
# controls: min · max · close — 16px glyphs; close hovered tints Danger
cm = x + 560 + 480 - 12
d.path(f"M{cm-73},{y+210} L{cm-63},{y+210}", "f1 g min", fill=NONE,
       stroke=DK["Muted"], strokeWidth=1.6, cap="round")
plate(cm - 49, y + 205, 10, 10, 2, "f1 g max", NONE, DK["Muted"], 1.4)
cross(cm - 20, y + 210, 4, "f1 g close", DK["Danger"], 1.8)
d.shape("rectangle", "f1 w1 body", x=x + 568, y=y + 232, width=464, height=286,
        fill=DK["Bg"], stroke=NONE)
# resize affordance: bottom-right grip
for i in range(3):
    d.path(f"M{x+1028-i*7},{y+520} L{x+1038},{y+510-i*7}", f"f1 grip {i}",
           fill=NONE, stroke=DK["Muted"], strokeWidth=1.5, cap="round")
noteline(x + 1080, y + 210, x + 1042, y + 210, "min · max · close — 16px, PadSM gaps", "f1 n1")
noteline(x + 1080, y + 260, x + 1041, y + 330, "focus ring — 2px inside bounds", "f1 n2")
noteline(x + 1080, y + 500, x + 1036, y + 514, "resize affordance", "f1 n3")
noteline(x + 60, y + 700, x + 90, y + 672, "snap guide — window mid-drag against a tile zone", "f1 n4")

# ==== FRAME 2 — MENUBAR + OPEN MENU =============================================
x, y = frameno(2, "MENUBAR + OPEN MENU", "appkit.MenuBar · row 24 · & mnemonics")
d.shape("rectangle", "f2 app", x=x, y=y + 22, width=1280, height=698,
        fill=DK["Bg"], stroke=NONE)
rail(x, y, [("GOEDIT", "focus")])
# menubar plate under the rail
plate(x, y + 22, 1280, 26, 0, "f2 bar", DK["Surface"], NONE)
d.path(f"M{x},{y+48} L{x+1280},{y+48}", "f2 bar rule", fill=NONE,
       stroke=DK["Border"], strokeWidth=1)
mx = x + 12
for i, m in enumerate(["File", "Edit", "View", "Go", "Help"]):
    w = 16 + len(m) * 8
    if i == 0:
        plate(mx - 6, y + 25, w + 12, 20, 4, "f2 m open", DK["BtnHover"], NONE)
    T(m, f"f2 m {m}", mx, y + 39.5, 13, font=UI, color=DK["Text"])
    mx += w + 24
# open File menu popover
fake_shadow(x + 6, y + 52, 268, 236, 8, "f2 pop sh")
plate(x + 6, y + 52, 268, 236, 8, "f2 pop", DK["Surface"], DK["Border"])
items = [
    ("New Window", "CTRL+N", "idle"), ("New Tab", "CTRL+T", "idle"),
    ("Open…", "CTRL+O", "hover"), ("SEP", "", "sep"),
    ("Save", "CTRL+S", "idle"), ("Save As…", "CTRL+SHIFT+S", "idle"),
    ("Export…", "", "disabled"), ("SEP", "", "sep"),
    ("Close Tab", "CTRL+W", "idle"),
]
for i, (label, accel, st) in enumerate(items):
    ry = y + 58 + i * 25
    if st == "sep":
        d.path(f"M{x+16},{ry+7} L{x+264},{ry+7}", f"f2 sep {i}", fill=NONE,
               stroke=DK["Rule"], strokeWidth=1)
        continue
    if st == "hover":
        plate(x + 12, ry, 256, 24, 4, "f2 row hover", DK["BtnHover"], NONE)
    fg = DK["Muted"] if st == "disabled" else DK["Text"]
    T(label, f"f2 it {i}", x + 20, ry + 16.5, 12.5, font=UI, color=fg)
    if accel:
        T(accel, f"f2 ac {i}", x + 258, ry + 16.5, 10, font=MONO,
          color=DK["Muted"], j="right")
# app content hint below
plate(x + 320, y + 120, 700, 420, 8, "f2 body", DK["ChromeBg"], DK["Border"])
T("app content — MenuBar owns the top row; alt+letter opens a menu", "f2 body t",
  x + 670, y + 320, 12, font=UI, color=FAINT, j="center")
T("rows h24 · accelerators right · disabled = Muted label", "f2 body t2",
  x + 670, y + 342, 10.5, font=UI, color=FAINT, j="center")
noteline(x + 340, y + 90, x + 280, y + 84, "open menu — Surface popover + shared shadow", "f2 n1")

# ==== FRAME 3 — NOTIFICATIONS ====================================================
x, y = frameno(3, "NOTIFICATION CENTER + TOASTS", "kind-12 · 4-deep queue · 8-row history")
rail(x, y, [("GOBUILD", "notify"), ("GOFILES", "focus"), ("GOSTORE", "idle")])
d.shape("rectangle", "f3 vp", x=x, y=y + 22, width=1280, height=698,
        fill=lin(WALL_TOP, WALL_BOT, (x, y), (x, y + 698)), stroke=NONE)
# re-draw wallpaper under chrome (vp paint was opaque; keep gradient look)
# toast stack, bottom-left, 4-deep
stack = [("recovery toast", "machine image parked — reopen to restore", "tst0"),
         ("update ready", "GOSTORE · click to focus tab", "tst1"),
         ("build finished", "GOBUILD · ran 9s — posted on finish", "tst2")]
for i, (ti, su, lb) in enumerate(stack):
    toast(x + 16, y + 470 + i * 62, ti, su, lb)
# notifications center panel, right side
px, py = x + 872, y + 300
fake_shadow(px, py, 380, 380, 8, "f3 nc sh")
plate(px, py, 380, 380, 8, "f3 nc", DK["Surface"], DK["Border"])
plate(px + 3, py + 8, 2, 364, 1, "f3 nc rule", DK["Accent"], NONE)
T("Notifications", "f3 nc t", px + 20, py + 28, 14, font=UISB, color=DK["Text"])
# DND toggle, right of header
plate(px + 330, py + 14, 32, 18, 9, "f3 dnd tr", DK["BtnIdle"], NONE)
d.shape("ellipse", "f3 dnd kn", x=px + 332, y=py + 16, width=14, height=14,
        fill=DK["Ink"], stroke=NONE)
T("DND", "f3 dnd t", px + 328, py + 45, 9, font=MONO, color=DK["Muted"], j="right")
rows = [("●", "GOBUILD — build finished", "14:32"),
        ("●", "GOFILES — copy complete", "14:21"),
        ("●", "GOSTORE — update ready", "13:58"),
        ("●", "GOEDIT — session restored", "13:40"),
        ("●", "seat — recovery toast sent", "12:02")]
for i, (dot, s, tm) in enumerate(rows):
    ry = py + 56 + i * 30
    T(dot, f"f3 r dot {i}", px + 20, ry + 14, 8, font=UI, color=DK["Accent"])
    T(s, f"f3 r {i}", px + 34, ry + 15, 11.5, font=UI, color=DK["Text"])
    T(tm, f"f3 r tm {i}", px + 360, ry + 15, 10, font=MONO, color=DK["Muted"], j="right")
# progress row (kind-22) with cancel
ry = py + 56 + 5 * 30 + 8
plate(px + 14, ry, 352, 44, 4, "f3 prog", DK["ChromeBg"], DK["Border"])
T("GOFILES — copying files", "f3 prog t", px + 26, ry + 18, 11.5, font=UI, color=DK["Text"])
plate(px + 26, ry + 26, 240, 4, 2, "f3 prog tr", DK["Gutter"], NONE)
plate(px + 26, ry + 26, 150, 4, 2, "f3 prog fl", DK["Accent"], NONE)
plate(px + 288, ry + 10, 66, 24, 4, "f3 prog btn", DK["BtnIdle"], DK["Border"])
T("Cancel", "f3 prog btn t", px + 321, ry + 26, 11, font=UI, color=DK["Text"], j="center")
caption(x + 20, y + 660, "toasts: kind-12 · 24-byte message budget · click focuses the sender", "f3 c1")
caption(x + 20, y + 678, "queue 4-deep bottom-left · dropped with a dead sender", "f3 c2")
caption(px, y + 700, "center: 8-row history · survives a seat restart", "f3 c3")

# ==== FRAME 4 — LOCK CURTAIN =====================================================
x, y = frameno(4, "LOCK CURTAIN", "ctrl+shift+l · vault re-auth")
rail(x, y, [("GOTERM", "focus"), ("GOFILES", "idle")])
d.shape("rectangle", "f4 vp", x=x, y=y + 22, width=1280, height=698,
        fill=lin(WALL_TOP, WALL_BOT, (x, y), (x, y + 698)), stroke=NONE)
dockband(x, y)
# the curtain: dim veil over the whole scanout
d.shape("rectangle", "f4 veil", x=x, y=y, width=1280, height=720,
        fill="#0A0A14", opacity=72, stroke=NONE)
# centered credential plate
cx0, cy0 = x + 1280 / 2, y + 720 / 2
fake_shadow(cx0 - 190, cy0 - 90, 380, 196, 8, "f4 card sh")
plate(cx0 - 190, cy0 - 90, 380, 196, 8, "f4 card", DK["Surface"], DK["Border"])
T("\ue001", "f4 mark", cx0, cy0 - 58, 30, font=DISP, color=GOLD, j="center")
T("Screen locked", "f4 card t", cx0, cy0 - 26, 15, font=UISB, color=DK["Text"], j="center")
plate(cx0 - 140, cy0 - 8, 280, 30, 4, "f4 field", DK["ChromeBg"], DK["Border"])
T("••••••••", "f4 dots", cx0 - 126, cy0 + 13, 15, font=UI, color=DK["Text"])
d.path(f"M{cx0+96},{cy0-2} L{cx0+96},{cy0+16}", "f4 caret", fill=NONE,
       stroke=DK["Accent"], strokeWidth=1.5)
T("unlock re-auths the vault passphrase", "f4 hint", cx0, cy0 + 52, 11,
  font=UI, color=DK["Muted"], j="center")
T("no readable credential refuses by name — never a silent no-op", "f4 hint2",
  cx0, cy0 + 70, 9.5, font=UI, color=FAINT, j="center")
noteline(cx0 - 480, cy0 - 110, cx0 - 260, cy0 - 60,
         "curtain dims the whole scanout — a 1×1 sink owns input", "f4 n1")

# ==== FRAME 5 — WELCOME TOUR =====================================================
x, y = frameno(5, "WELCOME TOUR", "GOWELCOME.ELF · 512×384 natural")
rail(x, y, [("GOWELCOME", "focus")])
d.shape("rectangle", "f5 vp", x=x, y=y + 22, width=1280, height=698,
        fill=DK["Bg"], stroke=NONE)
# the tour surface, native 512x384, centered in the viewport
wx, wy = x + (1280 - 512) / 2, y + 22 + (698 - 384) / 2
plate(wx, wy, 512, 384, 2, "f5 tour", DK["Bg"], DK["Border"])
T("Welcome to VirelaiOS", "f5 t title", wx + 12, wy + 30, 15, font=UISB, color=DK["Text"])
T("Five gestures for the first hour", "f5 t sub", wx + 12, wy + 50, 11.5,
  font=UI, color=DK["Muted"])
gest = [("CLICK", "focus a tab — the rail up top lists open windows"),
        ("CTRL+SPACE", "summon the launcher — the whole app catalogue"),
        ("CTRL+TAB", "cycle the open tabs · +shift steps back"),
        ("DRAG", "drag a rail tab to reorder it"),
        ("CTRL+SHIFT+P", "command palette — find anything")]
for i, (k, s) in enumerate(gest):
    gy = wy + 66 + i * 44
    plate(wx + 12, gy, 118, 38, 4, f"f5 chip {i}", DK["Accent"], NONE)
    T(k, f"f5 chip t {i}", wx + 71, gy + 23.5, 10.5, font=UISB,
      color=DK["OnAccent"], j="center")
    T(s, f"f5 desc {i}", wx + 138, gy + 23.5, 11.5, font=UI, color=DK["Text"])
T("Get started — one click opens it:", "f5 head", wx + 12, wy + 300, 11,
  font=UI, color=DK["Muted"])
for i, lb in enumerate(["Settings", "Files", "Store", "Terminal"]):
    bx = wx + 12 + i * 121
    plate(bx, wy + 312, 113, 44, 4, f"f5 btn {i}", DK["BtnIdle"], DK["Border"])
    T(lb, f"f5 btn t {i}", bx + 56.5, wy + 339, 12, font=UI, color=DK["Text"], j="center")
T("1-4 launch · esc closes · reopen from the launcher", "f5 foot",
  wx + 12, wy + 374, 10, font=UI, color=DK["Muted"])
noteline(x + 60, y + 660, wx - 8, wy + 330,
         "first-boot tab — teaches the five moves + four launchers", "f5 n1")

# --- finish ---------------------------------------------------------------------
os.makedirs("work/out", exist_ok=True)
d.finish("seat-shell-V1R00")
res = d.m.request("tools/call", {"name": "render_preview", "arguments": {"max_side": 1600}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/seat-shell-V1R00-preview.png", "wb").write(base64.b64decode(c["data"]))
        print("preview saved")

#!/usr/bin/env python3
"""VirelaiOS figcraft sheet — design tokens + primitives, V1R00 (#1264).
The design-system-of-record later sheets cite. 1920x1408 sheet, dark-theme
specimens at real pixel sizes; color table shows both shipped palettes.
Ground truth: VirelaiOS docs/ui-primitives.md (contract v2),
user/go/theme/theme.go, kernel/src/settings.zig, virelai/notes/style-bible.md.
"""
import sys, os, json, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import DARK as DK, LIGHT as LT, WALL_TOP, WALL_BOT

d = Draw()
d.new_doc("VirelaiOS — Design Tokens + Primitives", 1920, 1408)

UI, UISB, MONO, DIG, DISP = "Inter", "Inter SemiBold", "JetBrains Mono", "Source Sans 3", "Virelai Sans"
VMONO = "Virelai Mono"

# page chrome — the sheet's own surface, deliberately off the token values
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
           fill="#000000", opacity=10, stroke=NONE)
    d.path(rr(x, y + 4, w, h, r), f"{label} core", fill="#000000", opacity=22, stroke=NONE)

def panel(x, y, w, h, title, tag=None):
    plate(x, y, w, h, 10, f"panel {title}", PANEL, EDGE)
    T(title, f"title {title}", x + 20, y + 26, 14, font=UISB, color=TITLE)
    if tag:
        T(tag, f"tag {title}", x + w - 20, y + 26, 10, font=MONO, color=FAINT, j="right")

# --- page ---------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1920, height=1408,
        fill=lin(PAGE_TOP, PAGE_BOT, (960, 0), (960, 1408)), stroke=NONE)

# --- header -------------------------------------------------------------------
T("VIRELAIOS", "wordmark", 40, 58, 17, font=DISP, color=GOLD)
T("TOKENS AND PRIMITIVES", "title", 40, 96, 32, font=DISP, color=TITLE)
T("figcraft design sheet — the design-system-of-record · cites VirelaiOS "
  "docs/ui-primitives.md (contract v2) + user/go/theme/theme.go · issue #1264",
  "subtitle", 40, 118, 12, font=UI, color=MUT)
# theme badges, right side
plate(1660, 44, 220, 28, 14, "badge dark", DK["Bg"], DK["Border"])
d.shape("ellipse", "badge dark dot", x=1674, y=54, width=8, height=8, fill=DK["Accent"], stroke=NONE)
T("DARK — BOOT DEFAULT", "badge dark text", 1690, 62, 11, font=UI, color=DK["Text"])
plate(1430, 44, 216, 28, 14, "badge light", LT["Surface"], LT["Border"])
d.shape("ellipse", "badge light dot", x=1444, y=54, width=8, height=8, fill=LT["Accent"], stroke=NONE)
T("LIGHT — SHIPPED ALTERNATE", "badge light text", 1460, 62, 11, font=UI, color=LT["Text"])
T("theme=custom resolves palette_* at paint", "badge note", 1880, 90, 10,
  font=UI, color=FAINT, j="right")

# ================= PANEL A — COLOR STYLES =====================================
AX, AY, AW, AH = 40, 136, 880, 536
panel(AX, AY, AW, AH, "COLOR STYLES", "theme.Tokens — dark byte-identical to Zig THEME_DARK")
T("ROLE", "A hdr role", AX + 24, AY + 50, 10, font=MONO, color=FAINT)
T("DARK — BOOT", "A hdr dark", AX + 290, AY + 50, 10, font=MONO, color=FAINT)
T("LIGHT — ALT", "A hdr light", AX + 620, AY + 50, 10, font=MONO, color=FAINT)

ROWS = ["Bg", "Surface", "ChromeBg", "Gutter", "Border", "Rule", "Text", "Muted",
        "Ink", "InkMuted", "Accent", "OnAccent", "BtnIdle", "BtnHover", "BtnPressed",
        "Selection", "Danger", "Warning", "Shadow"]
ry = AY + 66
def chip(x, y, w, h, fill, label):
    plate(x, y, w, h, 3, label, fill, "#4A4A5C", 1)
for i, role in enumerate(ROWS):
    y = ry + i * 21
    T(role, f"A role {role}", AX + 24, y + 11, 12, font=MONO, color=BODY)
    if role == "Shadow":
        chip(AX + 290, y, 96, 14, "#000000", "A chip d Shadow")
        T("#000000 · peak 25%", "A hex d Shadow", AX + 396, y + 11, 10, font=MONO, color=MUT)
        chip(AX + 620, y, 96, 14, LT["Shadow"], "A chip l Shadow")
        T("#0F172A · peak 25%", "A hex l Shadow", AX + 726, y + 11, 10, font=MONO, color=MUT)
    else:
        chip(AX + 290, y, 96, 14, DK[role], f"A chip d {role}")
        T(DK[role], f"A hex d {role}", AX + 396, y + 11, 10, font=MONO, color=MUT)
        chip(AX + 620, y, 96, 14, LT[role], f"A chip l {role}")
        T(LT[role], f"A hex l {role}", AX + 726, y + 11, 10, font=MONO, color=MUT)
# Success / Ok split row
y = ry + len(ROWS) * 21
T("Success · Ok", "A role Success", AX + 24, y + 11, 12, font=MONO, color=BODY)
chip(AX + 290, y, 48, 14, DK["Success"], "A chip d Succ")
chip(AX + 338, y, 48, 14, DK["Ok"], "A chip d Ok")
T("#22C55E · #3FB950", "A hex d Succ", AX + 396, y + 11, 10, font=MONO, color=MUT)
chip(AX + 620, y, 96, 14, LT["Success"], "A chip l Succ")
T("#16A34A both", "A hex l Succ", AX + 726, y + 11, 10, font=MONO, color=MUT)
# Wallpaper gradient row
y += 21
T("Wallpaper", "A role Wall", AX + 24, y + 11, 12, font=MONO, color=BODY)
plate(AX + 290, y, 96, 14, 3, "A chip d Wall",
      lin(WALL_TOP, WALL_BOT, (AX + 290, y), (AX + 386, y)), "#4A4A5C", 1)
T("#1A1A2E→#0A0A14", "A hex d Wall", AX + 396, y + 11, 10, font=MONO, color=MUT)
plate(AX + 620, y, 96, 14, 3, "A chip l Wall",
      lin(LT["WallpaperTop"], LT["WallpaperBot"], (AX + 620, y), (AX + 716, y)), "#4A4A5C", 1)
T("#F1F5F9→#E2E8F0", "A hex l Wall", AX + 726, y + 11, 10, font=MONO, color=MUT)
T("Caret = Accent · gradient is the seat desktop's one sanctioned surface",
  "A foot", AX + 24, AY + AH - 12, 10, font=UI, color=FAINT)

# ================= PANEL B — TYPE STYLES ======================================
BX, BY, BW, BH = 940, 136, 460, 536
panel(BX, BY, BW, BH, "TYPE STYLES", "user/go/ttf role faces")
T("INTER — UI", "B h inter", BX + 20, BY + 52, 10, font=MONO, color=FAINT)
specs = [(11, "Badges, captions, rail pills"), (13, "Chrome labels — the nominal"),
         (15, "Section titles inside apps"), (17, "Dialog and empty-state titles")]
sy = BY + 82
for size, s in specs:
    T(s, f"B spec {size}", BX + 20, sy, size, font=UI, color=BODY)
    T(str(size), f"B tag {size}", BX + BW - 20, sy, 10, font=MONO, color=MUT, j="right")
    sy += 30
T("FIRA CODE — CODE / TERMINAL · 13", "B h code", BX + 20, sy + 14, 10, font=MONO, color=FAINT)
for i, s in enumerate(["seat: 2 tabs — focus GOFILES", "tabapp.Notify(kind 12)",
                       "ctrl+shift+p  palette"]):
    T(s, f"B code {i}", BX + 20, sy + 36 + i * 20, 12, font=VMONO, color="#A9C1DE")
T("specimen set in Virelai Mono — Fira Code ships in the OS image",
  "B code note", BX + 20, sy + 96, 10, font=UI, color=FAINT)
T("VIRELAI SANS — DISPLAY / WORDMARK", "B h disp", BX + 20, sy + 130, 10, font=MONO, color=FAINT)
T("VIRELAI", "B spec disp", BX + 20, sy + 170, 34, font=DISP, color=GOLD)
T("no digit glyphs — digits set in Source Sans 3", "B disp note",
  BX + 20, sy + 192, 11, font=UI, color=MUT)
r = T("PLATE V1R02", "B spec digits", BX + 20, sy + 222, 18, font=DISP, color=BODY)
if r:
    d.cmd("text.setStyle", "B digit 1", id=r["id"], font=DIG, start=7, end=8)
    d.cmd("text.setStyle", "B digit 02", id=r["id"], font=DIG, start=9, end=11)
T("0123456789 — Source Sans 3 digit fallback", "B spec ss3", BX + 20, sy + 252, 14,
  font=DIG, color=BODY)
T("roles: ui → Inter · code → Fira Code · symbol → VirelaiChrome (PUA E000–E01D)",
  "B foot", BX + 20, BY + BH - 32, 10, font=UI, color=FAINT)
T("wordmark + mascot mark → Virelai Sans (mark at U+E001)",
  "B foot 2", BX + 20, BY + BH - 16, 10, font=UI, color=FAINT)

# ================= PANEL C — GEOMETRY + EFFECTS ===============================
CX0, CY0, CW, CH = 1420, 136, 460, 536
panel(CX0, CY0, CW, CH, "GEOMETRY + EFFECTS", "contract §2.2–2.5")
T("SPACING — shown ×8", "C h space", CX0 + 20, CY0 + 52, 10, font=MONO, color=FAINT)
for i, (name, v) in enumerate([("PadXS", 2), ("PadSM", 4), ("PadMD", 8), ("PadLG", 16)]):
    y = CY0 + 66 + i * 22
    T(f"{name} {v}", f"C pad {name}", CX0 + 20, y + 10, 10, font=MONO, color=BODY)
    plate(CX0 + 120, y, v * 8, 12, 2, f"C bar {name}", DK["Accent"], NONE)
T("composed values sum adjacent steps — 12 = 8 + 4", "C pad note",
  CX0 + 20, CY0 + 168, 10, font=UI, color=FAINT)
T("CORNER RADII — clamp min(w,h)/2", "C h radii", CX0 + 20, CY0 + 196, 10, font=MONO, color=FAINT)
plate(CX0 + 20, CY0 + 210, 120, 30, 4, "C r4", DK["BtnIdle"], DK["Border"])
T("control 4", "C r4 t", CX0 + 20, CY0 + 256, 10, font=MONO, color=MUT)
plate(CX0 + 170, CY0 + 210, 120, 30, 8, "C r8", DK["Surface"], DK["Border"])
T("window 8", "C r8 t", CX0 + 170, CY0 + 256, 10, font=MONO, color=MUT)
plate(CX0 + 320, CY0 + 210, 120, 30, 15, "C rpill", DK["Selection"], DK["Border"])
T("pill h/2", "C rpill t", CX0 + 320, CY0 + 256, 10, font=MONO, color=MUT)
T("STROKES", "C h strokes", CX0 + 20, CY0 + 288, 10, font=MONO, color=FAINT)
d.path(f"M{CX0+20},{CY0+312} L{CX0+220},{CY0+312}", "C border line", fill=NONE,
       stroke=DK["Border"], strokeWidth=1)
T("BorderW 1 — every border", "C border t", CX0 + 232, CY0 + 316, 10, font=MONO, color=BODY)
plate(CX0 + 20, CY0 + 330, 130, 26, 4, "C focus chip", DK["BtnIdle"], DK["Border"])
ring_in(CX0 + 20, CY0 + 330, 130, 26, 4, "C focus ring")
T("FocusW 2 — inside bounds", "C focus t", CX0 + 162, CY0 + 347, 10, font=MONO, color=BODY)
T("ELEVATION — one shared shadow", "C h elev", CX0 + 20, CY0 + 388, 10, font=MONO, color=FAINT)
fake_shadow(CX0 + 20, CY0 + 404, 150, 44, 8, "C shadow")
plate(CX0 + 20, CY0 + 404, 150, 44, 8, "C float plate", DK["Surface"], DK["Border"])
T("floating plate", "C plate t", CX0 + 95, CY0 + 430, 11, font=UI, color=DK["Text"], j="center")
T("dy 4 · blur 16 · Shadow peak 25%", "C elev t1", CX0 + 190, CY0 + 420, 10, font=MONO, color=BODY)
T("floating plates only — content casts none", "C elev t2", CX0 + 190, CY0 + 438, 10, font=UI, color=MUT)
T("FIXED MEASURES", "C h meas", CX0 + 20, CY0 + 472, 10, font=MONO, color=FAINT)
# mini titlebar 28
plate(CX0 + 20, CY0 + 486, 240, 28, 4, "C titlebar", DK["Surface"], DK["Border"])
T("app — title", "C tb title", CX0 + 30, CY0 + 504, 12, font=UI, color=DK["Text"])
for i, (cx, cc) in enumerate([(CX0 + 200, DK["Muted"]), (CX0 + 222, DK["Muted"]), (CX0 + 244, DK["Danger"])]):
    plate(cx - 7, CY0 + 492, 14, 14, 3, f"C tb ctl {i}", NONE, cc, 1.4)
T("titlebar 28 · min·max·close", "C tb t", CX0 + 272, CY0 + 500, 10,
  font=MONO, color=BODY)
T("16px controls · PadSM gaps", "C tb t2", CX0 + 272, CY0 + 514, 10, font=MONO, color=MUT)
T("list row 24 · scrollbar 12 · selected marker 3 · seat rail 22", "C meas t",
  CX0 + 20, CY0 + CH - 10, 10, font=MONO, color=MUT)

# ================= PANEL D — PRIMITIVES =======================================
DX, DY, DW, DH = 40, 692, 1840, 436
panel(DX, DY, DW, DH, "PRIMITIVES — DARK THEME · REAL PIXEL SIZES",
      "§2.3 states: default · hover · pressed · disabled · focused-visible · selected")
BLKW = 298
def block(i, row, title):
    x = DX + 16 + i * BLKW
    ty = DY + (54 if row == 0 else 260)
    T(title, f"D blk {title}", x, ty, 12, font=UISB, color=MONO_C)
    return x, ty + 26
def srow(x, y, name):
    T(name, f"D st {name} {x} {y}", x, y + 15, 9.5, font=MONO, color=MUT)

# -- BUTTON (6 states) ---------------------------------------------------------
bx, by = block(0, 0, "BUTTON")
def button(x, y, label, face, fg, focus=False, bord=None):
    plate(x, y, 170, 22, 4, f"btn {label}", face, bord or DK["Border"])
    T("Apply", f"btn t {label}", x + 85, y + 15.5, 13, font=UI, color=fg, j="center")
    if focus: ring_in(x, y, 170, 22, 4, "btn ring")
for k, (nm, face, fg, foc) in enumerate([
        ("default", DK["BtnIdle"], DK["Text"], False),
        ("hover", DK["BtnHover"], DK["Text"], False),
        ("pressed", DK["BtnPressed"], DK["Text"], False),
        ("disabled", "#27323E", DK["Muted"], False),
        ("focused", DK["BtnIdle"], DK["Text"], True)]):
    yy = by + k * 26
    srow(bx, yy, nm)
    button(bx + 76, yy, nm, face, fg, foc)
yy = by + 5 * 26
srow(bx, yy, "dialog def.")
button(bx + 76, yy, "accent", DK["Accent"], DK["OnAccent"], bord=DK["Accent"])

# -- TEXT FIELD -----------------------------------------------------------------
bx, by = block(1, 0, "TEXT FIELD")
def field(x, y, label, ring=False, placeholder=True, dim=False):
    plate(x, y, 190, 24, 4, f"fld {label}", "#11171C" if not dim else "#141B21", DK["Border"])
    if placeholder:
        T("Search apps…", f"fld ph {label}", x + 10, y + 16, 12, font=UI, color=DK["Muted"])
    else:
        T("gofiles", f"fld tx {label}", x + 10, y + 16, 12, font=UI,
          color=DK["Muted"] if dim else DK["Text"])
    if ring:
        ring_in(x, y, 190, 24, 4, "fld ring")
        d.path(f"M{x+62},{y+5} L{x+62},{y+19}", "fld caret", fill=NONE,
               stroke=DK["Accent"], strokeWidth=1.5)
for k, (nm, ring_, ph, dim) in enumerate([
        ("default", False, True, False), ("focused", True, False, False),
        ("disabled", False, False, True), ("filled", False, False, False)]):
    yy = by + k * 26
    srow(bx, yy, nm)
    field(bx + 76, yy, nm, ring_, ph, dim)
T("recessed ChromeBg · caret = Accent", "fld note", bx, by + 4 * 26 + 20, 9.5,
  font=UI, color=FAINT)

# -- TOGGLE ----------------------------------------------------------------------
bx, by = block(2, 0, "TOGGLE — 32×18")
def toggle(x, y, label, track, knob_x, knob, focus=False):
    plate(x, y, 32, 18, 9, f"tgl tr {label}", track, NONE)
    d.shape("ellipse", f"tgl kn {label}", x=knob_x, y=y + 2, width=14, height=14,
            fill=knob, stroke=NONE)
    if focus: ring_in(x - 1, y - 1, 34, 20, 10, "tgl ring")
for k, (nm, track, on, knob, foc) in enumerate([
        ("off", DK["BtnIdle"], False, DK["Ink"], False),
        ("on", DK["Accent"], True, "#FFFFFF", False),
        ("hover", DK["BtnHover"], False, DK["Ink"], False),
        ("pressed", DK["BtnPressed"], False, DK["Ink"], False),
        ("disabled", "#27323E", False, DK["InkMuted"], False),
        ("focused", DK["BtnIdle"], False, DK["Ink"], True)]):
    yy = by + k * 26
    srow(bx, yy, nm)
    toggle(bx + 76, yy, nm, track, bx + 78 + (16 if on else 0), knob, foc)

# -- CHECKBOX ---------------------------------------------------------------------
bx, by = block(3, 0, "CHECKBOX — spec'd")
def checkbox(x, y, label, face, check=False, focus=False, dim=False):
    plate(x, y, 16, 16, 4, f"chk {label}", face, DK["Border"])
    if check:
        d.path(f"M{x+3.5},{y+8.5} L{x+7},{y+12} L{x+12.5},{y+4.5}", "chk mark",
               fill=NONE, stroke=DK["OnAccent"], strokeWidth=1.8, cap="round")
    if focus: ring_in(x, y, 16, 16, 4, "chk ring")
for k, (nm, face, chk, foc) in enumerate([
        ("unchecked", DK["ChromeBg"], False, False),
        ("checked", DK["Accent"], True, False),
        ("disabled", "#27323E", False, False),
        ("focused", DK["ChromeBg"], False, True)]):
    yy = by + k * 26
    srow(bx, yy, nm)
    checkbox(bx + 76, yy, nm, face, chk, foc)
T("rides the toggle state machine —", "chk note", bx, by + 4 * 26 + 20, 9.5, font=UI, color=FAINT)
T("no form consumer yet (§5.2)", "chk note 2", bx, by + 4 * 26 + 34, 9.5, font=UI, color=FAINT)

# -- SLIDER -----------------------------------------------------------------------
bx, by = block(4, 0, "SLIDER — 4px track")
def slider(x, y, label, fillc=DK["Accent"], knob=DK["Ink"], focus=False, dim=False):
    plate(x, y + 8, 180, 4, 2, f"sld tr {label}", DK["ChromeBg"], NONE)
    plate(x, y + 8, 96, 4, 2, f"sld fl {label}", DK["InkMuted"] if dim else fillc, NONE)
    d.shape("ellipse", f"sld kn {label}", x=x + 89, y=y + 3, width=14, height=14,
            fill=knob, stroke=NONE)
    if focus:
        d.shape("ellipse", "sld kn ring", x=x + 87, y=y + 1, width=18, height=18,
                fill=NONE, stroke=DK["Accent"], strokeWidth=2)
for k, (nm, kn, foc, dim) in enumerate([
        ("default", DK["Ink"], False, False), ("hover", "#FFFFFF", False, False),
        ("drag", "#CBD5E1", False, False), ("disabled", DK["InkMuted"], False, True),
        ("focused", DK["Ink"], True, False)]):
    yy = by + k * 26
    srow(bx, yy, nm)
    slider(bx + 76, yy, nm, knob=kn, focus=foc, dim=dim)

# -- MENU ROW ----------------------------------------------------------------------
bx, by = block(5, 0, "MENU ROW — 24")
def menurow(x, y, label, face, fg, sel=False, dim=False):
    plate(x, y, 210, 24, 4, f"mnu {label}", face, NONE)
    if sel:
        d.path(f"M{x},{y+3} L{x},{y+21}", "mnu marker", fill=NONE,
               stroke=DK["Accent"], strokeWidth=3)
    fg2 = DK["Muted"] if dim else fg
    T("Reopen Closed Tab", f"mnu t {label}", x + 12, y + 16, 12, font=UI, color=fg2)
    T("CTRL+SHIFT+T", f"mnu a {label}", x + 198, y + 16, 10, font=MONO,
      color=DK["Muted"], j="right")
for k, (nm, face, sel, dim) in enumerate([
        ("default", DK["Surface"], False, False), ("hover", DK["BtnHover"], False, False),
        ("selected", DK["Selection"], True, False), ("disabled", DK["Surface"], False, True)]):
    yy = by + k * 26
    srow(bx, yy, nm)
    menurow(bx + 76, yy, nm, face, DK["Text"], sel, dim)
T("3px Accent left-edge marker", "mnu note", bx, by + 4 * 26 + 20, 9.5, font=UI, color=FAINT)

# -- RAIL TAB (row 2, block 0) ------------------------------------------------------
bx, by = block(0, 1, "RAIL TAB — seat strip, h22")
def railtab(x, y, label, face, mark=None, pin=False, badge=None):
    plate(x, y, 160, 22, 3, f"tab {label}", face, NONE)
    tx = x + 10
    if pin:
        d.path(f"M{x+9},{y+7} L{x+14},{y+11} L{x+9},{y+15} L{x+4},{y+11} Z",
               "tab pin", fill=DK["Muted"], stroke=NONE)
        tx = x + 22
    T("GOFILES", f"tab t {label}", tx, y + 15.5, 12, font=UI, color=DK["Text"])
    if mark:
        d.path(f"M{x},{y} L{x},{y+22}", "tab accent", fill=NONE,
               stroke=DK["Accent"], strokeWidth=3)
    if badge == "frozen":
        plate(x + 132, y + 4, 4, 14, 2, "tab frozen", DK["Warning"], NONE)
    if badge == "notify":
        plate(x + 126, y + 5, 16, 12, 6, "tab badge", DK["Accent"], NONE)
        T("2", "tab badge n", x + 134, y + 14.5, 9, font=UI, color=DK["OnAccent"], j="center")
    cross(x + 150, y + 11, 3.5, f"tab x {label}", DK["Muted"])
for k, (nm, face, mark, pin, badge) in enumerate([
        ("idle", DK["BtnIdle"], None, False, None),
        ("focused", DK["Surface"], "a", False, None),
        ("hover", DK["BtnHover"], None, False, None),
        ("pinned", DK["BtnIdle"], None, True, None),
        ("frozen", DK["BtnIdle"], None, False, "frozen"),
        ("notify", DK["BtnIdle"], None, False, "notify")]):
    yy = by + k * 26
    srow(bx, yy, nm)
    railtab(bx + 76, yy, nm, face, mark, pin, badge)

# -- BADGE / DOT ---------------------------------------------------------------------
bx, by = block(1, 1, "BADGE / DOT")
yy = by
srow(bx, yy, "notify dot"); d.shape("ellipse", "bdg dot", x=bx + 76, y=yy + 5, width=9, height=9, fill=DK["Accent"], stroke=NONE)
yy += 26
srow(bx, yy, "count pill")
plate(bx + 76, yy + 3, 22, 14, 7, "bdg pill", DK["Accent"], NONE)
T("3", "bdg pill n", bx + 87, yy + 13.5, 9.5, font=UI, color=DK["OnAccent"], j="center")
yy += 26
srow(bx, yy, "frozen")
plate(bx + 76, yy + 3, 4, 14, 2, "bdg frozen", DK["Warning"], NONE)
yy += 26
srow(bx, yy, "focus bdg")
plate(bx + 76, yy, 150, 20, 10, "bdg focus", DK["Surface"], DK["Border"])
T("EDIT", "bdg focus t", bx + 88, yy + 14, 11, font=UI, color=DK["Text"])
plate(bx + 196, yy + 3, 24, 14, 7, "bdg app", DK["Accent"], NONE)
T("APP", "bdg app t", bx + 208, yy + 13.5, 8.5, font=UI, color=DK["OnAccent"], j="center")
T("focus badge + clock ride the bottom band", "bdg note", bx, yy + 42, 9.5, font=UI, color=FAINT)

# -- SCROLLBAR ------------------------------------------------------------------------
bx, by = block(2, 1, "SCROLLBAR — 12px")
for i, (nm, face) in enumerate([("idle", DK["BtnIdle"]), ("hover", DK["BtnHover"]),
                                ("drag", DK["BtnPressed"])]):
    x = bx + 20 + i * 62
    plate(x, by, 12, 96, 6, f"scb track {nm}", DK["ChromeBg"], NONE)
    plate(x + 2, by + 6, 8, 30, 4, f"scb thumb {nm}", face, NONE)
    T(nm, f"scb t {nm}", x + 6, by + 112, 9.5, font=MONO, color=MUT, j="center")
T("ChromeBg track · pill thumb · min 24", "scb note", bx + 20, by + 132, 9.5,
  font=UI, color=FAINT)

# -- TOOLTIP ----------------------------------------------------------------------------
bx, by = block(3, 1, "TOOLTIP — proposed")
fake_shadow(bx + 20, by + 8, 130, 24, 4, "ttp shadow")
plate(bx + 20, by + 8, 130, 24, 4, "ttp plate", DK["Surface"], DK["Border"])
T("Copy path", "ttp text", bx + 85, by + 24, 11, font=UI, color=DK["Text"], j="center")
T("deferred — no pixel consumer yet (§5.2);", "ttp note", bx, by + 56, 9.5, font=UI, color=FAINT)
T("drawn here in contract vocabulary:", "ttp note 2", bx, by + 70, 9.5, font=UI, color=FAINT)
T("Surface + Border + shared shadow", "ttp note 3", bx, by + 84, 9.5, font=UI, color=FAINT)

# -- TOAST --------------------------------------------------------------------------------
bx, by = block(4, 1, "TOAST — kind-12")
fake_shadow(bx + 20, by + 6, 220, 48, 8, "tst shadow")
plate(bx + 20, by + 6, 220, 48, 8, "tst plate", DK["Surface"], DK["Border"])
plate(bx + 23, by + 11, 2, 38, 1, "tst rule", DK["Accent"], NONE)
T("build finished", "tst title", bx + 36, by + 26, 13, font=UI, color=DK["Text"])
T("GOBUILD · click to focus tab", "tst sub", bx + 36, by + 44, 10, font=UI, color=DK["Muted"])
T("4-deep queue, bottom-left · 2px seat rule", "tst note", bx, by + 74, 9.5, font=UI, color=FAINT)
T(">5s command posts on finish", "tst note 2", bx, by + 88, 9.5, font=UI, color=FAINT)

# -- DEFERRED ------------------------------------------------------------------------------
bx, by = block(5, 1, "DEFERRED (§5.2)")
for i, s in enumerate(["in-window tab strips — the seat", "owns tab identity; rail cells above",
                       "are the tab primitive", "", "menu surfaces — kebab/menu glyphs are",
                       "the affordance today", "", "radio groups — no consumer"]):
    T(s, f"def {i}", bx, by + i * 15, 10, font=UI, color=MUT if s else FAINT)

# ================= PANEL E — VARIABLES ===========================================
EX, EY, EW, EH = 40, 1148, 880, 216
panel(EX, EY, EW, EH, "VARIABLES — SETTINGS KEYS", "kernel/src/settings.zig schema-v2")
T("KEY", "E hdr k", EX + 20, EY + 50, 10, font=MONO, color=FAINT)
T("VALUES", "E hdr v", EX + 300, EY + 50, 10, font=MONO, color=FAINT)
T("RESOLVES TO", "E hdr r", EX + 560, EY + 50, 10, font=MONO, color=FAINT)
KEYS = [
    ("theme", "dark · light · amber · custom", "selects the token table — boot: dark"),
    ("palette_bg/_fg/_accent", "RRGGBB hex", "theme=custom → Bg / Text / Accent at paint"),
    ("a11y.contrast", "off · high", "high-contrast theme row"),
    ("a11y.reduce_motion", "off · on", "toast fade + curtain motion cut to instant"),
    ("a11y.text_scale", "100 · 125 · 150", "chrome label scale (reserved)"),
    ("notify_dnd", "off · on", "toasts held to the center — still acked"),
    ("wm", "gotabwm · tabwm · none", "which seat owns the scanout"),
    ("idle_minutes", "int", "arms the seat's idle-dim curtain"),
]
for i, (k, v, r_) in enumerate(KEYS):
    y = EY + 70 + i * 18
    T(k, f"E k {i}", EX + 20, y, 11, font=MONO, color=BODY)
    T(v, f"E v {i}", EX + 300, y, 10.5, font=MONO, color=MUT)
    T(r_, f"E r {i}", EX + 560, y, 10.5, font=UI, color=MUT)

FX, FY, FW, FH = 940, 1148, 940, 216
panel(FX, FY, FW, FH, "ACCESSIBILITY VARIANTS", "designs express these, not new palettes")
T("a11y.text_scale", "F h scale", FX + 20, FY + 50, 10, font=MONO, color=FAINT)
for i, (pct, size) in enumerate([("100", 13), ("125", 16), ("150", 20)]):
    x = FX + 20 + i * 300
    plate(x, FY + 62, 270, 30, 4, f"F scale {pct}", DK["BtnIdle"], DK["Border"])
    T("Seat rail label", f"F scale t {pct}", x + 12, FY + 82, size, font=UI, color=DK["Text"])
    T(pct, f"F scale n {pct}", x + 258, FY + 82, 10, font=MONO, color=MUT, j="right")
T("a11y.reduce_motion", "F h motion", FX + 20, FY + 118, 10, font=MONO, color=FAINT)
T("toast fade + lock-curtain motion collapse to instant state changes — the seat reads the key",
  "F motion t", FX + 20, FY + 136, 11, font=UI, color=MUT)
T("a11y.contrast", "F h contrast", FX + 20, FY + 160, 10, font=MONO, color=FAINT)
T("high ships as its own token row — never a recolor hint on these swatches",
  "F contrast t", FX + 20, FY + 178, 11, font=UI, color=MUT)
T("ground truth: drawmeanelephant/VirelaiOS — docs/ui-primitives.md · theme.go · settings.zig",
  "F foot", FX + 20, FY + FH - 14, 10, font=UI, color=FAINT)

# --- finish ---------------------------------------------------------------------
os.makedirs("work/out", exist_ok=True)
d.finish("tokens-V1R00")
res = d.m.request("tools/call", {"name": "render_preview", "arguments": {"max_side": 1400}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/tokens-V1R00-preview.png", "wb").write(base64.b64decode(c["data"]))
        print("preview saved")

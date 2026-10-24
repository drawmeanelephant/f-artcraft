## icon-\* V1R00 — a shared navy tile makes 31 icons one family at 16 px

- Kind: lesson
- Source: #1248; `work/virelai/icons.py` + `draw_sheet_icons.py`;
  `art/virelai/icon-*/` + `art/virelai/sheet-icons/`;
  proofs `work/out/proof-grid-{16,24}px.png` + `*-ship-big.png`
- Applies to: virelai icon family (and any future large icon sets)
- Status: pending

### Evidence

31 app icons shipped behind one `frame()` helper: navy-family squircle
(`#2E2E4A → #23233A → #181828`, radius 14 at 64 px, INK 3 px edge, soft top
sheen) with the per-app accent carried entirely by the glyph. At 16 px the
uniform tile silhouette is what keeps the set legible on both navy chrome
and light rows — the glyph inside only has to differentiate hue and one
strong shape.

What survived the 16 px gate: everything silhouette-first. What needed
fixing: GOVAULT's slate-on-slate dial mushed at 16 px — lightening the
door to the light-theme `Border` (#CBD5E1) restored it. What to watch next
time: `gowelcome`'s mascot bust is the busiest glyph in the set; it reads
as "the burger says hi" only because dome + lettuce frill + eyes are big
filled masses — the full `sexiburger.mascot()` rig at icon scale collapses
to ~1 px strokes, so draw a simplified bust, don't scale the rig.

Two helper tricks worth reusing: `_band()` (two-pass stroke — ink edge +
colored core — reads as a filled mass at small size, used for GOTOP's arc
and GOREC's cradle) and punch-through holes filled with the plate mid tone
(#23233A) when a glyph needs a "hole" over the tile (GOHELP, GOSET).

Proposed 8.3 adoption names (OS side converts PNG→QOI):
ICONCALC ICONNOTE ICONEDIT ICONFILE ICONTERM ICONWEB ICONPULS ICONGOSH
ICONHELP ICONWELC ICONTOP ICONSET ICONVIEW ICONSND ICONSTLG ICONSTOR
ICONINFR ICONREC ICONSNAP ICONASST ICONSHT ICONREAD ICONCLK ICONMINE
ICONSOL ICONEMOJ ICONIRC ICONVLT ICONMAIL ICONA11Y ICONTABM — sheet:
SHTICONS.

### Proposed change

Add to `prompts/` (virelai family rules): "icon sets above the chrome
register ship in a shared tile frame; differentiate by glyph hue, not by
tile" — and "at 64 px masters never scale the mascot rig under ~90 px;
draw a bust-crop instead".

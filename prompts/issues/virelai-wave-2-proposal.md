# VirelaiOS — wave 2 expansion proposal

Status: draft, not posted. One leaf issue per bullet when approved;
label `type:illustration` (+ `work:variation` for pose/sheet leaves that
extend an approved rig, `work:original` for new assets). See
`.github/LABELS.md`.

Wave 1 shipped the full families table in `virelai/README.md`: 31+4
`icon-*`, ten `cursor-*` (hotspots recorded in `art/virelai/HOTSPOTS.md`),
six `mascot-*` poses on the shared rig (`work/virelai/sexiburger.py`),
three `wallpaper-*`, eight `spot-*`, the `brand-boot-plate` +
`brand-about-emblem`, two `spinner-*`, ten `filetype-*`, and four figcraft
sheets (`tokens`, `seat-shell`, `app-screens`, `apps`). Taste rules:
`virelai/notes/style-bible.md` — two registers (chrome vs asset), warm
dark ink, navy field `#1E1E2E`, transparent backgrounds on chrome-painted
assets, the read-at-size gate, macabre-cute register.

Wave 2 fills the surfaces wave 1 left bare, in priority order:

## Cursors — the missing half of the set

The kernel's resize/move vocabulary is incomplete. Same family rules:
32×48 master, closed chunky outlines, 2-color-mask-safe, hotspot per new
piece appended to `HOTSPOTS.md`.

- `cursor-resize-diag-nwse` / `cursor-resize-diag-nesw` — diagonal
  double-arrows; hotspots center (16,24) like the orthogonal pair.
- `cursor-move` — four-way arrow for drag/pan; center hotspot.
- `cursor-zoom-in` / `cursor-zoom-out` — loupe with +/−; hotspot inside
  the lens (suggest 14,16).
- `cursor-context-menu` — arrow + small menu glyph, for right-click
  affordance; shares the arrow hotspot (2,2).

## Filetypes — second document run

Ten shipped leaves cover the wave-1 fleet but not the OS's own formats.
Flatter than app icons, one accent hue per family, 32×32 master, 16–20 px
read gate.

- `filetype-qoi` — the OS's native image format; adoption-side the most
  real filetype in the set. Accent: sample the WALLPAPER navy + mascot
  amber.
- `filetype-code` — `.go` source; braces glyph, accent `Accent` blue.
- `filetype-vector` — `.vcr`/`.svg`; pen-node glyph.
- `filetype-executable` — ELF binaries (the whole fleet ships `.ELF`);
  gear-in-document.
- `filetype-database` — GOSHEET/GOREADER stores; cylinder silhouette.
- `filetype-font` — Virelai Sans/VirelaiChrome/Virelai Mascots installs;
  "Aa" sans digits.

## Mascot poses — six more on the existing rig

`sexiburger.py`'s `POSES` table is built for this: limbs + face + props
only, dome/fillings/body identical, props ≥4 u, silhouette carries the
24 px read (`prompts/inbox/2026-10-24-mascot-poses-V1R00-pose-rig.md`).
Same 64×64 transparent slot, `mascot(d, 32, 5, 52)`.

- `mascot-point` — one glove pointing forward/down-left (link affordance
  and empty-state "look here").
- `mascot-carry` — arms up holding a small document/box (install,
  file-drop, move-in-progress).
- `mascot-lurk` — half-hidden behind a bottom edge, eyes only
  (spot-no-notifications companion; peeker for panel edges).
- `mascot-clap` — gloves together mid-clap (celebrate's quieter sibling;
  success toasts).
- `mascot-shrug` — already gesture-adjacent to `oops`; differentiate as
  palms-up "don't know / not found" for no-results.
- `mascot-salute` — glove to brow (logout/shutdown courtesy).

## Spots — the states wave 1 skipped

160×120, 80×60 read gate, one subject, dark AND light proof, sits behind
text. Shipped: blank-document, empty-folder, error, no-image,
no-notifications, no-results, offline, trash-empty.

- `spot-empty-inbox` — GOMAIL's zero state; an open envelope holding
  nothing but a moth (in-register, not a scene).
- `spot-success` — affirmative empty state; a single green-ribboned
  check mark, apologizing for interrupting nothing.
- `spot-permission-denied` — a velvet rope across a tiny doorway
  (companion to `mascot-locked`, object-level not character-level).
- `spot-update-available` — a parcel with a tag, waiting patiently.
- `spot-first-boot` — welcome/zero-account surface; one lit doorway in
  the dark.

## Brand — the shutdown plate

- `brand-shutdown-plate` — "safe to power off" 800×450. The macabre-cute
  register's most natural second member: the guillotine at rest, blade
  down, one candle lit. Same brand rules — wordmark in Virelai Sans, no
  version text.

## Wallpaper — two more stages

2560×1440, center-weighted, clear of seat chrome (top ~80 px + rails),
one actor per stage.

- `wallpaper-archive` — the archive room at night: shelving to the
  horizon, one desk-lamp pool center, tiny mascot silhouette cameo.
- `wallpaper-low-tide` — tide flats at dusk, stranded rowboat, gull
  weather; calm register, wide negative space for desktop icons.

## Figcraft sheet — surfaces wave 1 didn't spec

`virelai/design/` conventions apply (real window sizes, cite the token
sheet).

- `sheet-overlays` — modal dialog, context menu, tooltip, drag ghost,
  progress meter, scrollbar states; the transient layer none of
  tokens/seat-shell/app-screens/apps covered at component level.
  (Seat-shell's notification cards + lock screen sketch the territory;
  this sheet finishes it.)
- `sheet-print-export` — exploratory: a print/PDF skin for GOREADER/
  GOEDIT output — paper field, warm ink, how cel-shaded assets survive
  flattening. Optional; only if the OS roadmap wants export.

## Contact sheet

- `sheet-wave-2` — the wave's review contact sheet as its own piece, per
  the wave-1 convention (`sheet-icons`), uniform grid, one cell per new
  asset ordered by family.

## Ordering note

Cursors and filetypes are the most adoption-ready (the kernel mask table
and GOFILES already consume both families). Mascot poses are cheapest —
rig exists, leaves are ~10-line drivers. The print skin is the only
speculative leaf and should land last or be cut.

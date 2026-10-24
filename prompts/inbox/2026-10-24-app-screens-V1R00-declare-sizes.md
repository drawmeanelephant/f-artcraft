## app-screens V1R00 — declare-block sizes are the frame contract

- Kind: lesson
- Source: #1263 · `work/virelai/draw_app_screens.py` ·
  `virelai/design/app-screens/app-screens-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: virelai figcraft sheets + any driver that draws app chrome
- Status: pending

### Evidence

The sheet draws the six highest-traffic apps (GOSH, GOEDIT, GOFILES, WEB,
GOCALC, GOSET) as floating windows at their declare-block natural sizes —
512×384 for the five, 560×360 for GOSET — rather than seat-viewport fills.
Each frame shows the interaction state the issue calls out: GOSH find bar
open (`ctrl+shift+g`) with a live selection, GOEDIT doc tabs + per-function
heat gutter fed by `--prof=`, GOFILES QuickLook `.vcf` card + toast, WEB
tab strip + focused address field (FocusW 2 ring), GOCALC programmer mode
+ tape pane, GOSET schema list + edit pane.

What worked: window-first framing (28 px floating titlebar + declare-size
content) reads as the shipped chrome spec without needing the full seat;
the rail/dockband/toast helpers port cleanly from the seat-shell driver's
figcraft idiom to `draw_path`-built rounded rects (VectorCraft `draw_shape`
has no corner radius — every r4/r8 plate in this sheet is a path).

What didn't: VectorCraft's font set lacks Inter and Fira Code — the
.vectorcraft records them (correct for a design doc) but the PNG proof
falls back to its bundled sans, so mono regions proof wider than ship.
Virelai Sans still has no digit glyphs; captions use Source Sans 3.

### Proposed change

Keep a `prompts/themes/` entry or core note: *app-screen frames always use
declare-block natW/natH, never the 1280×720 viewport — the viewport is
seat-shell territory.* Also record that VectorCraft sheets should treat
rounded rectangles as `draw_path` work, and mono proofing is approximate
until Inter/Fira Code land in the app's font set. Destination:
`virelai/notes/style-bible.md` next consolidation.

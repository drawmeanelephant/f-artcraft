## Adirondack chair V1R00 — prism-per-board renderer for slatted furniture

- Kind: lesson
- Source: #1148, `work/furniture/draw_adirondack_chair.py`, `art/furniture/adirondack-chair/adirondack-chair-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates (anything built from flat boards)
- Status: pending

### Evidence

The chair is modelled in inches (x right, y up, +z back) and every board is an
8-corner prism; visible faces are culled by `normal · TO_VIEWER` and shaded by
`normal · LIGHT` through a shared two-stop vertical gradient. Two findings on
the proof:

- At pitch ≤16° the seat slats render nearly edge-on (~10px) and the chair
  reads seatless. Pitch 24° opens the seat surface; slat gaps then need
  ~0.4in of real spacing, not a hairline.
- Feet at ground y=0 land higher on screen the farther back they sit, so the
  floor chord FY must start above the deepest foot or rear legs float.
- A small translucent prop (tumbler on the arm) fixes the empty-left-arm
  balance better than re-centring the camera.

### Proposed change

Keep the prism helper as the reference pattern for board-built furniture in
`prompts/series/` (candidate: fold into the furniture spec note on next
consolidation). A proposal does not override current house rules.

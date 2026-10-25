## Elvis Presley V1R00 — a front-facing right-handed guitar necks to viewer's RIGHT

- Kind: analysis
- Source: issue #1538; `work/musicians/draw_elvis_presley.py`,
  `art/musicians/elvis-presley/elvis-presley-V1R00.{vectorcraft,svg}`,
  proof `work/out/elvis-presley-V1R00@2x.png`
- Applies to: musicians milestone series; any figure holding a guitar
- Status: pending

### Evidence

Two render loops; check_rim clean both times.

- **Handedness geometry:** a right-handed player facing the viewer frets
  with the hand that lands on the viewer's RIGHT — the neck/headstock
  goes there, body and strumming hand lower-left. (Left-handed flips the
  whole map — relevant for the Hendrix card.) Getting this right costs
  one minute of thinking; getting it wrong reads instantly as an
  impossible guitar.
- **Forearms reaching a raised neck must root inside the torso edge.**
  First pass floated the fret sleeve beside the chest as a detached pale
  boomerang. Re-drawing it as a tube starting ~60pt inside the torso
  silhouette and rising to the board fixed it — same lesson as
  Armstrong's sleeves, applied to a reaching (not raised) arm.
- **Pompadour = tall swept dome + separate forelock shape.** The loose
  lock drawn as its own small shape over the forehead reads "Sun-era"
  immediately; without it the hair is just tall.
- **"Mid-swivel" in a bust is a hem problem, not a pose problem** — the
  shirt bottom edge tilts and one swing-fold stroke arcs across it; the
  shoulders stay level. Cheap and enough.
- Rolled sleeve = a pale cuff arc at the forearm's end; keep it on the
  shoulder-side edge so it doesn't tangle with the hand.

### Proposed change

For the musicians note: guitar handedness map (RH player facing viewer
→ neck frame-right); reaching forearms root inside the silhouette;
the Sun-era forelock is a separate shape, not a hairline bump.

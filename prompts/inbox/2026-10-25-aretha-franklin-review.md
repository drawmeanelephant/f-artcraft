## Aretha Franklin V1R00 — gown and stole must be two value bands; ribs sell a capsule mic

- Kind: analysis
- Source: issue #1537; `work/musicians/draw_aretha_franklin.py`,
  `art/musicians/aretha-franklin/aretha-franklin-V1R00.{vectorcraft,svg}`,
  proof `work/out/aretha-franklin-V1R00@2x.png`
- Applies to: musicians milestone series; layered costumes; standing mics
- Status: pending

### Evidence

Two render loops; check_rim clean both times.

- **Ivory-on-ivory fails.** First pass ran a cream fur stole over a cream
  gown — at card scale the torso printed as one giant pillow. Deep wine
  gown (`#6E3247`→`#22101A`) under the ivory stole fixes it instantly:
  the stole reads as a wrap, the gown as the body beneath. Stole trim
  stays light (`#C8B89E`) so the neckline separates.
- **"Raised at the mic" needs the chin UP, not the mic low.** Chin
  lifted toward a tilted standing mic at mouth height, brows raised,
  irises riding high under the upper lid — reads as gospel lift without
  any arm gesture.
- **A tilted ribbed capsule wants latitude lines, not rotated arcs.** A
  `rot_ellipse` head (30×34, ~30°) with five slightly arced horizontal
  ribs reads "stage mic"; a rotated oblong with diagonal ribs read as a
  lollipop.
- **An open mid-note mouth is the Armstrong grin slimmed down** — dark
  interior blob + a teeth glint on the top edge only. Wider reads as a
  grin, taller keeps it a note.
- Bouffant: one big dark dome + two sheen ridges + small nape curls.
  Still borders turban at thumbnail size — a future revision could break
  the silhouette with a side part or a hairband.

### Proposed change

For the musicians note: costume layers separated by at least two value
steps; "raised/lifted" reads through chin-up + high irises, not arm
props; mic capsules take horizontal ribs on the rotated body, ribs do
not rotate with the head.

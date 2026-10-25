## juneteenth V1R00 — a lone arc turns floating links into a broken chain

- Kind: lesson
- Source: issue #989, `work/holidays/draw_juneteenth.py`,
  `art/holidays/juneteenth/juneteenth-V1R00.vectorcraft`,
  `work/out/juneteenth-V1R00@2x.png`
- Applies to: holidays / Festival Seals; any emblem built from repeated
  objects on an arc
- Status: pending

### Evidence

Eight `link()` ellipses (rotated outline ellipses: INK under-stroke + bronze
stroke + a short glint highlight) spaced 9° apart on a r=292 arc read
immediately as chain at seal scale — no interlocking geometry needed.
The break works because the two `broken_link` halves are drawn as open
C-arcs tilted toward the gap, not as ellipses with a chunk removed; three
flying shard strokes above the gap carry the "snap". First proof had the
chain floating in dead space below the star; a single faint `Horizon arc`
(svg arc segment, r=305, gold at opacity 32) behind the links grounded the
whole emblem — cheap, invisible-as-object, big structural win. The dawn
burst behind the star is tapered `burst_wedge` paths alternating
vermilion/cream; cream at opacity ~28 reads sage on the deep green field,
which is fine — it behaves like the flag's pale burst without becoming a
flag (no star-in-burst placement, no rectangular field).

### Proposed change

When an emblem splits into a hero above and a row of objects below, add one
low-opacity groundline/arc under the row before reaching for more objects.
`link()`/`broken_link()`/`burst_wedge()` are candidates for a shared
`festival_kit` emblem section on next consolidation.

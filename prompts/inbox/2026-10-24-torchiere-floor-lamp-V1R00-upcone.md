## Torchiere floor lamp V1R00 — uplight inverts the cone

- Kind: lesson
- Source: issue #1203, `work/furniture/draw_torchiere_floor_lamp.py`, `art/furniture/torchiere-floor-lamp/torchiere-floor-lamp-V1R00.*`
- Applies to: field plates — furniture
- Status: pending

### Evidence

Every other lamp plate hangs its light cone downward (billiard, oil,
arc); the torchiere's whole point is the *upward* wash, so the cone
inverts: narrow at the bowl rim, flaring to a wide "ceiling wash"
ellipse at the top of the disc. Deco styling carried by three cheap
devices: the stepped three-tier lathe base (ziggurat foot), collar rings
on the pole as the syncopated beat, and low-opacity sunburst rays inside
the cone. The alabaster liner is a two-ellipse trick — hot core over a
warm rim ring — plus a bloom ellipse hovering just above. Corner mood
came from one 16pt tonal wedge + a 3pt seam; keep it barely-there or the
seam competes with the pole. Watch extent: ray tips are screen-space
points — mark() the tip coordinates or the assert can't see them.

### Proposed change

For uplights/wall-washers: cone goes wide-side-up, and a faint radial
fan inside it does deco/sunburst duty for free. Destination:
`prompts/series/20-field-plates.md` furniture traps.

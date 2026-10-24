## sugar-glider V1R00 — membrane lobes must tuck under the body

- Kind: lesson
- Source: #1039, work/animals/draw_sugar_glider.py, art/animals/sugar-glider/sugar-glider-V1R00.*
- Applies to: animals field plates; gliding/webbed subjects (patagium, fins, webbing)
- Status: pending

### Evidence

First pass drew the patagium as a self-contained oval lobe on each side with a
visible dark gap between its inner edge and the body: at plate scale it read
as insect wings on a beetle, not a skin membrane. Pulling the lobe's inner
edge in under the body silhouette (letting the body stroke overdraw the seam)
and adding one stretch crease from wrist to ankle fixed the read. A second
note: a glow halo centered near the rim (moon) leaks past check_rim's r=430
band even at single-digit opacity — size glows so dist(center)+r stays ~420.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: membranes and webs are
tucked under the torso, never lobe-and-gap; and any radial glow near the rim
needs its outer stop checked against the disc radius.

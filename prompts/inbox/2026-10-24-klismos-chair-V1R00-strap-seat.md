## Klismos chair V1R00 — a strap seat wants a surface, not ribbons

- Kind: lesson
- Source: #1212, `work/furniture/draw_klismos_chair.py`, `art/furniture/klismos-chair/`
- Applies to: field plates — furniture (woven/strap seats)
- Status: pending

### Evidence

First pass drew the seat as seven separate tapered ribbons running
front-to-back. In the three-quarter projection their screen-space edges
overlapped into a row of orange chevrons — it read as ornament, not a seat.
The fix: one slung pad (trapezoid surface, parabolic sag mid-span in both
axes) with seam *lines* for the straps; reads instantly as leather webbing.
Also: stretchers placed by absolute coordinates overshot the bowed leg
silhouettes — a visible peg sticking out past the sabre. Attaching the ends
to points bisected on the leg spline (`leg_pt`) lands every joint. Sabre
legs need both x- and z-bow at yaw ~22° or they foreshorten into sticks.

### Proposed change

For `prompts/series/20-field-plates.md` (Furniture traps): seats and panels
are surfaces with seam lines; individual strap ribbons only survive at
frontier scale (deck-chair canvas). Curved legs should be splined ribbons
tapered along the member, and any member that joins a curved leg should
sample its endpoint off the leg's own spline.

# Library globe V1R00 — occlusion by draw order, land masses must sit in the varnish

- Kind: lesson
- Source: issue #1237; `work/furniture/draw_library_globe.py`,
  `art/furniture/library-globe/library-globe-V1R00.{vectorcraft,svg}`,
  proof `work/out/library-globe-V1R00@2x.png`
- Applies to: field plates; any ring/armillary-around-a-sphere subject
- Status: pending

### Evidence

Shipped after two render-and-critique loops. First pass shipped a correct
silhouette but the parchment continents ran too bright and covered ~50% of
the lit face — the ball read as cream-with-brown-rim, not "oceans the color
of varnish". Muting the land gradient from `#EBD9A8` to `#D8BE8C` at the
light end and `#9A7440`→`#84602F` at the foot put the continents back inside
the varnish; a few low-opacity island specks plus a faint cartouche oval
sell "antique map" better than more coastline vertices.

What worked, worth reusing:

- **Rings around a ball need no clipping.** Draw the far half of the ring
  band before the sphere, the near half after it; where a ring radius is
  larger than the ball's, the near half is *always* nearer than the sphere
  surface wherever they overlap in projection — draw order is the whole
  z-buffer. The horizon band crossing the ball's face is the read that says
  "library globe" instead of "ball on a table".
- **Latitude/longitude land:** keep coasts as rough lon/lat vertex lists,
  densify to ~4° steps, Sutherland-Hodgman clip to z>0, project — the clip
  boundary lands exactly on the silhouette circle. ~25 vertices per
  continent is plenty at plate scale.
- Four-leg stand reads cleaner than a pedestal at this size; splaying the
  feet wider than the ring (250→332 world units) is what makes it read
  "stand" rather than "stool legs".
- Compass-rose medallion on the stretcher ring carries the empire mood
  cheaply: brass disc + 8 alternating-weight rays + ink hub.

Residue: the Eurasian blob still reads a little helmet-like at thumbnail
and Madagascar floats slightly detached — a rendition could try an
Atlantic-facing map or a second idiom.

### Proposed change

For the field-plate note at consolidation: *spherical subjects — mute the
map, not the ocean; draw order replaces clipping for wraparound rings;
and a horizon band that visibly crosses the ball's face is the library-
globe tell.*

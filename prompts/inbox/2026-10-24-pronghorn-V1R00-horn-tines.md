## Pronghorn V1R00 — a horn needs its tine drawn as geometry, not implied

- Kind: lesson
- Source: issue #1068, `work/animals/draw_pronghorn.py`,
  `art/animals/pronghorn/pronghorn-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — horned/antlered subjects
- Status: pending

### Evidence

First pass built both horns as plain ribbons w≈12–15 and let the "prong" be
a short stub; at plate scale it read as two antennae. The fix that made the
species read: (a) near-beam width 18 at the base, (b) a real backward hook
drawn as a separate pointed path at the tip, (c) the forward prong as its
own tapered ribbon (w 11→3) starting ~40% up the front edge, long enough to
clear the beam silhouette. Antennae are parallel lines; a pronghorn horn is
a *branching* mass — the silhouette must fork.

Second nit: a tiny distant animal must not have more legs than its body can
carry. A ~50pt silhouette with four splayed leg-lines reads as a spider;
two vertical strokes under a clean body pill read as a grazer.

### Proposed change

Field-plates trap list, thin-geometry bullet family: *tines and hooks are
separate tapered shapes off the beam — a horn silhouette must visibly fork
or it reads as antennae.* Destination: `prompts/series/20-field-plates.md`.

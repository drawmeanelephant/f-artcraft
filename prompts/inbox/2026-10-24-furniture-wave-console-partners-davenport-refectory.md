## Furniture wave V1R00 (console table, partners desk, davenport desk, refectory table) — idiom routing and depth tricks

- Kind: lesson
- Source: issues #1189, #1190, #1191, #1192; drivers `work/furniture/draw_console_table.py`, `draw_partners_desk.py`, `draw_davenport_desk.py`, `draw_refectory_table.py`; natives + proofs under `art/furniture/<slug>/`
- Applies to: field plates — furniture
- Status: pending

### Evidence

Four V1R00 plates shipped and merged (PRs #1429, #1433, #1435, #1442) by routing each subject to the idiom its geometry rewards:

- **3/4 prism rig** (cedar-chest `prism()` + `P(x,y,z)` + face culling) carries compact sculptural pieces — console table (inches-modelled, yaw 28°/pitch 22°) and davenport desk (yaw 30°/pitch 22°). The davenport's "drawer of secrets" is one pulled prism + a cavity quad + a sealed parchment: three shapes sell the brief's storytelling word for word.
- **Front elevation** (secretary idiom) carries the partners desk: twin drawer pedestals flanking a kneehole are a symmetrical front story; the far side's cupboard door + floor sliver inside the recess encode "two people" without a second viewpoint. Widening the stance ~25 px/pedestal was the fix that made it read *partners* and not single pedestal.
- **Turned-member profiles** (ladderback `(y, halfwidth)` → `smooth()` silhouette) carry the refectory table: four cup-and-cover bulb legs + a perimeter stretcher, deliberately not trestles so it never collides with `trestle-table` (itself documented as "a refectory table"). First proof read the three back legs as hanging pendants — extending them below the stretcher so the beam occludes their feet is what makes them read as a planted back row.

Props: one per plate, fully inside the silhouette — calling-card bowl on the marble (entry hall), two opposed book piles (the disagreement), sealed parchment in the pulled drawer (the secret), two candles on the slab (the order at table). Marble veins needed ~50% opacity to read at @2x; under ~40% they vanish.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Pick the idiom by the subject's signature geometry — prism rig for compact carcasses and opened elements, front elevation for symmetrical multi-bay case pieces, `(y, halfwidth)` turned profiles for lathed members. Back-row members must pass under the front occluder or they hang. One brief-word prop per plate, staged fully inside the silhouette."

## Megatherium V1R00 — tripod pose and reach grammar

- Kind: analysis
- Source: issue #1141, `work/animals/draw_megatherium.py`,
  `art/animals/megatherium/megatherium-V1R00.{vectorcraft,svg}`
- Applies to: field plates (animals), extinct megafauna
- Status: pending

### Evidence

The reared tripod (two hind legs + tail planted as third leg) reads
immediately — the tail as a broad prop wedge behind the hips is the pose's
anchor. Foreclaws hooking a real branch (claw tips land just over the limb
line) carries "tall enough to browse". Watch-outs: the far arm must not
cross the face silhouette — at dark fill values it merges into the neck;
keep it offset or dimmer than the head edge. Head stayed readable because
the muzzle/eye details sit on the light end of the head gradient.

### Proposed change

For `prompts/series/20-field-plates.md`: for rearing/bipedal subjects, the
tail-prop silhouette is the legibility key — draw it first, as a wedge with
its own gradient, before the torso.

## Sailfish V1R00 — baitball prey must clear the hero's edges, or it reads as damage

- Kind: lesson
- Source: issue #1084; `work/animals/draw_atlantic_sailfish.py`, `art/animals/atlantic-sailfish/atlantic-sailfish-V1R00.*`
- Applies to: animals field plates; clustered background fauna (baitballs, flocks, swarms)
- Status: pending

### Evidence

Proof `work/out/atlantic-sailfish-V1R00@2x.png`. Baitball mood carried by
~18 tiny rotated-ellipse sardines (rx 11 ry 4.5, #C9D9DE, op 50–90) packed
in a loose disc plus a 10% shimmer blob behind them — cheap and legible.
First proof had two pale sardine dashes crossing the sail's dark ink
outline; at @2x they read as scratches on the hero shape, not as fish.
Fix was not restyling the sardines but pushing the cluster's right edge
~30pt clear of the sail contour. A prey mark that touches the subject's
silhouette reads as damage, not as depth — if one must overlap, it needs
an intentional occlusion relationship, not a nick.

The sail itself is the read: quarter-disc fan whose front edge rises
nearly vertical off the back, six membrane rays fanning from base points
(op 55, 4pt — thin-ray strokes would die), and the diagnostic dark-cobalt
spot scatter (op 65). Pelvic fins are two plain 4–5pt streamer strokes
under the belly — at plate scale that IS the filament.

### Proposed change

For `prompts/series/20-field-plates.md`: background fauna clusters get a
~30pt no-fly margin around the subject silhouette; check the proof for
marks grazing hero edges. Sailfish sail: tall rounded fan + 5–6 base-fan
rays + spot scatter is the species code.

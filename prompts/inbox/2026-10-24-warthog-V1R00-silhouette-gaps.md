## warthog V1R00 — separate head shapes need a bridge into the body

- Kind: lesson
- Source: #1036, work/animals/draw_warthog.py, art/animals/warthog/warthog-V1R00.*
- Applies to: animals field plates; any profile subject where the head is its own path
- Status: pending

### Evidence

First render carried the head as a closed wedge floating in front of the chest:
the throat arc ended above the chest front and the proof showed a concave notch
in the silhouette under the jaw. A "neck fill" wedge (same gradient as the head,
no stroke) bridging jaw to chest fixed it. The wart bumps also read as polka
dots when stroked — soft unstroked shade ellipses read as anatomy instead.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: when head and body are
separate paths, bridge the throat with an unstroked fill in the head's own
gradient; bumps on a face should be translucency, not outlined circles.

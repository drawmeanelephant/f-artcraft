## Loveseat V1R00 — rail ends curl into horns

- Kind: lesson
- Source: #1156, `work/furniture/draw_loveseat.py`, `art/furniture/loveseat/`
- Applies to: field plates — furniture, any smoothed closed silhouette
- Status: pending

### Evidence

The settee's front rail was first drawn as a six-point closed run through
`smooth()`. The Catmull-Rom corners at both ends curled upward into horn
hooks that read as handles. Extending the rail under the arm bodies
instead pushed pointed wing tabs out past the arm faces. Only an
explicit path with squared quadratic corners (`Q` at the caps) produced a
rail that sat cleanly between the arms. Cushion seam, scroll spirals,
crest and nailheads all survived their own critique at @2x.

### Proposed change

Add a line to the furniture format notes in `prompts/series/`: silhouette
bands (rails, aprons, seat decks) that terminate mid-field should use
explicit cornered paths, not smoothed closed point runs — smoothing turns
end caps into hooks. A proposal, not a rule, until consolidated.

## Andean condor V1R00 — the ruff is one collar, and sky decor leaks too

- Kind: lesson
- Source: issue #1079; `work/animals/draw_andean_condor.py`,
  `art/animals/andean-condor/andean-condor-V1R00.*`
- Applies to: field plates, dorsal soaring birds, rim rules
- Status: pending

### Evidence

The dorsal soar works: flat plank wings with slotted tips, a white covert
panel riding each upper wing, the pale head ahead of the ruff. Two failures
only showed on the proof. The ruff as seven separate ellipses rendered as a
pearl necklace — it wanted ONE blob with scalloped hem strokes inside.
And a distant ridge whose base was only "inside the near ridge" still leaked
past the rim: the disc's left edge at the low corner (x≈150, y≈700–745) is
outside the circle entirely, so every sky/mountain silhouette must be
checked against the disc itself, not just the floor shape it hides behind.
Tapering the far ridge's ends to points inside the near mass fixed it.

### Proposed change

Interior scenery that extends below the disc's side chords must still pass
`on_disc` — "hidden behind the floor" is not a rim pass if the floor itself
doesn't reach there. Destination: the rim section of the field-plate rules.

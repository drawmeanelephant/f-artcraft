## spot set V1R00 — mid-tone fills + ink outline carry the both-theme read

- Kind: lesson / analysis
- Source: issue #1253 · `work/virelai/draw_spot_*.py` ·
  `art/virelai/spot-{empty-folder,no-results,offline,error,no-notifications,blank-document,no-image,trash-empty}/…-V1R00.*` · proof sheet `work/out/spots-proof.png`
- Applies to: virelai `spot-` family and any transparent asset that must
  read on both dark chrome and light app surfaces
- Status: pending

### Evidence

Eight 160×120 transparent masters, proofed at 80×60 on a split
`#182026`/`#F1F5F9` field. What carried the read:

- **Fill value in the middle.** Every prop sits in the #4A5468–#E8EDF5
  band (steel blues, kraft tan, brass, paper cream) — bright enough off a
  dark field, the #503139 ink does the separation on light. Anything that
  would die on navy got a cream/brass detail, not more ink.
- **One prop + one absence cue per spot.** The meaning is the *missing*
  thing: folder's dark hollow mouth + dust motes, magnifier's dashed
  not-found ring, the plug's dashed ghost arc, dashed picture inside the
  photo card, sparkle inside the empty bin, rest-dots beside the bell.
- **Mascot cameo works at spot scale.** `spot-error` runs
  `POSES["oops"]` at h=96 — the shoulders-up silhouette + sweat drop
  survives 80×60 and apologizes exactly as briefed.
- **Ink-pair stroking.** Wide strokes get a two-layer treatment (INK under,
  lighter fill color over) so the outline never falls off a dark surface —
  same trick as the mascot rig's floored stroke widths.

Gotcha worth keeping in the bible: `draw_path`/`draw_shape` take
`dash=[d, g, …]` (pt array) — the older `n=[…]` kwarg in `work/aphorisms/`
drivers is dead on the current CLI.

### Proposed change

Candidate rule for `virelai/notes/style-bible.md`: *spots draw the object,
not the glyph — the empty/absent/failed state is told by one dashed or
hollow cue inside the prop, never by a crossed-out overlay.* Destination:
the motif-rules section.

## John Coltrane V1R00 — bowed head reads via chin-tuck, not rotation; sound arcs carry the "sheets"

- Kind: analysis
- Source: issue #1535; `work/musicians/draw_john_coltrane.py`,
  `art/musicians/john-coltrane/john-coltrane-V1R00.{vectorcraft,svg}`,
  proof `work/out/john-coltrane-V1R00@2x.png`
- Applies to: musicians milestone series; head-down / instrument-on-strap poses
- Status: pending

### Evidence

Two render loops; check_rim clean both times.

- **"Head tipped down" is chin-tuck, not a rotated skull.** Second pass
  dropped the chin ~8pt into the collar, hid most of the neck, dropped
  every feature ~4–6pt and let the hair cap dominate the crown. Reads as
  a bowed head at card scale without re-rigging the face ellipse.
- **A tenor sax is J-shaped on purpose:** swan neck down-over into a
  wide body tube, U-bow at the floor of the phrase, bell flaring
  up-and-out with a hand-built `rot_ellipse` mouth. First pass made the
  bell too small (24×38) and the whole horn read as a clarinet — tenor
  bell wants ~30×48 and a wide body tube.
- **The neck strap is ONE line.** First pass ran two strokes that ended
  inside the shirt and read as lapel seams; a single 3pt line from
  behind the collar to the neck/body join is enough.
- **Closed, serene eyes = lid arcs + a faint crease above**, no lashes —
  the Billie lowered-lid vocabulary minus the glamour.
- **"Sheets of sound" survives as three faint concentric arcs** off the
  bell (30/24/18% opacity, spacing ~28pt). Louder would be kitsch; this
  reads as air moving.
- Moustache as a filled band over the mouthpiece corner keeps the
  mouth/mouthpiece junction dark and simple — the mouthpiece covers the
  lip edge per the Armstrong rule.

### Proposed change

For the musicians note: strap-hung horns get one strap stroke to the
neck join; tenor/bari bells are 30×48-class mouths, not trumpet-mouth
sized; a bowed head is chin-tuck + low features, not a rotated head
shape.

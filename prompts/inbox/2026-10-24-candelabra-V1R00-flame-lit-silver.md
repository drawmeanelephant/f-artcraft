## Candelabra V1R00 — light-sourced metal on a near-black plate

- Kind: lesson
- Source: #1231, `work/furniture/draw_candelabra.py`, `art/furniture/candelabra/`
- Applies to: field plates — self-lit subjects (lamps, candles, lanterns)
- Status: pending

### Evidence

A power-cut plate wants the subject to be the light: the plate disc drops
to ~#10141A at the rim, and a warm radial bloom keyed on the flame row does
the mood. Sterling still reads because the metal gradient keeps a bright
specular band (~#E8EEF2 at offset .56) even at low ambient — cool darks,
not muddy ones. Two joins that mattered: a small "branch collar" knop where
the four arm ribbons converge, without which the arms dissolve into a dark
blob; and wax drips down the stem sell the "used for years" read better
than drips on the candles alone — but 3 rivulets per candle reads hairy,
2 is enough. Arms are tapered ribbons (spine polyline + normal offsets,
w0->w1 with a mid bulge) rather than thick strokes, so they take a gradient.

### Proposed change

Add to the field-plate notes: for self-lit subjects, draw the metal with a
full-value gradient against a rim-dark plate and let a warm radial supply
the light logic; multi-branch junctions need an explicit collar element.

## Jimi Hendrix V1R00 — skip the pickguard blob; pickups perpendicular to the string axis

- Kind: analysis
- Source: issue #1539; `work/musicians/draw_jimi_hendrix.py`,
  `art/musicians/jimi-hendrix/jimi-hendrix-V1R00.{vectorcraft,svg}`,
  proof `work/out/jimi-hendrix-V1R00@2x.png`
- Applies to: musicians milestone series; electric guitars, left-handed props
- Status: pending

### Evidence

Three render loops; check_rim clean throughout.

- **The Strat pickguard is a trap.** A dark guard drawn at believable
  size still eats the white body and reads as the guitar itself — first
  pass looked like a black paddle with a scratch on it. Deleting the
  guard and laying three 6pt pickup dashes directly on the body fixed
  the read entirely. Lesson: on pale bodies, marks beat panels.
- **Pickup dashes must sit perpendicular to the string axis** — the
  neck runs ~40° up-left, so pickups are steep `/` dashes spaced along
  the axis. Nearly-parallel dashes read as decoration, not hardware.
- **Left-handed flip:** neck to frame-LEFT, fret hand up on the raised
  neck (viewer's left), strum hand low-right over the bridge — the
  Elvis note's map mirrored. The long flipped headstock stays pale like
  the body (Strat headstocks match).
- **Headband = band shape + knot + two tail strokes**, all one red
  family; tails drawn past the hair edge read instantly.
- **"Wild hair" = a cloud silhouette + 4–6 curl ticks OUTSIDE the
  perimeter** — inner strokes alone read as a hat; it needs edge break.
- Fringe: short parallel strokes off sleeve undersides and the jacket
  seam — keep them light (`#DCC49A` on tan suede) or they vanish.

### Proposed change

For the musicians note: on light guitar bodies, use bare pickup/bridge
marks and no pickguard fill; hair clouds need silhouette-breaking curl
ticks; fringe is strokes on the garment's free edges, not on seams.

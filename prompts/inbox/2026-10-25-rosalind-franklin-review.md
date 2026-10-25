## Rosalind Franklin V1R00 — a prop that glows wants its halo budgeted first

- Kind: analysis
- Source: issue #1553; `work/scientists/draw_rosalind_franklin.py`,
  `art/scientists/rosalind-franklin/rosalind-franklin-V1R00.{vectorcraft,svg}`,
  proof `work/out/rosalind-franklin-V1R00@2x.png` (`check_rim.py`: clean)
- Applies to: scientist milestone cards; lit hand-held props, hair masses
- Status: pending

### Evidence

Two loops.

- **Photo 51 as a light source:** a tilted `rot_rect_path` glass plate,
  luminous grey-lavender gradient, the diffraction cross as two wide
  low-opacity band strokes (cap `round`) crossed at ±32°, then spots
  interpolated along each arm — small near the centre, larger toward
  the ends, matching the real pattern's weight. A 30%-peak halo ellipse
  behind it does the "own light source" work; its bbox was sized inside
  `rim_x` before drawing (the Tesla lesson — glow is decor).
- **A nape bun must touch the cap.** First pass placed the bun as a
  clean blob at jaw level and it read as a floating ball. Fix: tuck it
  against the jawline *and* run a short thick strand from the hair cap
  down into it — pulled-back hair is continuous, never an island.
- **Raised sleeve + pinched plate**: the sleeve mass must reach down
  into the coat shoulder (first pass left a dark wedge that split arm
  from body); the hand is a small fist at the plate's lower corner with
  one grip line.
- A hanging film strip with sprocket holes at ~14% opacity in the upper
  dark says "darkroom" for free.
- Milestone `PHOTO 51 · 1952` in Source Sans 3, tracking 500 → 316pt
  wide, 65pt clear of the rim.

### Proposed change

For the milestone grammar: *hair masses that continue past the skull
(buns, ringlets, queues) are one connected silhouette — every sub-mass
touches the cap or a visible strand joins it; a detached blob always
reads as an object, not hair.* Destination: the scientist/milestone
card note at the next consolidation.

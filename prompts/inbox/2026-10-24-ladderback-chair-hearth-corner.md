# ladderback-chair-V1R00 — scene props near the rim, turned members by profile

- Kind: lesson
- Source: issue #1153, driver `work/furniture/draw_ladderback_chair.py`,
  native + proof `art/furniture/ladderback-chair/`
- Applies to: furniture field plates; any plate adding floor props or a
  second light source
- Status: pending

### Evidence

The hearth-mood brief wanted a warm accent besides the usual upper-left
lamp. An ember glow + three stones + ember dots at the plate's bottom right
sold the hearth read, but the disc's bottom corner fits far less than it
looks: the first cluster placed at (820-860, 760-830) sat past the r=420
rim without tripping the bounds assert because prop coordinates were never
fed to it. Second attempt overcorrected and put stones under the chair's
feet. Final cluster hugs (700-780, 706-780) — just right of the front leg —
and every prop corner is pushed into the bounds list so the rim assert
covers it.

What survives critique: arched slats drawn before the rear posts so the
posts' turned silhouette swallows the slat ends (no mitre work needed);
rush seat as a two-family clipped grid over a sagging trapezoid reads at
plate scale; turned posts via a (y, halfwidth) profile list + smooth()
closed silhouette is compact and reusable.

### Proposed change

For `prompts/` consolidation: when a plate adds floor props (hearth,
rug, toys), their corners belong in the same extent check as the subject —
the rim assert only sees what it is given. And a turned-member profile
helper (`[(y, halfwidth)]` -> smooth silhouette) is worth promoting to
`work/vc.py` once a third piece needs it.

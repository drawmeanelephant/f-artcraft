## Siberian husky V1R00 — a curled tail wants a stroked brush, not a blob

- Kind: analysis
- Source: issue #1503; `work/dog-breeds/draw_siberian_husky.py`,
  `art/dog-breeds/siberian-husky/siberian-husky-V1R00.{vectorcraft,svg}`,
  proof `work/out/siberian-husky-V1R00@2x.png` (`check_rim.py`: clean)
- Applies to: dog-breeds milestone cards; curled/spitz tails
- Status: pending

### Evidence

Two loops plus a rim-leak fix (a wind-score groove on the snow started
at x300,y842 — past r430; every decor stroke's *endpoints* need the
`on_disc` test, not just its anchor).

Draft 1 drew the sickle tail as a closed smooth blob floating off the
croup — read as a balloon tied to the dog. Fix: the tail is one thick
round-capped gradient stroke (`strokeWidth=30`, cap `round`) that
springs visibly off the croup and curls its tip over the spine, with a
shorter white stroke laid on the curl end for the under-tip. A stroked
curve beats a closed path for any appendage that wants one continuous
taper — same lesson as the dhole legs.

What works: the signature arrives through the eye — pale ice-blue iris
(`#BEE0EC` core) against the dark masked face; pricked triangular ears
kept smaller and closer-set than the shepherd's; grey-and-white coat map
(dark saddle, white ruff, white underline, white stockings); snow crust
floor with crust chips; breath-frost puff off the nose. The cold
blue-grey disc inverts the warm-dog-on-cool-plate convention — here the
plate is the warmest dark and the dog is the cold one.

### Proposed change

For the grammar note: *curled/spitz tails are stroked brushes
(thick round-cap path + tip overlay), not closed comma blobs — a closed
blob detached from the croup reads as a balloon.*

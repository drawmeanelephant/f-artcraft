## Hammerhead V1R00 — the cephalofoil reads as a swung-forward crescent, not an ellipse

- Kind: lesson
- Source: issue #1081; `work/animals/draw_hammerhead_shark.py`, `art/animals/hammerhead-shark/hammerhead-shark-V1R00.*`
- Applies to: animals field plates; oblique/three-quarter head structures that defeat side-view silhouettes
- Status: pending

### Evidence

Proof `work/out/hammerhead-shark-V1R00@2x.png`. Three dead ends before the
read landed: (1) a near-vertical ellipse bar reads as a balloon taped to
the snout; (2) tilting it 30deg reads as a leaf/flipper stuck on the face;
(3) a thin shallow crescent reads as a giant upper lip once a smile is
drawn under it. What worked: a quadratic-Bezier centerline swept forward
from a low-left near tip (235,478) to a far tip wrapping back over the
neck (425,450), offset +-24pt into a closed ribbon — thick enough to be a
head, not a mouth. Eyes go ON the tips (near eye detailed, far eye dim),
nares ride the leading rim, ampullae dots pepper it.

Two connection details carried the illusion: the body chin was pushed
forward under the bar's rear edge (no water gap — a floating bar kills
the read instantly), and the smile was kept low and partial so it reads
as the underside seam, not lips under a moustache. The great-hammerhead
central notch is a Gaussian dip (depth ~12) pushed into the leading-edge
offset, not a drawn vertex — smooth() would round a hand-cut notch away.

### Proposed change

For `prompts/series/20-field-plates.md`: transverse head structures
(hammer, manta horns, sawfish rostrum in 3/4) — draw the bar as an
offset Bezier ribbon swung toward the viewer, eyes at both tips, and
overlap the body's chin/neck under its rear edge; an isolated ellipse or
thin arc will not survive critique.

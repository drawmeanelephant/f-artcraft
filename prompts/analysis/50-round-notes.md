## Analysis log

- **Round 0 — the existing body of work:** see
  [ANALYSIS-ROUND-0.md](../../ANALYSIS-ROUND-0.md).
  Baseline verdict: shading standard is set (portrait, bunny v2, Jolly set);
  recurring risks are clipped geometry at canvas edges and shapes reading
  flatter inside badges than in free compositions.
- **Orient festival roster completion (qingming · qixi · mid-autumn · holi ·
  navratri · ganesh-chaturthi · raksha-bandhan · onam):** per-piece notes in
  the commit messages; series-wide lessons: circles straddling a silhouette
  edge read as beads (umbrella scallops, mooncake) — build scalloped edges as
  single bump paths; the staged kit swallow/magpie needed redraws at plate
  scale (floating ears, penguin breasts); splash blobs must speak the same
  soft-puff language as the clouds around them; kit radial gradients take
  stop pairs only, no focus tuple. `inside()` guards caught two rim hangs,
  `check_rim.py` caught a third before any commit.

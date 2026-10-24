# work/virelai — drivers

One `draw_<slug>.py` per piece, matching `art/virelai/<slug>/` (and
`virelai/design/<sheet>/` for figcraft sheets). Bootstrapping is the same as
every series — the sys.path pattern from `work/animals/draw_axolotl.py`:

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
```

That puts `work/` on the path, so the shared VirelaiOS tokens come in as a
namespace import:

```python
from virelai.vkit import DARK, INK, NAVY, BUN, SIZE
```

`vkit.py` mirrors [`virelai/notes/style-bible.md`](../../virelai/notes/style-bible.md):
shipped theme hexes, sampled mascot/wallpaper colors, geometry tokens, and the
per-family master canvas sizes. Cite the bible for the rules; import vkit for
the numbers.

`Draw.finish("<slug>-V1R00")` writes to `work/out/`; copy `.vectorcraft`,
`.svg` and `@2x.png` into `art/virelai/<slug>/` (or `virelai/design/<sheet>/`)
— the `.pdf` stays local. For animation families, export frames then compose
the contact sheet on a uniform grid in animation order.

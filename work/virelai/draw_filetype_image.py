#!/usr/bin/env python3
"""filetype-image V1R00 — issue #1257.

GOFILES gutter icon: 32x32 master on transparent, document-convention
silhouette in the VirelaiChrome stroke family, one accent hue per family.
Reads at 16-20 px on light AND dark list rows; proof gate drops any
detail that dies at 16 px. Shape lives in virelai.filetypes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw
from virelai.filetypes import new_doc, SHAPES

d = Draw()
new_doc(d, "filetype-image-V1R00")
SHAPES["image"](d)
r = d.finish("filetype-image-V1R00")

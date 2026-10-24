#!/usr/bin/env python3
"""Register previous work into the V/R scheme (AGENTS.md).

The original previous-work/ dump (native .vectorcraft/.designcraft files) was
lost when the checkout was re-cloned. Natives are regenerated here from the
repo's canonical SVGs — the same files the README calls the public, viewable
form of every piece — so appearance is exact. Revision pairs already in the
archive stay revisions of one piece (bunny v1 -> v2, banner v1 -> v2).
empathegy-brochure: V1R01 is repacked from its surviving members; V1R00 was a
corrupt zip and is unrecoverable.
"""
import os, shutil, zipfile, json, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, ROOT, REPO

ART = os.path.join(ROOT, "art")
PDF = os.path.join(ROOT, "pdf")
os.makedirs(ART, exist_ok=True)
os.makedirs(PDF, exist_ok=True)

# (repo svg, piece slug, revision)
JOBS = [
    ("fart-knocker.svg",          "fart-knocker", "V1R00"),
    ("twitter/golly.svg",         "golly",        "V1R00"),
    ("twitter/bunny-avatar.svg",  "bunny-avatar", "V1R00"),
    ("twitter/bunny-avatar-v2.svg","bunny-avatar","V1R01"),
    ("twitter/bunny-banner.svg",  "bunny-banner", "V1R00"),
    ("twitter/bunny-banner-v2.svg","bunny-banner","V1R01"),
]

d = Draw()
for svg, slug, rev in JOBS:
    base = f"{slug}-{rev}"
    print(f"=== {svg} -> {base}")
    d.open(f"{REPO}/{svg}")
    d.call("save_file", {"path": f"{ART}/{base}.vectorcraft"}, "save")
    shutil.copyfile(f"{REPO}/{svg}", f"{ART}/{base}.svg")
    for fmt, path, scale in [("png", f"{ART}/{base}@2x.png", 2),
                             ("pdf", f"{PDF}/{base}.pdf", None)]:
        a = {"path": path, "format": fmt, "scale": scale}
        print(" ", fmt, json.dumps(d.call("export", a, f"export {fmt}"))[:140])

# --- empathegy-brochure-V1R01: repack from the surviving members ---------------
EB = "/tmp/eb"
dst = f"{ART}/empathegy-brochure-V1R01.designcraft"
if os.path.exists(f"{EB}/document.json"):
    with zipfile.ZipFile(dst, "w") as z:
        # mimetype first, stored, like the original
        z.writestr(zipfile.ZipInfo("mimetype"),
                   "application/vnd.designcraft+zip", zipfile.ZIP_STORED)
        for n in ("meta.json", "preview.png", "document.json"):
            z.write(f"{EB}/{n}", n, zipfile.ZIP_DEFLATED)
    shutil.copyfile(f"{EB}/preview.png", f"{ART}/empathegy-brochure-V1R01@2x.png")
    print("=== empathegy-brochure-V1R01 repacked + preview proof")
else:
    print("=== /tmp/eb missing — brochure unrecoverable")

print(f"DONE: errors={len(d.errors)}")
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])

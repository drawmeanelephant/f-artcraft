import sys
sys.path.insert(0, "/home/hatch/workspace/vectorcraft/work")
from vc import Draw, NONE
d = Draw()
d.new_doc("Font Test", 900, 420)
d.shape("rectangle", "bg", x=0, y=0, width=900, height=420, fill="#F5EFE0", stroke=NONE)
d.text("Virelai Sans — Fart Knocker", "t1", x=40, y=110, size=54, font="Virelai Sans", color="#26221C")
d.text("Source Sans — Fart Knocker", "t2", x=40, y=210, size=54, font="Source Sans 3", color="#26221C")
d.text("", "t3", x=40, y=330, size=90, font="Virelai Mascots", color="#26221C")
d.text("Aa Ee Gg Rr Ss 0123456789 & § ¶", "t4", x=40, y=400, size=30, font="Virelai Sans", color="#76755F")
d.finish("font-test")

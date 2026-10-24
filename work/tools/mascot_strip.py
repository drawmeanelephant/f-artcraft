import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
d = Draw()
d.new_doc("Mascot Strip", 1180, 260)
d.shape("rectangle", "bg", x=0, y=0, width=1180, height=260, fill="#F5EFE0", stroke=NONE)
for i in range(9):
    cp = 0xE002 + i
    x = 30 + i * 128
    d.text(chr(cp), f"g{i}", x=x + 44, y=120, size=92, font="Virelai Mascots", color="#26221C")
    d.text(f"U+{cp:04X}", f"l{i}", x=x + 44, y=200, size=19, font="Source Sans 3", color="#76755F", justify="center")
d.finish("mascot-strip")

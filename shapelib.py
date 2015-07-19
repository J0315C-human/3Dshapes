
#Shape library
#this just has the spiral thing
from BaseClasses import *
from templates import *


testM = [[0.95, 0, 0],  #Matrix for transformation - resize by 0.95
         [0, 0.95, 0],
         [0, 0, 0.95]]
Cubes= []
Cubes.append(Cube((0, 0, 60), 8))
extra = (Cube((-30, -50, 60), 4))
extra2 = (Cube((50, -50, 60), 6))
Cubes[0].add(extra)
Cubes[0].add(extra2)
C = Shape()
for i in range(20):
    Cubes.append(Cubes[i].copy())
    Cubes[i+1].rotate(10, "z")
    Cubes[i+1].map(testM)
    Cubes[i+1].shift((0, 0, 50))
    C.add(Cubes[i+1])

C.shift((10, 25, 0))

C.show()

C.show_rot(20, 90, "y")
C.show_rot(20, 90, "x")
C.show_rot(20, 90, "z")
C.show_rot(20, 90, "y")
C.show_rot(20, 90, "x")
C.show_rot(20, 90, "z")

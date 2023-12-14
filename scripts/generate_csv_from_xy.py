#!/usr/bin/env python3
import sys
from pymap3d import enu

anchor = (46.3392, 3.43392, 279.18)

print('latitude,longitude,altitude,x,y,z')

for line in sys.stdin:
    pos = list(map(float, line.split(' ')))
    coords = enu.enu2geodetic(*pos, *anchor)
    print(f"{coords[0]},{coords[1]},{coords[2]},{pos[0]},{pos[1]},{pos[2]}")

#!/usr/bin/env python3
import sys
from pymap3d import enu
import json

def convert_models_pos(input_file):
    """ Convert models position to WGS84
    Return the result in a list of (wgs84_coords, enu_coords)
    """
    anchor = (46.3392, 3.43392, 279.18)
    data = []

    for line in input_file:
        pos = tuple(map(float, line.split(' ')))
        coords = enu.enu2geodetic(*pos, *anchor)
        data.append((coords, pos))
        
    return data


def save_csv(data, filename):
    file = open(filename, 'w')
    file.write('latitude,longitude,altitude,x,y,z\n')

    for geo, pos in data:
        file.write(f"{geo[0]},{geo[1]},{geo[2]},{pos[0]},{pos[1]},{pos[2]}\n")

    file.close()


def save_geojson(data, filename):
    features = []
    for geo, _ in data:
        features.append({
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [geo[1], geo[0]],
                "type": "Point"
            }
        })

    root = {
        "type": "FeatureCollection",
        "features": features,
    }

    with open(filename, 'w') as file:
        json.dump(root, file)



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Syntax: {sys.argv[0]} <output_path>", file=sys.stderr)
        exit(1)

    output_name = sys.argv[1]
    data = convert_models_pos(sys.stdin)
    save_csv(data, output_name + '.csv')
    save_geojson(data, output_name + '.geojson')

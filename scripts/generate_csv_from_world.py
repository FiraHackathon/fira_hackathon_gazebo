#!/usr/bin/env python3
import sys
from pymap3d import enu
import json
import xml.etree.ElementTree as ET


MODEL_KEYWORD = 'Construction Cone'


def extract_models_pos(world_filename):
    root = ET.parse(world_filename).getroot()

    coords = root.find('./world/spherical_coordinates')
    anchor = (
        float(coords.findtext('latitude_deg')),
        float(coords.findtext('longitude_deg')),
        float(coords.findtext('elevation')),
    )

    data = []
    models = root.findall('./world/state/model')

    for model in models:
        if model.attrib['name'].startswith(MODEL_KEYWORD):
            str_values = model.findtext('pose').split(' ')[0:3]
            pos = tuple(map(float, str_values))
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
    if len(sys.argv) < 3:
        print(f"Syntax: {sys.argv[0]} <world_file> <output_file_base>", file=sys.stderr)
        exit(1)

    world_filename = sys.argv[1]
    output_name = sys.argv[2]
    data = extract_models_pos(world_filename)
    save_csv(data, output_name + '.csv')
    save_geojson(data, output_name + '.geojson')

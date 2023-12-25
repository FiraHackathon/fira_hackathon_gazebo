#!/usr/bin/env python3
import sys
from pymap3d import enu
import json
import xml.etree.ElementTree as ET


MODEL_KEYWORD = 'Construction Cone'


def extract_models_pos(world_filename, prefix):
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
        if model.attrib['name'].startswith(prefix):
            str_values = model.findtext('pose').split(' ')[0:3]
            pos = tuple(map(float, str_values))
            coords = enu.enu2geodetic(*pos, *anchor)
            data.append(list(coords) + list(pos))
            
    return data, anchor


def save_csv(data, filename):
    file = open(filename, 'w')
    file.write('latitude,longitude,altitude,x,y,z\n')

    for pt in data:
        file.write(','.join(map(str, pt)) + '\n')

    file.close()


def save_geojson(data, filename):
    features = []
    for point in data:
        features.append({
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [point[1], point[0]],
                "type": "Point"
            }
        })

    root = {
        "type": "FeatureCollection",
        "features": features,
    }

    with open(filename, 'w') as file:
        json.dump(root, file, indent=2)


def save_json(data, anchor, filename):
    root = {
        'origin': anchor,
        'start': data[0],
        'end': data[1],
        'waypoints': data[2:],
        'fields': {
            'vineyard': {},
            'crops_field': {}
        },
    }

    with open(filename, 'w') as file:
        json.dump(root, file, indent=2)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Syntax: {sys.argv[0]} <world_file> <output_file_base>", file=sys.stderr)
        exit(1)

    world_filename = sys.argv[1]
    output_name = sys.argv[2]
    data, anchor = extract_models_pos(world_filename, MODEL_KEYWORD)
    save_csv(data, output_name + '.csv')
    save_geojson(data, output_name + '.geojson')
    save_json(data, anchor, output_name + '.json')

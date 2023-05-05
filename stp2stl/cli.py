import cadquery as cq
import re
import os
import json
import argparse

def determine_bodies(assembly_name, lines):

    bodyIdIndex = {}
    idx = 0
    for line in lines:
        m = re.search("#([0-9]+)=MANIFOLD_SOLID_BREP\('(.*)'", line)
        if m:
            bodyIdIndex[m.group(1)] = idx
            idx += 1
    
    product_definition_id = None
    for line in lines:
        m = re.search("#([0-9]+)=PRODUCT_DEFINITION\('{}'".format(assembly_name), line)
        if m:
            product_definition_id = m.group(1)
            break
    product_definition_shape_id = None
    if product_definition_id:
        for line in lines:
            m = re.search("#([0-9]*)=PRODUCT_DEFINITION_SHAPE.*{}\);".format(product_definition_id), line)
            if m:
                product_definition_shape_id = m.group(1)
                break
    shape_definition_representation_id = None
    if product_definition_shape_id:
        for line in lines:
            m = re.search("#[0-9]*=SHAPE_DEFINITION_REPRESENTATION\(#{},#([0-9]*)".format(product_definition_shape_id), line)
            if m:
                shape_definition_representation_id = m.group(1)
                #print(shape_definition_representation_id)
                break
    shape_representation_id = None
    if shape_definition_representation_id:
        for line in lines:
            m = re.search("#[0-9]*=SHAPE_REPRESENTATION_RELATIONSHIP\(.*#{},#([0-9]*)".format(shape_definition_representation_id), line)
            if m:
                shape_representation_id = m.group(1)
                #print(shape_representation_id)
                break
    body_ids = None
    if shape_representation_id:
        for line in lines:
            m = re.search("#{}=ADVANCED_BREP_SHAPE_REPRESENTATION\((.*)\);".format(shape_representation_id), line)
            if m:
                #print(m.group(1))
                body_ids = re.split(r',\s*(?![^()]*\))', m.group(1))
                body_ids = body_ids[1][1:-1].split(",")
                break

    body_idxs = []
    for body_id in body_ids:
        body_idxs.append(bodyIdIndex[body_id[1:]])
    return body_idxs

def export_stls(parts_config):
    # check stl_filepath exists if not created
    os.makedirs(parts_config['stl_filepath'], exist_ok=True)

    print("Loading meta information from step file")

    lines = None
    with open(parts_config['filename'], "r") as f:
        lines = f.readlines()

    print("Loading step file into cadquery")

    model = cq.importers.importStep(parts_config['filename'])
    solids = model.val().Solids()

    for component in parts_config['components']:
        print("Exporting {}".format(component['component']))
        idxs = determine_bodies(component['component'], lines)
        combined_solids = []
        for idx in idxs:
            combined_solids.append(solids[idx])
        result = cq.Workplane('XY').newObject(combined_solids)
        
        if "rotations" in component:
            for rotation in component['rotations']:
                if rotation['axis'] == 'x':
                    result = result.rotate((0,0,0),(1,0,0),rotation['degrees'])
                elif rotation['axis'] == 'y':
                    result = result.rotate((0,0,0),(0,1,0),rotation['degrees'])
                elif rotation['axis'] == 'z':
                    result = result.rotate((0,0,0),(0,0,1),rotation['degrees'])

        cq.exporters.export(result,component['stl_filename'])

    print("Done")

def main():
    parser = argparse.ArgumentParser(description='Export stl files from step file')
    parser.add_argument('config', help='json file containing export configuration')
    args = parser.parse_args()
    parse_config = json.loads(open(args.config).read())
    export_stls(parse_config)

if __name__ == "__main__":
    main()
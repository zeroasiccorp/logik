import argparse
import json

import xml.etree.ElementTree as ET
import xml.dom.minidom


def main():

    option_parser = argparse.ArgumentParser()
    option_parser.add_argument("-constraints_map",
                               help="architecture-specific mapping of constraint pins "
                                    "to FPGA core pins")
    option_parser.add_argument("json_constraints",
                               help="JSON pin constraints file")
    option_parser.add_argument("constraints_file_out",
                               help="constraints XML file name")

    options = option_parser.parse_args()

    json_constraints_file = options.json_constraints
    constraints_map_file = options.constraints_map
    constraints_file_out = options.constraints_file_out

    json_generic_constraints = load_json_constraints(json_constraints_file)
    if (constraints_map_file):
        constraints_map = load_constraints_map(constraints_map_file)
    else:
        constraints_map = {}

    constraints_xml = generate_constraints(json_generic_constraints,
                                           constraints_map)

    write_vpr_constraints_xml_file(constraints_xml, constraints_file_out)


def load_json_constraints(json_constraints_file):

    json_generic_constraints = {}
    with (open(json_constraints_file, "r")) as json_constraints_data:
        json_generic_constraints = json.loads(json_constraints_data.read())

    return json_generic_constraints


def load_constraints_map(constraints_map_file):

    constraints_map = {}
    with (open(constraints_map_file, "r")) as constraints_map_data:
        constraints_map = json.loads(constraints_map_data.read())

    return constraints_map


def generate_constraints(json_generic_constraints,
                         constraints_map,
                         verbose=True,
                         quiet=False):

    reverse_constraints_map = flip_gasket_map(constraints_map)

    signal_dir = get_signal_directions(json_generic_constraints)

    design_constraints = map_constraints(json_generic_constraints,
                                         reverse_constraints_map,
                                         verbose=verbose,
                                         quiet=quiet)

    constraints_xml = generate_vpr_constraints_xml(design_constraints, constraints_map, signal_dir)
    return constraints_xml


def get_signal_directions(json_generic_constraints):

    signal_dir = {}
    for design_pin in json_generic_constraints:
        signal_dir[design_pin] = json_generic_constraints[design_pin]['direction']

    return signal_dir


def map_constraints(json_generic_constraints,
                    constraints_map,
                    verbose=True,
                    quiet=False):

    design_constraints = {}

    # If no constraints map is provided pass the constraints directly
    if (len(constraints_map) == 0):

        for design_pin in json_generic_constraints:
            design_constraints[design_pin] = json_generic_constraints[design_pin]['pin']

    # Otherwise use the constraints map to remap the constraints to the correct
    # internal FPGA core pin:
    else:
        for design_pin in json_generic_constraints:

            design_pin_assignment = json_generic_constraints[design_pin]['pin']

            if (design_pin_assignment in constraints_map):
                design_pin_constraint_assignment = constraints_map[design_pin_assignment]
            else:
                design_pin_constraint_assignment = None

            design_constraints[design_pin] = design_pin_constraint_assignment

    return design_constraints


def generate_vpr_constraints_xml(pin_map, gasket_map, signal_dir):

    constraints_xml = ET.Element("vpr_constraints")

    # Generate partition list section
    partition_list = generate_partition_list_xml(pin_map, gasket_map, signal_dir)

    constraints_xml.append(partition_list)

    return constraints_xml


def generate_partition_list_xml(pin_map, gasket_map, signal_dir):

    partition_list = ET.Element("partition_list")

    for pin in pin_map:

        errors = 0
        if pin not in pin_map:
            errors += 1
        else:
            if pin_map[pin] is None:
                errors += 1

        if errors == 0:
            if (len(gasket_map) == 0):
                cur_partition = generate_partition_xml(pin, pin_map[pin], pin_map[pin], signal_dir)
            else:
                cur_partition = generate_partition_xml(pin, pin_map[pin], gasket_map[pin_map[pin]],
                                                       signal_dir)
            partition_list.append(cur_partition)

    return partition_list


def generate_partition_xml(pin, mapped_pin, gasket_pin, signal_dir):

    partition = ET.Element("partition")

    comment = ET.Comment(f'{pin} <=> {gasket_pin} <=> {mapped_pin}')
    partition.insert(1, comment)

    pin_name = generate_vpr_pb_name(pin, signal_dir)

    partition_name = generate_partition_name(pin)
    partition.set("name", partition_name)

    atom_xml = generate_add_atom_xml(pin_name)
    partition.append(atom_xml)

    x_low, x_high, y_low, y_high, subtile = generate_region_from_mapped_pin(mapped_pin)
    region_xml = generate_add_region_xml(x_low, x_high, y_low, y_high, subtile)
    partition.append(region_xml)

    return partition


def generate_vpr_pb_name(pin_name, signal_dir, verbose=True):
    # VPR treats ports like they are blocks.
    # To help deal with name conflicts that come from
    # doing this, output block names get "out:" appended
    # to them, so we need to do that appending for
    # generating placement constraints

    if (signal_dir[pin_name] == "output"):
        return "out:" + pin_name
    elif (signal_dir[pin_name] == "input"):
        return pin_name
    else:
        return pin_name


def generate_partition_name(pin):

    partition_name = pin
    partition_name = partition_name.replace('[', '_')
    partition_name = partition_name.replace(']', '')
    partition_name = "part_" + partition_name

    return partition_name


def generate_region_from_mapped_pin(mapped_pin):

    x_low, y_low = extract_x_y_from_mapped_pin(mapped_pin)
    x_high = x_low
    y_high = y_low
    subtile = extract_subtile_from_mapped_pin(mapped_pin)

    return x_low, x_high, y_low, y_high, subtile


def extract_x_y_from_mapped_pin(mapped_pin):

    base_pin_name = extract_indexed_signal_name(mapped_pin)
    base_pin_name_components = base_pin_name.split('_')
    x = base_pin_name_components[len(base_pin_name_components) - 2]
    y = base_pin_name_components[len(base_pin_name_components) - 1]
    return x, y


def extract_subtile_from_mapped_pin(mapped_pin):

    return extract_array_index(mapped_pin)


def generate_add_atom_xml(pin_name):

    atom_xml = ET.Element("add_atom")

    atom_xml.set("name_pattern", str(pin_name))

    return atom_xml


def generate_add_region_xml(x_low, x_high, y_low, y_high, subtile):

    region_xml = ET.Element("add_region")

    region_xml.set("x_low", str(x_low))
    region_xml.set("y_low", str(y_low))
    region_xml.set("x_high", str(x_high))
    region_xml.set("y_high", str(y_high))
    region_xml.set("subtile", str(subtile))

    return region_xml


def write_vpr_constraints_xml_file(arch: ET.Element, filename: str):

    m_encoding = 'UTF-8'

    dom = xml.dom.minidom.parseString(ET.tostring(arch))
    xml_string = dom.toprettyxml()
    part1, part2 = xml_string.split('?>')

    with open(filename, 'w') as xfile:
        xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
        xfile.close()


def flip_gasket_map(gasket_map):
    # Dictionary inversion taken from
    # https://therenegadecoder.com/code/how-to-perform-a-reverse-dictionary-lookup-in-python/
    reverse_gasket_map = {}
    for pin in gasket_map:
        reverse_gasket_map[gasket_map[pin]] = pin

    return reverse_gasket_map


def extract_indexed_signal_name(signal_name):

    if ('[' in signal_name):
        return signal_name[0:(signal_name.find('['))]
    else:
        return signal_name


def extract_array_index(signal_name):
    array_index = None

    if (('[' in signal_name) and (']' in signal_name)):
        array_index = signal_name[(signal_name.find('[') + 1):(signal_name.find(']'))]

    return array_index


if __name__ == "__main__":
    main()

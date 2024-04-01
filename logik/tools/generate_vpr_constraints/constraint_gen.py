from logik.tools.generate_vpr_constraints import \
    generate_vpr_constraints as constraint_utils
from siliconcompiler.tools.vpr.vpr import find_single_file


def setup(chip):
    '''
    Perform bitstream finishing
    '''

    tool = 'generate_vpr_constraints'
    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')
    task = chip._get_task(step, index)

    part_name = chip.get('fpga', 'partname')

    # Require a constraints file of type "pinmap"
    chip.add('tool', tool, 'task', task, 'require',
             ",".join(['input', 'constraint', 'pinmap']),
             step=step, index=index)

    # Require the part name to specify a gasket map
    chip.add('tool', tool, 'task', task, 'require',
             ",".join(['fpga', part_name, 'file', 'gasket_map']),
             step=step, index=index)


def run(chip):
    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')

    part_name = chip.get('fpga', 'partname')

    constraint_file = find_single_file(chip, 'input', 'constraint', 'pinmap',
                                       step=step, index=index,
                                       file_not_found_msg="JSON constraints file not found")

    gasket_map_file = find_single_file(chip, 'fpga', part_name, 'file', 'gasket_map',
                                       file_not_found_msg="gasket map not found")

    xml_constraints_file = "outputs/sc_constraints.xml"

    gasket_map = constraint_utils.load_constraints_map(gasket_map_file)
    json_constraints = constraint_utils.load_json_constraints(constraint_file)
    xml_data = constraint_utils.generate_constraints(json_constraints, gasket_map)

    constraint_utils.write_vpr_constraints_xml_file(xml_data, xml_constraints_file)

    return 0

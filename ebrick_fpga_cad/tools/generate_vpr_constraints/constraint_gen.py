#bitstream_finish.py

import shutil

from ebrick_fpga_cad.tools.generate_vpr_constraints import generate_vpr_constraints as constraint_utils
from siliconcompiler.tools.vpr.vpr import find_single_file
from siliconcompiler.tools.vpr._xml_constraint import write_vpr_constraints_xml_file


######################################################################
# Make Docs
######################################################################
#def make_docs(chip):
#    chip.set('fpga', 'partname', 'ebrick_fpga_demo')
#    chip.load_target("ebrick_fpga_flow")


def setup(chip):
    '''
    Perform bitstream finishing
    '''

    tool = 'generate_vpr_constraints'
    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')
    task = chip._get_task(step, index)
    design = chip.top()

    part_name = chip.get('fpga', 'partname')
    
    #chip.set('tool', tool, 'exe', 'generate_vpr_constraints.py')

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
    tool, task = chip._get_tool_task(step, index)

    part_name = chip.get('fpga', 'partname')

    topmodule = chip.top()

    constraint_file = find_single_file(chip, 'input', 'constraint', 'pinmap',
                                       step=step, index=index,
                                       file_not_found_msg="JSON constraints file not found")

    gasket_map_file = find_single_file(chip, 'fpga', part_name, 'file', 'gasket_map',
                                       file_not_found_msg="gasket map not found")
    
    xml_constraints_file = f"outputs/sc_constraints.xml"

    gasket_map = constraint_utils.load_constraints_map(gasket_map_file)    
    json_constraints = constraint_utils.load_json_constraints(constraint_file)
    xml_data = constraint_utils.generate_constraints(json_constraints, gasket_map)
    
    constraint_utils.write_vpr_constraints_xml_file(xml_data, xml_constraints_file)
    
    return 0


################################
# Post_process (post executable)
################################


def post_process(chip):
    ''' Tool specific function to run after step execution
    '''

    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')
    tool = 'generate_vpr_constraints'
    task = chip._get_task(step, index)

    for file in chip.get('tool', tool, 'task', task, 'output', step=step, index=index):
        shutil.copy(file, 'outputs')
    design = chip.top()
    shutil.copy(f'inputs/{design}.blif', 'outputs')
    # TODO: return error code
    return 0

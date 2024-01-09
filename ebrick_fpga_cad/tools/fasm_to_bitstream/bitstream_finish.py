#bitstream_finish.py

######################################################################
# Make Docs
######################################################################
#def make_docs(chip):
#    chip.set('fpga', 'partname', 'zafg1um_0202')
#    chip.load_target("ebrick_fpga_flow")


def setup(chip):
    '''
    Perform bitstream finishing
    '''

    tool = 'fasm_to_bitstream'
    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')
    task = chip._get_task(step, index)
    design = chip.top()

    part_name = chip.get('fpga', 'partname')
    
    chip.set('tool', tool, 'exe', 'fasm2bitstream.py')

    # Input/output requirements.
    #chip.set('tool', tool, 'task', task, 'input', design + '.fasm', step=step, index=index)
    #chip.set('tool', tool, 'task', task, 'output', design + '_bitstream.json', step=step, index=index)

    # Require that a lut size is set for FPGA scripts.
    chip.add('tool', tool, 'task', task, 'require',
             ",".join(['fpga', part_name, 'file', 'bitstream_map']),
             step=step, index=index)


def runtime_options(chip):

    part_name = chip.get('fpga', 'partname')

    options = []

    if chip.valid('fpga', part_name, 'file', 'bitstream_map') and \
       chip.get('fpga', part_name, 'file', 'bitstream_map'):

        bitstream_maps = chip.find_files('fpga', part_name, 'file', 'bitstream_map')

    else:
        bitstream_maps = []

    topmodule = chip.top()
    fasm = f"inputs/{topmodule}.fasm"

    options.append(fasm)
    
    if (len(bitstream_maps) == 1):
        options.append(bitstream_maps[0])
    elif (len(bitstream_maps) == 0):
        chip.error("fasm2bitstream.py requires a bitstream map file",
                   fatal=True)
    else:
        chip.error("Only one bitstream map file can be passed to fasm2bitstream.py", fatal=True)

    json_outfile = f"outputs/{topmodule}_bitstream.json"
    options.append(json_outfile)

    return options
    
##################################################
def pre_process(chip):
    ''' Tool specific function to run before step execution
    '''

    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')
    tool, task = chip._get_tool_task(step, index)

    part_name = chip.get('fpga', 'partname')


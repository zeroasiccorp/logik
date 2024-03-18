#!/usr/bin/env python3

import os
import umi
import lambdalib

import siliconcompiler
from ebrick_fpga_cad.targets import ebrick_fpga_target


def main(part_name='ebrick_fpga_demo'):
    
    top_module = 'ebrick_demo'
    
    chip = siliconcompiler.Chip(f'{top_module}')

    if (__name__ == '__main__') :
        chip.create_cmdline(switchlist=['-fpga_partname'])

    # Set default part name
    chip.set('fpga', 'partname', part_name, clobber=False)
        
    set_part_name = chip.get('fpga', 'partname')
    
    # 1. Project setup

    # Add picorv32 data source
    chip.register_package_source(
        name='picorv32',
        path='git+https://github.com/YosysHQ/picorv32.git',
        ref='a7b56fc81ff1363d20fd0fb606752458cd810552')

    # Add the ebrick itself as a package source
    chip.register_package_source(
        name='ebrick_demo',
        path='git+https://github.com/zeroasiccorp/dev-ebrick-demo.git',
        ref='main')

    # Import umi and lambdalib libraries
    chip.use(umi)
    chip.use(lambdalib)

    # Set the libraries ebrick_core depends on
    chip.add('option', 'library', 'lumi')
    chip.add('option', 'library', 'umi')

    chip.add('option', 'library', 'lambdalib_stdlib')
    chip.add('option', 'library', 'lambdalib_ramlib')
    chip.add('option', 'library', 'lambdalib_vectorlib')

    # 2. Define source files

    # Add your core files here
    chip.input('picorv32.v', package='picorv32')

    # Add ebrick_core top
    chip.input('ebrick_demo/rtl/ebrick_core.v', package='ebrick_demo')
    chip.add('option', 'idir', 'ebrick_demo/config', package='ebrick_demo')

    # Set the top module to ebrick_core
    chip.set('option', 'entrypoint', 'ebrick_core')

    # 3. Define constraints
    project_path = os.path.abspath(__file__).replace('ebrick_demo.py','')
    chip.add('input', 'constraint', 'pinmap',
             os.path.join(project_path, 'constraints', f'pin_constraints_{set_part_name}.json'))
    
    # 3. Load target
    chip.load_target(ebrick_fpga_target)

    # 4. Customize steps for this design

    chip.set('option', 'quiet', True)
    chip.run()
    chip.summary()

if __name__ == "__main__":
    main()

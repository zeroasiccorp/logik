#build_tools.py

#This script executes all of the tool build scripts

import os


def main() :

    script_dir = os.path.abspath(__file__).replace("build_tools.py", "")
    print(f'Script dir: {script_dir}')
    
    tool_root = script_dir.replace("/build", "")
    print(f'Tool root: {tool_root}')
    
    vpr_dir = f'{tool_root}/vtr-verilog-to-routing'
    print(f'VPR install directory: {vpr_dir}')
    
    yosys_dir = f'{tool_root}/yosys'
    print(f'Yosys install directory: {yosys_dir}')
    
    os.system(f'cd {vpr_dir}; {script_dir}/install_vpr.sh')
    os.system(f'cd {yosys_dir}; {script_dir}/install_yosys.sh')
    
if __name__ == "__main__" :
    main()

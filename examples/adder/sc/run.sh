
#Solution for deriving SCRIPT_DIR from
#https://saturncloud.io/blog/how-to-get-the-directory-where-a-bash-script-is-located/
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
sc ${SCRIPT_DIR}/../rtl/adder.v -fpga_partname "zafg1um_0202" -flow "ebrick_fpga_flow" -target "ebrick_fpga_cad.targets.ebrick_fpga_target" -design "adder"

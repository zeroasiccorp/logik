#!/bin/bash -f

#Solution for deriving SCRIPT_DIR from
#https://saturncloud.io/blog/how-to-get-the-directory-where-a-bash-script-is-located/
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
sc ${SCRIPT_DIR}/../rtl/fir_filter.v \
   ${SCRIPT_DIR}/../rtl/fir_filter_wrapper.v \
   ${SCRIPT_DIR}/../rtl/tree_adder.v \
   -fpga_partname "$1" \
   -flow "ebrick_fpga_flow" \
   -target "ebrick_fpga_cad.targets.ebrick_fpga_target" \
   -design "fir_filter_wrapper" \
   -D "FIR_FILTER_CONSTANT_COEFFS"

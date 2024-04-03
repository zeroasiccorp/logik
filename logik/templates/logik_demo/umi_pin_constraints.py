# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import json


def main():

    # Test that the pin constraints generate correctly

    umi_to_fpga_pin_map = generate_umi_pin_constraints()
    with (open("test.json", "w")) as json_out:
        json_out.write(json.dumps(umi_to_fpga_pin_map, indent=2))
        json_out.write('\n')


def generate_umi_pin_constraints(fpga_ports_per_umi=300,
                                 umi_cmd_width=32,
                                 umi_data_width=128,
                                 umi_addr_width=64,
                                 umi_ports_used=[1, 2, 3],
                                 port_types=["uhost_req",
                                             "uhost_resp",
                                             "udev_req",
                                             "udev_resp"],
                                 umi_port_num_offset=1,
                                 index_control_bits=True):

    port_type_index = {"uhost_req": 0,
                       "uhost_resp": 1,
                       "udev_req": 2,
                       "udev_resp": 3}

    umi_to_fpga_pin_map = {}

    umi_bus_index = 0
    for umi_port_num in umi_ports_used:

        i = umi_port_num - umi_port_num_offset

        for port in port_types:

            # Resetting the umi bus index here re-locks
            # the index to a particular side of the array
            # for each port
            umi_bus_index = (4 * i + port_type_index[port]) * fpga_ports_per_umi

            if (index_control_bits):
                cur_signal = f'{port}_valid[{umi_bus_index}]'
            else:
                cur_signal = f'{port}_valid'

            # ***NOTE:  This direction will be the same for
            #           everything except ready
            if ((port == 'uhost_req') or (port == 'udev_resp')):
                cur_dir = 'output'
                cur_dir_short = 'out'
            else:
                cur_dir = 'input'
                cur_dir_short = 'in'

            mapped_signal_name = f"umi_io_{cur_dir_short}[{umi_bus_index}]"
            umi_to_fpga_pin_map[cur_signal] = {
                "direction": cur_dir,
                "pin": mapped_signal_name,
            }
            umi_bus_index += 1

            for j in range(umi_cmd_width):
                cur_signal = f'{port}_cmd[{i*umi_cmd_width+j}]'
                mapped_signal_name = f"umi_io_{cur_dir_short}[{umi_bus_index}]"
                umi_to_fpga_pin_map[cur_signal] = {
                    "direction": cur_dir,
                    "pin": mapped_signal_name,
                }
                umi_bus_index += 1

            for j in range(umi_addr_width):
                cur_signal = f'{port}_dstaddr[{i*umi_addr_width+j}]'
                mapped_signal_name = f"umi_io_{cur_dir_short}[{umi_bus_index}]"
                umi_to_fpga_pin_map[cur_signal] = {
                    "direction": cur_dir,
                    "pin": mapped_signal_name,
                }
                umi_bus_index += 1

            for j in range(umi_addr_width):
                cur_signal = f'{port}_srcaddr[{i*umi_addr_width+j}]'
                mapped_signal_name = f"umi_io_{cur_dir_short}[{umi_bus_index}]"
                umi_to_fpga_pin_map[cur_signal] = {
                    "direction": cur_dir,
                    "pin": mapped_signal_name,
                }
                umi_bus_index += 1

            for j in range(umi_data_width):
                cur_signal = f'{port}_data[{i*umi_data_width+j}]'
                mapped_signal_name = f"umi_io_{cur_dir_short}[{umi_bus_index}]"
                umi_to_fpga_pin_map[cur_signal] = {
                    "direction": cur_dir,
                    "pin": mapped_signal_name,
                }
                umi_bus_index += 1

            # Flip direction around for ready signal
            if ((port == 'uhost_req') or (port == 'udev_resp')):
                cur_dir = 'input'
                cur_dir_short = 'in'
            else:
                cur_dir = 'output'
                cur_dir_short = 'out'

            if (index_control_bits):
                cur_signal = f'{port}_ready[{umi_bus_index}]'
            else:
                cur_signal = f'{port}_ready'

            mapped_signal_name = f"umi_io_{cur_dir_short}[{umi_bus_index}]"
            umi_to_fpga_pin_map[cur_signal] = {
                "direction": cur_dir,
                "pin": mapped_signal_name,
            }
            umi_bus_index += 1

    return umi_to_fpga_pin_map


if __name__ == "__main__":
    main()

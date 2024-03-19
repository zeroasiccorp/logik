#umi_fir_filter_test.py
#Peter Grossmann
#31 October 2023
#$Id$
#$Log$

import argparse
import ast
import numpy as np
import random

from pathlib import Path
from switchboard import SbDut, UmiTxRx, random_umi_packet, delete_queue, verilator_run, binary_run

def main() :

    #option_parser = argparse.ArgumentParser()
    #***TO DO:  Add back in a command-line option to put more randomness back
    #           into the packet generation
    #option_parser.add_argument("",)

    umi_queues = setup_queues()

    device = UmiTxRx(umi_queues['client2rtl'], umi_queues['rtl2client'])
    host = UmiTxRx(umi_queues['host2rtl'], umi_queues['rtl2host'])

    input_vectors = load_binary_data("fir_filter_input_vectors.dat")
    expected_output = load_binary_data("fir_filter_output_vectors.dat")
    
    coeffs = [
        0x0001,
        0x0002,
        0x0004,
        0x0008,
        0x0008,
        0x0004,
        0x0002,
        0x0001,
    ]

    print("INFO:  Load coefficients")
    load_coeffs(device, coeffs)

    print("INFO:  Lauch verilator simulation")
    #Per suggestion from switchboard experts,
    #start the verilator sim after putting stuff in the queue
    vsim_process = verilator_run("obj_dir/Vumi_fir_filter_test",
                                 plusargs=['trace']
    )
    
    print("INFO:  Generate samples")
    run_samples(device, input_vectors)

    print("INFO:  Read back samples")
    filter_output = read_samples(device, len(input_vectors))

    print("INFO:  Check outputs")
    errors = 0
    for i in range(len(filter_output)) :
        if (expected_output[i] != filter_output[i]) :
            print(f"ERROR in output {i}: expected {hex(expected_output[i])} got {hex(filter_output[i])}")
            errors += 1

    print(f"ERRORS = {errors}")
    if (errors == 0) :
        print("PASS")
    else :
        print("FAIL")

def load_binary_data(datafile) :

    binary_data = []
    
    with open(datafile, "r") as bin_data :
        for data_entry in bin_data.readlines() :
            binary_data.append(int(data_entry, base=2))

    bin_data.close()
    
    return np.array(binary_data, dtype='uint64')
        
def load_coeffs(umi, coeffs) :

    umi.write(0x0000000000000010, np.array(coeffs, dtype='uint16'), posted=True)

def run_samples(umi, data_samples) :

    for i in range(len(data_samples)) :
        umi.write(0x0000000000000020, data_samples[i])

def read_samples(umi, num_samples) :

    output_data = []
    for i in range(num_samples) :
        output_data.append(umi.read(0x0000000000000030+(64*i), np.uint64))
        
    return output_data
                           
def setup_queues(client2rtl="client2rtl.q",
                 rtl2client="rtl2client.q",
                 host2rtl="host2rtl.q",
                 rtl2host="rtl2host.q"
) :

    # clean up old queues if present
    for q in [client2rtl, rtl2client, host2rtl, rtl2host]:
        delete_queue(q)
        
    all_queues = { "client2rtl": client2rtl,
                   "rtl2client": rtl2client,
                   "host2rtl": host2rtl,
                   "rtl2host": rtl2host,
                   #"tb2bitstreamif": tb2bitstreamif,
                   #"bitstreamif2tb": bitstreamif2tb
                   }
    
    return all_queues
     

if __name__ == '__main__':
    main()

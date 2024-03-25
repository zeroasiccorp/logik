#generate_vectors.py
#Peter Grossmann
#6 October 2023
#$Id$
#$Log$

import argparse
import math
import random
import sys

def main() :

    option_parser = argparse.ArgumentParser()

    option_parser.add_argument("test_data_width", help="bit width of input vectors", type=int)
    option_parser.add_argument("num_vectors", help="number of vectors to generate", type=int)
    
    options = option_parser.parse_args()
    
    test_data_width = options.test_data_width
    num_vectors = options.num_vectors

    generate_fir_filter_vectors(test_data_width, num_vectors)


def generate_fir_filter_vectors(test_data_width, num_vectors) :
    
    num_coeffs = 8
    
    num_corner_cases = 0
    
    output_data_width = 2*test_data_width+int(math.log2(num_coeffs))
    out_file = open("fir_filter_coeff_vectors.dat", "w")

    #***NOTE:  This MUST match what's in fir_filter_wrapper.v
    all_coeffs = [1, 2, 4, 8, 8, 4, 2, 1]

    out_file = open("fir_filter_input_vectors.dat", "w")

    all_data_inputs = []
    for i in range(num_vectors - num_corner_cases) :
        cur_data = random.randint(0, 2**test_data_width-1)
        all_data_inputs.append(cur_data)
        a_vector = format(cur_data, 'b').zfill(test_data_width)
        out_file.write(a_vector)
        out_file.write("\n");

    out_file.close()

    out_file = open("fir_filter_output_vectors.dat", "w")

    for i in range(num_vectors - num_corner_cases) :

        cur_data = 0
        for j in range(num_coeffs) :
            if ((i-j) >= 0) :
                #cur_data = y[i]
                cur_data += all_coeffs[j] * all_data_inputs[i-j]
        
        out_vector = format(cur_data, 'b').zfill(output_data_width)
        out_file.write(out_vector)
        out_file.write("\n");

    out_file.close()

    

if __name__ == '__main__':
    main()

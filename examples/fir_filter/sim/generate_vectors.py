# generate_vectors.py

import argparse
import math
import random
import numpy as np


gen_vec_ref_coeffs = np.array([1, 2, 4, 8, 8, 4, 2, 1])


def generate_fir_filter_vectors(dtype=np.uint16,
                                num_vectors=1024,
                                coeffs_vector=gen_vec_ref_coeffs,
                                num_corner_cases=0):

    num_coeffs = coeffs_vector.size
    num_inputs = num_vectors-num_corner_cases
    abs_min = np.iinfo(dtype).min
    abs_max = np.iinfo(dtype).max

    inputs_vector = np.random.randint(low=abs_min,
                                     high=(abs_max+1),
                                     size=num_inputs,
                                     dtype=dtype)

    outputs_vector = np.zeros(num_inputs, dtype=np.uint64)
    for i in range(num_inputs):
        for j in range(num_coeffs):
            if ((i - j) >= 0):
                outputs_vector[i] += coeffs_vector[j] * inputs_vector[i - j]

    return inputs_vector, outputs_vector


def write_vector_to_file(file_name, data_vector, dtype=np.uint64):

    out_file = open(file_name, "w")

    for i in range(data_vector.size):
        vector_elem = format(data_vector[i], 'b').zfill(8*dtype.itemsize)
        out_file.write(vector_elem)
        out_file.write("\n")

    out_file.close()


def main():

    option_parser = argparse.ArgumentParser()
    option_parser.add_argument("data_width", help="bit width of input vectors", type=int,
                               choices=[8, 16, 32, 64])
    option_parser.add_argument("num_vectors", help="number of vectors to generate", type=int)
    options = option_parser.parse_args()

    data_width = int(options.data_width/8)
    data_type = np.dtype(f'u{data_width}')
    num_vectors = options.num_vectors

    inputs_vector, outputs_vector = generate_fir_filter_vectors(data_type.type, num_vectors)
    write_vector_to_file("fir_filter_input_vectors.dat", inputs_vector, dtype=data_type)
    write_vector_to_file("fir_filter_output_vectors.dat", outputs_vector, dtype=np.dtype(np.uint64))


if __name__ == '__main__':
    main()

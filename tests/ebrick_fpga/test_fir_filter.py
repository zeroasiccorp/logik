import os
import subprocess

import pytest
import siliconcompiler


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'zaeg1aa_0101',
                             'zafg00um_0202',
                             'zafg1um_0202',
                             'ebrick_fpga_demo',
                         ])
def test_py(setup_example_test, part_name):
    setup_example_test('fir_filter/sc')

    import fir_filter
    fir_filter.main(part_name)

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
                         ])
def test_py(setup_example_test, part_name):
    setup_example_test('fir_filter/sc')

    import fir_filter
    fir_filter.main(part_name)

@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'zaeg1aa_0101',
                             'zafg00um_0202',
                             'zafg1um_0202',
                         ])
def test_cli(setup_example_test, part_name):
    fir_filter_dir = setup_example_test('fir_filter/sc')

    proc = subprocess.run([os.path.join(fir_filter_dir, 'fir_filter.py'),
                           '-fpga_partname',
                           part_name])
    
    assert proc.returncode == 0


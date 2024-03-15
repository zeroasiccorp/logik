import os
import subprocess

import pytest
import siliconcompiler


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'ebrick_fpga_demo',
                         ])
def test_py(setup_example_test, part_name):
    setup_example_test('fir_filter')

    import fir_filter
    fir_filter.main(part_name)

@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'ebrick_fpga_demo',
                         ])
def test_cli(setup_example_test, part_name):
    fir_filter_dir = setup_example_test('fir_filter')

    proc = subprocess.run([os.path.join(fir_filter_dir, 'fir_filter.py'),
                           '-fpga_partname',
                           part_name])
    
    assert proc.returncode == 0


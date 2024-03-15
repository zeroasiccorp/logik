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
    setup_example_test('dp_memory_8192x32')

    import dp_memory_8192x32
    dp_memory_8192x32.main(part_name=part_name)


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'ebrick_fpga_demo',
                         ])
def test_cli(setup_example_test, part_name):
    dp_memory_8192x32_dir = setup_example_test('dp_memory_8192x32')

    proc = subprocess.run([os.path.join(dp_memory_8192x32_dir, 'dp_memory_8192x32.py'),
                           '-fpga_partname',
                           part_name])
    assert proc.returncode == 0

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
    setup_example_test('adder/sc')

    import adder
    adder.main(part_name=part_name)


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'zaeg1aa_0101',
                             'zafg00um_0202',
                             'zafg1um_0202',
                         ])
def test_cli(setup_example_test, part_name):
    adder_dir = setup_example_test('adder/sc')

    proc = subprocess.run([os.path.join(adder_dir, 'adder.py'),
                           '-fpga_partname',
                           part_name])
    assert proc.returncode == 0

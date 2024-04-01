import pytest
import subprocess
import os


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'logik_demo',
                         ])
def test_py(setup_example_test, part_name):
    setup_example_test('ebrick_demo_fpga')

    import ebrick_demo_fpga
    ebrick_demo_fpga.main(part_name)


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'logik_demo',
                         ])
def test_cli(setup_example_test, part_name):
    ebrick_demo_dir = setup_example_test('ebrick_demo_fpga')

    proc = subprocess.run([os.path.join(ebrick_demo_dir, 'ebrick_demo_fpga.py'),
                           '-fpga_partname',
                           part_name])

    assert proc.returncode == 0

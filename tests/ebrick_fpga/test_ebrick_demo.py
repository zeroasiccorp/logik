import pytest
import subprocess
import os


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'ebrick_fpga_demo',
                         ])
def test_py(setup_example_test, part_name):
    setup_example_test('ebrick_demo')

    import ebrick_demo
    ebrick_demo.main(part_name)


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'ebrick_fpga_demo',
                         ])
def test_cli(setup_example_test, part_name):
    ebrick_demo_dir = setup_example_test('ebrick_demo')

    proc = subprocess.run([os.path.join(ebrick_demo_dir, 'ebrick_demo.py'),
                           '-fpga_partname',
                           part_name])

    assert proc.returncode == 0

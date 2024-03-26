import pytest
import subprocess
import os


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'ebrick_fpga_demo',
                         ])
def test_py(setup_example_test, part_name):
    setup_example_test('umi_fir_filter')

    import umi_fir_filter
    umi_fir_filter.main(part_name)


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'ebrick_fpga_demo',
                         ])
def test_cli(setup_example_test, part_name):
    umi_fir_filter_dir = setup_example_test('umi_fir_filter')

    proc = subprocess.run([os.path.join(umi_fir_filter_dir, 'umi_fir_filter.py'),
                           '-fpga_partname',
                           part_name])

    assert proc.returncode == 0

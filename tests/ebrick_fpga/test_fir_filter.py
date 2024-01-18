import os
import subprocess

import pytest
import siliconcompiler

@pytest.mark.quick
@pytest.mark.timeout(300)
def test_py(setup_example_test):
    setup_example_test('fir_filter/sc')

    import fir_filter
    fir_filter.main()

@pytest.mark.quick
@pytest.mark.timeout(300)
def test_cli(setup_example_test):
    fir_filter_dir = setup_example_test('fir_filter/sc')

    proc = subprocess.run(['bash', os.path.join(fir_filter_dir, 'run.sh')])
    assert proc.returncode == 0


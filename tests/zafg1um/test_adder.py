import os
import subprocess

import pytest
import siliconcompiler

@pytest.mark.quick
@pytest.mark.timeout(300)
def test_py(setup_example_test):
    setup_example_test('adder/sc')

    import adder
    adder.main()

@pytest.mark.quick
@pytest.mark.timeout(300)
def test_cli(setup_example_test):
    adder_dir = setup_example_test('adder/sc')

    proc = subprocess.run(['bash', os.path.join(adder_dir, 'run.sh')])
    assert proc.returncode == 0


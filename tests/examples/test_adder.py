import os
import subprocess

import pytest


@pytest.mark.timeout(300)
def test_py(setup_example_test):
    setup_example_test('adder')

    import adder
    adder.hello_adder()


@pytest.mark.timeout(300)
def test_cli(setup_example_test):
    adder_dir = setup_example_test('adder')

    proc = subprocess.run([os.path.join(adder_dir, 'adder.py')])
    assert proc.returncode == 0

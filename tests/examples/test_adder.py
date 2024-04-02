# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import os
import subprocess

import pytest


@pytest.mark.timeout(300)
def test_py(setup_example_test, monkeypatch):
    adder_dir = setup_example_test('adder')

    monkeypatch.chdir(adder_dir)

    import adder
    adder.hello_adder()


@pytest.mark.timeout(300)
def test_cli(setup_example_test):
    adder_dir = setup_example_test('adder')

    proc = subprocess.run([os.path.join(adder_dir, 'adder.py')], cwd=adder_dir)
    assert proc.returncode == 0

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
@pytest.mark.parametrize("part_name",
                         ['example_arch_X005Y005',
                          'example_arch_X008Y008',
                          'example_arch_X014Y014',
                          'example_arch_X030Y030'])
def test_example_parts(part_name, setup_example_test, monkeypatch):
    adder_dir = setup_example_test('adder')

    monkeypatch.chdir(adder_dir)

    import adder
    adder.hello_adder(part_name=part_name)


@pytest.mark.timeout(300)
def test_cli(setup_example_test):
    adder_dir = setup_example_test('adder')

    proc = subprocess.run([os.path.join(adder_dir, 'adder.py')], cwd=adder_dir)
    assert proc.returncode == 0

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import os
import subprocess

import pytest


@pytest.mark.timeout(300)
def test_py(setup_example_test, monkeypatch):
    umi_hello_dir = setup_example_test('umi_hello')

    monkeypatch.chdir(umi_hello_dir)

    import umi_hello
    umi_hello.umi_hello()


@pytest.mark.timeout(300)
def test_cli(setup_example_test):
    umi_hello_dir = setup_example_test('umi_hello')

    proc = subprocess.run([os.path.join(umi_hello_dir, 'umi_hello.py')], cwd=umi_hello_dir)
    assert proc.returncode == 0

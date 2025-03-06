# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import os
import subprocess

import pytest


@pytest.mark.timeout(360)
def test_py(setup_example_test, monkeypatch):
    eth_mac_1g_dir = setup_example_test('eth_mac_1g')

    monkeypatch.chdir(eth_mac_1g_dir)

    import eth_mac_1g
    eth_mac_1g.build()


@pytest.mark.timeout(360)
def test_cli(setup_example_test):
    eth_mac_1g_dir = setup_example_test('eth_mac_1g')

    proc = subprocess.run([os.path.join(eth_mac_1g_dir, 'eth_mac_1g.py')], cwd=eth_mac_1g_dir)
    assert proc.returncode == 0

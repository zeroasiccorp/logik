# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import pytest
import subprocess
import os
from siliconcompiler import Chip


def _check_fir_filter(manifest):
    chip = Chip('umi_fir_filter')
    chip.read_manifest(manifest)

    for step in ('syn', 'place', 'route', 'bitstream'):
        assert chip.get('metric', 'brams', step=step, index=0) == 2
        assert chip.get('metric', 'dsps', step=step, index=0) == 8


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'logik_demo',
                         ])
def test_py(setup_example_test, part_name):
    setup_example_test('umi_fir_filter')

    import umi_fir_filter
    umi_fir_filter.main(part_name)

    _check_fir_filter('build/umi_fir_filter/job0/umi_fir_filter.pkg.json')


@pytest.mark.timeout(300)
@pytest.mark.parametrize("part_name",
                         [
                             'logik_demo',
                         ])
def test_cli(setup_example_test, part_name):
    umi_fir_filter_dir = setup_example_test('umi_fir_filter')

    proc = subprocess.run([os.path.join(umi_fir_filter_dir, 'umi_fir_filter.py'),
                           '-fpga_partname',
                           part_name])

    assert proc.returncode == 0

    _check_fir_filter('build/umi_fir_filter/job0/umi_fir_filter.pkg.json')

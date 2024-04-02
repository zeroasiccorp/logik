###############################################################################
# Copyright 2024 Zero ASIC Corporation
#
# Licensed under the MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY,WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ----
#
##############################################################################

import pytest
import subprocess
import os
from siliconcompiler import Chip


def _check_fir_filter(manifest):
    chip = Chip('umi_fir_filter')
    chip.read_manifest(manifest)

    for step in ('syn', 'place', 'route', 'genfasm'):
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


@pytest.mark.timeout(300)
def test_sim(setup_example_test):
    umi_fir_filter_dir = setup_example_test('umi_fir_filter')

    proc = subprocess.run([os.path.join(umi_fir_filter_dir, 'sim', 'umi_fir_filter_test.py')])

    assert proc.returncode == 0

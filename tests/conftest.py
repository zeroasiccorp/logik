@@ -1,3 +1,30 @@
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

import siliconcompiler

import os

import pytest


@pytest.fixture
def setup_example_test(monkeypatch):
    '''
    This file is cloned from Silicon Compiler.  We follow its convention
    for organizing CI tests with pytest, so that all testing can be done with
    similar efficiency.  See Silicon Compiler documentation for details
    '''
    def setup(dir):
        cad_root = ebrick_fpga_cad_root()
        ex_dir = os.path.join(cad_root, 'examples', dir)

        def _mock_show(chip, filename=None, screenshot=False):
            pass

        # pytest's monkeypatch lets us modify sys.path for this test only.
        monkeypatch.syspath_prepend(ex_dir)
        # Mock chip.show() so it doesn't run.
        monkeypatch.setattr(siliconcompiler.Chip, 'show', _mock_show)

        return ex_dir

    return setup


def ebrick_fpga_cad_root():
    cur_dir = os.path.abspath(__file__).replace('/conftest.py', "")
    root_dir = cur_dir.replace("/tests", "")
    return root_dir

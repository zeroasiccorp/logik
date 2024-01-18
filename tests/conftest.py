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

def ebrick_fpga_cad_root() :

    cur_dir = os.path.abspath(__file__).replace('/conftest.py',"")
    root_dir = cur_dir.replace("/tests", "")
    return root_dir

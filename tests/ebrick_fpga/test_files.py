import pytest
import siliconcompiler

from ebrick_fpga_cad.fpgas import ebrick_fpga_demo


@pytest.mark.parametrize(
    "part",
    [
        ebrick_fpga_demo,
    ])
def test_file_paths(part):
    chip = siliconcompiler.Chip("test")
    chip.use(part)

    assert chip.check_filepaths()

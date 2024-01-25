import pytest
import siliconcompiler

from ebrick_fpga_cad.fpgas import zafg00um, zafg1um


@pytest.mark.parametrize(
    "part",
    [
        zafg00um,
        zafg1um,
    ])
def test_file_paths(part):
    chip = siliconcompiler.Chip("test")
    chip.use(part)

    assert chip.check_filepaths()

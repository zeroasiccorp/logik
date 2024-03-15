import pytest
import siliconcompiler

from ebrick_fpga_cad.fpgas import zaeg1aa, zafg00um, zafg1um, ebrick_fpga_demo


@pytest.mark.parametrize(
    "part",
    [
        zaeg1aa,
        zafg00um,
        zafg1um,
        ebrick_fpga_demo,
    ])
def test_file_paths(part):
    chip = siliconcompiler.Chip("test")
    chip.use(part)

    assert chip.check_filepaths()
